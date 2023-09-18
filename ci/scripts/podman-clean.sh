#!/usr/bin/env bash

set -e

IMAGE_REGISTRY=${bamboo_registry_docker}
IMAGE_REPOSITORY=devops/nexus-docker-cleaner
IMAGE_TAG=${bamboo_planRepository_branchName//\//-}-${bamboo_buildNumber}
IMAGE_NAME=${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}:${IMAGE_TAG}

podman rmi ${IMAGE_NAME}