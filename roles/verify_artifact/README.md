# smallstep.sigstore.verify_artifact

This is a role that uses the `smallstep.sigstore.sigstore_verify` module from the `smallstep.sigstore` Ansible collection to verify the [Sigstore](https://www.sigstore.dev/) signature on an artifact. it can be configured to fail the playbook run if this verification of the signature fails. It can also ensure that the required python package, [sigstore](https://github.com/sigstore/sigstore-python), is installed on the target servers.

## Requirements

* `ansible-galaxy collection install smallstep.sigstore` (on control node)
* `pip install sigstore` (on servers)

## Role Variables

```yaml
verify_artifact_file: /path/to/artifact.tar.gz # Has to be full path to the archive (Required)
verify_artifact_certificate: /path/to/artifact.tar.gz.pem # Has to be full path to the certificate and it can be an ASCII PEM or Base64 encoded PEM (Required)
verify_artifact_signature: /path/to/artifact.tar.gz.sig # Has to be full path to the archive signature file (Required)
verify_artifact_cert_identity: user@example.com # The identity to check for in the certificate's Subject Alternative Name (Required)
verify_artifact_cert_oidc_issuer: https://oidc.example.com # The OIDC issuer URL to check for in the certificate's OIDC issuer extension (Required)
verify_artifact_fail_run: True # If set to False it will fail the playbook run (Defaults to True)
verify_artifact_pip_sigstore_install: True # Ensure the pip sigstore package is installed (Defaults to True)
verify_artifact_pip_sigstore_version: 1.1.2 # Specific version to install. (Defaults to 1.1.2)
```

## Example Playbook

Here is how you can include this role in your playbook to verify an archive with its PEM and .sig files after they all have been downloaded:

```yaml
- hosts: localhost
  tasks:
  - name: Verify the foo.tar.gz artifact using Sigstore and fail if it doesn't pass verification
    ansible.builtin.include_role:
      name: smallstep.sigstore.verify_artifact
    vars:
      verify_artifact_file: /path/to/foo.tar.gz
      verify_artifact_certificate: /path/to/foo.tar.gz.pem
      verify_artifact_signature: /path/to/foo.tar.gz.sig
      verify_artifact_cert_identity: user@example.com
      verify_artifact_cert_oidc_issuer: https://oidc.example.com
      verify_artifact_fail_run: True
      verify_artifact_pip_sigstore_install: True
      verify_artifact_pip_sigstore_version: 1.1.2
```

## Author Information

Joe Doss @jdoss
Smallstep Engineering

## License

[Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>)

Copyright 2023 Smallstep Labs Inc.
