# ee-windows

Execution Environment with Windows modules and kerberos enabled
<br>
[🗂️ Quay Repo](https://quay.io/repository/zleblanc/ee-windows?tab=info)
<br>
[🐳 Dockerfile](./.files/Dockerfile)

## additional build steps

Define additional build steps for injecting krb5 conf and enabling encryption support for Active Directory
```yaml
additional_build_steps:
  prepend: 
    - COPY krb5.conf /etc/krb5.conf
  append:
    - RUN dnf install -y crypto-policies-scripts
    - RUN update-crypto-policies --set DEFAULT:AD-SUPPORT
```