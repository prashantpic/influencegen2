```bash
#!/bin/bash

set -e
set -u
set -o pipefail

# Expected Environment Variables
# ODOO_MODULES_TO_TEST: Comma-separated list of Odoo modules to test (e.g., "influence_gen_portal,influence_gen_campaign")
# ODOO_DB_NAME: Name of the test database (e.g., "influencegen_test_db")
# TEST_REPORTS_OUTPUT_DIR: Directory to save JUnit XML reports (e.g., "test-reports/unit")

echo "Starting unit tests execution..."

# Validate expected environment variables
: "${ODOO_MODULES_TO_TEST:?Error: ODOO_MODULES_TO_TEST environment variable is not set.}"
: "${ODOO_DB_NAME:?Error: ODOO_DB_NAME environment variable is not set.}"
: "${TEST_REPORTS_OUTPUT_DIR:?Error: TEST_REPORTS_OUTPUT_DIR environment variable is not set.}"

echo "Odoo modules to test: $ODOO_MODULES_TO_TEST"
echo "Odoo test database name: $ODOO_DB_NAME"
echo "Test reports output directory: $TEST_REPORTS_OUTPUT_DIR"

# Create the test reports directory if it doesn't exist
mkdir -p "$TEST_REPORTS_OUTPUT_DIR"

ODOO_TEST_EXIT_CODE=0

# --- Odoo Unit Tests ---
echo "Running Odoo unit tests..."
# The odoo-bin command for tests.
# --test-enable: Enables test mode.
# --stop-after-init: Stops the server after modules are initialized/updated and tests are run.
# -i "$ODOO_MODULES_TO_TEST": Specifies the modules to install/update and test.
# -d "$ODOO_DB_NAME": Specifies the database to use. Odoo will create it if it doesn't exist and initialize it for tests.
# --log-level=test: Sets the log level appropriate for testing.
# --test-report-directory="$TEST_REPORTS_OUTPUT_DIR": Odoo's native test runner might not directly produce JUnit XML.
#   This directory is where Odoo would typically store its own test artifacts if supported.
#   For GitLab JUnit integration, a file named like `gl-junit-report.xml` is often expected.
#   If using `pytest-odoo`, it would handle JUnit XML generation.
#   The Dockerfile installs `pytest-odoo` and `pytest-json-report`.
#   If `odoo-bin` itself is used, a custom test runner or a post-processor script might be needed to convert Odoo's test output to JUnit XML.
#   Let's assume for now, if pytest-odoo is configured as the default test runner for odoo-bin or used separately, it produces the report.
#   For this script, we'll assume a file `gl-junit-report.xml` is generated in TEST_REPORTS_OUTPUT_DIR by the Odoo test process.

# Example if using pytest-odoo directly (this is an alternative to odoo-bin for tests if configured)
# pytest --odoo-db="$ODOO_DB_NAME" \
#        --odoo-modules="$ODOO_MODULES_TO_TEST" \
#        --junitxml="$TEST_REPORTS_OUTPUT_DIR/odoo-junit-report.xml" \
#        # Add other relevant pytest-odoo options

# Using odoo-bin as per SDS, and assuming the build environment/Odoo setup handles JUnit output:
# Odoo's `--test-report-directory` is for its own reporting, not necessarily JUnit.
# If a tool like `odoo-test-helper` or similar is used, it might provide a wrapper for JUnit.
# For now, let's proceed with the basic odoo-bin command and note the JUnit report name.
# It's crucial that "gl-junit-report.xml" (or whatever GitLab CI job expects) appears in $TEST_REPORTS_OUTPUT_DIR.
# A common approach is to use odoo's test tags if tests are tagged with 'post_install' or similar to run after module loading.
# The `--test-tags` option can be used with `odoo-bin`.
# The modules specified with `-i` will be loaded, and their tests tagged as `standard` are typically run.
# If `pytest-odoo` is integrated, it might automatically generate the JUnit XML.
# Let's assume the current setup generates a JUnit report named `odoo-junit-report.xml`.

echo "Executing: odoo-bin -d "$ODOO_DB_NAME" --test-enable --stop-after-init -i "$ODOO_MODULES_TO_TEST" --log-level=test --test-report-directory="$TEST_REPORTS_OUTPUT_DIR""
if odoo-bin -d "$ODOO_DB_NAME" --test-enable --stop-after-init -i "$ODOO_MODULES_TO_TEST" --log-level=test --test-report-directory="$TEST_REPORTS_OUTPUT_DIR"; then
    echo "Odoo unit tests completed successfully."
    # We need to ensure the report is in the correct format and name.
    # If odoo-bin directly doesn't produce it, a post-processing step would be here.
    # For now, assume a report 'odoo-junit-report.xml' is somehow generated in TEST_REPORTS_OUTPUT_DIR.
    # If there is a standard Odoo generated file like 'tests.xml', rename it:
    if [ -f "$TEST_REPORTS_OUTPUT_DIR/tests.xml" ]; then # Example name
        mv "$TEST_REPORTS_OUTPUT_DIR/tests.xml" "$TEST_REPORTS_OUTPUT_DIR/odoo-junit-report.xml"
        echo "Renamed Odoo test report to odoo-junit-report.xml"
    elif [ ! -f "$TEST_REPORTS_OUTPUT_DIR/odoo-junit-report.xml" ] && [ ! -f "$TEST_REPORTS_OUTPUT_DIR/gl-junit-report.xml" ]; then
        echo "Warning: Expected Odoo JUnit report (odoo-junit-report.xml or gl-junit-report.xml) not found in $TEST_REPORTS_OUTPUT_DIR."
        echo "Please ensure your Odoo test setup generates a JUnit XML report."
    fi
else
    ODOO_TEST_EXIT_CODE=$?
    echo "Error: Odoo unit tests failed with exit code $ODOO_TEST_EXIT_CODE."
    # Even on failure, Odoo might produce a report.
    if [ -f "$TEST_REPORTS_OUTPUT_DIR/tests.xml" ]; then
        mv "$TEST_REPORTS_OUTPUT_DIR/tests.xml" "$TEST_REPORTS_OUTPUT_DIR/odoo-junit-report.xml"
    fi
fi

# --- N8N Custom JavaScript Function Tests (Placeholder) ---
# This part is conditional based on whether such tests exist and how they are structured.
# Assume N8N custom function tests are in a directory `n8n_custom_functions_tests`
# and use Jest with jest-junit reporter.
N8N_TEST_PROJECT_PATH="n8n_custom_functions_tests" # Example path, configure as needed
N8N_TEST_EXIT_CODE=0

if [ -d "$N8N_TEST_PROJECT_PATH" ]; then
  echo "Running N8N custom function tests..."
  cd "$N8N_TEST_PROJECT_PATH"

  if [ ! -d "node_modules" ]; then
    echo "Installing N8N test dependencies..."
    npm install
  fi

  # Configure jest-junit to output to the correct directory
  # This might be in package.json or jest.config.js.
  # Example: "test": "jest --reporters=default --reporters=jest-junit"
  # And jest-junit config in package.json:
  # "jest-junit": { "outputDirectory": "../test-reports/unit", "outputName": "n8n-junit-report.xml" }
  # For the script, we can override or ensure this.
  # Let's assume package.json is configured or use CLI override if possible.
  # jest-junit CLI options for output: JEST_JUNIT_OUTPUT_DIR and JEST_JUNIT_OUTPUT_NAME
  export JEST_JUNIT_OUTPUT_DIR="../$TEST_REPORTS_OUTPUT_DIR" # Relative to N8N_TEST_PROJECT_PATH
  export JEST_JUNIT_OUTPUT_NAME="n8n-junit-report.xml"

  echo "Executing N8N tests (npm test)..."
  if npm test; then
    echo "N8N custom function tests completed successfully."
  else
    N8N_TEST_EXIT_CODE=$?
    echo "Error: N8N custom function tests failed with exit code $N8N_TEST_EXIT_CODE."
  fi
  cd .. # Return to original directory
else
  echo "N8N custom function test project path ($N8N_TEST_PROJECT_PATH) not found. Skipping N8N tests."
fi

# --- Final Exit Code ---
# Combine exit codes if necessary. Fail if any test suite fails.
FINAL_EXIT_CODE=0
if [ "$ODOO_TEST_EXIT_CODE" -ne 0 ]; then
    FINAL_EXIT_CODE=$ODOO_TEST_EXIT_CODE
elif [ "$N8N_TEST_EXIT_CODE" -ne 0 ]; then
    FINAL_EXIT_CODE=$N8N_TEST_EXIT_CODE
fi

if [ "$FINAL_EXIT_CODE" -ne 0 ]; then
    echo "One or more unit test suites failed."
else
    echo "All unit tests passed."
fi

echo "Unit test script finished."
exit $FINAL_EXIT_CODE
```