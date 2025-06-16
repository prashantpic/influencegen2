import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Trend } from 'k6/metrics';
// import { defaultK6Options } from '../../config/k6_options_default.js';

// Custom trend for page load durations
const pageLoadTime = new Trend('page_load_duration', true); // `true` indicates it's a time-based metric

// REQ-UIUX-007: 95% of pages must load in < 3 seconds.
export const options = {
    // ...defaultK6Options,
    scenarios: {
        influencer_portal_pages: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '30s', target: 10 }, // Ramp up to 10 VUs (simulating light browsing load)
                { duration: '1m', target: 10 },  // Stay at 10 VUs
                { duration: '30s', target: 20 }, // Increase to 20 VUs (moderate load)
                { duration: '1m', target: 20 },  // Stay at 20 VUs
                { duration: '30s', target: 0 },   // Ramp down
            ],
            exec: 'loadInfluencerPortalPages',
            gracefulRampDown: '30s',
        },
        // Optionally, add another scenario for admin backend pages if they are critical for performance monitoring
        // admin_backend_pages: {
        //     executor: 'ramping-vus',
        //     startVUs: 0,
        //     stages: [ /* ... similar stages, perhaps fewer VUs ... */ ],
        //     exec: 'loadAdminBackendPages',
        //     gracefulRampDown: '30s',
        // },
    },
    thresholds: {
        'http_req_failed': ['rate<0.01'], // Less than 1% of page requests should fail
        'page_load_duration': ['p(95)<3000'], // 95th percentile of page load times should be below 3000ms
        // Example of a per-page group threshold if needed:
        // 'page_load_duration{group:::Page: /influencer/dashboard}': ['p(95)<2500'],
    },
    // userAgent: 'InfluenceGenK6PageLoadTester/1.0',
};

// List of key Influencer Portal pages to test
// These URLs should be relative to the BASE_URL
const influencerPortalPageUrls = [
    '/influencer/dashboard',         // Example, adjust to actual URLs
    '/influencer/campaigns/discover',
    '/influencer/profile/edit',
    '/my/kyc',                       // KYC form page
    '/help',                         // A static/help page if available
    // Add more key pages that influencers frequently access
];

// List of key Admin Backend pages to test (if scenario is enabled)
// const adminBackendPageUrls = [
//     '/web#action=crm.crm_lead_action_pipeline&model=crm.lead&view_type=kanban', // Example Odoo admin view
//     '/web#menu_id=...&action=...', // Other admin views
// ];

// Function to execute for the influencer_portal_pages scenario
export function loadInfluencerPortalPages() {
    const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069';

    // Authentication: For pages requiring login, k6 needs to handle sessions/cookies.
    // This typically involves a login request in the setup() function or at the beginning of the VU iteration,
    // and then k6 automatically uses the cookies for subsequent requests within the same VU.
    // For simplicity, this example assumes pages might be accessible or auth is handled globally/per VU.
    // If login is needed per VU:
    // if (__ITER === 0) { // Login once per VU iteration if session expires or not sticky
    //   http.post(`${BASE_URL}/web/login`, { login: 'test_influencer_user', password: 'password' });
    // }

    influencerPortalPageUrls.forEach(pageUrl => {
        group(`Page: ${pageUrl}`, function () {
            const res = http.get(`${BASE_URL}${pageUrl}`, {
                // headers: { 'Accept': 'text/html,...' }, // Standard browser accept headers
            });
            check(res, {
                [`Status is 200 for ${pageUrl}`]: (r) => r.status === 200,
                [`Content of ${pageUrl} is not empty`]: (r) => r.body && r.body.length > 0,
            });
            pageLoadTime.add(res.timings.duration); // Total time from start of request to end of response
        });
        sleep(Math.random() * 2 + 1); // Simulate user think time between page loads (1-3 seconds)
    });
}

// Function to execute for the admin_backend_pages scenario (if defined)
// export function loadAdminBackendPages() {
//     const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069';
//     // Similar logic to loadInfluencerPortalPages, but for admin URLs
//     // Admin pages will definitely require authentication.
//     adminBackendPageUrls.forEach(pageUrl => {
//         group(`Admin Page: ${pageUrl}`, function () {
//             // ... http.get, check, pageLoadTime.add ...
//         });
//         sleep(Math.random() * 3 + 1);
//     });
// }