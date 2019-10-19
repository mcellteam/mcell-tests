"""
Copyright (C) 2019 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

For the complete terms of the GNU General Public License, please see this URL:
http://www.gnu.org/licenses/gpl-2.0.html
"""

"""
This module contains functions to check tests in tests_mdl.
"""

import os
import sys
import shutil

from test_settings import *
from tester_base import TesterBase
from test_utils import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE=False

MCELL_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterMdl(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)        
        
    def update_reference(self) -> None:
        reference = os.path.join('..', self.test_src_path, REF_VIZ_OUTPUT_DIR, SEED_DIR)
        new_res = os.path.join(VIZ_OUTPUT_DIR, SEED_DIR)

        log("Updating reference " + reference + " with data from " + new_res + " (cwd:" + os.getcwd() + ")")
        
        # remove whole directory
        if os.path.exists(reference):
            log("Cleaning old data in " + reference + " (cwd:" + os.getcwd() + ")")
            shutil.rmtree(reference)
            
        shutil.copytree(new_res, reference)

    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED

        self.clean_and_create_work_dir()
        
        res = self.run_mcell(MCELL_ARGS, os.path.join('..', self.test_src_path, MAIN_MDL_FILE))
    
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(SEED_DIR)
        else:
            if res != PASSED:
                fatal_error("Tried to update reference data but mcell execution failed!")
                
            self.update_reference()
        
        return res
