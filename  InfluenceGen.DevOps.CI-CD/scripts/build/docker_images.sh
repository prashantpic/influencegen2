```bash
#!/bin/bash

set -e
set -u
set -o pipefail

# Parameters passed from GitLab CI job
DOCKERFILE_PATH_PARAM="${1}"         # Path to the Dockerfile
IMAGE_NAME_PARAM="${2}"            # Name for the Docker image (e.g., my-app)
IMAGE_TAG_PARAM="${3}"             # Tag for the Docker image (e.g., $CI_COMMIT_SHA, latest)
# REGISTRY_IMAGE_BASE_PARAM is the GitLab CI_REGISTRY_IMAGE (e.g., registry.gitlab.com/group/project)
# If set, image will be pushed as $REGISTRY_IMAGE_BASE_PARAM/$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM
REGISTRY_IMAGE_BASE_PARAM="${4:-}" # Optional: URL of the Docker registry image base (e.g., $CI_REGISTRY_IMAGE)

# GitLab CI provides these for its own registry
# CI_REGISTRY, CI_REGISTRY_USER, CI_REGISTRY_PASSWORD

echo "Starting Docker image build..."
echo "Dockerfile: $DOCKERFILE_PATH_PARAM"
echo "Image Name: $IMAGE_NAME_PARAM"
echo "Image Tag: $IMAGE_TAG_PARAM"
echo "Registry Image Base: $REGISTRY_IMAGE_BASE_PARAM"

# Validate parameters
if [ -z "$DOCKERFILE_PATH_PARAM" ]; then
  echo "Error: Dockerfile path not provided."
  exit 1
fi
if [ ! -f "$DOCKERFILE_PATH_PARAM" ]; then
  echo "Error: Dockerfile not found at '$DOCKERFILE_PATH_PARAM'."
  exit 1
fi
if [ -z "$IMAGE_NAME_PARAM" ]; then
  echo "Error: Image name not provided."
  exit 1
fi
if [ -z "$IMAGE_TAG_PARAM" ]; then
  echo "Error: Image tag not provided."
  exit 1
fi

LOCAL_IMAGE_FULL_NAME="$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM"

# Determine build context. Assume Dockerfile is relative to project root or path includes context.
# For simplicity, assume build context is the directory containing the Dockerfile.
BUILD_CONTEXT=$(dirname "$DOCKERFILE_PATH_PARAM")
if [ "$BUILD_CONTEXT" == "." ]; then
    # If Dockerfile is in current dir, context is current dir.
    # Often, CI jobs checkout code and run scripts from the project root.
    # Let's assume the Dockerfile is at the root of the context it needs,
    # or the path to Dockerfile correctly implies the context.
    # A common pattern is to have Dockerfiles in the project root or a `dockerfiles/` dir,
    # and the context is `.` (project root).
    # If DOCKERFILE_PATH_PARAM is e.g. "dockerfiles/my_app.Dockerfile", dirname is "dockerfiles"
    # But often the context is the project root "."
    # The SDS implies docker build -f ... .
    # So we will use "." as context. User must ensure Dockerfile path is correct relative to this.
    BUILD_CONTEXT="."
fi

echo "Building Docker image: $LOCAL_IMAGE_FULL_NAME from Dockerfile: $DOCKERFILE_PATH_PARAM with context: $BUILD_CONTEXT"
if docker build -f "$DOCKERFILE_PATH_PARAM" -t "$LOCAL_IMAGE_FULL_NAME" "$BUILD_CONTEXT"; then
  echo "Docker image built successfully: $LOCAL_IMAGE_FULL_NAME"
else
  echo "Error: Docker image build failed."
  exit 1
fi

if [ -n "$REGISTRY_IMAGE_BASE_PARAM" ]; then
  # Ensure CI_REGISTRY, CI_REGISTRY_USER, CI_REGISTRY_PASSWORD are set for pushing
  if [ -z "${CI_REGISTRY:-}" ] || [ -z "${CI_REGISTRY_USER:-}" ] || [ -z "${CI_REGISTRY_PASSWORD:-}" ]; then
      echo "Error: CI_REGISTRY, CI_REGISTRY_USER, or CI_REGISTRY_PASSWORD is not set. Cannot push image."
      exit 1
  fi

  REMOTE_IMAGE_FULL_NAME="$REGISTRY_IMAGE_BASE_PARAM/$IMAGE_NAME_PARAM:$IMAGE_TAG_PARAM"
  echo "Pushing image to registry: $REMOTE_IMAGE_FULL_NAME"

  echo "Logging into Docker registry: $CI_REGISTRY"
  if echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"; then
    echo "Docker login successful."
  else
    echo "Error: Docker login failed."
    exit 1
  fi

  echo "Tagging image $LOCAL_IMAGE_FULL_NAME as $REMOTE_IMAGE_FULL_NAME"
  if docker tag "$LOCAL_IMAGE_FULL_NAME" "$REMOTE_IMAGE_FULL_NAME"; then
    echo "Image tagged successfully."
  else
    echo "Error: Failed to tag image."
    exit 1
  fi

  echo "Pushing image $REMOTE_IMAGE_FULL_NAME"
  if docker push "$REMOTE_IMAGE_FULL_NAME"; then
    echo "Image pushed successfully."
  else
    echo "Error: Failed to push image."
    exit 1
  fi
else
  echo "REGISTRY_URL_PARAM not set. Skipping Docker push."
fi

echo "Script completed."
exit 0
```