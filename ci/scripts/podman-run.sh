#!/usr/bin/env bash

set -e

IMAGE_REGISTRY=${bamboo_registry_docker}
IMAGE_REPOSITORY=devops/nexus-docker-cleaner
IMAGE_TAG=${bamboo_planRepository_branchName//\//-}-${bamboo_buildNumber}
IMAGE_NAME=${IMAGE_REGISTRY}/${IMAGE_REPOSITORY}:${IMAGE_TAG}

USER_LOGIN=${bamboo_nexus_username}
USER_PSW=${bamboo_nexus_password}
NEXUS_URL=${bamboo_nexus_url}
CLEAN_TASK_ID=${bamboo_nexus_clean_task_id}
REPOSITORY=${bamboo_nexus_clean_repository}
SAVE_QUOTA=${bamboo_nexus_clean_saveQuota}
SEARCH_REPOS="${bamboo_nexus_clean_search_repos}"
SEARCH_TAGS="${bamboo_nexus_clean_search_tags}"

podman run --rm -e USER_LOGIN=${USER_LOGIN} \
                -e USER_PSW="${USER_PSW}" \
                -e NEXUS_URL=${NEXUS_URL} \
                -e CLEAN_TASK_ID=${CLEAN_TASK_ID} \
                -e REPOSITORY=${REPOSITORY} \
                -e SAVE_QUOTA=${SAVE_QUOTA} \
                -e SEARCH_REPOS="${SEARCH_REPOS}" \
                -e SEARCH_TAGS="${SEARCH_TAGS}" \
                ${IMAGE_NAME}