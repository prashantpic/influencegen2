import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Trend } from 'k6/metrics';
// import { defaultK6Options } from '../../config/k6_options_default.js'; // Assuming default options are in this path

// Custom trends for specific actions in the onboarding flow
const registrationTime = new Trend('registration_request_duration', true);
const kycSubmissionTime = new Trend('kyc_submission_request_duration', true);

// Throughput: Target 50-100 registrations/hour, peak 150/hour.
// 150 registrations/hour = 2.5 registrations/minute.
// Each VU will attempt to complete the registration + KYC submission flow.
// If flow takes ~10s of active API time per VU, we need to manage VUs and iterations.
// Let's aim for 2-3 iterations per minute per VU for sustained load.
// To achieve 2.5 registrations/min:
// e.g. 5 VUs * ~0.5 iterations/min/VU = 2.5 iterations/min
// Peak: 10 VUs * ~0.25 iterations/min/VU (allowing for more think time or slower responses under peak)

export const options = {
    // ...defaultK6Options, // Spread default options if any are defined
    stages: [
        { duration: '1m', target: 5 },  // Ramp up to 5 VUs over 1 minute
        { duration: '5m', target: 5 },  // Stay at 5 VUs for 5 minutes (simulates ~60-75 registrations total if 2-3 iters/min/VU)
        { duration: '1m', target: 10 }, // Ramp up to 10 VUs for peak load
        { duration: '3m', target: 10 }, // Stay at 10 VUs for 3 minutes (simulates ~45-75 registrations total at peak)
        { duration: '1m', target: 0 },  // Ramp down
    ],
    thresholds: {
        'http_req_failed': ['rate<0.01'], // Less than 1% of requests should fail
        'registration_request_duration': ['p(95)<5000'], // REQ-PERF-KYC-001 (initial form submission part)
        'kyc_submission_request_duration': ['p(95)<10000'], // REQ-PERF-KYC-001 (automated KYC API step)
        // Add iteration based throughput check if needed:
        // 'iterations': ['count>=X'] // Where X is calculated based on stages and desired throughput
    },
    // userAgent: 'InfluenceGenK6OnboardingTester/1.0', // Can be part of defaultK6Options
};

export default function () {
    const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069'; // Get from environment variable

    // Unique data per iteration
    const uniqueId = __VU * 10000 + __ITER; // Simple unique ID based on VU and iteration
    const userEmail = `testuser_${uniqueId}@influencegen-onboarding.com`;
    const userName = `Test User ${uniqueId}`;

    group('Influencer Registration API', function () {
        const registrationPayload = {
            name: userName,
            login: userEmail, // Odoo typically uses 'login' for email on signup
            password: 'ValidPassword123!',
            confirm_password: 'ValidPassword123!',
            phone: `+1${Math.floor(1000000000 + Math.random() * 9000000000)}`, // Example phone
            // Potentially other fields like 'company_name' if it's a B2B signup model for Odoo
            // Or 'website_id' if multi-website context
        };
        // The Odoo signup endpoint might be /web/signup or a custom controller
        const registrationEndpoint = `${BASE_URL}/web/signup`; // Adjust if custom
        
        const res = http.post(registrationEndpoint, registrationPayload, { 
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' } // Odoo standard web controllers often expect form data
            // If it's a JSON API: JSON.stringify(registrationPayload) and 'Content-Type': 'application/json'
        });

        check(res, {
            'Registration successful (status 200 or redirect 30x)': (r) => r.status === 200 || (r.status >= 300 && r.status < 400),
            // Odoo signup often results in a redirect or a 200 with a page indicating next steps
            // Add more specific checks if response body has identifiable success markers
        });
        registrationTime.add(res.timings.duration);

        // If registration creates a session, extract session cookies for subsequent requests
        // let sessionCookies = res.cookies; // This requires careful handling with k6 cookies
    });

    sleep(Math.random() * 2 + 1); // Think time between registration and KYC (1-3 seconds)

    group('KYC Data Submission API', function () {
        // This part assumes the user is now "logged in" or has a session from registration,
        // or the KYC endpoint is public but linked to the user created.
        // For simplicity, we'll hit a conceptual KYC endpoint. It might require user_id or token.
        const kycPayload = {
            user_identifier: userEmail, // Or some ID returned from registration
            document_type: 'passport',
            document_front_image_base64: 'dummy_base64_encoded_image_data_front', // Placeholder
            document_back_image_base64: 'dummy_base64_encoded_image_data_back', // Placeholder (optional)
            // Other KYC fields as required by the /influencer_portal/kyc_submit_api
            address_street: "123 Main St",
            address_city: "Anytown",
            address_zip: "12345",
            address_country: "US"
        };

        const kycEndpoint = `${BASE_URL}/influencer_portal/kyc_submit_api`; // Conceptual API endpoint
        
        const params = {
            headers: { 
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${authToken}` // If an auth token is needed and obtained
            },
            // cookies: sessionCookies // If session cookies are managed
        };

        const res = http.post(kycEndpoint, JSON.stringify(kycPayload), params);

        check(res, {
            'KYC submission accepted (status 200 or 202)': (r) => r.status === 200 || r.status === 202,
            // Check for success message in response if applicable
            // 'KYC submission response contains success message': (r) => r.json('status') === 'success',
        });
        kycSubmissionTime.add(res.timings.duration);
    });

    sleep(Math.random() * 3 + 2); // Longer think time after KYC (2-5 seconds) before next iteration
}

// Note: REQ-UIUX-007 (UI page load times) is not directly tested here as this script focuses on API endpoints.
// Page load times for UI are covered by page_load_times_test.js.
// REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004 are supported by having a stable,
// representative test environment against which these performance tests run.
// REQ-SEC-VULN-001 is covered by DAST scans, not this performance test.
// REQ-14-006 (Accessibility) is covered by UI accessibility tests.