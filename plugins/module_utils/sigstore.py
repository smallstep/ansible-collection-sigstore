# Copyright: (c) 2023, Smallstep Labs, Inc. <techadmin@smallstep.com>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0/)

from ansible.module_utils.ansible_release import __version__


class Sigstore:
    def __init__(self, module, represent):
        self.module = module
        self.represent = represent
        self.result = {"changed": False, self.represent: None}

    def _set_changed(self):
        self.result["changed"] = True

    @staticmethod
    def default_module_arguments():
        return {}
