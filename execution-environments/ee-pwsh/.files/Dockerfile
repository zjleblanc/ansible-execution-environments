ARG EE_BASE_IMAGE=quay.io/ansible/ansible-runner:latest
ARG EE_BUILDER_IMAGE=quay.io/ansible/ansible-builder:latest

FROM $EE_BASE_IMAGE as galaxy
ARG ANSIBLE_GALAXY_CLI_COLLECTION_OPTS=
ARG ANSIBLE_GALAXY_CLI_ROLE_OPTS=
USER root


FROM $EE_BUILDER_IMAGE as builder

FROM $EE_BASE_IMAGE
USER root
COPY microsoft.repo /etc/yum.repos.d/microsoft.repo
COPY --from=builder /output/ /output/
RUN /output/install-from-bindep && rm -rf /output/wheels
RUN dnf install --assumeyes powershell
LABEL ansible-execution-environment=true
