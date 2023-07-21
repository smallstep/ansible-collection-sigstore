# Ansible Collection - smallstep.sigstore

This is collection provides the `smallstep.sigstore.sigstore_verify` module which requires the [sigstore](https://github.com/sigstore/sigstore-python) python package. This module can be used verify the signature on an artifact that was signed by [Sigstore](https://www.sigstore.dev/). It also provides the `smallstep.sigstore.verify_artifact` role which can be included in playbooks to verify the Sigstore signature on an aritifact and it can ensure that [sigstore](https://github.com/sigstore/sigstore-python) python package is installed and it can be configured to fail the playbook run if the verification of the signature fails.

## Requirements

* `ansible-galaxy collection install smallstep.sigstore` (on control node)
* `pip install sigstore` (on servers)

## Module: smallstep.sigstore.sigstore_verify

### Usage

Here is an example of using the module:

```yaml
- name: Verify an artifact with Sigstore
  smallstep.sigstore.sigstore_verify:
    file: /path/to/foo.tar.gz
    certificate: /path/to/foo.tar.gz.pem
    signature: /path/to/foo.tar.gz.sig
    cert_identity: user@example.com
    cert_oidc_issuer: https://oidc.example.com
  register: sigstore_verify_results
```

### Return data

If you register the results from `smallstep.sigstore.sigstore_verify` it will return the `file`, `certificate`, `signature`, `cert_identity`, and `cert_oidc_issuer` (useful for debugging) and `verification_status` will return `True` or `False`. If it returns `False`, it will also return `verification_failure_reason` which is the reason for the error from [sigstore](https://github.com/sigstore/sigstore-python). Here are two examples of the return data.

#### Verification successful

```json
"cert_identity": "https://github.com/smallstep/cli/.github/workflows/release.yml@refs/tags/v0.24.4",
"cert_oidc_issuer": "https://token.actions.githubusercontent.com",
"certificate": "/files/checksums.txt.pem",
"file": "/files/checksums.txt",
"signature": "/files/checksums.txt.sig",
"verification_status": "True"
```

#### Verification failure

```json
"cert_identity": "https://github.com/smallstep/cli/.github/workflows/release.yml@refs/tags/v0.24.4",
"cert_oidc_issuer": "https://token.actions.githubusercontent.com",
"certificate": "/files/checksums.txt.pem",
"file": "/files/checksums.txt",
"signature": "/files/checksums.txt.sig.bad",
"verification_failure_reason": "Signature is invalid for input",
"verification_status": "False"
```

## Role: smallstep.sigstore.verify_artifact

### Role variables

```yaml
verify_artifact_file: /path/to/artifact.tar.gz # Has to be full path to the archive (Required)
verify_artifact_certificate: /path/to/artifact.tar.gz.pem # Has to be full path to the certificate and it can be an ASCII PEM or Base64 encoded PEM (Required)
verify_artifact_signature: /path/to/artifact.tar.gz.sig # Has to be full path to the archive signature file (Required)
verify_artifact_cert_identity: user@example.com # The identity to check for in the certificate's Subject Alternative Name (Required)
verify_artifact_cert_oidc_issuer: https://oidc.example.com # The OIDC issuer URL to check for in the certificate's OIDC issuer extension (Required)
verify_artifact_fail_run: True # If set to False it will _not_ fail the playbook run if verification fails (Defaults to True)
verify_artifact_pip_sigstore_install: True # Ensure the pip sigstore package is installed (Defaults to True)
verify_artifact_pip_sigstore_version: 1.1.2 # Specific version to install. (Defaults to 1.1.2)
```

### Example Playbook

```yaml
- hosts: localhost
  tasks:
  - name: Verify the foo.tar.gz artifact using sigstore and fail if it doesn't pass verification
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

## Testing

### Install the collection locally

```bash
ansible-galaxy collection build --output-path /tmp --force
ansible-galaxy collection install /tmp/smallstep-sigstore-0.0.1.tar.gz --force
```

You can then use the example playbook to test your changes. See `tests/integration/targets/sigstore_verify/files/` for some test data.

### ansible-test sanity

```bash
ansible-test sanity --docker --skip-test validate-modules
```

### ansible-test integration*

```bash
ansible-test integration --docker
```

## License

[Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>)

Copyright 2023 Smallstep Labs Inc.
