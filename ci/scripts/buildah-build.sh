#!/usr/bin/env bash

set -e

REDHAT_REGISTRY=${bamboo_registry_redhat}
PYTHON39_IMAGE=${bamboo_images_python39}
PYTHON_REPOSITORY=${bamboo_repository_python}

IMAGE_REGISTRY=${bamboo_registry_docker}
IMAGE_REPOSITORY=devops/nexus-docker-cleaner
IMAGE_TAG=${bamboo_planRepository_branchName//\//-}-${bamboo_buildNumber}
IMAGE_NAME=${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}:${IMAGE_TAG}

buildah bud -f docker/Dockerfile --no-cache \
        --build-arg REDHAT_REGISTRY=${REDHAT_REGISTRY} \
        --build-arg PYTHON_IMAGE=${PYTHON39_IMAGE} \
        --build-arg PYTHON_REPOSITORY=${PYTHON_REPOSITORY} \
        --tag ${IMAGE_NAME} .