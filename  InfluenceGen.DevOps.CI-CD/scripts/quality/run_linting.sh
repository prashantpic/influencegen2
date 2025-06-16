```bash
#!/bin/bash

# set -e: Exit immediately if a command exits with a non-zero status.
# For linting, we might want to run all linters and collect all reports
# even if one fails, then decide based on overall status.
# So, 'set -e' is used, but individual lint commands will be handled.
set -e
set -u
set -o pipefail


# Expected Environment Variables
# LINT_TARGET_PATH: Path to the Odoo custom modules source code.
# LINT_REPORTS_DIR: Directory for linting reports.

echo "Starting code linting..."

: "${LINT_TARGET_PATH:?Error: LINT_TARGET_PATH environment variable is not set.}"
: "${LINT_REPORTS_DIR:?Error: LINT_REPORTS_DIR environment variable is not set.}"

if [ ! -d "$LINT_TARGET_PATH" ]; then
  echo "Error: Lint target path '$LINT_TARGET_PATH' does not exist."
  exit 1
fi

echo "Lint Target Path: $LINT_TARGET_PATH"
echo "Lint Reports Directory: $LINT_REPORTS_DIR"

mkdir -p "$LINT_REPORTS_DIR"

FLAKE8_REPORT_FILE="$LINT_REPORTS_DIR/flake8-report.txt"
PYLINT_REPORT_FILE="$LINT_REPORTS_DIR/pylint-report.txt"

flake8_exit_code=0
pylint_exit_code=0

# --- Flake8 ---
echo "Running Flake8..."
# The --format=gitlab option can produce GitLab Code Quality compatible JSON.
# Default format is text. SDS says "default or GitLab compatible format".
# For now, using text output.
if flake8 "$LINT_TARGET_PATH" --output-file="$FLAKE8_REPORT_FILE" --format=default; then
  echo "Flake8 found no issues."
else
  flake8_exit_code=$?
  echo "Flake8 found issues. Report generated at $FLAKE8_REPORT_FILE. Exit code: $flake8_exit_code"
  # Continue to run pylint
fi

# --- Pylint ---
echo "Running Pylint..."
# Pylint has various output formats. Default is text.
# For GitLab CI, a parseable format or a tool to convert pylint output to GitLab Code Quality JSON might be used.
if pylint "$LINT_TARGET_PATH" > "$PYLINT_REPORT_FILE"; then
  echo "Pylint found no issues."
else
  pylint_exit_code=$?
  # Pylint uses different bits in exit code for different types of messages.
  # Any non-zero usually means issues were found.
  echo "Pylint found issues. Report generated at $PYLINT_REPORT_FILE. Exit code: $pylint_exit_code"
  # Continue
fi

echo "Linting reports generated in $LINT_REPORTS_DIR."

# Decision on overall script exit code
# The CI job template uses `allow_failure: true`, so this script's exit code
# determines if the job is marked as failed (even if allowed to not fail the pipeline).
if [ "$flake8_exit_code" -ne 0 ] || [ "$pylint_exit_code" -ne 0 ]; then
  echo "Linting checks detected issues."
  # To make the job fail (if allow_failure is false in consuming job):
  exit 1
else
  echo "All linting checks passed."
  exit 0
fi
```