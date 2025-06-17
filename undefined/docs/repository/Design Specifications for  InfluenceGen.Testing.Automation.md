# Software Design Specification: InfluenceGen.Testing.Automation

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `InfluenceGen.Testing.Automation` repository. This repository is responsible for housing all automated test scripts, configurations, and related utilities for the InfluenceGen platform. The tests cover various aspects including Odoo backend unit and integration testing, UI end-to-end testing (functional and accessibility), API testing for Odoo and N8N endpoints, performance testing, and security vulnerability scanning configurations.
The goal is to ensure software quality, validate functional and non-functional requirements, and facilitate CI/CD integration.

### 1.2 Scope
The scope of this repository includes:
*   **Unit Tests:** For Odoo Python business logic components.
*   **Integration Tests:** For Odoo APIs, particularly those interacting with N8N.
*   **End-to-End (E2E) UI Tests:** For influencer portal and admin backend workflows.
*   **Accessibility Tests:** For influencer portal WCAG 2.1 AA compliance.
*   **Performance Tests:** Stress, load, and throughput testing for critical system functionalities.
*   **Security Test Configurations:** Scripts and configurations to trigger DAST tools.
*   **Shared Test Utilities:** Reusable components like API clients, Page Objects, fixtures, and test data loaders.
*   **Test Configurations:** Environment-specific settings, test runner configurations, and reporting configurations.

### 1.3 Target Audiences for Test Execution
*   Development Team (for unit, integration, and local E2E runs)
*   QA Team (for E2E, performance, accessibility, and security test execution)
*   CI/CD System (for automated execution of various test suites)

## 2. Overall Design and Test Strategy

### 2.1 Test Automation Strategy
The test automation strategy focuses on a multi-layered approach:
1.  **Unit Testing (PyTest):** Targeting individual Odoo business logic functions and methods in isolation. Heavy use of mocking.
2.  **Integration Testing (PyTest):** Verifying interactions between Odoo components (e.g., API endpoints, ORM calls) and between Odoo and N8N (simulated or actual callbacks).
3.  **UI End-to-End Testing (Playwright/Selenium):** Simulating user journeys through the Odoo influencer portal and admin backend. Employs the Page Object Model (POM) for maintainability.
4.  **Accessibility Testing (Playwright/Selenium + Axe-core):** Ensuring the influencer portal meets WCAG 2.1 AA standards.
5.  **API Testing (PyTest/Newman):** Testing REST APIs of Odoo (custom endpoints) and N8N (webhook triggers, callback simulations).
6.  **Performance Testing (k6):** Measuring system responsiveness, stability, and resource usage under various load conditions.
7.  **Security Testing (DAST Tool Integration):** Automating the triggering of DAST tools like OWASP ZAP against deployed environments.

### 2.2 Framework Choices
*   **Python Backend & API Tests:** PyTest
*   **UI E2E & Accessibility Tests:** Playwright (primary, Selenium as alternative/fallback)
*   **Performance Tests:** k6 (JavaScript-based)
*   **N8N API (Postman Collection Execution):** Newman

### 2.3 Environment Strategy
*   Tests will be configurable to run against different environments (Development, Staging/UAT, Production - with caution for prod).
*   Environment-specific configurations (URLs, credentials placeholders) will be managed in dedicated JSON files.
*   A dedicated training/test environment with representative and anonymized data is crucial for effective testing (REQ-DTS-003).

### 2.4 CI/CD Integration
All test suites are designed for integration into a CI/CD pipeline. This includes:
*   Parameterized execution.
*   Standardized reporting (e.g., JUnit XML, Allure).
*   Scripts for easy triggering of test suites.

## 3. Detailed Design of Test Components

This section details the design for each file and directory structure within the `InfluenceGen.Testing.Automation` repository.

### 3.1 Root Directory Files

#### 3.1.1 `package.json`
*   **Purpose:** Manages Node.js dependencies and scripts for JavaScript-based test tools (Playwright, k6, Newman).
*   **Key Dependencies:**
    *   `playwright`: For UI E2E and accessibility tests.
    *   `@playwright/test`: Playwright test runner.
    *   `axe-playwright`: For accessibility testing with Axe-core.
    *   `k6`: Global installation assumed, or local via a wrapper if preferred.
    *   `newman`: For running Postman collections.
    *   `dotenv`: For managing environment variables.
*   **Key Scripts (`scripts` section):**
    *   `test:e2e:playwright`: "playwright test tests/e2e/ui/features"
    *   `test:accessibility`: "playwright test tests/e2e/ui/accessibility"
    *   `test:perf:k6:onboarding`: "k6 run tests/performance/scripts/k6/onboarding_stress_test.js"
    *   `test:perf:k6:ai_gen`: "k6 run tests/performance/scripts/k6/ai_generation_stress_test.js"
    *   `test:perf:k6:page_load`: "k6 run tests/performance/scripts/k6/page_load_times_test.js"
    *   `test:api:newman:n8n_workflow_example`: "newman run tests/api/postman_collections/n8n_example_workflow.postman_collection.json -e tests/config/environments/staging_config.postman_environment.json" (example)
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004, REQ-PERF-STRESS-001, REQ-SEC-VULN-001, REQ-14-006, REQ-PERF-THR-001, REQ-PERF-KYC-001, REQ-UIUX-007

#### 3.1.2 `requirements.txt`
*   **Purpose:** Specifies Python package dependencies for PyTest, Selenium, and other Python-based utilities.
*   **Key Dependencies:**
    *   `pytest`
    *   `pytest-html` (for HTML reports)
    *   `pytest-cov` (for code coverage if Odoo backend tests target coverage)
    *   `pytest-xdist` (for parallel test execution)
    *   `selenium` (if Selenium is used as an alternative to Playwright, or for specific scenarios)
    *   `requests` (for API client utilities)
    *   `python-dotenv` (for managing environment variables in Python tests)
    *   `odoo-client-lib` (if interacting with Odoo via its XML-RPC or JSON-RPC for setup/teardown in tests, or directly using Odoo's test utils if tests are run within Odoo context)
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004, REQ-PERF-STRESS-001, REQ-SEC-VULN-001, REQ-14-006, REQ-PERF-THR-001, REQ-PERF-KYC-001, REQ-UIUX-007

#### 3.1.3 `pytest.ini`
*   **Purpose:** Configures the PyTest test runner for Python tests.
*   **Content:**
    ini
    [pytest]
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    markers =
        smoke: marks tests as smoke tests
        regression: marks tests as regression tests
        api: marks tests as API tests
        ui: marks tests as UI tests (if PyTest is used to drive Selenium/Playwright)
        unit: marks tests as unit tests
        integration: marks tests as integration tests
        performance: marks tests as performance tests (if PyTest orchestrates performance scripts)
        security: marks tests as security tests
        accessibility: marks tests as accessibility tests
    # Add other configurations like log_cli, allure-pytest integration, etc.
    # testpaths = tests/unit tests/integration tests/api (if using PyTest for API tests)
    env_files =
        .env
    
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004

#### 3.1.4 `playwright.config.js`
*   **Purpose:** Configures the Playwright test runner for E2E UI automation tests.
*   **Key Configurations:**
    *   `testDir`: './tests/e2e/ui/features'
    *   `projects`: Define configurations for Chromium, Firefox, WebKit.
        *   `name`: e.g., 'chromium'
        *   `use`: `{ ...devices['Desktop Chrome'], headless: process.env.CI ? true : false, baseURL: process.env.BASE_URL || 'http://localhost:8069' }` (use environment variables)
    *   `fullyParallel`: true
    *   `forbidOnly`: !!process.env.CI
    *   `retries`: process.env.CI ? 2 : 0
    *   `workers`: process.env.CI ? 1 : undefined
    *   `reporter`: [['html'], ['list'], ['allure-playwright']] (example)
    *   `use`:
        *   `baseURL`: To be loaded from environment configuration.
        *   `actionTimeout`: 0
        *   `trace`: 'on-first-retry' or 'retain-on-failure'
        *   `screenshot`: 'only-on-failure'
        *   `video`: 'retain-on-failure'
        *   `headless`: Configurable via environment variable.
    *   `globalSetup`, `globalTeardown`: Potentially for setting up/tearing down test data or logging in globally.
*   **Implemented Requirements:** REQ-14-006, REQ-UIUX-007

### 3.2 `tests/` Directory

#### 3.2.1 `tests/unit/odoo/onboarding/test_kyc_logic_simulation.py`
*   **Purpose:** Validates individual units of KYC business logic in Odoo.
*   **Framework:** PyTest
*   **Key Test Scenarios:**
    *   `test_valid_document_type_acceptance(mock_kyc_service)`:
        *   Logic: Simulate `mock_kyc_service.validate_document_type('passport')` returning `True`. Assert outcome.
    *   `test_invalid_document_type_rejection(mock_kyc_service)`:
        *   Logic: Simulate `mock_kyc_service.validate_document_type('library_card')` returning `False`. Assert outcome.
    *   `test_kyc_status_update_on_approval(mock_influencer_profile, mock_kyc_data_model)`:
        *   Logic: Mock `mock_influencer_profile` and `mock_kyc_data_model`. Call a simulated service function `approve_kyc(influencer_id)`. Assert that `influencer_profile.kyc_status` is updated to 'approved' and `kyc_data_model.verification_status` is 'approved'.
    *   Test cases for various validation rules (e.g., document expiry, data format checks within the KYC logic - if these are pure Python functions).
*   **Mocking:** Use `pytest-mock` or `unittest.mock` to mock Odoo ORM methods (`env['model'].search()`, `record.write()`, etc.) and external service calls.
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003 (indirectly, by ensuring core logic works for training environments).

#### 3.2.2 `tests/integration/odoo_api/test_n8n_callback_api.py`
*   **Purpose:** Ensures the Odoo callback API for N8N functions correctly.
*   **Framework:** PyTest
*   **Utilities:** `tests/shared/utils/api_client_base.py`
*   **Key Test Scenarios:**
    *   `test_successful_image_result_callback(api_client, sample_image_data)`:
        *   Logic: `api_client` (configured for staging/test Odoo) POSTs `sample_image_data` (JSON payload simulating N8N success) to `/influence_gen/n8n/ai_image_callback`.
        *   Assert HTTP 200 OK.
        *   Verify Odoo records (`AIImageGenerationRequest`, `GeneratedImage`) are updated correctly (e.g., status to 'completed', image URL stored). Use `odoo_test_utils` or direct API calls if available to check state.
    *   `test_failed_image_generation_callback(api_client, sample_error_data)`:
        *   Logic: `api_client` POSTs `sample_error_data` (JSON payload simulating N8N error) to the callback URL.
        *   Assert HTTP 200 OK (or appropriate error code if the callback itself handles errors differently).
        *   Verify `AIImageGenerationRequest` status is updated to 'failed' and error details are logged.
    *   `test_unauthenticated_callback_rejection(unauth_api_client)`:
        *   Logic: `unauth_api_client` (without valid auth token/key) attempts to POST to the callback URL.
        *   Assert HTTP 401 Unauthorized or 403 Forbidden.
    *   Test with malformed payloads to check error handling.
    *   Test idempotency if the callback is designed to be idempotent.
*   **Implemented Requirements:** REQ-DTS-003

#### 3.2.3 `tests/e2e/ui/page_objects/influencer_portal/registration_page.py`
*   **Purpose:** POM for the Influencer Registration page.
*   **Framework:** Playwright (or Selenium)
*   **Structure:**
    python
    class RegistrationPage:
        def __init__(self, page): # page is Playwright page fixture
            self.page = page
            # Locators
            self.full_name_input = page.locator("#full_name_id") # Example ID
            self.email_input = page.locator("input[name='email']")
            self.password_input = page.locator("input[type='password'][name='password']")
            self.confirm_password_input = page.locator("input[type='password'][name='confirm_password']")
            self.submit_button = page.locator("button[type='submit']")
            self.error_message_area = page.locator(".alert-danger") # Example

        def navigate(self):
            self.page.goto("/influencer/register") # Example URL

        def fill_registration_form(self, name, email, password, confirm_password):
            self.full_name_input.fill(name)
            self.email_input.fill(email)
            self.password_input.fill(password)
            self.confirm_password_input.fill(confirm_password)

        def submit_form(self):
            self.submit_button.click()

        def get_error_message(self):
            if self.error_message_area.is_visible():
                return self.error_message_area.text_content()
            return None

        # Add methods for other interactions like checking a terms and conditions box
    
*   **Implemented Requirements:** REQ-UIUX-007, REQ-PERF-KYC-001 (as part of onboarding flow tests)

#### 3.2.4 `tests/e2e/ui/features/test_influencer_onboarding_flow.py`
*   **Purpose:** E2E validation of the influencer onboarding process.
*   **Framework:** Playwright (or Selenium) with PyTest as test runner.
*   **POMs Used:** `RegistrationPage`, `LoginPage`, `KYCSubmissionPage`, `InfluencerDashboardPage` (and others as needed for the flow).
*   **Key Test Scenarios:**
    *   `test_successful_onboarding_journey(page, test_data_onboarding)`:
        *   Load `test_data_onboarding` (e.g., from CSV or fixture).
        *   Navigate to registration page.
        *   Fill and submit registration form.
        *   Verify successful registration message/redirect to login or KYC.
        *   Log in if necessary.
        *   Navigate to KYC submission.
        *   Fill and submit KYC details (personal info, document uploads - mock uploads or use test files).
        *   Verify KYC submission confirmation.
        *   (Admin part - optional if E2E only from influencer perspective, or requires admin login): Admin approves KYC.
        *   Influencer logs in again, verifies account is active and dashboard is accessible.
        *   *Performance Measurement (REQ-UIUX-007, REQ-PERF-KYC-001):* Wrap critical page loads and form submissions with timing mechanisms to assert against thresholds.
    *   `test_onboarding_with_invalid_kyc_data(page, test_data_invalid_kyc)`:
        *   Simulate registration.
        *   Submit KYC form with invalid data (e.g., missing fields, invalid document format).
        *   Verify appropriate error messages are displayed on the KYC page.
    *   `test_registration_with_existing_email(page, existing_user_data)`:
        *   Attempt registration with an email that already exists.
        *   Verify error message indicating email is taken.
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-UIUX-007, REQ-PERF-KYC-001

#### 3.2.5 `tests/e2e/ui/accessibility/test_influencer_portal_wcag.py`
*   **Purpose:** Ensures the influencer portal meets WCAG 2.1 AA.
*   **Framework:** Playwright with `axe-playwright` (or Selenium with `axe-selenium-python`).
*   **Structure:**
    python
    import pytest
    from playwright.sync_api import Page
    from axe_playwright_python.sync_playwright import Axe

    axe = Axe()

    @pytest.mark.accessibility
    def test_registration_page_accessibility(page: Page, base_url):
        page.goto(f"{base_url}/influencer/register") # Ensure base_url is from config
        results = axe.run(page)
        assert results.violations_count == 0, f"Accessibility violations found: {results.generate_report()}"

    @pytest.mark.accessibility
    def test_dashboard_accessibility(page: Page, logged_in_influencer_fixture, base_url): # Fixture for logged-in state
        # logged_in_influencer_fixture would handle login
        page.goto(f"{base_url}/my/dashboard")
        results = axe.run(page)
        assert results.violations_count == 0, f"Accessibility violations found: {results.generate_report()}"

    # Add tests for other key pages: KYC form, campaign discovery, content submission, profile page
    
*   **Implemented Requirements:** REQ-14-006

#### 3.2.6 `tests/performance/scripts/k6/onboarding_stress_test.js`
*   **Purpose:** Stress/throughput test for influencer onboarding.
*   **Framework:** k6
*   **Configuration:** Uses `tests/performance/config/k6_options_default.js` and overrides specific stages/thresholds.
*   **Target Endpoints:**
    *   POST `/influencer/register` (or equivalent Odoo controller endpoint)
    *   POST `/my/kyc/submit` (or equivalent)
*   **Logic:**
    javascript
    import http from 'k6/http';
    import { check, sleep, group } from 'k6';
    import { Trend } from 'k6/metrics';
    // import defaultOptions from '../../config/k6_options_default.js'; // If you export it

    // Custom trends for specific actions
    const registrationTime = new Trend('registration_request_duration', true);
    const kycSubmissionTime = new Trend('kyc_submission_request_duration', true);

    export const options = {
      // defaultOptions, // Spread default options if any
      stages: [ // REQ-PERF-THR-001 (50-100 new registrations/hour, peak 150/hr)
                 // 150/hr = 2.5/min = ~0.04/sec.
                 // To achieve this, VUs need to complete flow faster.
                 // Let's aim for a certain number of iterations per minute.
        { duration: '1m', target: 10 }, // Ramp up to 10 VUs
        { duration: '5m', target: 10 }, // Stay at 10 VUs (simulating 50-100 registrations/hr might need more complex staging)
        { duration: '1m', target: 20 }, // Peak 20 VUs (simulating up to 150/hr)
        { duration: '2m', target: 20 },
        { duration: '1m', target: 0 },  // Ramp down
      ],
      thresholds: {
        'http_req_failed': ['rate<0.01'], // Less than 1% failures
        'registration_request_duration{group:::Registration}': ['p(95)<5000'], // REQ-PERF-KYC-001 (initial form submission < 5s)
        'kyc_submission_request_duration{group:::KYC Submission}': ['p(95)<10000'], // REQ-PERF-KYC-001 (automated steps < 10s - here refers to API response of submission)
      },
    };

    export default function () {
      const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069';
      let registrationPayload = { /* ... valid registration data ... */ };
      let kycPayload = { /* ... valid KYC data ... */ };

      group('Registration', function () {
        const res = http.post(`${BASE_URL}/influencer_portal/register_api`, JSON.stringify(registrationPayload), { headers: { 'Content-Type': 'application/json' } });
        check(res, { 'Registration successful': (r) => r.status === 200 || r.status === 201 });
        registrationTime.add(res.timings.duration);
      });

      sleep(1); // Think time

      // Assume registration was successful and we can proceed to KYC for the same "user flow"
      // This might need more complex session handling or data correlation in a real scenario
      // For simplicity here, we just hit the KYC endpoint.
      group('KYC Submission', function () {
        const res = http.post(`${BASE_URL}/influencer_portal/kyc_submit_api`, JSON.stringify(kycPayload), { headers: { 'Content-Type': 'application/json' /*, 'Authorization': 'Bearer token_if_needed'*/ } });
        check(res, { 'KYC submission successful': (r) => r.status === 200 });
        kycSubmissionTime.add(res.timings.duration);
      });
      sleep(1);
    }
    
*   **Implemented Requirements:** REQ-PERF-STRESS-001, REQ-PERF-THR-001, REQ-PERF-KYC-001, REQ-UIUX-007 (indirectly for API response times part of the flow)

#### 3.2.7 `tests/performance/scripts/k6/ai_generation_stress_test.js`
*   **Purpose:** Stress test AI image generation feature.
*   **Framework:** k6
*   **Target Endpoint:** Odoo endpoint that triggers N8N webhook for AI generation.
*   **Logic:**
    javascript
    import http from 'k6/http';
    import { check, sleep, group } from 'k6';
    import { Trend } from 'k6/metrics';

    const aiRequestTime = new Trend('ai_generation_trigger_duration', true);

    export const options = {
      stages: [ // REQ-PERF-STRESS-001 (200 concurrent requests)
        { duration: '30s', target: 50 },
        { duration: '1m', target: 200 }, // Simulate 200 concurrent VUs making requests
        { duration: '1m', target: 200 },
        { duration: '30s', target: 0 },
      ],
      thresholds: {
        'http_req_failed': ['rate<0.05'], // Max 5% failure rate for triggering AI
        'ai_generation_trigger_duration': ['p(95)<2000'], // Odoo's response for *triggering* the async task
      },
    };

    export default function () {
      const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069';
      const aiGenPayload = {
        prompt: `A beautiful landscape at sunset, epic, cinematic, ${Math.random()}`, // Add randomness
        negative_prompt: "ugly, blurry, watermark",
        model_id: "flux_lora_default_model_id_placeholder", // Get from config
        // ... other parameters
      };
      // Assume authentication token is handled if needed (e.g., via setup function or environment)
      const headers = { 'Content-Type': 'application/json', /* 'Authorization': 'Bearer ...' */ };

      group('AI Image Generation Trigger', function () {
        const res = http.post(`${BASE_URL}/influence_gen/ai/generate_image`, JSON.stringify(aiGenPayload), { headers });
        check(res, { 'AI generation request accepted': (r) => r.status === 202 || r.status === 200 }); // 202 Accepted for async
        aiRequestTime.add(res.timings.duration);
      });
      sleep(Math.random() * 3 + 1); // Random sleep between 1-4 seconds
    }
    
*   **Note:** This tests the Odoo endpoint's ability to handle requests and trigger N8N. Actual AI generation time (10-20s for Flux LoRA) is an asynchronous N8N process. Testing that end-to-end time under load would require a different k6 script that polls for results or a system to measure webhook callback times.
*   **Implemented Requirements:** REQ-PERF-STRESS-001

#### 3.2.8 `tests/performance/scripts/k6/page_load_times_test.js`
*   **Purpose:** Measure UI page load times.
*   **Framework:** k6
*   **Logic:**
    javascript
    import http from 'k6/http';
    import { check, group } from 'k6';
    import { Trend } from 'k6/metrics';

    const pageLoadTime = new Trend('page_load_duration', true);

    export const options = {
      scenarios: {
        influencer_portal_pages: {
          executor: 'ramping-vus',
          startVUs: 0,
          stages: [
            { duration: '30s', target: 10 }, // Typical load for page browsing
            { duration: '1m', target: 10 },
          ],
          exec: 'loadInfluencerPages',
        },
        // Add more scenarios for admin pages if needed
      },
      thresholds: {
        'http_req_failed': ['rate<0.01'],
        'page_load_duration': ['p(95)<3000'], // REQ-UIUX-007 (95% of pages load in < 3s)
      },
    };

    // List of key pages to test
    const influencerPages = [
      '/influencer/dashboard', // Example, adjust URLs
      '/influencer/campaigns/discover',
      '/influencer/profile/edit',
      // ... add more key pages
    ];

    export function loadInfluencerPages() {
      const BASE_URL = __ENV.BASE_URL || 'http://localhost:8069';
      // Assume k6 is configured with cookies for logged-in state or pages are public
      // For logged-in pages, k6 setup() would need to handle login and pass session cookies.

      influencerPages.forEach(pageUrl => {
        group(`Page: ${pageUrl}`, function () {
          const res = http.get(`${BASE_URL}${pageUrl}`);
          check(res, { [`Status is 200 for ${pageUrl}`]: (r) => r.status === 200 });
          pageLoadTime.add(res.timings.duration);
        });
      });
    }
    
*   **Implemented Requirements:** REQ-UIUX-007

#### 3.2.9 `tests/security/scripts/vulnerability_scans/run_zap_scan.sh`
*   **Purpose:** Automate OWASP ZAP DAST scans.
*   **Tool:** Shell script + OWASP ZAP (Dockerized or local install)
*   **Logic:**
    bash
    #!/bin/bash
    TARGET_URL="${ZAP_TARGET_URL:-http://staging.influencegen.local:8069}" # Get from env or default
    ZAP_API_KEY="${ZAP_API_KEY_PLACEHOLDER}" # Placeholder, get from secure store
    REPORT_NAME="zap_scan_report_$(date +%Y%m%d_%H%M%S).html"
    CONTEXT_FILE_PATH="${WORKSPACE:-.}/tests/security/config/zap_context.context" # Example
    POLICY_NAME="InfluenceGenScanPolicy" # Custom policy if defined in ZAP

    echo "Starting ZAP Scan against: $TARGET_URL"

    # Example for Dockerized ZAP
    # docker run -v $(pwd)/reports:/zap/wrk/:rw \
    #   -t owasp/zap2docker-stable zap-baseline.py \
    #   -t $TARGET_URL \
    #   -r $REPORT_NAME \
    #   -c $CONTEXT_FILE_PATH \ # Optional: context file
    #   -P $POLICY_NAME # Optional: scan policy

    # Or using ZAP API if ZAP is running as a daemon
    # curl "http://localhost:8080/JSON/spider/action/scan/?apikey=${ZAP_API_KEY}&url=${TARGET_URL}&contextName=MyContext"
    # ... wait for scan ...
    # curl "http://localhost:8080/JSON/ascan/action/scan/?apikey=${ZAP_API_KEY}&url=${TARGET_URL}&recurse=true&inScopeOnly=true&scanPolicyName=${POLICY_NAME}&contextId=..."
    # ... wait for scan ...
    # curl "http://localhost:8080/OTHER/core/other/htmlreport/?apikey=${ZAP_API_KEY}" > $REPORT_NAME

    echo "ZAP Scan initiated. Check ZAP UI or logs for progress. Report will be: $REPORT_NAME (if configured for local generation)"
    # This script primarily triggers; actual scan logic and reporting is within ZAP.
    # CI/CD would need to wait for scan completion and parse results.
    
*   **Implemented Requirements:** REQ-SEC-VULN-001

### 3.3 `tests/shared/` Directory

#### 3.3.1 `tests/shared/utils/api_client_base.py`
*   **Purpose:** Reusable base for API clients.
*   **Framework:** Python `requests` library.
*   **Structure:**
    python
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv() # Loads .env file for local development

    class APIClientBase:
        def __init__(self, base_url_env_var="API_BASE_URL"):
            self.base_url = os.getenv(base_url_env_var)
            if not self.base_url:
                raise ValueError(f"Environment variable {base_url_env_var} not set.")
            self.session = requests.Session()
            self.auth_token = None # Or load from env if static for test user

        def authenticate(self, username_env_var, password_env_var, auth_endpoint="/api/auth/login"):
            # Example auth, adapt to Odoo's auth mechanism (e.g. session_id or token)
            username = os.getenv(username_env_var)
            password = os.getenv(password_env_var)
            if not username or not password:
                # Potentially use a pre-configured test user token from env
                self.auth_token = os.getenv("DEFAULT_TEST_API_TOKEN")
                if self.auth_token:
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    return
                raise ValueError("Credentials for authentication not found in environment.")

            # This is a placeholder. Odoo auth might involve getting a session_id
            # or CSRF token first, then logging in.
            # response = self.session.post(f"{self.base_url}{auth_endpoint}", data={"login": username, "password": password})
            # response.raise_for_status()
            # self.auth_token = response.json().get("token") # Example
            # self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
            pass # Actual Odoo API auth needs careful implementation

        def post(self, endpoint, data=None, json_payload=None, headers=None):
            custom_headers = self.session.headers.copy()
            if headers:
                custom_headers.update(headers)
            url = f"{self.base_url}{endpoint}"
            return self.session.post(url, data=data, json=json_payload, headers=custom_headers)

        def get(self, endpoint, params=None, headers=None):
            custom_headers = self.session.headers.copy()
            if headers:
                custom_headers.update(headers)
            url = f"{self.base_url}{endpoint}"
            return self.session.get(url, params=params, headers=custom_headers)

        # Add PUT, DELETE etc. as needed
    

#### 3.3.2 `tests/shared/utils/odoo_test_utils.py`
*   **Purpose:** Odoo-specific test helpers for backend tests.
*   **Note:** These utilities are most effective when tests run within an Odoo test environment (e.g., using `odoo.tests.common.HttpCase` or similar for integration tests). If testing externally, they might need to use an Odoo client library or XML-RPC/JSON-RPC.
*   **Structure (assuming Odoo test environment context):**
    python
    # from odoo.tests.common import tagged, HttpCase # If running within Odoo
    # from odoo.addons.your_module_name.models import ... # For type hinting

    class OdooTestUtils: # Or just standalone functions

        @staticmethod
        def create_test_influencer(env, name, email, password="testpassword", **kwargs):
            # env is the Odoo environment (self.env in Odoo tests)
            user_model = env['res.users']
            # Check if user exists by email
            user = user_model.search([('login', '=', email)], limit=1)
            if not user:
                user_vals = {
                    'name': name,
                    'login': email,
                    'password': password,
                    'groups_id': [(6, 0, [env.ref('base.group_portal').id])] # Example group
                }
                user = user_model.create(user_vals)

            influencer_profile_model = env['influence_gen.influencer_profile'] # Use actual model name
            profile = influencer_profile_model.search([('email', '=', email)], limit=1)
            if not profile:
                profile_vals = {
                    'user_id': user.id,
                    'full_name': name,
                    'email': email,
                    # ... other required fields from kwargs
                }
                profile_vals.update(kwargs)
                profile = influencer_profile_model.create(profile_vals)
            return profile

        @staticmethod
        def get_campaign_by_name(env, campaign_name):
            return env['influence_gen.campaign'].search([('name', '=', campaign_name)], limit=1)

        @staticmethod
        def set_kyc_status(env, influencer_profile_id, status, reviewer_id=None):
            profile = env['influence_gen.influencer_profile'].browse(influencer_profile_id)
            if profile:
                # This assumes KYC data is directly on profile or a related one2one/many2one
                # Adjust if KYCData is a separate one2many model
                write_vals = {'kyc_status': status}
                # if reviewer_id:
                #   write_vals['kyc_reviewer_id'] = reviewer_id # Adjust field name
                profile.write(write_vals)
            return profile

        # Add more helpers as needed, e.g., for creating campaigns, submissions etc.
    

#### 3.3.3 `tests/shared/fixtures/common_fixtures.py`
*   **Purpose:** Reusable PyTest fixtures.
*   **Structure:**
    python
    import pytest
    import os
    import json
    from dotenv import load_dotenv
    from tests.shared.utils.api_client_base import APIClientBase # Example

    load_dotenv()

    @pytest.fixture(scope='session')
    def environment_config():
        env = os.getenv("TEST_ENV", "staging") # Default to staging
        config_path = f"tests/config/environments/{env}_config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            pytest.fail(f"Environment config file not found: {config_path}")

    @pytest.fixture(scope='session')
    def odoo_api_client(environment_config):
        client = APIClientBase(base_url_env_var="ODOO_BASE_URL_PLACEHOLDER") # Placeholder name from config
        # client.base_url = environment_config.get("odoo_app_url") # Set from loaded config
        # client.authenticate("ODOO_TEST_USER_PLACEHOLDER", "ODOO_TEST_PASS_PLACEHOLDER") # Example
        return client

    @pytest.fixture
    def random_email():
        import uuid
        return f"testuser_{uuid.uuid4().hex[:8]}@example.com"

    # For Playwright, fixtures are often defined differently or using Playwright's own mechanisms.
    # This file is primarily for PyTest driven tests.
    # Example for Playwright if using PyTest as runner:
    # @pytest.fixture(scope="session")
    # def browser_type_launch_args(browser_type_launch_args):
    #     return {
    #         **browser_type_launch_args,
    #         "headless": os.getenv("HEADLESS", "true").lower() == "true",
    #     }
    

### 3.4 `tests/test_data/` Directory

#### 3.4.1 `tests/test_data/onboarding/influencer_profiles_valid.csv`
*   **Purpose:** Valid input data for successful influencer onboarding tests.
*   **Format:** CSV
*   **Columns (Example):** `test_case_id,fullName,email_prefix,phone,password,kycDocumentName,kycDocumentType,expected_status`
*   **Content:** Rows of data representing different valid profiles. Emails can be constructed with `email_prefix` + `@example.com`. `kycDocumentName` could be a path to a dummy test file.
*   **Data characteristics (REQ-DTS-003):** Must be representative, though for unit/E2E, full anonymization might not be needed if data is synthetic. For staging runs, ensure anonymized if sourced from prod.

### 3.5 `tests/config/environments/` Directory

#### 3.5.1 `tests/config/environments/staging_config.json`
*   **Purpose:** Staging environment specific parameters.
*   **Format:** JSON
*   **Content (Example):**
    json
    {
      "odoo_app_url": "https://staging.influencegen.example.com",
      "odoo_api_base_url": "https://staging.influencegen.example.com/api/v1",
      "n8n_webhook_base_url": "https://staging-n8n.influencegen.example.com/webhook",
      "default_influencer_username_placeholder": "STAGING_INFLUENCER_USER", // Actual value from env var
      "default_influencer_password_placeholder": "STAGING_INFLUENCER_PASS", // Actual value from env var
      "default_admin_username_placeholder": "STAGING_ADMIN_USER",
      "default_admin_password_placeholder": "STAGING_ADMIN_PASS",
      "zap_target_url": "https://staging.influencegen.example.com"
    }
    
*   **Note:** Actual sensitive credentials (passwords, API keys) MUST NOT be stored here. Instead, use placeholder keys, and the test framework/CI system should populate these from environment variables or a secure vault.

### 3.6 `tests/reports_config/` Directory

#### 3.6.1 `tests/reports_config/allure_config.json`
*   **Purpose:** Customize Allure test reports.
*   **Format:** JSON (Specific to Allure command-line or plugin)
*   **Content (Example based on typical Allure structure):**
    json
    {
      "categories": [
        {
          "name": "Critical Defects",
          "matchedStatuses": ["failed"],
          "messageRegex": ".*(CriticalError|NullPointerException).*"
        },
        {
          "name": "Known Issues",
          "matchedStatuses": ["failed"],
          "traceRegex": ".*KnownIssueTicket-123.*"
        }
      ],
      "executor": {
        "name": "Jenkins",
        "type": "jenkins",
        "url": "http://jenkins.example.com",
        "buildOrder": 123, // To be set by CI
        "buildName": "InfluenceGen-Test-Run #123", // To be set by CI
        "reportUrl": "http://jenkins.example.com/job/InfluenceGen/123/Allure_20_Report/" // To be set by CI
      }
      // Other Allure specific settings
    }
    

### 3.7 `tests/performance/config/k6_options_default.js`
*   **Purpose:** Base k6 options for consistency.
*   **Format:** JavaScript
*   **Content:**
    javascript
    // tests/performance/config/k6_options_default.js
    export const defaultK6Options = {
      discardResponseBodies: true, // Saves memory, set to false if you need to check bodies
      summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)', 'count'],
      noConnectionReuse: false,
      userAgent: 'InfluenceGenK6PerformanceTester/1.0',
      // Default thresholds - can be overridden by specific test scripts
      thresholds: {
        'http_req_duration': ['p(95)<2000'], // Default P95 for any HTTP request < 2s
        'http_req_failed': ['rate<0.02'],    // Default failure rate < 2%
        'checks': ['rate>0.98'],             // Default check success rate > 98%
      },
    };
    
    Specific k6 test scripts will import and potentially extend these options:
    javascript
    // Example in a k6 test script:
    // import { defaultK6Options } from '../config/k6_options_default.js';
    // export const options = Object.assign({}, defaultK6Options, {
    //   stages: [ /* specific stages */ ],
    //   thresholds: {
    //     ...defaultK6Options.thresholds, // inherit default thresholds
    //     'http_req_duration{scenario:myScenario}': ['p(95)<500'], // override for a specific scenario
    //   }
    // });
    

## 4. Test Data Management Strategy
*   **Source:** Test data will primarily be stored in CSV files (`tests/test_data/`) or generated dynamically within fixtures/tests.
*   **Anonymization:** For staging/UAT environments, if data is derived from production, it MUST be anonymized/masked as per REQ-DTS-003 and general security practices (SRS 6.2.1).
*   **Data Driven Testing:** Tests (especially E2E and API) should be designed to be data-driven, consuming data from these external files or fixtures.
*   **Categorization:** Separate files for valid, invalid, and edge-case data.

## 5. Test Execution and Reporting
*   **Execution:**
    *   PyTest tests: `pytest <options> <path_to_tests>`
    *   Playwright tests: `npx playwright test <options>` or via `package.json` scripts.
    *   k6 tests: `k6 run <script.js> -e BASE_URL=...` or via `package.json` scripts.
    *   Newman: `newman run ...` or via `package.json` scripts.
*   **Reporting:**
    *   **Allure:** Primary framework for aggregated rich test reports across different test types. PyTest and Playwright will be configured to generate Allure results.
    *   **PyTest HTML Report:** Optional, for quick local HTML reports from PyTest runs.
    *   **k6 Summary Output:** k6 provides detailed console summary and can output JSON/CSV for further analysis or integration with monitoring tools.
    *   **DAST Tool Reports:** OWASP ZAP (or other tools) will generate their own HTML/XML/JSON reports.

## 6. Dependencies on Other Repositories
The tests in this repository target the application code and APIs exposed by:
*   `REPO-IGOP-001` (InfluenceGen.Odoo.Portal.Endpoints) - For UI E2E, Accessibility tests.
*   `REPO-IGOA-002` (InfluenceGen.Odoo.Admin.Backend) - For Admin UI E2E tests (if in scope).
*   `REPO-IGBS-003` (InfluenceGen.Odoo.Business.Services) - For Odoo Unit & Integration tests targeting business logic.
*   `REPO-IGOII-004` (InfluenceGen.Odoo.Infrastructure.Integration.Services) - For Integration tests targeting Odoo APIs and N8N callback.
*   `REPO-N8NO-005` (InfluenceGen.N8N.Orchestration.Workflows) - For API tests triggering N8N webhooks (using Newman or PyTest).
*   `REPO-IGEI-006` (InfluenceGen.External.AI.Service.Integration) - Indirectly, performance and integration tests will stress this component via N8N.

Test environments must have these dependent services deployed and configured correctly.

## 7. Non-Functional Requirements Addressed
This test suite directly addresses the following non-functional requirements through specific test types:
*   **Performance & Scalability:** REQ-PERF-STRESS-001, REQ-PERF-THR-001, REQ-PERF-KYC-001 (k6 tests).
*   **Security:** REQ-SEC-VULN-001 (DAST scan triggers).
*   **Usability (Responsiveness):** REQ-UIUX-007 (k6 page load tests, E2E interaction timing).
*   **Accessibility:** REQ-14-006 (Playwright/Axe tests).
*   **Maintainability & Testability (of the application):** Validated indirectly by the ability to write stable and effective automated tests. The test suite itself adheres to maintainability principles.
*   **Documentation & Training Support (System Readiness for):** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003 are validated by ensuring the system under test is stable and test environments are representative, which is a prerequisite for effective training.

markdown
# Software Design Specification: InfluenceGen.Testing.Automation

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `InfluenceGen.Testing.Automation` repository. This repository is responsible for housing all automated test scripts, configurations, and related utilities for the InfluenceGen platform. The tests cover various aspects including Odoo backend unit and integration testing, UI end-to-end testing (functional and accessibility), API testing for Odoo and N8N endpoints, performance testing, and security vulnerability scanning configurations.
The goal is to ensure software quality, validate functional and non-functional requirements, and facilitate CI/CD integration.

### 1.2 Scope
The scope of this repository includes:
*   **Unit Tests:** For Odoo Python business logic components.
*   **Integration Tests:** For Odoo APIs, particularly those interacting with N8N.
*   **End-to-End (E2E) UI Tests:** For influencer portal and admin backend workflows.
*   **Accessibility Tests:** For influencer portal WCAG 2.1 AA compliance.
*   **Performance Tests:** Stress, load, and throughput testing for critical system functionalities.
*   **Security Test Configurations:** Scripts and configurations to trigger DAST tools.
*   **Shared Test Utilities:** Reusable components like API clients, Page Objects, fixtures, and test data loaders.
*   **Test Configurations:** Environment-specific settings, test runner configurations, and reporting configurations.

### 1.3 Target Audiences for Test Execution
*   Development Team (for unit, integration, and local E2E runs)
*   QA Team (for E2E, performance, accessibility, and security test execution)
*   CI/CD System (for automated execution of various test suites)

## 2. Overall Design and Test Strategy

### 2.1 Test Automation Strategy
The test automation strategy focuses on a multi-layered approach:
1.  **Unit Testing (PyTest):** Targeting individual Odoo business logic functions and methods in isolation. Heavy use of mocking.
2.  **Integration Testing (PyTest):** Verifying interactions between Odoo components (e.g., API endpoints, ORM calls) and between Odoo and N8N (simulated or actual callbacks).
3.  **UI End-to-End Testing (Playwright/Selenium):** Simulating user journeys through the Odoo influencer portal and admin backend. Employs the Page Object Model (POM) for maintainability.
4.  **Accessibility Testing (Playwright/Selenium + Axe-core):** Ensuring the influencer portal meets WCAG 2.1 AA standards.
5.  **API Testing (PyTest/Newman):** Testing REST APIs of Odoo (custom endpoints) and N8N (webhook triggers, callback simulations).
6.  **Performance Testing (k6):** Measuring system responsiveness, stability, and resource usage under various load conditions.
7.  **Security Testing (DAST Tool Integration):** Automating the triggering of DAST tools like OWASP ZAP against deployed environments.

### 2.2 Framework Choices
*   **Python Backend & API Tests:** PyTest 8.2.2
*   **UI E2E & Accessibility Tests:** Playwright 1.45.0 (primary), Selenium 4.22.0 as potential alternative.
*   **Performance Tests:** k6 0.51.0 (JavaScript-based)
*   **N8N API (Postman Collection Execution):** Newman 6.2.0

### 2.3 Environment Strategy
*   Tests will be configurable to run against different environments (Development, Staging/UAT, Production - with caution for prod).
*   Environment-specific configurations (URLs, credentials placeholders) will be managed in dedicated JSON files. Sensitive credentials will be sourced from environment variables or a secure vault at runtime.
*   A dedicated training/test environment with representative and anonymized data is crucial for effective testing (REQ-DTS-003).

### 2.4 CI/CD Integration
All test suites are designed for integration into a CI/CD pipeline. This includes:
*   Parameterized execution (e.g., target environment, browser).
*   Standardized reporting formats (e.g., JUnit XML for test results, Allure for comprehensive reports).
*   Scripts for easy triggering of different test suites.
*   Return codes indicating test success/failure for pipeline control.

## 3. Detailed Design of Test Components

This section details the design for each file and directory structure within the `InfluenceGen.Testing.Automation` repository.

### 3.1 Root Directory Files

#### 3.1.1 `package.json`
*   **Purpose:** Manages Node.js dependencies and scripts for JavaScript-based test tools (Playwright, k6, Newman).
*   **Key Dependencies:**
    *   `playwright: "^1.45.0"`
    *   `@playwright/test: "^1.45.0"`
    *   `axe-playwright: "^1.3.0"` (or similar for Playwright with Axe-core)
    *   `newman: "^6.2.0"`
    *   `dotenv: "^16.3.1"` (for local environment variable loading)
    *   Cross-env (for setting environment variables in scripts cross-platform)
*   **Key Scripts (`scripts` section):**
    *   `"test:e2e:playwright": "playwright test tests/e2e/ui/features --config=playwright.config.js"`
    *   `"test:e2e:report": "playwright show-report"`
    *   `"test:accessibility": "playwright test tests/e2e/ui/accessibility --config=playwright.config.js"`
    *   `"test:perf:k6:onboarding": "k6 run tests/performance/scripts/k6/onboarding_stress_test.js"`
    *   `"test:perf:k6:ai_gen": "k6 run tests/performance/scripts/k6/ai_generation_stress_test.js"`
    *   `"test:perf:k6:page_load": "k6 run tests/performance/scripts/k6/page_load_times_test.js"`
    *   `"test:api:newman:n8n_workflow_example": "newman run tests/api/postman_collections/n8n_example_workflow.postman_collection.json -e tests/config/environments/staging_config.postman_environment.json"`
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004, REQ-PERF-STRESS-001, REQ-SEC-VULN-001, REQ-14-006, REQ-PERF-THR-001, REQ-PERF-KYC-001, REQ-UIUX-007

#### 3.1.2 `requirements.txt`
*   **Purpose:** Specifies Python package dependencies for PyTest, Selenium, and other Python-based utilities.
*   **Key Dependencies:**
    *   `pytest==8.2.2`
    *   `pytest-html`
    *   `pytest-cov`
    *   `pytest-xdist`
    *   `selenium==4.22.0`
    *   `requests`
    *   `python-dotenv`
    *   `allure-pytest` (for Allure reporting with PyTest)
    *   `odoo-client-lib` (if required for external Odoo interactions, otherwise Odoo's test utils are used when running tests inside Odoo context)
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004, REQ-PERF-STRESS-001, REQ-SEC-VULN-001, REQ-14-006, REQ-PERF-THR-001, REQ-PERF-KYC-001, REQ-UIUX-007

#### 3.1.3 `pytest.ini`
*   **Purpose:** Configures the PyTest test runner for Python tests.
*   **Content:**
    ini
    [pytest]
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    markers =
        smoke: marks tests as smoke tests
        regression: marks tests as regression tests
        api: marks tests as API tests
        ui_pytest: marks tests as UI tests driven by PyTest (e.g., with Selenium)
        unit: marks tests as unit tests
        integration: marks tests as integration tests
        accessibility_pytest: marks tests as accessibility tests driven by PyTest
    testpaths = tests/unit tests/integration tests/api
    env_files =
        .env
    # Example for Allure reporting
    addopts = --alluredir=allure-results
    
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004

#### 3.1.4 `playwright.config.js`
*   **Purpose:** Configures the Playwright test runner for E2E UI automation tests.
*   **Key Configurations:**
    *   `testDir`: `'./tests/e2e/ui'` (includes `features` and `accessibility` subfolders)
    *   `projects`:
        javascript
        projects: [
          {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'], headless: !!process.env.CI, baseURL: process.env.BASE_URL || 'http://localhost:8069' },
          },
          {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'], headless: !!process.env.CI, baseURL: process.env.BASE_URL || 'http://localhost:8069' },
          },
          {
            name: 'webkit',
            use: { ...devices['Desktop Safari'], headless: !!process.env.CI, baseURL: process.env.BASE_URL || 'http://localhost:8069' },
          },
        ],
        
    *   `fullyParallel`: `true`
    *   `forbidOnly`: `!!process.env.CI`
    *   `retries`: `process.env.CI ? 2 : 0`
    *   `workers`: `process.env.CI ? 1 : undefined` (or a reasonable number based on CI agent resources)
    *   `reporter`: `[['html', { open: 'never' }], ['list'], ['allure-playwright']]`
    *   `use`:
        *   `actionTimeout`: `10 * 1000` (10 seconds)
        *   `navigationTimeout`: `30 * 1000` (30 seconds)
        *   `trace`: `'on-first-retry'`
        *   `screenshot`: `'only-on-failure'`
        *   `video`: `'retain-on-failure'`
    *   `globalSetup`: (Optional) `require.resolve('./tests/e2e/ui/global-setup.js')`
    *   `globalTeardown`: (Optional) `require.resolve('./tests/e2e/ui/global-teardown.js')`
*   **Implemented Requirements:** REQ-14-006, REQ-UIUX-007

### 3.2 `tests/` Directory

#### 3.2.1 `tests/unit/odoo/onboarding/test_kyc_logic_simulation.py`
*   **Purpose:** Validates individual units of KYC business logic in Odoo.
*   **Framework:** PyTest
*   **Key Test Scenarios & Logic:**
    *   `test_valid_document_type_acceptance(mock_kyc_service_instance)`:
        *   Mock a KYC service method (e.g., `validate_document_type`).
        *   Call with 'passport', expect `True`.
    *   `test_invalid_document_type_rejection(mock_kyc_service_instance)`:
        *   Call with 'library_card', expect `False`.
    *   `test_kyc_status_update_on_approval(mock_influencer_profile_record, mock_kyc_data_record)`:
        *   Mock `InfluencerProfile.write()` and `KYCData.write()`.
        *   Call a conceptual `kyc_approval_service.approve(profile_id)`.
        *   Assert `write()` was called on mocks with `kyc_status='approved'` and `verification_status='approved'`.
    *   Additional tests for specific validation rules (e.g., required fields for KYC data, format validation for submitted data points) if implemented as testable Python functions.
*   **Mocking:** Use `pytest-mock` (`mocker` fixture) to mock Odoo model methods (`env['model'].search`, `create`, `write`, `browse`) and any external service calls if the unit test is for a service layer interacting with them.
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003 (by ensuring core logic robustness for stable test/training environments).

#### 3.2.2 `tests/integration/odoo_api/test_n8n_callback_api.py`
*   **Purpose:** Ensures the Odoo callback API for N8N (AI image results) functions correctly.
*   **Framework:** PyTest
*   **Utilities:** `tests/shared/utils/api_client_base.py`, `tests/shared/utils/odoo_test_utils.py` (for pre/post state verification).
*   **Fixtures:** `odoo_api_client` (from `common_fixtures.py`).
*   **Key Test Scenarios:**
    *   `test_successful_image_result_callback(odoo_api_client, setup_ai_request_in_odoo)`:
        *   `setup_ai_request_in_odoo`: Fixture to create an `AIImageGenerationRequest` record in Odoo in a 'processing' state.
        *   Payload: `{'request_id': ..., 'status': 'completed', 'image_url': '...', 'image_metadata': {...}}`.
        *   Action: `odoo_api_client.post('/influence_gen/n8n/ai_image_callback', json_payload=payload)`.
        *   Assert: HTTP 200. Verify `AIImageGenerationRequest` status is 'completed', `GeneratedImage` record created with correct details via Odoo ORM (using test utils or another API call if needed).
    *   `test_failed_image_generation_callback(odoo_api_client, setup_ai_request_in_odoo)`:
        *   Payload: `{'request_id': ..., 'status': 'failed', 'error_message': '...'}`.
        *   Action: POST to callback.
        *   Assert: HTTP 200. Verify `AIImageGenerationRequest` status is 'failed', error message stored.
    *   `test_unauthenticated_callback_rejection(unauthenticated_api_client_fixture)`:
        *   Action: POST with an API client that lacks valid authentication.
        *   Assert: HTTP 401 or 403.
    *   `test_callback_with_invalid_request_id(odoo_api_client)`:
        *   Payload with non-existent `request_id`.
        *   Assert: Appropriate error response (e.g., HTTP 404 or 400).
    *   `test_callback_with_malformed_payload(odoo_api_client, setup_ai_request_in_odoo)`:
        *   Payload missing required fields.
        *   Assert: HTTP 400 Bad Request.
*   **Implemented Requirements:** REQ-DTS-003 (by testing a critical integration point).

#### 3.2.3 `tests/e2e/ui/page_objects/influencer_portal/registration_page.py`
*   **Purpose:** POM for the Influencer Registration page.
*   **Framework:** Playwright.
*   **Class Structure:**
    python
    # In Python for Playwright with PyTest, or JS if preferred for Playwright native runner
    class RegistrationPage:
        URL = "/influencer/register" # Or the specific Odoo portal path

        def __init__(self, page): # Playwright Page object
            self.page = page
            # Locators (use robust selectors)
            self.full_name_input = page.locator("input[name='name']") # Example, adjust to actual field names
            self.email_input = page.locator("input[name='login']")
            self.phone_input = page.locator("input[name='phone']")
            self.password_input = page.locator("input[name='password']")
            self.confirm_password_input = page.locator("input[name='password_confirm']")
            self.tos_checkbox = page.locator("input[name='terms_accepted']")
            self.submit_button = page.locator("button[type='submit']:has-text('Register')") # Example
            self.success_message = page.locator("div.oe_signup_successful") # Example
            self.error_message_field_specific = lambda field_name: page.locator(f"//input[@name='{field_name}']/following-sibling::div[@class='o_form_invalid_feedback']") # Example for field specific error
            self.generic_error_message = page.locator(".alert-danger")


        async def navigate(self):
            await self.page.goto(self.URL)

        async def fill_registration_form(self, full_name, email, phone, password, confirm_password):
            await self.full_name_input.fill(full_name)
            await self.email_input.fill(email)
            await self.phone_input.fill(phone)
            await self.password_input.fill(password)
            await self.confirm_password_input.fill(confirm_password)

        async def accept_tos(self):
            await self.tos_checkbox.check()

        async def submit_form(self):
            await self.submit_button.click()
            # Add waits for navigation or expected outcome
            # e.g., await self.page.wait_for_url("**/kyc**") or await self.success_message.wait_for()

        async def get_field_error_message(self, field_name):
            locator = self.error_message_field_specific(field_name)
            if await locator.is_visible():
                return await locator.text_content()
            return None

        async def get_generic_error_message(self):
            if await self.generic_error_message.is_visible():
                return await self.generic_error_message.text_content()
            return None
    
*   **Implemented Requirements:** (Supports tests for) REQ-UIUX-007, REQ-PERF-KYC-001.

#### 3.2.4 `tests/e2e/ui/features/test_influencer_onboarding_flow.py`
*   **Purpose:** E2E validation of the influencer onboarding process.
*   **Framework:** Playwright with PyTest as test runner (or Playwright native).
*   **POMs Used:** `RegistrationPage`, `LoginPage`, `KYCPage` (for personal details, document upload), `SocialMediaPage`, `BankAccountPage`, `DashboardPage`.
*   **Fixtures:** `page` (Playwright), test data fixtures (e.g., loading from CSV).
*   **Key Test Scenarios (Async for Playwright):**
    *   `async def test_successful_onboarding_journey(page, valid_influencer_data)`:
        *   Instantiate `RegistrationPage`. Navigate and fill form with `valid_influencer_data`. Accept ToS. Submit.
        *   Assert successful registration (e.g., redirect to KYC or dashboard, success message).
        *   *Performance (REQ-UIUX-007):* Measure `page.goto` time, form submission response time.
        *   Instantiate `KYCPage`. Fill personal details.
        *   Upload mock ID documents (use `page.set_input_files`).
        *   Submit KYC data. Assert confirmation.
        *   *Performance (REQ-PERF-KYC-001 related UI interaction):* Measure KYC form submission response time.
        *   (Simulate admin approval if not part of this E2E scope, or use test utils to set status).
        *   Instantiate `LoginPage`. Login with new credentials.
        *   Instantiate `DashboardPage`. Assert successful login and dashboard elements are visible. Account status is 'active'.
    *   `async def test_onboarding_with_invalid_kyc_document_upload(page, registered_user_fixture, invalid_doc_data)`:
        *   Use `registered_user_fixture` to log in an influencer at KYC stage.
        *   Instantiate `KYCPage`. Attempt to upload invalid file type for ID.
        *   Assert UI error message related to file type.
    *   `async def test_onboarding_missing_required_fields_registration(page)`:
        *   Instantiate `RegistrationPage`. Attempt to submit with missing required fields.
        *   Assert field-specific error messages.
*   **Implemented Requirements:** REQ-DTS-001, REQ-DTS-002, REQ-DTS-003 (by testing the flow in a representative env), REQ-UIUX-007, REQ-PERF-KYC-001.

#### 3.2.5 `tests/e2e/ui/accessibility/test_influencer_portal_wcag.py`
*   **Purpose:** Ensures the influencer portal meets WCAG 2.1 AA.
*   **Framework:** Playwright with `axe-playwright`.
*   **Structure (Async for Playwright):**
    python
    # Using PyTest with Playwright
    import pytest
    from playwright.async_api import Page
    from axe_playwright.async_api import Axe # Async version

    @pytest.mark.accessibility
    async def test_registration_page_accessibility(page: Page, environment_config):
        axe = Axe()
        await page.goto(f"{environment_config['odoo_app_url']}/influencer/register") # Example URL
        results = await axe.run(page)
        assert len(results.violations) == 0, f"Accessibility violations on Registration Page: {results.generate_report()}"

    @pytest.mark.accessibility
    async def test_dashboard_accessibility(page: Page, logged_in_influencer_page: Page, environment_config): # logged_in_influencer_page is a fixture providing a logged-in page
        axe = Axe()
        # logged_in_influencer_page is already on dashboard or navigate to it
        await logged_in_influencer_page.goto(f"{environment_config['odoo_app_url']}/my/dashboard")
        results = await axe.run(logged_in_influencer_page)
        assert len(results.violations) == 0, f"Accessibility violations on Dashboard: {results.generate_report()}"

    # Similarly, tests for:
    # - Campaign Discovery Page
    # - Campaign Details Page
    # - Content Submission Form
    # - Profile Management Page
    # - KYC Forms
    
*   **Key Checks:** Test for keyboard navigation, screen reader compatibility (manual checks often supplement automated ones), color contrast, alt text. Axe-core helps automate many of these.
*   **Implemented Requirements:** REQ-14-006.

#### 3.2.6 `tests/performance/scripts/k6/onboarding_stress_test.js`
*   **Purpose:** Stress/throughput test for influencer onboarding (API focused).
*   **Framework:** k6
*   **Configuration:** `tests/performance/config/k6_options_default.js` provides base.
*   **Target Endpoints (API-level for backend stress):**
    *   Odoo controller for registration form submission.
    *   Odoo controller for KYC data submission.
*   **Logic Details:**
    *   Use `setup()` function in k6 to prepare any common data or tokens if needed.
    *   Main `default` function:
        *   `group('User Registration API', ...)`: POST to registration API.
        *   `check()` for HTTP 200/201 and specific success conditions in response.
        *   Add request duration to a `Trend` metric for registration.
        *   `sleep()` for think time.
        *   `group('KYC Data Submission API', ...)`: POST to KYC API (correlate user if possible, or simulate distinct KYC submissions).
        *   `check()` for HTTP 200 and success.
        *   Add request duration to a `Trend` metric for KYC submission.
    *   **Options (`export const options = ...`)**:
        *   `stages`: Define ramp-up, sustained load, and ramp-down stages to meet REQ-PERF-THR-001 (50-100/hr, peak 150/hr for registrations). E.g., Calculate VUs and iteration rates needed. (150 registrations/hr is roughly 2.5 registrations/minute. If a full flow takes, say, 10 seconds of active requests, multiple VUs will be needed).
        *   `thresholds`:
            *   `http_req_failed`: `<0.01`
            *   `registration_api_duration{group:::User Registration API}`: `p(95)<5000` (REQ-PERF-KYC-001 for initial form submission)
            *   `kyc_submission_api_duration{group:::KYC Data Submission API}`: `p(95)<10000` (REQ-PERF-KYC-001 for API part of KYC step)
            *   `iterations`: check if total iterations meet the throughput requirement (e.g., `count>=X` within the sustained load duration).
*   **Implemented Requirements:** REQ-PERF-STRESS-001, REQ-PERF-THR-001, REQ-PERF-KYC-001.

#### 3.2.7 `tests/performance/scripts/k6/ai_generation_stress_test.js`
*   **Purpose:** Stress test AI image generation trigger API.
*   **Framework:** k6
*   **Target Endpoint:** Odoo API endpoint that initiates AI generation via N8N.
*   **Logic Details:**
    *   Main `default` function:
        *   `group('AI Image Generation Trigger API', ...)`: POST to Odoo's AI trigger endpoint with a unique prompt.
        *   `check()` for HTTP 202 (Accepted) or 200.
        *   Add request duration to a `Trend` metric.
    *   **Options:**
        *   `stages`: Ramp up to 200 concurrent VUs as per REQ-PERF-STRESS-001.
        *   `thresholds`:
            *   `http_req_failed`: `<0.05`
            *   `ai_trigger_api_duration`: `p(95)<2000` (time for Odoo to accept the request and fire webhook).
*   **Implemented Requirements:** REQ-PERF-STRESS-001.

#### 3.2.8 `tests/performance/scripts/k6/page_load_times_test.js`
*   **Purpose:** Measure UI page load times for key pages.
*   **Framework:** k6 (potentially using `k6-browser` module for more accurate Web Vitals, or simplified HTTP GETs for server response + base HTML).
*   **Target Pages:** Key influencer portal pages (Dashboard, Campaign Discovery, Profile) and critical Admin backend pages.
*   **Logic Details:**
    *   List of URLs to test.
    *   `default` function iterates through URLs.
    *   `group` for each page.
    *   `http.get(url)` to fetch the page.
    *   `check()` for HTTP 200.
    *   Add `res.timings.duration` to a `Trend`. If using `k6-browser`, collect Core Web Vitals.
    *   **Options:**
        *   `stages`: Simulate typical concurrent browsing users (e.g., 10-50 VUs).
        *   `thresholds`:
            *   `http_req_failed`: `<0.01`
            *   `page_load_duration_trend_all_pages`: `p(95)<3000` (REQ-UIUX-007).
            *   Individual thresholds per page group if some are expected to be heavier.
*   **Implemented Requirements:** REQ-UIUX-007.

#### 3.2.9 `tests/security/scripts/vulnerability_scans/run_zap_scan.sh`
*   **Purpose:** Automate triggering of OWASP ZAP DAST scans.
*   **Tool:** Shell script.
*   **Logic Details:**
    *   Accept `TARGET_URL` as an environment variable or parameter.
    *   Use ZAP Docker image (`owasp/zap2docker-stable`).
    *   Command: `docker run --rm -v $(pwd)/zap_reports:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t $TARGET_URL -r influencegen_zap_report.html`
    *   (Optional) Integrate ZAP context files for authenticated scans.
    *   (Optional) Use ZAP Full Scan or API Scan if more depth is needed beyond baseline.
    *   The script's role is to *initiate* the scan. CI/CD pipeline would handle report collection/parsing.
*   **Implemented Requirements:** REQ-SEC-VULN-001.

### 3.3 `tests/shared/` Directory

#### 3.3.1 `tests/shared/utils/api_client_base.py`
*   **Purpose:** Reusable base class for API clients.
*   **Framework:** Python with `requests`.
*   **Class Structure:**
    python
    import requests
    import os
    from dotenv import load_dotenv

    class APIClientBase:
        def __init__(self, base_url_env_key="BASE_URL", default_base_url="http://localhost:8069"):
            load_dotenv()
            self.base_url = os.getenv(base_url_env_key, default_base_url)
            self.session = requests.Session()
            self.default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            self.session.headers.update(self.default_headers)
            # Implement a method or expect token to be set for authenticated requests
            # self.set_auth_token(os.getenv("API_AUTH_TOKEN_PLACEHOLDER"))

        def set_auth_token(self, token):
            if token:
                self.session.headers.update({'Authorization': f'Bearer {token}'})
            elif 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']

        def _make_request(self, method, endpoint, params=None, data=None, json_payload=None, headers=None, **kwargs):
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            merged_headers = self.session.headers.copy()
            if headers:
                merged_headers.update(headers)
            
            try:
                response = self.session.request(method, url, params=params, data=data, json=json_payload, headers=merged_headers, **kwargs)
                response.raise_for_status() # Optional: raise HTTPError for bad responses (4xx or 5xx)
                return response
            except requests.exceptions.RequestException as e:
                # Log error or handle as needed
                print(f"API Request Failed: {e}")
                raise

        def get(self, endpoint, params=None, headers=None, **kwargs):
            return self._make_request("GET", endpoint, params=params, headers=headers, **kwargs)

        def post(self, endpoint, data=None, json_payload=None, headers=None, **kwargs):
            return self._make_request("POST", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)
        
        # Add put, delete, patch methods as needed
    

#### 3.3.2 `tests/shared/utils/odoo_test_utils.py`
*   **Purpose:** Odoo-specific test helpers for backend tests (primarily for tests running within Odoo's test runner context).
*   **Structure (for use with `odoo.tests.common`):**
    python
    # To be used when tests are part of an Odoo module and run with Odoo's test runner
    # For external tests, one might use an Odoo client library (e.g. ERPpeek, odoorpc)

    def create_test_influencer(env, name, email, **extra_profile_vals):
        """Creates a res.users and an associated influence_gen.influencer_profile."""
        UserModel = env['res.users']
        ProfileModel = env['influence_gen.influencer_profile'] # Replace with actual model name

        user = UserModel.search([('login', '=', email)], limit=1)
        if not user:
            user = UserModel.create({
                'name': name,
                'login': email,
                'password': 'testpassword123', # Default test password
                'groups_id': [(6, 0, [env.ref('base.group_portal').id])], # Example
            })
        
        profile = ProfileModel.search([('user_id', '=', user.id)], limit=1)
        if not profile:
            profile_vals = {
                'user_id': user.id,
                'full_name': name,
                'email': email,
            }
            profile_vals.update(extra_profile_vals)
            profile = ProfileModel.create(profile_vals)
        return profile

    def get_campaign_by_name(env, campaign_name):
        """Fetches a campaign by its name."""
        CampaignModel = env['influence_gen.campaign'] # Replace with actual model name
        return CampaignModel.search([('name', '=', campaign_name)], limit=1)

    def set_kyc_status_for_influencer(env, influencer_profile_id, new_status, reviewer_user_id=None):
        """Updates the KYC status for a given influencer profile."""
        ProfileModel = env['influence_gen.influencer_profile'] # Replace with actual model name
        profile = ProfileModel.browse(influencer_profile_id)
        if not profile.exists():
            raise ValueError(f"Influencer profile with ID {influencer_profile_id} not found.")
        
        # This assumes KYC status is on the profile. If it's on a separate KYCData model:
        # KYCModel = env['influence_gen.kyc_data']
        # kyc_record = KYCModel.search([('influencer_profile_id', '=', influencer_profile_id)], limit=1, order='create_date desc')
        # if kyc_record:
        #    kyc_record.write({'verification_status': new_status, 'reviewer_user_id': reviewer_user_id})
        # else: # Or create one if test assumes it
        #    raise ValueError("No KYC record found for profile.")
        profile.write({'kyc_status': new_status}) # If status is directly on profile
        return profile
    

#### 3.3.3 `tests/shared/fixtures/common_fixtures.py`
*   **Purpose:** Reusable PyTest fixtures.
*   **Structure:**
    python
    import pytest
    import os
    import json
    import uuid
    from dotenv import load_dotenv
    from tests.shared.utils.api_client_base import APIClientBase

    @pytest.fixture(scope='session', autouse=True)
    def load_env_vars():
        load_dotenv() # Load .env for local runs

    @pytest.fixture(scope='session')
    def environment_config():
        env_name = os.getenv("TEST_ENV", "staging") # Default if not set
        config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'environments', f"{env_name}_config.json")
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            # Replace placeholders with actual env vars
            for key, value in config.items():
                if isinstance(value, str) and value.endswith("_PLACEHOLDER"):
                    env_var_name = value.replace("_PLACEHOLDER", "")
                    config[key] = os.getenv(env_var_name, f"MISSING_ENV_VAR_{env_var_name}")
            return config
        except FileNotFoundError:
            pytest.fail(f"Environment configuration file not found: {config_file}")
        except json.JSONDecodeError:
            pytest.fail(f"Error decoding JSON from environment configuration file: {config_file}")

    @pytest.fixture(scope='session')
    def odoo_api_client_session(environment_config):
        client = APIClientBase(base_url_env_key="ODOO_API_BASE_URL_PLACEHOLDER") # Key in JSON config
        client.base_url = environment_config.get("odoo_api_base_url", client.base_url)
        # Attempt authentication if auth details are provided in config/env
        # client.set_auth_token(environment_config.get("default_test_api_token"))
        return client
    
    @pytest.fixture
    def odoo_api_client_function(environment_config): # Function scope if state needs to be reset
        client = APIClientBase(base_url_env_key="ODOO_API_BASE_URL_PLACEHOLDER")
        client.base_url = environment_config.get("odoo_api_base_url", client.base_url)
        return client

    @pytest.fixture
    def generate_random_email():
        return f"test.user.{uuid.uuid4().hex[:6]}@influencegen-test.com"

    # Playwright specific fixtures are usually handled within Playwright's test structure (e.g. page fixture)
    # but if using PyTest to run Playwright, global browser setup can be a fixture.
    

### 3.4 `tests/test_data/` Directory

#### 3.4.1 `tests/test_data/onboarding/influencer_profiles_valid.csv`
*   **Purpose:** Valid input data for successful influencer onboarding tests.
*   **Format:** CSV.
*   **Example Columns:** `test_case_id,full_name,email_suffix,phone_number,password,kyc_doc_file,kyc_doc_type,social_platform,social_handle`
*   **Example Row:** `TC001_ValidOnboarding,Alice Wonderland,alice_valid,1234567890,ValidPass123!,dummy_passport.pdf,passport,Instagram,alice_insta_valid`
*   **Notes:**
    *   `email_suffix` can be combined with a base domain (e.g., `@example.com`) by the test script.
    *   `kyc_doc_file` points to a dummy file within the test suite (e.g., `tests/test_data/documents/dummy_passport.pdf`).
    *   Ensure data is representative as per REQ-DTS-003.
    *   Create corresponding `influencer_profiles_invalid.csv` for negative test cases.

### 3.5 `tests/config/environments/` Directory

#### 3.5.1 `tests/config/environments/staging_config.json`
*   **Purpose:** Staging environment-specific parameters.
*   **Format:** JSON.
*   **Content (Example with placeholders for env vars):**
    json
    {
      "odoo_app_url": "STAGING_ODOO_APP_URL_PLACEHOLDER",
      "odoo_api_base_url": "STAGING_ODOO_API_BASE_URL_PLACEHOLDER",
      "n8n_webhook_base_url": "STAGING_N8N_WEBHOOK_URL_PLACEHOLDER",
      "default_influencer_username_placeholder": "STAGING_INFLUENCER_USERNAME_ENV_VAR",
      "default_influencer_password_placeholder": "STAGING_INFLUENCER_PASSWORD_ENV_VAR",
      "default_admin_username_placeholder": "STAGING_ADMIN_USERNAME_ENV_VAR",
      "default_admin_password_placeholder": "STAGING_ADMIN_PASSWORD_ENV_VAR",
      "zap_target_url_placeholder": "STAGING_ODOO_APP_URL_PLACEHOLDER",
      "k6_base_url_placeholder": "STAGING_ODOO_APP_URL_PLACEHOLDER"
    }
    
    *   The test framework (e.g., in `common_fixtures.py`) will resolve these `_PLACEHOLDER` values against actual environment variables at runtime.
    *   Similar files like `dev_config.json`, `prod_config.json` (for prod, with extreme caution) would exist.

### 3.6 `tests/reports_config/` Directory

#### 3.6.1 `tests/reports_config/allure_config.json` (Conceptual - Allure is usually configured via its CLI or CI plugin)
*   **Purpose:** Illustrates how Allure might be customized if directly configurable via a JSON. In practice, this is often handled by `allure-pytest` or `allure-playwright` command-line arguments or environment variables passed to the Allure generator.
*   **Example (if such a file were directly used by a custom Allure generation script):**
    json
    {
      "reportName": "InfluenceGen Test Execution Report",
      "categories": [
        {
          "name": "Critical UI Failures",
          "messageRegex": ".*TimeoutError.*|.*ElementNotFound.*",
          "matchedStatuses": ["failed", "broken"]
        },
        {
          "name": "API Validation Errors",
          "messageRegex": ".*(400 Bad Request|401 Unauthorized|API schema validation failed).*",
          "matchedStatuses": ["failed"]
        }
      ],
      "environment": [ // These would typically be passed to Allure during report generation
        {"name": "Target Environment", "value": "Staging"},
        {"name": "Browser", "value": "Chromium"},
        {"name": "Build Version", "value": "1.2.3"}
      ]
    }
    

### 3.7 `tests/performance/config/k6_options_default.js`
*   **Purpose:** Base k6 options for consistency across performance test scripts.
*   **Format:** JavaScript module exporting an options object.
*   **Content:**
    javascript
    export const defaultK6Options = {
      discardResponseBodies: false, // Set to true for pure load tests if bodies not needed
      summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)', 'count', 'rate'],
      noConnectionReuse: false,
      userAgent: 'InfluenceGenK6PerformanceTester/1.0 (REQ-PERF-STRESS-001; REQ-PERF-THR-001; REQ-PERF-KYC-001; REQ-UIUX-007)',
      thresholds: { // General default thresholds
        'http_req_duration': ['p(95) < 3000'], // Default max p95 duration for any request
        'http_req_failed': ['rate < 0.01'], // Less than 1% requests failing
        'checks': ['rate > 0.99'], // Over 99% of checks should pass
      },
      // Common tags that can be applied to all metrics
      // tags: {
      //   test_type: 'performance',
      // },
    };
    
    **Usage in individual k6 scripts:**
    javascript
    import { defaultK6Options } from '../config/k6_options_default.js';
    import { Trend } from 'k6/metrics';
    // ...

    export const options = Object.assign({}, defaultK6Options, {
      stages: [ /* specific stages for this test */ ],
      thresholds: {
        ...defaultK6Options.thresholds, // Inherit default thresholds
        'http_req_duration{group:::CriticalFlowStep}': ['p(95)<500'], // Override/add specific
        'my_custom_trend': ['avg < 100'],
      }
    });
    

## 4. Test Data Management Strategy
*   **Source:** Primary test data will be stored in CSV files within `tests/test_data/` subdirectories, categorized by feature (e.g., `onboarding`, `campaigns`). Dynamic data generation (e.g., unique emails, random strings) will be handled by utility functions or fixtures.
*   **Structure:** Each CSV will have a header row. Test scripts will parse these CSVs to drive tests.
*   **Anonymization (REQ-DTS-003):** For tests running against Staging/UAT (especially if data is ever seeded from a sanitized prod backup), any PII-like data must be fully anonymized or synthetic. For local/dev tests with purely synthetic data, this is less critical but good practice.
*   **Accessibility:** Test files (e.g., dummy documents for KYC uploads) will be stored in `tests/test_data/documents/`.

## 5. Test Execution and Reporting
*   **Execution:** Test suites will be triggered via `npm run <script-name>` (for JS-based tests) or `pytest <path>` (for Python tests). CI/CD pipelines will use these commands.
*   **Reporting:**
    *   **Allure Framework:** Primary reporting tool. `allure-pytest` and `allure-playwright` will generate Allure results. CI will then use Allure CLI to generate the HTML report.
    *   **PyTest HTML:** `pytest-html` for quick local reports from PyTest.
    *   **k6 Output:** k6 provides CLI summary and can output results to JSON, CSV, or directly to InfluxDB/Prometheus for dashboards (e.g., Grafana).
    *   **Newman Output:** Can generate JUnit XML, HTML reports.
    *   **DAST Reports:** OWASP ZAP generates HTML reports. CI will archive these.

## 6. Dependencies on Other Repositories (Systems Under Test)
The tests within this repository will interact with and validate the functionalities of:
*   `REPO-IGOP-001` (InfluenceGen.Odoo.Portal.Endpoints): UI tests, accessibility tests.
*   `REPO-IGOA-002` (InfluenceGen.Odoo.Admin.Backend): Admin UI tests.
*   `REPO-IGBS-003` (InfluenceGen.Odoo.Business.Services): Odoo unit and integration tests.
*   `REPO-IGOII-004` (InfluenceGen.Odoo.Infrastructure.Integration.Services): API integration tests, N8N callback tests.
*   `REPO-N8NO-005` (InfluenceGen.N8N.Orchestration.Workflows): API tests triggering N8N.
*   `REPO-IGEI-006` (InfluenceGen.External.AI.Service.Integration): Indirectly via N8N.

Test environments must have correctly deployed and configured versions of these dependent systems.

## 7. Non-Functional Requirements Coverage
This test suite is designed to provide coverage for the following key non-functional requirements:
*   **Performance & Scalability:** (REQ-PERF-STRESS-001, REQ-PERF-THR-001, REQ-PERF-KYC-001) Covered by k6 stress, load, and throughput tests.
*   **Security:** (REQ-SEC-VULN-001) Covered by DAST scan automation scripts. API tests will also verify authentication/authorization.
*   **Usability (Responsiveness & Page Load):** (REQ-UIUX-007) Covered by k6 page load tests and interaction time measurements within E2E UI tests.
*   **Accessibility:** (REQ-14-006) Covered by Playwright/Axe-core tests against WCAG 2.1 AA.
*   **System Readiness for Documentation & Training:** (REQ-DTS-001, REQ-DTS-002, REQ-DTS-003, REQ-DTS-004) While not directly testing the training materials, the suite ensures the application's stability and that test environments are representative, which are prerequisites for creating and delivering effective training and documentation. The configuration of a training-like environment for testing (`staging_config.json`) aligns with REQ-DTS-003.
