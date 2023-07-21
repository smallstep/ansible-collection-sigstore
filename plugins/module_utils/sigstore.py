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

    def _gather_result(self) -> dict:
        """Gather all of the result for every module

        :return: dict
        """
        return {}

    def get_result(self):
        if getattr(self, self.represent) is not None:
            self.result[self.represent] = self._gather_result()
        return self.result
