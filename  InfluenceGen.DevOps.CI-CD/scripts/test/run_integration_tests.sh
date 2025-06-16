```bash
#!/bin/bash

set -e
set -u
set -o pipefail

# Expected Environment Variables
# TEST_ENVIRONMENT_URL: Base URL of the deployed application for testing.
# TEST_SUITE_PATH: Path to the integration test suite/files (e.g., tests/integration, specific_test_file.py).
# INTEGRATION_TEST_REPORTS_DIR: Directory for JUnit XML reports.

echo "Starting integration tests execution..."

: "${TEST_ENVIRONMENT_URL:?Error: TEST_ENVIRONMENT_URL environment variable is not set.}"
: "${TEST_SUITE_PATH:?Error: TEST_SUITE_PATH environment variable is not set.}"
: "${INTEGRATION_TEST_REPORTS_DIR:?Error: INTEGRATION_TEST_REPORTS_DIR environment variable is not set.}"

echo "Test Environment URL: $TEST_ENVIRONMENT_URL"
echo "Test Suite Path: $TEST_SUITE_PATH"
echo "Integration Test Reports Directory: $INTEGRATION_TEST_REPORTS_DIR"

mkdir -p "$INTEGRATION_TEST_REPORTS_DIR"

# The working directory for test execution is assumed to be the root of the integration test project,
# or pytest should be able_to find tests from TEST_SUITE_PATH.
# If TEST_SUITE_PATH is relative, it's relative to the CI job's working directory.

# Exporting TEST_ENVIRONMENT_URL so tests can access it if needed.
export APP_BASE_URL="$TEST_ENVIRONMENT_URL" # Some test frameworks might pick this up.

echo "Running integration tests using Pytest..."
# Example using Pytest:
# Adjust the command based on the actual test framework and its requirements.
# The `-E` flag mentioned in SDS is not a standard pytest flag for setting base URL.
# Instead, tests should be written to consume an environment variable or a pytest custom option.
# Here, we set APP_BASE_URL as an env var. Tests can use os.environ.get('APP_BASE_URL').
# If using pytest-base-url plugin, it would be --base-url="$TEST_ENVIRONMENT_URL".

PYTEST_COMMAND="pytest \"$TEST_SUITE_PATH\" --junitxml=\"$INTEGRATION_TEST_REPORTS_DIR/integration-junit-report.xml\""

# Pass environment variables to pytest tests by exporting them, or using pytest's -E (if it's a plugin like pytest-env)
# For now, relying on environment export.
echo "Executing: $PYTEST_COMMAND"

TEST_EXIT_CODE=0
if eval "$PYTEST_COMMAND"; then
  echo "Integration tests completed successfully."
else
  TEST_EXIT_CODE=$?
  echo "Error: Integration tests failed with exit code $TEST_EXIT_CODE."
fi

# Unset the exported variable if necessary, though job environment is ephemeral
# unset APP_BASE_URL

echo "Integration test script finished."
exit $TEST_EXIT_CODE
```