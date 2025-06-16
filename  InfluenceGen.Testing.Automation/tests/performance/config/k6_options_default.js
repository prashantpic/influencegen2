/**
 * Default configuration options for k6 performance test scripts.
 * This file exports a base `defaultK6Options` object that can be imported
 * and extended by specific k6 test scripts to promote consistency.
 *
 * It includes default settings for:
 * - discardResponseBodies: To save memory, especially under high load.
 * - summaryTrendStats: Metrics to display in the k6 summary.
 * - noConnectionReuse: For simulating new connections per iteration if needed.
 * - userAgent: A custom user agent for k6 requests.
 * - thresholds: Default pass/fail criteria for HTTP request duration, failure rate, and checks.
 *
 * Individual test scripts can override these defaults or add script-specific
 * configurations (like stages, scenarios, or per-metric thresholds).
 *
 * k6 version: 0.51.0 (as per SDS)
 */

export const defaultK6Options = {
  // discardResponseBodies: false by default as per SDS, set to true for pure load tests if bodies aren't checked
  // If set to true, it saves memory but you can't check response bodies in your scripts.
  discardResponseBodies: false,

  // Stats to include in the end-of-test summary for trend metrics
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)', 'count', 'rate'],

  // If true, k6 will not reuse TCP connections between iterations.
  // Default is false, which is generally better for performance testing real-world scenarios.
  noConnectionReuse: false,

  // Custom User-Agent string for k6 requests.
  // Including REQ tags as per SDS example for traceability.
  userAgent: 'InfluenceGenK6PerformanceTester/1.0 (REQ-PERF-STRESS-001; REQ-PERF-THR-001; REQ-PERF-KYC-001; REQ-UIUX-007)',

  // Default thresholds for all HTTP requests made in the test.
  // These can be overridden or extended in specific test script options.
  thresholds: {
    // 95% of all HTTP requests should complete within 3000ms.
    // This is a general default; specific scenarios might have tighter or looser requirements.
    'http_req_duration': ['p(95)<3000'],

    // Global failure rate for HTTP requests should be less than 1%.
    'http_req_failed': ['rate<0.01'],

    // More than 99% of custom checks should pass.
    // Checks are assertions made on responses or conditions within the script.
    'checks': ['rate>0.99'],

    // Example for a specific metric if you define it (e.g., a custom Trend)
    // 'my_custom_metric': ['avg<100'],
  },

  // Common tags that can be applied to all metrics emitted by k6.
  // This can be useful for filtering results in k6 Cloud or other backends.
  // tags: {
  //   test_suite: 'influencegen-performance',
  //   test_type: 'generic', // Can be overridden by specific scripts
  //   environment: __ENV.TEST_ENV || 'unknown', // Example of using environment variables
  // },

  // Other global options can be set here, for example:
  // systemTags: ['proto', 'subproto', 'status', 'method', 'url', 'name', 'group', 'check', 'error', 'error_code', 'tls_version'],
  // ext: { // For extensions like k6-browser
  //   loadimpact: {
  //     projectID: 123456, // Your k6 Cloud project ID
  //     // name: "My k6 Test Script Default Name" // Can be set here or per script
  //   }
  // }
};

/*
 * How to use in individual k6 test scripts:
 *
 * import { defaultK6Options } from './path/to/k6_options_default.js';
 * import http from 'k6/http';
 * import { check } from 'k6';
 *
 * // Merge default options with script-specific options
 * export const options = Object.assign({}, defaultK6Options, {
 *   // Script-specific stages or scenarios
 *   stages: [
 *     { duration: '30s', target: 10 },
 *     { duration: '1m', target: 10 },
 *     { duration: '30s', target: 0 },
 *   ],
 *   // Override or add thresholds
 *   thresholds: {
 *     ...defaultK6Options.thresholds, // Inherit default thresholds
 *     'http_req_duration{scenario:mySpecificScenario}': ['p(95)<500'], // Override for a specific scenario or tag
 *     'http_req_duration{name:SpecificAPICallName}': ['p(95)<200'], // Threshold for a named request
 *     'checks{check_tag:critical_flow}': ['rate>0.999'], // Stricter check rate for tagged checks
 *   },
 *   // Script-specific tags
 *   tags: {
 *     ...defaultK6Options.tags, // Inherit if any
 *     test_script_name: 'my_specific_test',
 *   },
 * });
 *
 * export default function () {
 *   const res = http.get('https://test-api.k6.io/public/crocodiles/');
 *   check(res, {
 *     'status is 200': (r) => r.status === 200,
 *   }, { check_tag: 'critical_flow' }); // Tagging a check
 * }
 */