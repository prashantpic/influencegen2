```bash
#!/bin/bash

set -e
set -u
set -o pipefail

SOURCE_DIR="$1"
OUTPUT_ARTIFACT_NAME="$2"

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

echo "Starting N8N workflows packaging..."
echo "Source directory: $SOURCE_DIR"
echo "Output artifact: $OUTPUT_ARTIFACT_NAME"

cd "$SOURCE_DIR"

# Find all .json workflow files and any associated configuration/script files
# Assuming workflows are .json files at the root or in subdirectories
# And specific directories like 'config_files' or 'script_files' if they exist.

# Collect all .json files, config_files, and script_files
FILES_TO_PACKAGE=()
while IFS= read -r -d $'\0' file; do
    FILES_TO_PACKAGE+=("$file")
done < <(find . -maxdepth 1 -name '*.json' -print0) # JSON files in root

# Add specific directories if they exist
if [ -d "config_files" ]; then
    FILES_TO_PACKAGE+=("config_files")
fi
if [ -d "script_files" ]; then
    FILES_TO_PACKAGE+=("script_files")
fi
# Add other directories or file patterns as needed

if [ ${#FILES_TO_PACKAGE[@]} -eq 0 ]; then
    echo "Warning: No N8N workflow files or specified directories found for packaging in $SOURCE_DIR."
    # Create an empty zip if nothing is found
    touch empty.txt
    zip -r "../$OUTPUT_ARTIFACT_NAME" empty.txt
    rm empty.txt
    echo "Created an empty artifact as no N8N workflows were found."
    cd ..
    exit 0
fi

echo "Files and directories to be packaged: ${FILES_TO_PACKAGE[*]}"

# Create the archive in the parent directory (CI job's working directory)
zip_command="zip -r ../$OUTPUT_ARTIFACT_NAME"
for item in "${FILES_TO_PACKAGE[@]}"; do
    zip_command+=" \"$item\"" # Quote items to handle spaces
done
zip_command+=" -x '*/.git/*' '*/.DS_Store'" # Exclude common unwanted files

echo "Executing: $zip_command"
if eval "$zip_command"; then
  echo "N8N workflows packaged successfully into '../$OUTPUT_ARTIFACT_NAME'"
else
  echo "Error: Failed to package N8N workflows."
  exit 1
fi

cd ..

echo "Script completed."
exit 0
```