# Software Design Specification: InfluenceGen.DevOps.CI-CD

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specifications for the `InfluenceGen.DevOps.CI-CD` repository. This repository is responsible for defining and managing the Continuous Integration and Continuous Deployment (CI/CD) pipelines for the entire InfluenceGen project. It automates the build, test, quality assurance, and deployment processes for Odoo custom modules, N8N workflows, associated Docker images, and training materials.

This SDS will guide the implementation of GitLab CI/CD YAML files and supporting shell scripts.

### 1.2 Scope
The scope of this SDS covers:
*   The main GitLab CI/CD pipeline configuration (`.gitlab-ci.yml`).
*   Reusable pipeline templates for build, test, quality, and deployment jobs.
*   Shell scripts that execute specific tasks within the pipeline stages.
*   Dockerfile definitions for creating consistent build and test environments.
*   Integration points with version control (Git), artifact repositories, testing frameworks, quality scanning tools, and deployment targets.
*   Mechanisms to support change management processes for production deployments (`REQ-OP-CM-004`).
*   Automation of unit and integration testing (`REQ-DDSI-004`).
*   Deployment of training materials (`REQ-DTS-001`).

### 1.3 Definitions, Acronyms, and Abbreviations
*   **CI:** Continuous Integration
*   **CD:** Continuous Deployment/Delivery
*   **IaC:** Infrastructure as Code
*   **YAML:** YAML Ain't Markup Language
*   **Odoo:** OpenERP, a suite of business management software tools.
*   **N8N:** A free and open node-based workflow automation tool.
*   **MR:** Merge Request (GitLab term, similar to Pull Request)
*   **UAT:** User Acceptance Testing
*   **LFS:** Large File Storage (Git LFS)
*   **S3:** Amazon Simple Storage Service

### 1.4 References
*   InfluenceGen System Requirements Specification (SRS)
*   InfluenceGen Architecture Design Document
*   GitLab CI/CD Documentation (Version 17.0.x)
*   Docker Documentation (Version 26.1.3)
*   Bash Scripting Guide (Version 5.2.x)
*   Organizational Change Management Policy
*   Organizational Coding Standards and Development Guidelines

## 2. System Overview
The CI/CD system for InfluenceGen leverages GitLab CI/CD as its core orchestrator. Pipelines are defined in YAML and triggered by Git events (e.g., pushes, merge requests). These pipelines execute a series of jobs organized into stages, such as validating code, building artifacts, running various tests, performing quality scans, and deploying to different environments (Development, Staging, Production).

Docker containers are used to provide consistent and isolated environments for build and test jobs. Shell scripts encapsulate the logic for specific tasks like packaging Odoo modules, building Docker images, running tests, and deploying artifacts.

The system integrates with:
*   Source code repositories (Odoo modules, N8N workflows, etc.).
*   The IaC repository (`REPO-IGINF-007`) for environment provisioning insights if needed for deployment scripts.
*   The testing automation repository (`REPO-IGTEST-010`) for test scripts.
*   External services like Slack for notifications and JIRA for change management tracking.

## 3. Design Considerations

### 3.1 Assumptions and Dependencies
*   GitLab Runner (version compatible with GitLab 17.0.x) is available and configured with necessary executors (e.g., Docker executor).
*   Target deployment environments (Dev, Staging, Prod) for Odoo, N8N, and AI services are accessible from GitLab Runners (network connectivity, credentials).
*   Docker Engine (26.1.3) is available on runners or wherever Docker builds occur.
*   Source code for Odoo modules, N8N workflows, and other components are in separate, accessible Git repositories.
*   A container registry (e.g., GitLab Container Registry, Docker Hub, AWS ECR) is available for storing Docker images.
*   Secrets (API keys, SSH keys, tokens) are managed securely as GitLab CI/CD variables (masked and protected).
*   Organizational policies for change management, coding standards, and security are defined and accessible.
*   JIRA (or a similar tool) is used for change management and its API is accessible if integration is enabled.
*   Slack is used for notifications and a webhook URL is available.
*   S3 or a similar service is used for storing training materials artifacts if `deploy_training_materials.sh` targets such a service.

### 3.2 General Design Principles
*   **Pipeline as Code:** All pipeline definitions are stored in version control (`.gitlab-ci.yml` and templates).
*   **DRY (Don't Repeat Yourself):** Reusable job templates are used to minimize redundancy.
*   **Atomicity:** Each script and job performs a single, well-defined task.
*   **Idempotency:** Deployment scripts should be designed to be idempotent where possible.
*   **Security:** Secrets are managed securely. Security scans are part of the pipeline.
*   **Speed and Efficiency:** Pipelines are optimized for fast feedback loops.
*   **Reliability:** Pipelines are robust with proper error handling.
*   **Traceability:** Clear logging and reporting for all pipeline stages.
*   **Environment Parity:** Staging environment deployment process mirrors production as closely as possible.

### 3.3 Technology Stack
*   **Orchestration:** GitLab CI/CD (GitLab 17.0.x runner compatible)
*   **Scripting:** YAML (GitLab CI syntax), Bash 5.2.x
*   **Containerization:** Docker Engine 26.1.3
*   **Version Control:** Git 2.45.2

## 4. System Architecture (CI/CD Perspective)
The CI/CD architecture is centered around GitLab CI/CD pipelines.

*   **Trigger:** Git push to feature branches, `develop`, `main`, or tags; Merge Request events.
*   **Stages:**
    1.  `validate`: Linting, static analysis, configuration validation.
    2.  `build`: Compile/package Odoo modules, N8N workflows, build Docker images.
    3.  `test`: Run unit tests, integration tests.
    4.  `quality_scan`: Run security scans (SAST, DAST if applicable), dependency checks.
    5.  `deploy_dev`: Deploy to the development environment.
    6.  `deploy_staging`: Deploy to the staging/UAT environment (potentially with manual approval).
    7.  `deploy_prod`: Deploy to the production environment (strict manual approval, change management checks).
    8.  `deploy_training`: Deploy training materials.
*   **Jobs:** Specific tasks within each stage, defined in `.gitlab-ci.yml` often using templates.
*   **Artifacts:** Outputs of build jobs (e.g., zipped Odoo modules, N8N workflow bundles, Docker image IDs) passed to subsequent stages. Test reports are also treated as artifacts.
*   **Environments:** GitLab CI/CD environments are used to track deployments to Dev, Staging, and Prod.

## 5. Detailed Design

### 5.1 `.gitlab-ci.yml` - Main Pipeline Configuration
*   **Purpose:** Defines and orchestrates the CI/CD pipeline for the InfluenceGen project.
*   **Requirement Mapping:** `REQ-DDSI-004`, `REQ-OP-CM-004`.
*   **Logic Description:**
    *   **`stages`**:
        yaml
        stages:
          - validate
          - build
          - test
          - quality_scan
          - deploy_dev
          - deploy_staging
          - deploy_prod
          - deploy_training_materials # REQ-DTS-001
        
    *   **`variables`**: Global variables, e.g., `DOCKER_DRIVER: overlay2`. Project-specific variables (e.g., `ODOO_VERSION: "18.0"`, `N8N_VERSION: "latest"`) should be defined in GitLab CI/CD settings.
    *   **`default`**:
        yaml
        default:
          image: registry.gitlab.com/influencegen/devops/cicd/odoo-build-env:latest # Default image from dockerfiles/odoo-build-env.Dockerfile
          interruptible: true
          tags: # Specify runner tags if applicable
            - docker 
        
    *   **`include`**:
        yaml
        include:
          - local: 'pipeline_templates/build_jobs.yml'
          - local: 'pipeline_templates/test_jobs.yml'
          - local: 'pipeline_templates/quality_jobs.yml'
          - local: 'pipeline_templates/deploy_jobs.yml'
        
    *   **Workflow Rules**: Define when pipelines run (e.g., on merge requests to `main`/`develop`, on pushes to `main`/`develop`/feature branches).
        yaml
        workflow:
          rules:
            - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
            - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
              when: never # Avoid duplicate pipelines for MRs
            - if: '$CI_COMMIT_BRANCH'
            - if: '$CI_COMMIT_TAG'
        
    *   **Job Definitions (Examples, using extended templates):**
        *   **Validate Stage:**
            *   `lint_odoo_modules`: Extends `.run_linting_template`, specifies Odoo code path.
            *   `lint_n8n_scripts` (if custom JS exists): Extends `.run_linting_template`.
        *   **Build Stage:**
            *   `build_odoo_addons`: Extends `.build_odoo_modules_template`. Produces `odoo_addons.zip`.
            *   `build_n8n_package`: Extends `.build_n8n_workflows_template`. Produces `n8n_workflows.zip`.
            *   `build_custom_test_image` (if needed): Extends `.build_docker_image_template`.
        *   **Test Stage:**
            *   `unit_test_odoo`: Extends `.run_unit_tests_template`, depends on `build_odoo_addons`.
            *   `integration_test_services`: Extends `.run_integration_tests_template`, depends on `deploy_dev` (or a dedicated test env deployment). Needs `TEST_ENVIRONMENT_URL`.
        *   **Quality Scan Stage:**
            *   `security_scan_code`: Extends `.run_security_scans_template`. Uses tools like SonarQube (if available) or Snyk/Trivy.
        *   **Deploy Stages:**
            *   Jobs for `deploy_dev_odoo`, `deploy_dev_n8n` extending respective templates from `deploy_jobs.yml`.
            *   Jobs for `deploy_staging_odoo`, `deploy_staging_n8n` extending templates, potentially with `when: manual` or rules for `develop` branch.
            *   Jobs for `deploy_prod_odoo`, `deploy_prod_n8n` extending templates, with `when: manual` and rules for `main` branch/tags. These jobs will use the `CHANGE_REQUEST_ID` variable for `REQ-OP-CM-004`.
        *   **Deploy Training Materials Stage:**
            *   `deploy_training_docs`: Extends `.deploy_training_materials_template`. Runs only on `main` branch or tags. `REQ-DTS-001`.
    *   **Caching:** Define caching for dependencies (e.g., Python pip packages, npm packages if used) to speed up jobs.
    *   **Artifacts:** Jobs will define artifacts (e.g., build outputs, test reports). Test reports should use `reports: junit:` for GitLab integration.

### 5.2 `pipeline_templates/build_jobs.yml`
*   **Purpose:** Standardized build job templates.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Logic Description:**
    *   **`.build_odoo_modules_template` (YAML Anchor):**
        *   `stage: build`
        *   `script`: Calls `scripts/build/odoo_modules.sh $CI_PROJECT_DIR/odoo-repo-checkout odoo_addons.zip` (assuming Odoo code is checked out to `odoo-repo-checkout`).
        *   `artifacts`:
            *   `paths: [odoo_addons.zip]`
            *   `expire_in: 1 week`
    *   **`.build_n8n_workflows_template` (YAML Anchor):**
        *   `stage: build`
        *   `script`: Calls `scripts/build/n8n_workflows.sh $CI_PROJECT_DIR/n8n-repo-checkout n8n_workflows.zip`
        *   `artifacts`:
            *   `paths: [n8n_workflows.zip]`
            *   `expire_in: 1 week`
    *   **`.build_docker_image_template` (YAML Anchor):**
        *   `stage: build`
        *   `image: docker:26.1.3` (Docker-in-Docker or specific Docker image)
        *   `services: [docker:26.1.3-dind]`
        *   `variables`: `DOCKER_TLS_CERTDIR: "/certs"`
        *   `script`: Calls `scripts/build/docker_images.sh $DOCKERFILE_PATH $IMAGE_NAME $IMAGE_TAG $CI_REGISTRY_IMAGE` (expects these vars to be set by extending job).
        *   Needs `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD` for pushing.

### 5.3 `pipeline_templates/test_jobs.yml`
*   **Purpose:** Standardized test job templates.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Logic Description:**
    *   **`.run_unit_tests_template` (YAML Anchor):**
        *   `stage: test`
        *   `script`: Calls `scripts/test/run_unit_tests.sh`
        *   `dependencies`: Job that builds the necessary artifacts (e.g., `build_odoo_addons`).
        *   `artifacts`:
            *   `reports: junit: gl-junit-report.xml` (or whatever the script outputs)
            *   `paths: [test_reports_dir/]`
            *   `expire_in: 1 week`
    *   **`.run_integration_tests_template` (YAML Anchor):**
        *   `stage: test`
        *   `script`: Calls `scripts/test/run_integration_tests.sh $TEST_SUITE_PATH` (expects `TEST_ENVIRONMENT_URL` to be set).
        *   `dependencies`: Job that deploys to the test environment (e.g., `deploy_dev_odoo`).
        *   `artifacts`:
            *   `reports: junit: gl-integration-junit-report.xml`
            *   `paths: [integration_test_reports_dir/]`
            *   `expire_in: 1 week`
    *   **`.run_ui_automation_tests_template` (YAML Anchor):** (If applicable)
        *   `stage: test`
        *   `script`: Calls script for UI tests (e.g., Selenium, Playwright).
        *   `dependencies`: Job that deploys to the test environment.
        *   `artifacts`: Similar to integration tests.

### 5.4 `pipeline_templates/quality_jobs.yml`
*   **Purpose:** Standardized quality check job templates.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Logic Description:**
    *   **`.run_linting_template` (YAML Anchor):**
        *   `stage: validate` (or `quality_scan`)
        *   `script`: Calls `scripts/quality/run_linting.sh $LINT_TARGET_PATH`
        *   `allow_failure: true` (initially, can be set to `false` later)
        *   `artifacts`:
            *   `paths: [lint_reports/]`
            *   `when: always`
    *   **`.run_static_analysis_template` (YAML Anchor):**
        *   `stage: quality_scan`
        *   `script`: Executes static analysis tools (e.g., SonarScanner CLI, if SonarQube is integrated).
        *   `allow_failure: true`
    *   **`.run_security_scans_template` (YAML Anchor):**
        *   `stage: quality_scan`
        *   `script`: Executes security scanning tools (e.g., Trivy for container images, Snyk/OWASP ZAP for dependencies/DAST).
        *   `allow_failure: true` (or based on severity)
        *   `artifacts`:
            *   `paths: [security_reports/]`
            *   `when: always`

### 5.5 `pipeline_templates/deploy_jobs.yml`
*   **Purpose:** Standardized deployment job templates.
*   **Requirement Mapping:** `REQ-DDSI-004`, `REQ-OP-CM-004`, `REQ-DTS-001`.
*   **Logic Description:**
    *   **`.deploy_to_dev_template` (YAML Anchor):**
        *   `stage: deploy_dev`
        *   `script`: Calls `scripts/deploy/to_dev.sh`
        *   `environment`:
            *   `name: development/$CI_COMMIT_REF_SLUG`
            *   `url: http://dev-$CI_COMMIT_REF_SLUG.influencegen.com` (example)
        *   `rules`: Define when to run (e.g., for feature branches, `develop` branch).
    *   **`.deploy_to_staging_template` (YAML Anchor):**
        *   `stage: deploy_staging`
        *   `script`: Calls `scripts/deploy/to_staging.sh`
        *   `environment`:
            *   `name: staging`
            *   `url: http://staging.influencegen.com`
        *   `when: manual` (or on push to `develop` if `ENABLE_AUTO_DEPLOY_TO_STAGING` is true)
        *   `allow_failure: false`
    *   **`.deploy_to_production_template` (YAML Anchor):**
        *   `stage: deploy_prod`
        *   `script`:
            *   `scripts/utils/jira_integrate.sh check_approval $CHANGE_REQUEST_ID` (if JIRA integration enabled for `REQ-OP-CM-004`)
            *   `scripts/deploy/to_production.sh`
        *   `environment`:
            *   `name: production`
            *   `url: http://influencegen.com`
        *   `when: manual`
        *   `allow_failure: false`
        *   `rules`: Only for `main` branch or tags.
    *   **`.deploy_training_materials_template` (YAML Anchor):** `REQ-DTS-001`
        *   `stage: deploy_training_materials`
        *   `script`: Calls `scripts/deploy/deploy_training_materials.sh`
        *   `dependencies`: Job that builds training materials (if separate build step).
        *   `rules`: Only for `main` branch or specific tags.

### 5.6 Shell Scripts (`scripts/`)

#### 5.6.1 `scripts/build/odoo_modules.sh`
*   **Purpose:** Package Odoo custom modules.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Parameters:**
    *   `$1` (source_dir): Path to the checked-out Odoo modules repository.
    *   `$2` (output_artifact_name): Name of the output zip/tar.gz file.
*   **Logic:**
    1.  Validate input parameters.
    2.  `cd` to `$1`.
    3.  Identify InfluenceGen custom addon directories (e.g., based on a manifest or predefined list).
    4.  Create an archive (e.g., `zip -r $2 identified_addon_dir1 identified_addon_dir2 ...`).
    5.  Exclude VCS directories (`.git`) and `__pycache__`.
    6.  Place the artifact in the CI job's working directory for GitLab to pick up.
    7.  Echo success or failure. Exit with 0 on success, 1 on failure.

#### 5.6.2 `scripts/build/n8n_workflows.sh`
*   **Purpose:** Package N8N workflows.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Parameters:**
    *   `$1` (source_dir): Path to the checked-out N8N workflows repository.
    *   `$2` (output_artifact_name): Name of the output zip file.
*   **Logic:**
    1.  Validate input parameters.
    2.  `cd` to `$1`.
    3.  Find all `.json` workflow files and any associated configuration/script files.
    4.  Create an archive (e.g., `zip -r $2 *.json config_files/ script_files/`).
    5.  Place the artifact in the CI job's working directory.
    6.  Echo success or failure. Exit with 0 on success, 1 on failure.

#### 5.6.3 `scripts/build/docker_images.sh`
*   **Purpose:** Build and push Docker images.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Environment Variables Expected:**
    *   `DOCKERFILE_PATH_PARAM`: Path to the Dockerfile.
    *   `IMAGE_NAME_PARAM`: Name for the Docker image.
    *   `IMAGE_TAG_PARAM`: Tag for the Docker image (e.g., `$CI_COMMIT_SHA`, `latest`).
    *   `REGISTRY_URL_PARAM` (Optional): URL of the Docker registry (e.g., `$CI_REGISTRY_IMAGE`).
    *   `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD` (provided by GitLab if pushing to GitLab registry).
*   **Logic:**
    1.  Validate parameters.
    2.  `docker build -f "$DOCKERFILE_PATH_PARAM" -t "$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM" .` (adjust context `.` as needed).
    3.  If `REGISTRY_URL_PARAM` is set:
        *   `docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY` (or equivalent for other registries).
        *   `docker tag "$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM" "$REGISTRY_URL_PARAM/$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM"`
        *   `docker push "$REGISTRY_URL_PARAM/$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM"`
    4.  Echo success or failure. Exit with 0 on success, 1 on failure.

#### 5.6.4 `scripts/test/run_unit_tests.sh`
*   **Purpose:** Execute unit tests for Odoo modules.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Environment Variables Expected:**
    *   `ODOO_MODULES_TO_TEST`: Comma-separated list of Odoo modules to test (e.g., `influence_gen_portal,influence_gen_campaign`).
    *   `ODOO_DB_NAME`: Name of the test database.
    *   `TEST_REPORTS_OUTPUT_DIR`: Directory to save JUnit XML reports.
*   **Logic:**
    1.  Ensure Odoo environment and database are set up (often handled by the Docker image).
    2.  `odoo-bin -d "$ODOO_DB_NAME" --test-enable --stop-after-init -i "$ODOO_MODULES_TO_TEST" --log-level=test --test-report-directory="$TEST_REPORTS_OUTPUT_DIR"`
        *   Ensure the output format is JUnit XML compatible with GitLab (e.g., `gl-junit-report.xml`). This might require a custom Odoo test runner or post-processing.
    3.  If N8N custom JavaScript functions have tests (e.g., using Jest):
        *   `cd path/to/n8n/custom_functions_tests`
        *   `npm install` (if not in Docker image)
        *   `npm test -- --reporters=jest-junit` (configure output to `TEST_REPORTS_OUTPUT_DIR`).
    4.  Collect all JUnit reports into a single file or known location if GitLab expects one.
    5.  Echo success or failure. Exit with Odoo test runner's exit code.

#### 5.6.5 `scripts/test/run_integration_tests.sh`
*   **Purpose:** Execute integration tests.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Environment Variables Expected:**
    *   `TEST_ENVIRONMENT_URL`: Base URL of the deployed application for testing.
    *   `TEST_SUITE_PATH`: Path to the integration test suite/files.
    *   `INTEGRATION_TEST_REPORTS_DIR`: Directory for reports.
*   **Logic:**
    1.  `cd` to the integration test project directory.
    2.  Execute tests using the chosen framework (e.g., `pytest $TEST_SUITE_PATH --junitxml=$INTEGRATION_TEST_REPORTS_DIR/integration-report.xml -E $TEST_ENVIRONMENT_URL`).
    3.  Echo success or failure. Exit with test runner's exit code.

#### 5.6.6 `scripts/quality/run_linting.sh`
*   **Purpose:** Run linters on Odoo Python code.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Environment Variables Expected:**
    *   `LINT_TARGET_PATH`: Path to the Odoo custom modules source code.
    *   `LINT_REPORTS_DIR`: Directory for linting reports.
*   **Logic:**
    1.  `flake8 "$LINT_TARGET_PATH" --output-file="$LINT_REPORTS_DIR/flake8-report.txt" --format=default` (or GitLab compatible format).
    2.  `pylint "$LINT_TARGET_PATH" > "$LINT_REPORTS_DIR/pylint-report.txt"` (or use options for specific report formats).
    3.  Check exit codes of linters. If errors exceed threshold, exit 1.
    4.  Echo summary.

#### 5.6.7 `scripts/deploy/to_dev.sh`, `scripts/deploy/to_staging.sh`
*   **Purpose:** Deploy artifacts to Dev/Staging.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Environment Variables Expected (example for Dev):**
    *   `DEV_ODOO_SERVER_SSH_HOST`, `DEV_ODOO_SERVER_SSH_USER`, `DEV_ODOO_SSH_KEY_PATH` (from CI secret var)
    *   `DEV_ODOO_ADDONS_PATH`
    *   `DEV_ODOO_SERVICE_NAME`
    *   `DEV_N8N_INSTANCE_URL`, `DEV_N8N_API_KEY` (from CI secret var)
    *   `ODOO_ARTIFACT_NAME` (e.g., `odoo_addons.zip`)
    *   `N8N_ARTIFACT_NAME` (e.g., `n8n_workflows.zip`)
*   **Logic (Odoo part):**
    1.  `scp -i "$DEV_ODOO_SSH_KEY_PATH" "$ODOO_ARTIFACT_NAME" "$DEV_ODOO_SERVER_SSH_USER@$DEV_ODOO_SERVER_SSH_HOST:/tmp/"`
    2.  `ssh -i "$DEV_ODOO_SSH_KEY_PATH" "$DEV_ODOO_SERVER_SSH_USER@$DEV_ODOO_SERVER_SSH_HOST" "sudo unzip -o /tmp/$ODOO_ARTIFACT_NAME -d $DEV_ODOO_ADDONS_PATH && sudo systemctl restart $DEV_ODOO_SERVICE_NAME && odoo-bin -d <dev_db> -u influence_gen_portal,influence_gen_campaign --stop-after-init"` (update modules)
*   **Logic (N8N part):**
    1.  Unzip `$N8N_ARTIFACT_NAME`.
    2.  Iterate through workflow `.json` files.
    3.  Use `curl` and N8N API (with `DEV_N8N_API_KEY`) to upload/update workflows on `DEV_N8N_INSTANCE_URL`.
    4.  Perform health checks.
    5.  Echo success/failure.

#### 5.6.8 `scripts/deploy/to_production.sh`
*   **Purpose:** Deploy artifacts to Production with change management.
*   **Requirement Mapping:** `REQ-DDSI-004`, `REQ-OP-CM-004`.
*   **Environment Variables:** Similar to Staging, but for Production (e.g., `PROD_ODOO_SERVER_SSH_HOST`). Also `CHANGE_REQUEST_ID`.
*   **Logic:**
    1.  Call `scripts/utils/jira_integrate.sh get_jira_issue_status "$CHANGE_REQUEST_ID"`.
    2.  Check if status is "Approved for Deployment". If not, exit 1.
    3.  **(Optional) Pre-deployment backup step.**
    4.  Follow deployment logic similar to `to_staging.sh`, but targeting production servers and configurations.
    5.  **(Crucial) Run extensive post-deployment validation and health checks.**
    6.  Call `scripts/utils/slack_notify.sh` for deployment status.
    7.  **(Optional) Call `scripts/utils/jira_integrate.sh update_jira_issue_status "$CHANGE_REQUEST_ID" "Deployed"`**
    8.  Echo success/failure.

#### 5.6.9 `scripts/deploy/deploy_training_materials.sh`
*   **Purpose:** Deploy training materials.
*   **Requirement Mapping:** `REQ-DTS-001`.
*   **Environment Variables:**
    *   `TRAINING_MATERIALS_ARTIFACT_PATH`: Path to the built training materials artifact (e.g., `training_docs.zip`).
    *   `TRAINING_PORTAL_TARGET_TYPE`: (e.g., `S3`, `WEBSERVER_SSH`)
    *   If `WEBSERVER_SSH`: `TRAINING_PORTAL_SSH_HOST`, `TRAINING_PORTAL_SSH_USER`, `TRAINING_PORTAL_SSH_KEY_PATH`, `TRAINING_PORTAL_TARGET_DIR`.
    *   If `S3`: `TRAINING_S3_BUCKET_URL`, `AWS_ACCESS_KEY_ID_SECRET`, `AWS_SECRET_ACCESS_KEY_SECRET`.
*   **Logic:**
    1.  Unzip `$TRAINING_MATERIALS_ARTIFACT_PATH`.
    2.  If `TRAINING_PORTAL_TARGET_TYPE` is `WEBSERVER_SSH`:
        *   `rsync -avz -e "ssh -i $TRAINING_PORTAL_SSH_KEY_PATH" unzipped_materials/ "$TRAINING_PORTAL_SSH_USER@$TRAINING_PORTAL_SSH_HOST:$TRAINING_PORTAL_TARGET_DIR/"`
    3.  If `TRAINING_PORTAL_TARGET_TYPE` is `S3`:
        *   Use `aws s3 sync unzipped_materials/ "$TRAINING_S3_BUCKET_URL/" --delete` (ensure AWS CLI is in Docker image).
    4.  Echo success/failure.

#### 5.6.10 `scripts/utils/slack_notify.sh`
*   **Purpose:** Send Slack notifications.
*   **Requirement Mapping:** `REQ-DDSI-004` (for pipeline feedback).
*   **Environment Variables:** `SLACK_WEBHOOK_URL` (e.g., `SLACK_WEBHOOK_URL_CRITICAL` or `SLACK_WEBHOOK_URL_INFO` passed as arg or selected based on status).
*   **Parameters:**
    *   `$1` (channel): Slack channel (e.g., `#devops-alerts`).
    *   `$2` (message_title): Title of the message.
    *   `$3` (message_body): Detailed message.
    *   `$4` (status): `success`, `failure`, `info`.
*   **Logic:**
    1.  Construct JSON payload for Slack. Include `$CI_PROJECT_URL/-/pipelines/$CI_PIPELINE_ID` for links.
    2.  Color-code message based on status.
    3.  `curl -X POST -H 'Content-type: application/json' --data "$payload" "$SLACK_WEBHOOK_URL"`
    4.  Echo success/failure of notification.

#### 5.6.11 `scripts/utils/jira_integrate.sh`
*   **Purpose:** Interact with JIRA.
*   **Requirement Mapping:** `REQ-OP-CM-004`.
*   **Environment Variables:** `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN_SECRET` (GitLab CI secret).
*   **Sub-commands / Parameters:**
    *   `get_jira_issue_status <issue_key>`: Prints the status of the JIRA issue.
    *   `update_jira_issue_status <issue_key> <transition_name_or_id> [comment_body]`: Transitions issue and optionally adds a comment.
*   **Logic:**
    1.  Parse sub-command and parameters.
    2.  Construct JIRA REST API URL based on `JIRA_BASE_URL` and command.
    3.  Use `curl -u "$JIRA_USERNAME:$JIRA_API_TOKEN_SECRET" -H "Content-Type: application/json" ...`
    4.  For `get_status`: Parse JSON response to extract status field. Echo it.
    5.  For `update_status`: Send POST request with appropriate payload for transition and comment.
    6.  Handle API errors from JIRA. Echo results or error messages.

### 5.7 Dockerfiles (`dockerfiles/`)

#### 5.7.1 `dockerfiles/odoo-build-env.Dockerfile`
*   **Purpose:** Consistent build/test environment for Odoo.
*   **Requirement Mapping:** `REQ-DDSI-004`.
*   **Logic:**
    dockerfile
    ARG ODOO_VERSION=18.0
    FROM odoo:${ODOO_VERSION} # Or a suitable Python base image if more control is needed

    USER root

    # Install common dev tools, linters, test tools
    RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        zip \
        unzip \
        # Python tools
        python3-pip \
        python3-venv \
        # Other build/test dependencies
        # For N8N JS testing (if done here)
        # nodejs npm 
        && rm -rf /var/lib/apt/lists/*

    # Install Python packages for linting, testing
    RUN pip3 install --no-cache-dir \
        flake8 \
        pylint \
        pytest \
        pytest-odoo \
        pytest-cov \
        coverage \
        # For JUnit reports with pytest
        pytest-xdist \
        pytest-json-report \
        # If specific Odoo test report formatters are used
        # odoo-test-helper or similar

    # (Optional) Install specific versions of Node/NPM if needed for N8N related tasks
    # RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    # RUN apt-get install -y nodejs

    # Create a non-root user for operations if desired, though CI often runs as root in container
    # RUN useradd -ms /bin/bash cicduser
    # USER cicduser
    # WORKDIR /home/cicduser

    USER odoo # Switch back to Odoo user if starting from official Odoo image
    WORKDIR /mnt/src

    # Copy any necessary helper scripts or default configs into the image
    # COPY ci_scripts/ /usr/local/bin/
    # RUN chmod +x /usr/local/bin/*

    # Default command could be bash or a specific entrypoint
    CMD ["bash"]
    

## 6. Configuration Variables

The following CI/CD variables need to be configured in GitLab project settings (many as protected and masked):

*   `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`: For Docker registry (GitLab provides these automatically for its own registry).
*   `CI_REGISTRY_IMAGE`: Base path for Docker images in GitLab registry.
*   **Development Environment:**
    *   `DEV_ODOO_SERVER_SSH_HOST`, `DEV_ODOO_SERVER_SSH_USER`, `DEV_ODOO_SSH_KEY_SECRET`
    *   `DEV_ODOO_ADDONS_PATH`, `DEV_ODOO_DB_NAME`, `DEV_ODOO_SERVICE_NAME`
    *   `DEV_N8N_INSTANCE_URL`, `DEV_N8N_API_KEY_SECRET`
*   **Staging Environment:**
    *   `STAGING_ODOO_SERVER_SSH_HOST`, `STAGING_ODOO_SERVER_SSH_USER`, `STAGING_ODOO_SSH_KEY_SECRET`
    *   `STAGING_ODOO_ADDONS_PATH`, `STAGING_ODOO_DB_NAME`, `STAGING_ODOO_SERVICE_NAME`
    *   `STAGING_N8N_INSTANCE_URL`, `STAGING_N8N_API_KEY_SECRET`
*   **Production Environment:**
    *   `PROD_ODOO_SERVER_SSH_HOST`, `PROD_ODOO_SERVER_SSH_USER`, `PROD_ODOO_SSH_KEY_SECRET`
    *   `PROD_ODOO_ADDONS_PATH`, `PROD_ODOO_DB_NAME`, `PROD_ODOO_SERVICE_NAME`
    *   `PROD_N8N_INSTANCE_URL`, `PROD_N8N_API_KEY_SECRET`
*   **Notifications & Integrations:**
    *   `SLACK_WEBHOOK_URL_CRITICAL_SECRET`, `SLACK_WEBHOOK_URL_INFO_SECRET`
    *   `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN_SECRET`
    *   `CHANGE_MANAGEMENT_PROJECT_KEY` (e.g., "INFLCM")
*   **Training Materials Deployment:**
    *   `TRAINING_PORTAL_TARGET_TYPE` (e.g., `S3`, `WEBSERVER_SSH`)
    *   `TRAINING_S3_BUCKET_URL` (if S3)
    *   `AWS_ACCESS_KEY_ID_SECRET`, `AWS_SECRET_ACCESS_KEY_SECRET` (if S3)
    *   `TRAINING_PORTAL_SSH_HOST`, `TRAINING_PORTAL_SSH_USER`, `TRAINING_PORTAL_SSH_KEY_SECRET`, `TRAINING_PORTAL_TARGET_DIR` (if WEBSERVER_SSH)
*   **Feature Toggles (CI/CD Variables):**
    *   `ENABLE_AUTO_DEPLOY_TO_DEV` (default: "true")
    *   `REQUIRE_MANUAL_APPROVAL_FOR_STAGING` (default: "true")
    *   `ENABLE_SECURITY_SCANS_ON_MR` (default: "true")
    *   `ENABLE_SLACK_NOTIFICATIONS` (default: "true")
    *   `ENABLE_JIRA_INTEGRATION_FOR_PROD_DEPLOY` (default: "true")

## 7. Error Handling and Logging
*   All shell scripts will use `set -e` and `set -o pipefail` to ensure errors cause script termination.
*   Scripts will echo significant actions and results to standard output, captured by GitLab CI logs.
*   GitLab CI jobs will fail if any script exits with a non-zero status.
*   Test jobs will produce JUnit XML reports, integrated with GitLab UI for test summaries.
*   Deployment jobs will notify status (success/failure) via Slack. Production deployment failures should trigger high-priority alerts.

## 8. Security Considerations
*   **Secrets Management:** All sensitive credentials (API keys, SSH keys, passwords) must be stored as GitLab CI/CD protected and masked variables. Scripts will access them as environment variables.
*   **Least Privilege:** SSH keys and API tokens used by the pipeline should have the minimum necessary permissions for their tasks.
*   **Image Security:** Docker images used in pipelines (both base images and custom-built ones) should be regularly scanned for vulnerabilities (e.g., using Trivy in a `quality_scan` stage).
*   **Dependency Scanning:** Scan application dependencies (Python, JS if any) for known vulnerabilities.
*   **Change Management:** Production deployments are gated by manual approval and adherence to `REQ-OP-CM-004`.

## 9. Future Considerations
*   Integration with more sophisticated SAST/DAST tools.
*   Canary or Blue/Green deployment strategies for production.
*   Automated rollback procedures.
*   Performance testing integrated into the pipeline for staging deployments.
*   More granular environment configuration using tools like HashiCorp Vault integrated with GitLab CI.