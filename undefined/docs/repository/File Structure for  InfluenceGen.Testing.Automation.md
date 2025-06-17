# Specification

# 1. Files

- **Path:** package.json  
**Description:** Project configuration for JavaScript-based testing tools (e.g., Playwright, k6, Newman). Manages dependencies, scripts for running tests, and other project metadata.  
**Template:** JavaScript Project Descriptor  
**Dependancy Level:** 0  
**Name:** package  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management (JS)
    - Test Execution Scripts (JS)
    
**Requirement Ids:**
    
    - REQ-DTS-001
    - REQ-DTS-002
    - REQ-DTS-003
    - REQ-DTS-004
    - REQ-PERF-STRESS-001
    - REQ-SEC-VULN-001
    - REQ-14-006
    - REQ-PERF-THR-001
    - REQ-PERF-KYC-001
    - REQ-UIUX-007
    
**Purpose:** Defines JavaScript project dependencies and scripts for test execution.  
**Logic Description:** Contains configurations for npm/yarn, including dependencies for Playwright, k6, Newman, and any supporting JavaScript libraries. Defines script aliases for running different test suites (e.g., 'npm run test:e2e', 'npm run test:perf:k6').  
**Documentation:**
    
    - **Summary:** Manages Node.js package dependencies and scripts for executing JavaScript-based automated tests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BuildConfiguration
    
- **Path:** requirements.txt  
**Description:** Lists Python dependencies for the testing framework (e.g., PyTest, Selenium, requests). Used by pip to install necessary packages.  
**Template:** Python Requirements File  
**Dependancy Level:** 0  
**Name:** requirements  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dependency Management (Python)
    
**Requirement Ids:**
    
    - REQ-DTS-001
    - REQ-DTS-002
    - REQ-DTS-003
    - REQ-DTS-004
    - REQ-PERF-STRESS-001
    - REQ-SEC-VULN-001
    - REQ-14-006
    - REQ-PERF-THR-001
    - REQ-PERF-KYC-001
    - REQ-UIUX-007
    
**Purpose:** Specifies Python package dependencies for the test automation suite.  
**Logic Description:** A plain text file listing Python packages and their versions required for running PyTest, Selenium, and other Python-based test scripts and utilities. Example: pytest==7.x.x, selenium==4.x.x.  
**Documentation:**
    
    - **Summary:** Defines Python dependencies needed for the test automation framework.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BuildConfiguration
    
- **Path:** pytest.ini  
**Description:** Configuration file for PyTest. Defines test discovery patterns, markers, plugins, and default command-line options for Python-based tests.  
**Template:** PyTest Configuration  
**Dependancy Level:** 0  
**Name:** pytest  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Test Runner Configuration (PyTest)
    
**Requirement Ids:**
    
    - REQ-DTS-001
    - REQ-DTS-002
    - REQ-DTS-003
    - REQ-DTS-004
    
**Purpose:** Configures the PyTest test runner for Python tests.  
**Logic Description:** Contains sections like [pytest] to specify options such as 'python_files = test_*.py', 'python_classes = Test*', 'python_functions = test_*'. May include settings for reporting, fixtures, and test markers.  
**Documentation:**
    
    - **Summary:** PyTest runner configuration file. Controls test discovery, execution parameters, and plugin settings for Python tests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestConfiguration
    
- **Path:** playwright.config.js  
**Description:** Configuration file for Playwright. Defines browser settings, test execution parameters (e.g., parallelism, timeouts), reporter options, and project setups for E2E UI tests.  
**Template:** Playwright Configuration  
**Dependancy Level:** 0  
**Name:** playwright.config  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Test Runner Configuration (Playwright)
    
**Requirement Ids:**
    
    - REQ-14-006
    - REQ-UIUX-007
    
**Purpose:** Configures the Playwright test runner for E2E UI automation tests.  
**Logic Description:** JavaScript file exporting a configuration object. Specifies projects for different browsers (Chromium, Firefox, WebKit), global setup/teardown, base URL, viewport settings, trace options, and screenshot/video recording settings.  
**Documentation:**
    
    - **Summary:** Playwright test framework configuration. Defines browser contexts, test execution settings, and reporting for UI tests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestConfiguration
    
- **Path:** tests/unit/odoo/onboarding/test_kyc_logic_simulation.py  
**Description:** Unit tests for simulating KYC logic components within the Odoo business logic layer. Focuses on isolated validation rules and status transitions related to KYC, potentially mocking Odoo ORM calls for true unit testing.  
**Template:** Python PyTest File  
**Dependancy Level:** 2  
**Name:** test_kyc_logic_simulation  
**Type:** UnitTest  
**Relative Path:** unit/odoo/onboarding/test_kyc_logic_simulation.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_valid_document_type_acceptance  
**Parameters:**
    
    - mock_kyc_service
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_invalid_document_type_rejection  
**Parameters:**
    
    - mock_kyc_service
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_kyc_status_update_on_approval  
**Parameters:**
    
    - mock_influencer_profile
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - KYC Logic Unit Testing
    
**Requirement Ids:**
    
    - REQ-DTS-001
    - REQ-DTS-002
    - REQ-DTS-003
    
**Purpose:** Validates individual units of KYC business logic implemented in Odoo modules.  
**Logic Description:** Uses PyTest. Mocks dependencies like Odoo models or external services if testing pure logic. Tests functions responsible for validating KYC data fields, checking document requirements, and managing KYC status transitions. Verifies that these units behave correctly given various inputs.  
**Documentation:**
    
    - **Summary:** Contains unit tests for KYC business logic components in Odoo, ensuring individual functions operate as expected.
    
**Namespace:** InfluenceGen.Testing.Unit.Odoo.Onboarding  
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/integration/odoo_api/test_n8n_callback_api.py  
**Description:** Integration tests for the Odoo REST API endpoint that N8N calls back with AI image generation results. Verifies API authentication, request/response format, and processing of callback data.  
**Template:** Python PyTest File  
**Dependancy Level:** 3  
**Name:** test_n8n_callback_api  
**Type:** IntegrationTest  
**Relative Path:** integration/odoo_api/test_n8n_callback_api.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_successful_image_result_callback  
**Parameters:**
    
    - api_client
    - sample_image_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_failed_image_generation_callback  
**Parameters:**
    
    - api_client
    - sample_error_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_unauthenticated_callback_rejection  
**Parameters:**
    
    - unauth_api_client
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Odoo N8N Callback API Integration Testing
    
**Requirement Ids:**
    
    - REQ-DTS-003
    
**Purpose:** Ensures the Odoo callback API for N8N functions correctly, processing image results or errors.  
**Logic Description:** Uses PyTest and a shared API client (e.g., `requests` wrapper). Makes HTTP POST requests to the Odoo callback endpoint, simulating N8N. Validates HTTP status codes, response structure, and data persistence/updates in Odoo models (e.g., `AIImageGenerationRequest`, `GeneratedImage` status updates).  
**Documentation:**
    
    - **Summary:** Integration tests for the Odoo API endpoint that receives AI image generation results from N8N.
    
**Namespace:** InfluenceGen.Testing.Integration.OdooAPI  
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/e2e/ui/page_objects/influencer_portal/registration_page.py  
**Description:** Page Object Model (POM) representation for the Influencer Registration page in the Odoo portal. Encapsulates UI elements and actions.  
**Template:** Python Selenium/Playwright Page Object  
**Dependancy Level:** 3  
**Name:** registration_page  
**Type:** PageObject  
**Relative Path:** e2e/ui/page_objects/influencer_portal/registration_page.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    - **Name:** full_name_input  
**Type:** Locator  
**Attributes:** private  
    - **Name:** email_input  
**Type:** Locator  
**Attributes:** private  
    - **Name:** submit_button  
**Type:** Locator  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** fill_registration_form  
**Parameters:**
    
    - name
    - email
    - password
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** submit_form  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_error_message  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Registration Page Abstraction
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    - REQ-PERF-KYC-001
    
**Purpose:** Provides a reusable, maintainable abstraction for interacting with the influencer registration page.  
**Logic Description:** Defines locators for page elements (e.g., input fields, buttons) and methods to perform actions like filling the form, clicking submit, and retrieving validation messages. Uses Selenium or Playwright API.  
**Documentation:**
    
    - **Summary:** Page Object for the influencer registration UI. Abstracts element locators and user interactions.
    
**Namespace:** InfluenceGen.Testing.E2E.UI.PageObjects.InfluencerPortal  
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/e2e/ui/features/test_influencer_onboarding_flow.py  
**Description:** End-to-end test script for the complete influencer onboarding flow, from registration to KYC submission and account activation.  
**Template:** Python Selenium/Playwright Test Script  
**Dependancy Level:** 4  
**Name:** test_influencer_onboarding_flow  
**Type:** E2ETest  
**Relative Path:** e2e/ui/features/test_influencer_onboarding_flow.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    - PageObjectModel
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_successful_onboarding_journey  
**Parameters:**
    
    - browser_context
    - test_data_onboarding
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_onboarding_with_invalid_kyc_data  
**Parameters:**
    
    - browser_context
    - test_data_invalid_kyc
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - E2E Influencer Onboarding Validation
    
**Requirement Ids:**
    
    - REQ-DTS-001
    - REQ-DTS-002
    - REQ-DTS-003
    - REQ-UIUX-007
    - REQ-PERF-KYC-001
    
**Purpose:** Validates the entire influencer onboarding process from a user's perspective.  
**Logic Description:** Uses Page Objects for UI interactions (e.g., `RegistrationPage`, `KYCSubmissionPage`). Simulates an influencer registering, submitting KYC documents, and verifying account status updates. Asserts UI elements, messages, and potentially data state changes. Measures page load times and interaction feedback times as per REQ-UIUX-007.  
**Documentation:**
    
    - **Summary:** End-to-end tests covering the influencer onboarding workflow via the UI.
    
**Namespace:** InfluenceGen.Testing.E2E.UI.Features  
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/e2e/ui/accessibility/test_influencer_portal_wcag.py  
**Description:** Accessibility tests for the influencer portal, checking compliance with WCAG 2.1 Level AA standards.  
**Template:** Python Playwright/Selenium Accessibility Test  
**Dependancy Level:** 4  
**Name:** test_influencer_portal_wcag  
**Type:** AccessibilityTest  
**Relative Path:** e2e/ui/accessibility/test_influencer_portal_wcag.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_registration_page_accessibility  
**Parameters:**
    
    - page
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_dashboard_accessibility  
**Parameters:**
    
    - page
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** test_campaign_discovery_accessibility  
**Parameters:**
    
    - page
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Portal WCAG 2.1 AA Compliance Testing
    
**Requirement Ids:**
    
    - REQ-14-006
    
**Purpose:** Ensures the influencer portal meets specified accessibility standards.  
**Logic Description:** Uses Playwright or Selenium with an accessibility testing library (e.g., Axe-Playwright, Axe-Selenium). Navigates to key influencer portal pages and runs accessibility scans. Asserts that there are no critical or serious WCAG violations according to Level AA.  
**Documentation:**
    
    - **Summary:** Automated accessibility tests for the influencer portal using WCAG 2.1 AA guidelines.
    
**Namespace:** InfluenceGen.Testing.E2E.UI.Accessibility  
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/performance/scripts/k6/onboarding_stress_test.js  
**Description:** k6 performance test script for simulating high load and stress on the influencer onboarding process (registration, KYC submission steps).  
**Template:** JavaScript k6 Script  
**Dependancy Level:** 3  
**Name:** onboarding_stress_test  
**Type:** PerformanceTest  
**Relative Path:** performance/scripts/k6/onboarding_stress_test.js  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** default  
**Parameters:**
    
    - data
    
**Return Type:** void  
**Attributes:** export  
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** object  
**Attributes:** export function  
    
**Implemented Features:**
    
    - Influencer Onboarding Performance/Stress Testing
    
**Requirement Ids:**
    
    - REQ-PERF-STRESS-001
    - REQ-PERF-THR-001
    - REQ-PERF-KYC-001
    - REQ-UIUX-007
    
**Purpose:** Measures the performance and stability of the influencer onboarding system under heavy load.  
**Logic Description:** k6 script defining virtual users (VUs) and scenarios for registration and KYC API endpoints. Simulates concurrent users. Collects metrics like request duration (REQ-PERF-KYC-001, REQ-UIUX-007), error rates, and throughput (REQ-PERF-THR-001). Checks against defined thresholds.  
**Documentation:**
    
    - **Summary:** k6 script for stress and throughput testing of the influencer onboarding APIs and UI interactions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/performance/scripts/k6/ai_generation_stress_test.js  
**Description:** k6 performance test script for simulating stress on the AI image generation feature, focusing on the Odoo-N8N interaction and overall processing time.  
**Template:** JavaScript k6 Script  
**Dependancy Level:** 3  
**Name:** ai_generation_stress_test  
**Type:** PerformanceTest  
**Relative Path:** performance/scripts/k6/ai_generation_stress_test.js  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** default  
**Parameters:**
    
    - data
    
**Return Type:** void  
**Attributes:** export  
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** object  
**Attributes:** export function  
    
**Implemented Features:**
    
    - AI Image Generation Performance/Stress Testing
    
**Requirement Ids:**
    
    - REQ-PERF-STRESS-001
    
**Purpose:** Evaluates the performance of the AI image generation workflow under high concurrency (200 concurrent requests).  
**Logic Description:** k6 script simulating multiple users concurrently requesting AI image generations. Hits the Odoo endpoint that triggers N8N. Measures request success rates, overall generation time (if polling for results or relying on webhook timing), and error rates under stress. Validates against REQ-PERF-STRESS-001 targets.  
**Documentation:**
    
    - **Summary:** k6 script for stress testing the AI image generation feature, particularly the Odoo to N8N webhook invocation.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/performance/scripts/k6/page_load_times_test.js  
**Description:** k6 performance test script focused on measuring page load times for key influencer portal and admin backend pages.  
**Template:** JavaScript k6 Script  
**Dependancy Level:** 3  
**Name:** page_load_times_test  
**Type:** PerformanceTest  
**Relative Path:** performance/scripts/k6/page_load_times_test.js  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** default  
**Parameters:**
    
    - data
    
**Return Type:** void  
**Attributes:** export  
    
**Implemented Features:**
    
    - UI Page Load Time Performance Testing
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    
**Purpose:** Measures client-side and server-side rendering times for critical UI pages to ensure they meet performance targets.  
**Logic Description:** k6 script using browser module (if available and suitable) or making HTTP GET requests to specific page URLs. Measures response times and core web vitals if possible. Checks if 95% of requests load within 3 seconds as per REQ-UIUX-007.  
**Documentation:**
    
    - **Summary:** k6 script to measure and validate page load times for critical UI views.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestCode
    
- **Path:** tests/security/scripts/vulnerability_scans/run_zap_scan.sh  
**Description:** Shell script to automate running OWASP ZAP (or similar DAST tool) scans against deployed environments of the InfluenceGen platform.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** run_zap_scan  
**Type:** SecurityTestScript  
**Relative Path:** security/scripts/vulnerability_scans/run_zap_scan.sh  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Vulnerability Scanning Execution
    
**Requirement Ids:**
    
    - REQ-SEC-VULN-001
    
**Purpose:** Facilitates regular execution of dynamic application security testing (DAST) scans.  
**Logic Description:** A shell script that uses the ZAP API or command-line interface to initiate an automated scan against a target URL (e.g., staging environment). Configures scan policies, context, and authentication. Generates a report upon completion. This script is a trigger; ZAP itself performs the scan.  
**Documentation:**
    
    - **Summary:** Script to automate the execution of OWASP ZAP vulnerability scans against the application.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestTooling
    
- **Path:** tests/shared/utils/api_client_base.py  
**Description:** Base class or utility functions for creating API clients to interact with Odoo, N8N, or other service APIs during tests.  
**Template:** Python Utility Class  
**Dependancy Level:** 1  
**Name:** api_client_base  
**Type:** TestUtility  
**Relative Path:** shared/utils/api_client_base.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** base_url  
**Type:** str  
**Attributes:** protected  
    - **Name:** session  
**Type:** requests.Session  
**Attributes:** protected  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - base_url
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** post  
**Parameters:**
    
    - endpoint
    - data=None
    - json=None
    - headers=None
    
**Return Type:** requests.Response  
**Attributes:** public  
    - **Name:** get  
**Parameters:**
    
    - endpoint
    - params=None
    - headers=None
    
**Return Type:** requests.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - Reusable API Client Logic
    
**Requirement Ids:**
    
    
**Purpose:** Provides a common foundation for making HTTP requests to various APIs under test.  
**Logic Description:** Contains methods for common HTTP verbs (GET, POST, PUT, DELETE), handling authentication (e.g., token injection), setting common headers, and basic response parsing or error handling. Uses the `requests` library.  
**Documentation:**
    
    - **Summary:** Base utility for creating HTTP API clients used in integration and E2E API tests.
    
**Namespace:** InfluenceGen.Testing.Shared.Utils  
**Metadata:**
    
    - **Category:** TestUtility
    
- **Path:** tests/shared/utils/odoo_test_utils.py  
**Description:** Utility functions specific to testing Odoo. May include helpers for creating/querying Odoo records via ORM (for integration tests), or setting up Odoo test environments.  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** odoo_test_utils  
**Type:** TestUtility  
**Relative Path:** shared/utils/odoo_test_utils.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** create_test_influencer  
**Parameters:**
    
    - env
    - name
    - email
    
**Return Type:** odoo.model.browse_record  
**Attributes:** public static  
    - **Name:** get_campaign_by_name  
**Parameters:**
    
    - env
    - campaign_name
    
**Return Type:** odoo.model.browse_record  
**Attributes:** public static  
    - **Name:** set_kyc_status  
**Parameters:**
    
    - env
    - influencer_id
    - status
    
**Return Type:** void  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Odoo-Specific Test Helpers
    
**Requirement Ids:**
    
    
**Purpose:** Simplifies interactions with the Odoo environment during backend unit and integration tests.  
**Logic Description:** Provides functions that wrap Odoo ORM calls to create, find, or update records in a test context. May include methods to simulate user context or specific Odoo configurations for tests.  
**Documentation:**
    
    - **Summary:** Collection of helper functions for facilitating Odoo-specific operations within tests.
    
**Namespace:** InfluenceGen.Testing.Shared.Utils  
**Metadata:**
    
    - **Category:** TestUtility
    
- **Path:** tests/test_data/onboarding/influencer_profiles_valid.csv  
**Description:** Test data file containing valid influencer profile information for onboarding scenarios.  
**Template:** CSV Data File  
**Dependancy Level:** 0  
**Name:** influencer_profiles_valid  
**Type:** TestData  
**Relative Path:** test_data/onboarding/influencer_profiles_valid.csv  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    - DataDrivenTesting
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Valid Onboarding Test Data
    
**Requirement Ids:**
    
    - REQ-DTS-003
    
**Purpose:** Provides valid input data for testing successful influencer onboarding flows.  
**Logic Description:** CSV file with columns like: fullName, email, phone, password, kycDocumentPath, etc. Each row represents a valid test case for successful registration and KYC submission. Data must be representative as per REQ-DTS-003.  
**Documentation:**
    
    - **Summary:** Contains valid sample data for influencer profiles used in onboarding tests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestData
    
- **Path:** tests/config/environments/staging_config.json  
**Description:** Configuration file containing settings specific to the Staging test environment (e.g., application URLs, API endpoints, test user credentials placeholders).  
**Template:** JSON Configuration File  
**Dependancy Level:** 0  
**Name:** staging_config  
**Type:** EnvironmentConfiguration  
**Relative Path:** config/environments/staging_config.json  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Staging Environment Test Configuration
    
**Requirement Ids:**
    
    - REQ-DTS-003
    
**Purpose:** Provides environment-specific parameters for running tests against the Staging environment.  
**Logic Description:** JSON file with key-value pairs for staging_url, staging_api_base_url, default_influencer_username_placeholder, default_admin_password_placeholder (actual sensitive values sourced from secure vault/env vars). Includes settings needed for REQ-DTS-003 representative environment.  
**Documentation:**
    
    - **Summary:** Environment-specific configuration settings for the Staging environment.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestConfiguration
    
- **Path:** tests/reports_config/allure_config.json  
**Description:** Configuration for the Allure test reporting framework. Defines report generation options, categories, and integrations.  
**Template:** JSON Configuration File  
**Dependancy Level:** 0  
**Name:** allure_config  
**Type:** ReportConfiguration  
**Relative Path:** reports_config/allure_config.json  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Test Report Configuration (Allure)
    
**Requirement Ids:**
    
    
**Purpose:** Customizes the generation and appearance of Allure test reports.  
**Logic Description:** JSON file specifying Allure report settings, such as categories for defect classification, custom links, executor information, and history trend settings. Used by the Allure command-line tool or CI plugin.  
**Documentation:**
    
    - **Summary:** Configuration settings for the Allure reporting tool.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ReportConfiguration
    
- **Path:** tests/performance/config/k6_options_default.js  
**Description:** Default k6 options configuration file. Can be overridden or extended by specific test scripts. Defines default VU stages, durations, thresholds.  
**Template:** JavaScript k6 Configuration  
**Dependancy Level:** 1  
**Name:** k6_options_default  
**Type:** PerformanceTestConfiguration  
**Relative Path:** performance/config/k6_options_default.js  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default k6 Performance Test Options
    
**Requirement Ids:**
    
    - REQ-PERF-STRESS-001
    - REQ-PERF-THR-001
    - REQ-PERF-KYC-001
    - REQ-UIUX-007
    
**Purpose:** Provides a base set of options for k6 performance tests, promoting consistency.  
**Logic Description:** JavaScript file exporting an `options` object for k6. Includes default settings for `stages`, `thresholds` (e.g., http_req_failed, http_req_duration p(95)), `summaryTrendStats`. Specific scripts can import and merge these options.  
**Documentation:**
    
    - **Summary:** Default configuration options for k6 performance test scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestConfiguration
    
- **Path:** tests/shared/fixtures/common_fixtures.py  
**Description:** PyTest fixtures that are commonly used across different types of Python-based tests (unit, integration, E2E).  
**Template:** Python PyTest Fixtures File  
**Dependancy Level:** 1  
**Name:** common_fixtures  
**Type:** TestFixture  
**Relative Path:** shared/fixtures/common_fixtures.py  
**Repository Id:** REPO-IGTEST-010  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** test_config  
**Parameters:**
    
    - request
    
**Return Type:** dict  
**Attributes:** @pytest.fixture(scope='session')  
    - **Name:** random_email  
**Parameters:**
    
    
**Return Type:** str  
**Attributes:** @pytest.fixture  
    
**Implemented Features:**
    
    - Reusable PyTest Fixtures
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable setup and teardown logic, and test data generation for PyTest tests.  
**Logic Description:** Defines PyTest fixtures for loading test configurations, generating random test data (like emails, names), initializing API clients with environment-specific settings, or managing browser instances for UI tests.  
**Documentation:**
    
    - **Summary:** Common PyTest fixtures shared across various Python test suites.
    
**Namespace:** InfluenceGen.Testing.Shared.Fixtures  
**Metadata:**
    
    - **Category:** TestUtility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - runAccessibilityTests
  - runFullStressTests
  - generateDetailedPerformanceReport
  
- **Database Configs:**
  
  - test_db_connection_string_placeholder
  - odoo_test_user_placeholder
  - odoo_test_password_placeholder
  


---

