ARG REDHAT_REGISTRY=registry.access.redhat.com
ARG PYTHON_IMAGE=ubi8/python-39:1-134

FROM $REDHAT_REGISTRY/$PYTHON_IMAGE
COPY --chown=1001:0 src/ .
ARG PYTHON_REPOSITORY=https://pypi.org
RUN pip install -r requirements.txt --index-url ${PYTHON_REPOSITORY}
ENTRYPOINT ["python3", "nexus-docker-cleaner.py", "--no-interactive"]