# Automate Execution Environment Builds for Offline Use Cases

This document supports the Autodotes Blog Post for building EEs that are prepped for offline use cases. Check out the post for details - below are the files used in this process:

## Bitbucket Pipeline

The [bitbucket-pipelines.yml](./bitbucket-pipelines.yml) definition describes a default pipeline which runs a custom python script. The pipeline file uses the latest python image from Docker Hub and installs the requirements before running the script.

## The Python Script

The [bitbucket-trigger-ansible.py](./bitbucket-trigger-ansible.py) script contains the logic to determine **_which_** execution environments to build based on changes in the associated commit. For each execution environment folder that has modifications an Ansible Job Template will be launched to build the new version.

## The Ansible Playbook

The [build-ee.yml](./ansible/build-ee.yml) playbook uses the [infra.ee_utilities](https://github.com/redhat-cop/ee_utilities) collection to build an execution environment on a dedicated build server. The resulting image is published to a specified destination registry and a tarball is published to a dedicated artifacts server for offline usage.