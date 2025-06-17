# Specification

# 1. Files

- **Path:** .gitlab-ci.yml  
**Description:** Main GitLab CI/CD pipeline configuration file. Defines stages, jobs, rules, and includes pipeline templates for building, testing, and deploying InfluenceGen components (Odoo modules, N8N workflows). Orchestrates the entire CI/CD process.  
**Template:** GitLab CI/CD YAML Template  
**Dependancy Level:** 0  
**Name:** .gitlab-ci  
**Type:** PipelineDefinition  
**Relative Path:** .gitlab-ci.yml  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    - PipelineAsCode
    - DevOpsPractices
    
**Members:**
    
    - **Name:** stages  
**Type:** List  
**Attributes:** pipeline-definition  
    - **Name:** variables  
**Type:** Map  
**Attributes:** pipeline-definition  
    - **Name:** default  
**Type:** Map  
**Attributes:** pipeline-definition  
    - **Name:** include  
**Type:** List  
**Attributes:** pipeline-definition  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Continuous Integration
    - Continuous Deployment
    - Automated Testing Orchestration
    - Quality Gates
    - Environment-specific Deployments
    - Change Management Integration Hooks
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    - REQ-OP-CM-004
    
**Purpose:** Defines and orchestrates the CI/CD pipeline for the InfluenceGen project.  
**Logic Description:** Specifies pipeline stages (e.g., validate, build, test, quality_scan, deploy_dev, deploy_staging, deploy_prod). Defines jobs for each stage, utilizing included templates and scripts. Manages job dependencies, artifacts, and rules for execution (e.g., branch-specific, manual triggers for production). Integrates GitLab CI/CD variables for secrets and environment configuration.  
**Documentation:**
    
    - **Summary:** This file is the entry point for all CI/CD automation within GitLab. It structures the flow of how code is validated, built, tested, and deployed across different environments.
    
**Namespace:** InfluenceGen.DevOps.CICD  
**Metadata:**
    
    - **Category:** CICDOrchestration
    
- **Path:** pipeline_templates/build_jobs.yml  
**Description:** GitLab CI/CD template defining reusable build jobs for Odoo modules, N8N workflows, and Docker images.  
**Template:** GitLab CI/CD YAML Template  
**Dependancy Level:** 1  
**Name:** build_jobs  
**Type:** PipelineTemplate  
**Relative Path:** pipeline_templates/build_jobs.yml  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    - PipelineAsCode
    -  DRY
    
**Members:**
    
    - **Name:** .build_odoo_modules_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .build_n8n_workflows_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .build_docker_image_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Build Job Definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Provides standardized templates for build jobs to ensure consistency and reduce duplication in the main pipeline file.  
**Logic Description:** Defines YAML anchors for common build tasks. Each template specifies script execution, artifact handling, and potentially Docker image usage for the build environment. For example, `.build_odoo_modules_template` would define steps to package Odoo addons.  
**Documentation:**
    
    - **Summary:** Contains abstract job definitions for various build processes, intended to be included and extended in the main .gitlab-ci.yml file.
    
**Namespace:** InfluenceGen.DevOps.CICD.Templates  
**Metadata:**
    
    - **Category:** CICDConfiguration
    
- **Path:** pipeline_templates/test_jobs.yml  
**Description:** GitLab CI/CD template defining reusable test jobs for unit, integration, and UI automation tests.  
**Template:** GitLab CI/CD YAML Template  
**Dependancy Level:** 1  
**Name:** test_jobs  
**Type:** PipelineTemplate  
**Relative Path:** pipeline_templates/test_jobs.yml  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    - PipelineAsCode
    - DRY
    
**Members:**
    
    - **Name:** .run_unit_tests_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .run_integration_tests_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .run_ui_automation_tests_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Test Job Definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Provides standardized templates for various testing stages, ensuring consistent test execution across different parts of the application.  
**Logic Description:** Defines YAML anchors for test execution. Templates specify commands to run test scripts, test report generation/collection, and dependencies on build stages. For example, `.run_unit_tests_template` would call the unit test execution script.  
**Documentation:**
    
    - **Summary:** Contains abstract job definitions for automated testing, meant to be included and customized in the main pipeline configuration.
    
**Namespace:** InfluenceGen.DevOps.CICD.Templates  
**Metadata:**
    
    - **Category:** CICDConfiguration
    
- **Path:** pipeline_templates/quality_jobs.yml  
**Description:** GitLab CI/CD template defining reusable jobs for code quality checks like linting, static analysis, and security scans.  
**Template:** GitLab CI/CD YAML Template  
**Dependancy Level:** 1  
**Name:** quality_jobs  
**Type:** PipelineTemplate  
**Relative Path:** pipeline_templates/quality_jobs.yml  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    - PipelineAsCode
    - DRY
    
**Members:**
    
    - **Name:** .run_linting_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .run_static_analysis_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .run_security_scans_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Quality Check Job Definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Provides standardized templates for code quality assurance stages, promoting consistent quality checks.  
**Logic Description:** Defines YAML anchors for executing quality scanning tools. Templates specify commands for linters, static analysis tools, and security scanners, along with how to handle their outputs (e.g., failing the pipeline on critical issues).  
**Documentation:**
    
    - **Summary:** Contains abstract job definitions for various code quality and security scanning processes.
    
**Namespace:** InfluenceGen.DevOps.CICD.Templates  
**Metadata:**
    
    - **Category:** CICDConfiguration
    
- **Path:** pipeline_templates/deploy_jobs.yml  
**Description:** GitLab CI/CD template defining reusable deployment jobs for different environments (dev, staging, prod).  
**Template:** GitLab CI/CD YAML Template  
**Dependancy Level:** 1  
**Name:** deploy_jobs  
**Type:** PipelineTemplate  
**Relative Path:** pipeline_templates/deploy_jobs.yml  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    - PipelineAsCode
    - DRY
    
**Members:**
    
    - **Name:** .deploy_to_dev_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .deploy_to_staging_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .deploy_to_production_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    - **Name:** .deploy_training_materials_template  
**Type:** JobDefinition  
**Attributes:** yaml-anchor  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Deployment Job Definitions
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    - REQ-OP-CM-004
    - REQ-DTS-001
    
**Purpose:** Provides standardized templates for deployment tasks, ensuring consistent deployment processes across environments and integrating change management controls for production.  
**Logic Description:** Defines YAML anchors for deployment jobs. Templates specify deployment scripts, environment-specific variables, manual approval steps (especially for production), and integration with change management systems for `REQ-OP-CM-004`. The training materials deployment template handles `REQ-DTS-001` if applicable.  
**Documentation:**
    
    - **Summary:** Contains abstract job definitions for deploying application artifacts and training materials to various environments.
    
**Namespace:** InfluenceGen.DevOps.CICD.Templates  
**Metadata:**
    
    - **Category:** CICDConfiguration
    
- **Path:** scripts/build/odoo_modules.sh  
**Description:** Shell script to prepare Odoo custom modules for deployment. This may involve gathering addons, running pre-compilation steps if any, and creating an archive.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** odoo_modules  
**Type:** AutomationScript  
**Relative Path:** scripts/build/odoo_modules.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main_execution_block  
**Parameters:**
    
    - source_dir
    - output_artifact_name
    
**Return Type:** exit_code  
**Attributes:** script-execution  
    
**Implemented Features:**
    
    - Odoo Module Packaging
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the process of building Odoo custom module artifacts.  
**Logic Description:** Accepts source directory of Odoo modules and an output artifact name. Navigates to the Odoo modules repository checkout. Collects specified InfluenceGen Odoo modules (UI, Business Logic, Infrastructure/Integration). Potentially filters out unnecessary files (e.g., .pyc, .git). Creates a zip or tar.gz archive of the modules. Stores the artifact for later pipeline stages.  
**Documentation:**
    
    - **Summary:** This script packages Odoo custom modules from their source repository into a deployable artifact.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Build  
**Metadata:**
    
    - **Category:** BuildAutomation
    
- **Path:** scripts/build/n8n_workflows.sh  
**Description:** Shell script to package N8N workflows for deployment. This might involve collecting JSON workflow files and associated configuration.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** n8n_workflows  
**Type:** AutomationScript  
**Relative Path:** scripts/build/n8n_workflows.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main_execution_block  
**Parameters:**
    
    - source_dir
    - output_artifact_name
    
**Return Type:** exit_code  
**Attributes:** script-execution  
    
**Implemented Features:**
    
    - N8N Workflow Packaging
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the preparation of N8N workflow artifacts.  
**Logic Description:** Accepts source directory of N8N workflow JSON files. Navigates to the N8N workflows repository checkout. Collects workflow files and any associated helper scripts or configuration files. Creates an archive (e.g., zip) of these assets. Stores the artifact for later deployment stages.  
**Documentation:**
    
    - **Summary:** This script packages N8N workflows and related configurations into a deployable artifact.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Build  
**Metadata:**
    
    - **Category:** BuildAutomation
    
- **Path:** scripts/build/docker_images.sh  
**Description:** Shell script to build Docker images required for testing or specific service deployments.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** docker_images  
**Type:** AutomationScript  
**Relative Path:** scripts/build/docker_images.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DOCKERFILE_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** IMAGE_NAME  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** IMAGE_TAG  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** build_and_push_image  
**Parameters:**
    
    - dockerfile
    - image_name
    - image_tag
    - registry_url
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Docker Image Building
    - Docker Image Pushing
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the building and optional pushing of Docker images to a container registry.  
**Logic Description:** Accepts parameters for Dockerfile path, image name, tag, and registry URL. Executes `docker build` command with appropriate context and arguments. If a registry URL is provided, logs into the Docker registry (credentials via CI/CD variables) and executes `docker push`.  
**Documentation:**
    
    - **Summary:** This script builds specified Docker images using Dockerfiles and can push them to a container registry.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Build  
**Metadata:**
    
    - **Category:** BuildAutomation
    
- **Path:** scripts/test/run_unit_tests.sh  
**Description:** Shell script to execute unit tests for Odoo modules and potentially N8N custom functions.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** run_unit_tests  
**Type:** AutomationScript  
**Relative Path:** scripts/test/run_unit_tests.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** ODOO_MODULES_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** TEST_REPORTS_DIR  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** execute_odoo_tests  
**Parameters:**
    
    - modules_to_test
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Unit Test Execution
    - Test Report Generation (JUnit/XUnit format)
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the execution of unit tests and collection of test results.  
**Logic Description:** Sets up the test environment (e.g., activates Python virtualenv for Odoo). Navigates to the Odoo codebase. Uses Odoo's test runner (`odoo-bin test`) to execute unit tests for specified modules. Configures test runner to output reports in a standard format (e.g., JUnit XML) to `TEST_REPORTS_DIR`. If N8N custom functions have unit tests, includes steps to run them (e.g., using Jest/Mocha).  
**Documentation:**
    
    - **Summary:** This script runs unit tests for application components and generates reports for CI/CD integration.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Test  
**Metadata:**
    
    - **Category:** TestAutomation
    
- **Path:** scripts/test/run_integration_tests.sh  
**Description:** Shell script to execute integration tests, verifying interactions between different components.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** run_integration_tests  
**Type:** AutomationScript  
**Relative Path:** scripts/test/run_integration_tests.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** TEST_ENVIRONMENT_URL  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** execute_tests  
**Parameters:**
    
    - test_suite_path
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Integration Test Execution
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the execution of integration tests against a deployed environment.  
**Logic Description:** Sets up any necessary test data or prerequisites in the target test environment. Executes integration test suites (e.g., PyTest, Postman collections run via Newman) against the `TEST_ENVIRONMENT_URL`. Collects test results and reports.  
**Documentation:**
    
    - **Summary:** This script runs integration tests to validate interactions between system components.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Test  
**Metadata:**
    
    - **Category:** TestAutomation
    
- **Path:** scripts/quality/run_linting.sh  
**Description:** Shell script to run linters (e.g., Pylint, Flake8 for Python) on Odoo module code.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** run_linting  
**Type:** AutomationScript  
**Relative Path:** scripts/quality/run_linting.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** CODE_SOURCE_PATH  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** lint_python_code  
**Parameters:**
    
    - path_to_lint
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Code Linting
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Enforces coding style and identifies potential errors through linting.  
**Logic Description:** Installs necessary linters (e.g., Pylint, Flake8, ESLint for JS if needed). Runs the linters against the specified `CODE_SOURCE_PATH` (e.g., Odoo custom modules). Reports findings and potentially fails the script if error thresholds are exceeded. Outputs report in a format consumable by GitLab CI.  
**Documentation:**
    
    - **Summary:** This script performs code linting to maintain code quality and consistency.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Quality  
**Metadata:**
    
    - **Category:** QualityAssurance
    
- **Path:** scripts/deploy/to_dev.sh  
**Description:** Shell script for deploying artifacts to the development environment.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** to_dev  
**Type:** AutomationScript  
**Relative Path:** scripts/deploy/to_dev.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** DEV_SERVER_HOST  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** ODOO_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** N8N_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** deploy_odoo  
**Parameters:**
    
    - artifact
    - target_server
    
**Return Type:** exit_code  
**Attributes:** script-function  
    - **Name:** deploy_n8n  
**Parameters:**
    
    - artifact
    - target_n8n_instance
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Deployment to Development Environment
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the deployment of application artifacts to the development environment.  
**Logic Description:** Retrieves build artifacts (Odoo modules, N8N workflows). Connects to the development server(s) (Odoo, N8N) using appropriate credentials/keys (from CI/CD variables). Copies Odoo module artifacts to the Odoo addons path and triggers an Odoo update/restart. Deploys N8N workflows to the N8N instance (e.g., via API or by placing files and restarting). Runs post-deployment checks.  
**Documentation:**
    
    - **Summary:** This script handles the deployment of built artifacts to the designated development environment.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Deploy  
**Metadata:**
    
    - **Category:** DeploymentAutomation
    
- **Path:** scripts/deploy/to_staging.sh  
**Description:** Shell script for deploying artifacts to the staging environment. Similar to dev, but targets staging servers.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** to_staging  
**Type:** AutomationScript  
**Relative Path:** scripts/deploy/to_staging.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** STAGING_SERVER_HOST  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** ODOO_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** N8N_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** deploy_odoo  
**Parameters:**
    
    - artifact
    - target_server
    
**Return Type:** exit_code  
**Attributes:** script-function  
    - **Name:** deploy_n8n  
**Parameters:**
    
    - artifact
    - target_n8n_instance
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Deployment to Staging Environment
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Automates the deployment of application artifacts to the staging environment for UAT and further testing.  
**Logic Description:** Retrieves build artifacts. Connects to staging servers using secure credentials. Deploys Odoo modules (update addons, restart Odoo service). Deploys N8N workflows to the staging N8N instance. Performs basic health checks post-deployment. May include steps for database migrations if applicable in staging.  
**Documentation:**
    
    - **Summary:** This script handles the deployment of built artifacts to the staging/UAT environment.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Deploy  
**Metadata:**
    
    - **Category:** DeploymentAutomation
    
- **Path:** scripts/deploy/to_production.sh  
**Description:** Shell script for deploying artifacts to the production environment. Includes checks for change management approval.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** to_production  
**Type:** AutomationScript  
**Relative Path:** scripts/deploy/to_production.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** PROD_SERVER_HOST  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** ODOO_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** N8N_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** CHANGE_REQUEST_ID  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** check_change_approval  
**Parameters:**
    
    - change_request_id
    
**Return Type:** boolean  
**Attributes:** script-function  
    - **Name:** deploy_odoo_prod  
**Parameters:**
    
    - artifact
    - target_server
    
**Return Type:** exit_code  
**Attributes:** script-function  
    - **Name:** deploy_n8n_prod  
**Parameters:**
    
    - artifact
    - target_n8n_instance
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Deployment to Production Environment
    - Change Management Gate
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    - REQ-OP-CM-004
    
**Purpose:** Automates the deployment of application artifacts to the production environment, ensuring adherence to change management policies.  
**Logic Description:** Retrieves build artifacts. Calls `check_change_approval` function (which might interact with JIRA or another change management tool via `scripts/utils/jira_integrate.sh`) using `CHANGE_REQUEST_ID`. If approved, proceeds with deployment. Connects to production servers. Deploys Odoo modules and N8N workflows following production deployment procedures (e.g., blue/green, canary if configured, database backups pre-deployment, schema migrations). Performs comprehensive post-deployment validation and health checks. Notifies stakeholders of deployment status.  
**Documentation:**
    
    - **Summary:** This script handles the carefully controlled deployment to the production environment, including change management verification.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Deploy  
**Metadata:**
    
    - **Category:** DeploymentAutomation
    
- **Path:** scripts/deploy/deploy_training_materials.sh  
**Description:** Shell script to deploy training materials (e.g., static HTML, PDFs) to a designated location or system.  
**Template:** Shell Script  
**Dependancy Level:** 2  
**Name:** deploy_training_materials  
**Type:** AutomationScript  
**Relative Path:** scripts/deploy/deploy_training_materials.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** TRAINING_MATERIALS_ARTIFACT_PATH  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** TRAINING_PORTAL_TARGET_PATH  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** main_execution_block  
**Parameters:**
    
    
**Return Type:** exit_code  
**Attributes:** script-execution  
    
**Implemented Features:**
    
    - Training Material Deployment
    
**Requirement Ids:**
    
    - REQ-DTS-001
    
**Purpose:** Automates the deployment of training materials to their accessible location.  
**Logic Description:** Retrieves the training materials artifact. Connects to the target server or system where training materials are hosted (e.g., a web server, a shared drive, an LMS content folder). Copies the materials to the `TRAINING_PORTAL_TARGET_PATH`. May involve cache clearing or re-indexing steps on the target system if applicable.  
**Documentation:**
    
    - **Summary:** This script deploys versioned training materials to the platform or documentation portal.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Deploy  
**Metadata:**
    
    - **Category:** DeploymentAutomation
    
- **Path:** scripts/utils/slack_notify.sh  
**Description:** Utility shell script to send notifications to Slack channels.  
**Template:** Shell Script  
**Dependancy Level:** 1  
**Name:** slack_notify  
**Type:** AutomationScript  
**Relative Path:** scripts/utils/slack_notify.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** SLACK_WEBHOOK_URL  
**Type:** String  
**Attributes:** environment-variable  
    
**Methods:**
    
    - **Name:** send_slack_message  
**Parameters:**
    
    - channel
    - message
    - status
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - Slack Notification Sending
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Provides a common utility for sending pipeline status or deployment notifications to Slack.  
**Logic Description:** Accepts parameters for Slack channel, message content, and status (e.g., success, failure). Uses `curl` or a similar tool to send a POST request with a JSON payload to the `SLACK_WEBHOOK_URL`. Formats the message based on the status.  
**Documentation:**
    
    - **Summary:** A helper script to integrate Slack notifications into CI/CD pipelines.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** scripts/utils/jira_integrate.sh  
**Description:** Utility shell script to interact with JIRA for change management or issue tracking updates.  
**Template:** Shell Script  
**Dependancy Level:** 1  
**Name:** jira_integrate  
**Type:** AutomationScript  
**Relative Path:** scripts/utils/jira_integrate.sh  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** JIRA_API_URL  
**Type:** String  
**Attributes:** environment-variable  
    - **Name:** JIRA_API_TOKEN  
**Type:** String  
**Attributes:** environment-variable secret  
    
**Methods:**
    
    - **Name:** get_jira_issue_status  
**Parameters:**
    
    - issue_key
    
**Return Type:** String  
**Attributes:** script-function  
    - **Name:** update_jira_issue_status  
**Parameters:**
    
    - issue_key
    - new_status
    - comment
    
**Return Type:** exit_code  
**Attributes:** script-function  
    
**Implemented Features:**
    
    - JIRA API Interaction
    
**Requirement Ids:**
    
    - REQ-OP-CM-004
    
**Purpose:** Provides common utilities for interacting with JIRA, typically for change management validation or updating issue statuses.  
**Logic Description:** Accepts JIRA issue key and other parameters. Uses `curl` to make authenticated REST API calls to the `JIRA_API_URL` using `JIRA_API_TOKEN`. Can fetch issue details (e.g., status to check for approval) or update issues (e.g., add comments, transition status).  
**Documentation:**
    
    - **Summary:** A helper script to integrate CI/CD pipelines with JIRA for tasks like change request validation.
    
**Namespace:** InfluenceGen.DevOps.CICD.Scripts.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** dockerfiles/odoo-build-env.Dockerfile  
**Description:** Dockerfile to create a consistent build and test environment for Odoo modules.  
**Template:** Dockerfile  
**Dependancy Level:** 0  
**Name:** odoo-build-env.Dockerfile  
**Type:** ContainerDefinition  
**Relative Path:** dockerfiles/odoo-build-env.Dockerfile  
**Repository Id:** REPO-IGDOPS-008  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Build Environment Setup
    - Odoo Test Environment Setup
    
**Requirement Ids:**
    
    - REQ-DDSI-004
    
**Purpose:** Defines a Docker image with all necessary dependencies (Odoo base, Python, libraries, testing tools) for building and testing Odoo custom modules.  
**Logic Description:** Starts from a base Odoo image or a suitable Python image. Installs Odoo core dependencies. Installs Python development tools, linters (Pylint, Flake8), and test runners (e.g., coverage.py). Copies any necessary configuration files for testing. Sets up entry points or default commands if needed for test execution.  
**Documentation:**
    
    - **Summary:** This Dockerfile specifies the environment for building and running tests for Odoo modules.
    
**Namespace:** InfluenceGen.DevOps.CICD.Dockerfiles  
**Metadata:**
    
    - **Category:** Containerization
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - ENABLE_AUTO_DEPLOY_TO_DEV
  - REQUIRE_MANUAL_APPROVAL_FOR_STAGING
  - ENABLE_SECURITY_SCANS_ON_MR
  - ENABLE_SLACK_NOTIFICATIONS
  - ENABLE_JIRA_INTEGRATION_FOR_PROD_DEPLOY
  
- **Database Configs:**
  
  
- **Environment Variables:**
  
  - CI_REGISTRY_USER
  - CI_REGISTRY_PASSWORD
  - CI_REGISTRY_IMAGE
  - DEV_ODOO_SERVER_SSH_HOST
  - DEV_ODOO_SERVER_SSH_USER
  - DEV_N8N_API_URL
  - DEV_N8N_API_KEY
  - STAGING_ODOO_SERVER_SSH_HOST
  - STAGING_N8N_API_URL
  - PROD_ODOO_SERVER_SSH_HOST
  - PROD_N8N_API_URL
  - SLACK_WEBHOOK_URL_CRITICAL
  - SLACK_WEBHOOK_URL_INFO
  - JIRA_BASE_URL
  - JIRA_USERNAME
  - JIRA_API_TOKEN_SECRET
  - CHANGE_MANAGEMENT_PROJECT_KEY
  - TRAINING_MATERIALS_S3_BUCKET
  - AWS_ACCESS_KEY_ID_SECRET
  - AWS_SECRET_ACCESS_KEY_SECRET
  


---

