```bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
set -u
# Pipestatus: Preserve exit status of the last command in a pipe that failed.
set -o pipefail

SOURCE_DIR="$1"
OUTPUT_ARTIFACT_NAME="$2"

# Validate input parameters
if [ -z "$SOURCE_DIR" ]; then
  echo "Error: Source directory (param 1) not provided."
  exit 1
fi

if [ -z "$OUTPUT_ARTIFACT_NAME" ]; then
  echo "Error: Output artifact name (param 2) not provided."
  exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Source directory '$SOURCE_DIR' does not exist."
  exit 1
fi

echo "Starting Odoo modules packaging..."
echo "Source directory: $SOURCE_DIR"
echo "Output artifact: $OUTPUT_ARTIFACT_NAME"

# Navigate to the source directory
cd "$SOURCE_DIR"

# Identify InfluenceGen custom addon directories
# This assumes custom modules are prefixed with 'influence_gen_' or are explicitly listed.
# For simplicity, we'll try to find directories.
# A more robust way would be to have a manifest file listing modules.
MODULE_DIRS_TO_PACKAGE=()
for dir in */; do
    # Check if it's a directory and looks like an Odoo module (e.g., has __manifest__.py)
    if [ -d "$dir" ] && [ -f "${dir}__manifest__.py" ]; then
        # Example: only package modules starting with influence_gen_
        # if [[ "$dir" == influence_gen_* ]]; then
        #    MODULE_DIRS_TO_PACKAGE+=("${dir%/}") # Remove trailing slash
        # fi
        # For this script, let's assume all valid modules in subdirs are to be packaged.
        MODULE_DIRS_TO_PACKAGE+=("${dir%/}") # Add all directories with a manifest
    fi
done

if [ ${#MODULE_DIRS_TO_PACKAGE[@]} -eq 0 ]; then
    echo "Warning: No Odoo module directories found or matched for packaging in $SOURCE_DIR."
    # Depending on requirements, this could be an error or just an empty zip.
    # For now, create an empty zip if nothing is found to avoid later CI steps failing on missing artifact.
    touch empty.txt
    zip -r "../$OUTPUT_ARTIFACT_NAME" empty.txt
    rm empty.txt
    echo "Created an empty artifact as no modules were found."
    cd ..
    exit 0
fi

echo "Modules to be packaged: ${MODULE_DIRS_TO_PACKAGE[*]}"

# Create the archive in the parent directory (CI job's working directory)
# Exclude VCS directories and __pycache__
# The zip command runs from within SOURCE_DIR, so target is ../$OUTPUT_ARTIFACT_NAME
zip_command="zip -r ../$OUTPUT_ARTIFACT_NAME"
for module_dir in "${MODULE_DIRS_TO_PACKAGE[@]}"; do
    zip_command+=" $module_dir"
done
zip_command+=" -x '*/.git/*' '*/__pycache__/*'"

echo "Executing: $zip_command"
if eval "$zip_command"; then
  echo "Odoo modules packaged successfully into '../$OUTPUT_ARTIFACT_NAME'"
else
  echo "Error: Failed to package Odoo modules."
  exit 1
fi

# Navigate back to the original directory (CI job's workspace)
cd ..

echo "Script completed."
exit 0
```