# ee-pwsh

Execution Environment with Powershell for Linux
<br>
[🗂️ Quay Repo](https://quay.io/repository/zleblanc/ee-pwsh?tab=info)
<br>
[🐳 Dockerfile](./.files/Dockerfile)

## required changes

1. Create a yum repo conf file for microsoft packages
    ```ini
    ## mkdir -p context && touch context/microsoft.repo
    [msft-prod]
    name=msft-prod
    baseurl=https://packages.microsoft.com/rhel/8/prod/
    enabled=1
    gpgcheck=1
    gpgkey=https://packages.microsoft.com/keys/microsoft.asc
    ```
1. Define additional build steps for injecting repo file and installing powershell
    ```yaml
    additional_build_steps:
    prepend: 
      - COPY microsoft.repo /etc/yum.repos.d/microsoft.repo
    append:
      - RUN dnf install --assumeyes powershell
    ```