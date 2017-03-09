from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *

import os
import shutil
import unittest

from util import run_cmd, maybe_create_dir, zeroth_line_starts_with


class AcceptanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_directory = os.path.splitext(__file__)[0]
        self.test_name = os.path.basename(self.test_directory)
        self.script = os.path.join(os.environ["BIN_DIR"], "basecall_network.py")

        self.work_dir = os.path.join(os.environ["ACCTEST_WORK_DIR"], self.test_name)
        maybe_create_dir(self.work_dir)

        self.data_dir = os.path.join(os.environ["DATA_DIR"], self.test_name)

    def test_usage(self):
        cmd = [self.script]
        run_cmd(self, cmd).return_code(2).stderr(zeroth_line_starts_with(u"usage"))

    def test_raw_iteration_failure_on_files_with_no_raw_data(self):
        model_file = os.path.join(self.data_dir, "raw_model_1pt2_cpu.pkl")
        self.assertTrue(os.path.exists(model_file))

        reads_dir = os.path.join(self.data_dir, "no_raw", "reads")
        self.assertTrue(os.path.exists(reads_dir))

        cmd = [self.script, "raw", model_file, reads_dir]
        run_cmd(self, cmd).return_code(0).stderr(last_line_starts_with(u"no raw data to basecall"))
