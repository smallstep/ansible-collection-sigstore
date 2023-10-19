#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Smallstep Labs, Inc. <techadmin@smallstep.com>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0/)


DOCUMENTATION = """
---
module: sigstore_verify

short_description: Verify an artifact with Sigstore

description:
    - Verify an artifact with Sigstore

author:
    - Joe Doss (@jdoss)

options:
    file:
        description:
            - The file you want to verify.
            - Required.
        type: str
    certificate:
        description:
            - The certificate file.
            - Required.
        type: str
    signature:
        description:
            - The signature file.
            - Required.
        type: str
    cert_identity:
        description:
            - The identity to check for in the certificate's Subject Alternative Name.
            - Required.
        type: str
    cert_oidc_issuer:
        description:
            - The OpenID Connect issuer to use.
            - Required.
        type: str
"""

EXAMPLES = """
- name: Verify an artifact with Sigstore
  smallstep.sigstore.sigstore_verify:
    file: artifact.tar.gz
    certificate: artifact.tar.gz.pem
    signature: artifact.tar.gz.sig
    cert_identity: user@example.org
    cert_oidc_issuer: https://token.actions.githubusercontent.com
"""

RETURN = """
sigstore_verify:
    description: The verification status of an artifact
    returned: Always
    type: dict
    contains:
        file:
            description: Returns the name of the artifact file that was verified
            returned: always
            type: str
            sample: artifact.tar.gz
        certificate:
            description: Returns the name of the certificate file that was used to verify the artifact
            returned: always
            type: str
            sample: artifact.tar.gz.pem
        signature:
            description: Returns the name of the signature file that was used to verify the artifact
            returned: always
            type: str
            sample: artifact.tar.gz.sig
        cert_identity:
            description: Returns the certificate identity used to check in the certificate's Subject Alternative Name
            returned: always
            type: str
            sample: user@example.org
        cert_oidc_issuer:
            description: Returns the OIDC issuer URL
            returned: always
            type: str
            sample: https://token.actions.githubusercontent.com
        verification_status:
            description: Returns the status of the file verification.
            returned: always
            type: bool
            sample: True
        verification_failure_reason:
            description: If verification_status is False, this will output the reason for the failure
            returned: always
            type: bool
            sample: True
"""

import base64  # noqa: E402
import binascii  # noqa: E402
import traceback  # noqa: E402
from pathlib import Path  # noqa: E402

from ansible.module_utils.basic import AnsibleModule, missing_required_lib  # noqa: E402
from ansible.module_utils.common.text.converters import to_native  # noqa: E402
from ansible_collections.smallstep.sigstore.plugins.module_utils.sigstore import (  # noqa: E402
    Sigstore,
)

try:
    from sigstore.verify import VerificationMaterials, Verifier
    from sigstore.verify.policy import Identity
except ImportError:
    HAS_SIGSTORE = False
    SIGSTORE_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_SIGSTORE = True
    SIGSTORE_IMPORT_ERROR = None


class AnsibleSigstoreVerify(Sigstore):
    def __init__(self, module):
        super().__init__(module, "sigstore_verify")
        self.sigstore_verify = None

    def verify_artifact(self) -> list:
        self.module.fail_on_missing_params(
            required_params=[
                "file",
                "certificate",
                "signature",
                "cert_identity",
                "cert_oidc_issuer",
            ]
        )

        params = self.module.params

        try:
            # The artifact to verify
            artifact = Path(params["file"])

            # The signing certificate
            cert = Path(params["certificate"])

            # The signature to verify
            signature = Path(params["signature"])

            with artifact.open("rb") as a, cert.open("r") as c, signature.open(
                "rb"
            ) as s:
                try:
                    cert_data = c.read()
                    cert_data_processed = base64.b64decode(
                        cert_data, validate=True
                    ).decode("utf-8")
                except binascii.Error:
                    cert_data_processed = cert_data
                materials = VerificationMaterials(
                    input_=a,
                    cert_pem=cert_data_processed,
                    signature=base64.b64decode(s.read()),
                    rekor_entry=None,
                )
                verifier = Verifier.production()
                file_status = verifier.verify(
                    materials,
                    Identity(
                        identity=params["cert_identity"],
                        issuer=params["cert_oidc_issuer"],
                    ),
                )

            results = params
            if file_status.success:
                results["verification_status"] = to_native(True)
            else:
                results["verification_status"] = to_native(False)
                results["verification_failure_reason"] = to_native(file_status.reason)

            return results

        except Exception as excep:
            self.module.fail_json(msg=to_native(excep))

    @staticmethod
    def define_module():
        return AnsibleModule(
            argument_spec=dict(
                file={"type": "str"},
                certificate={"type": "str"},
                signature={"type": "str"},
                cert_identity={"type": "str"},
                cert_oidc_issuer={"type": "str"},
                **Sigstore.default_module_arguments()
            ),
            required_together=[
                (
                    "file",
                    "certificate",
                    "signature",
                    "cert_identity",
                    "cert_oidc_issuer",
                ),
            ],
            supports_check_mode=True,
        )


def main():
    module = AnsibleSigstoreVerify.define_module()
    if not HAS_SIGSTORE:
        module.fail_json(
            msg=missing_required_lib("sigstore"), exception=SIGSTORE_IMPORT_ERROR
        )

    sigstore = AnsibleSigstoreVerify(module)

    results = sigstore.verify_artifact()

    module.exit_json(**results)


if __name__ == "__main__":
    main()
