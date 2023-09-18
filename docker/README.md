# nexus-docker-cleaner

## Сборка

### Список аргументов

Файл `docker/Dockerfile` содержит в себе следующие аргументы:

| Имя аргумента       | Описание                                                    | Значение по умолчанию      |
|---------------------|-------------------------------------------------------------|----------------------------|
| REDHAT_REGISTRY     | ссылка на репозиторий контейнеров Red Hat Container Catalog | registry.access.redhat.com |
| PYTHON_REPOSITORY   | ссылка на репозиторий NPM-пакетов                           | https://pypi.org/simple    |

Значение аргумента можно переопределить с помощью параметра `--build-arg` в командах `docker build` и `buildah bud`.

### Сборка контейнера:

```commandline
buildah bud --no-cache -f docker/Dockerfile \
            --build-arg REDHAT_REGISTRY=registry.access.redhat.com \
            --build-arg PYTHON_REPOSITORY=https://pypi.org/simple \
            -t devops/nexus-docker-cleaner:local .
```

### Запуск контейнера

```commandline
podman run  -e USER_LOGIN="login" \
            -e USER_PSW="password" \
            -e NEXUS_URL="https://nexus.example.com" \
            -e CLEAN_TASK_ID="" \
            -e REPOSITORY="example-name-repo-docker" \
            -e SAVE_QUOTA=3 \
            -e SEARCH_REPOS="app app1 app2" \
            -e SEARCH_TAGS="develop test master" \
            devops/nexus-docker-cleaner:local
```