import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Trend } from 'k6/metrics';
// import { defaultK6Options } from '../../config/k6_options_default.js';

// Custom trend for AI generation trigger API request duration
const aiRequestTime = new Trend('ai_generation_trigger_duration', true);

// REQ-PERF-STRESS-001: System must handle up to 200 concurrent AI image generation requests.
export const options = {
    // ...defaultK6Options,
    stages: [
        { duration: '30s', target: 50 },  // Ramp up to 50 VUs
        { duration: '1m', target: 50 },   // Stay at 50 VUs
        { duration: '30s', target: 100 }, // Ramp up to 100 VUs
        { duration: '1m', target: 100 },  // Stay at 100 VUs
        { duration: '30s', target: 200 }, // Ramp up to 200 VUs (target concurrency)
        { duration: '2m', target: 200 },  // Stay at 200 VUs for 2 minutes to observe behavior under stress
        { duration: '30s', target: 0 },   // Ramp down
    ],
    thresholds: {
        'http_req_failed': ['rate<0.05'], // Max 5% failure rate for triggering AI generation
        'ai_generation_trigger_duration': ['p(95)<2000'], // Odoo's response for *triggering* the async task (not full generation time)
    },
    // userAgent: 'InfluenceGenK6AIGenTester/1.0',
};

export default function () {
    const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069'; // Get from environment variable
    const aiGenEndpoint = `${BASE_URL}/influence_gen/ai/generate_image`; // As per SDS implied target

    // Generate a somewhat unique prompt for each request to avoid identical requests if caching is aggressive
    const randomSuffix = Math.random().toString(36).substring(2, 8);
    const aiGenPayload = {
        prompt: `A stunning futuristic cityscape at dusk, cinematic lighting, high detail, ${randomSuffix}`,
        negative_prompt: "ugly, blurry, watermark, noisy, text, signature",
        model_id: "flux_lora_default_model_id_placeholder", // This should be a valid model ID from the system
        resolution: "1024x1024", // Example
        aspect_ratio: "1:1",     // Example
        // Other parameters as required by the API: seed, inferenceSteps, cfgScale etc.
        // e.g., seed: Math.floor(Math.random() * 1000000000)
    };

    // Assume authentication is handled if the endpoint requires it.
    // This might involve a setup function in k6 to obtain a token, or passing it via __ENV.
    const headers = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${__ENV.API_TOKEN || 'your_static_test_token_placeholder'}`, // Example auth
    };

    group('AI Image Generation Trigger API', function () {
        const res = http.post(aiGenEndpoint, JSON.stringify(aiGenPayload), { headers: headers });

        check(res, {
            'AI generation request accepted (status 202 or 200)': (r) => r.status === 202 || r.status === 200,
            // 202 Accepted is common for asynchronous operations.
            // 200 OK might be used if the system queues and responds immediately.
        });
        aiRequestTime.add(res.timings.duration);

        if (res.status !== 202 && res.status !== 200) {
            console.error(`AI Gen Request Error: Status ${res.status}, Body: ${res.body}`);
        }
    });

    // Sleep for a random interval to simulate varied user behavior and not overload in a tight loop.
    // Average 1 request per VU every 2-5 seconds.
    sleep(Math.random() * 3 + 1); // Random sleep between 1-4 seconds
}

// Note: This script tests the Odoo endpoint's ability to accept requests and trigger N8N.
// The actual AI image generation time (e.g., 10-20s for Flux LoRA) is an asynchronous process
// handled by N8N and the external AI service. Measuring that end-to-end time under load
// would require a more complex k6 script (e.g., polling for results if an API exists)
// or analysis of system logs/metrics for webhook callback processing times.