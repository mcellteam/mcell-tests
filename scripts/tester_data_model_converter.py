"""
Copyright (C) 2019 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

"""
This module contains functions to check tests in tests_mdl.
"""

import os
import sys
import shutil
from typing import List, Dict


from test_settings import *
from tester_base import TesterBase
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE = False

MCELL_BASE_ARGS = ['-seed', '1']


class TesterDataModelConverter(TesterBase):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_src_path, args, tool_paths)
        
    @staticmethod
    def check_prerequisites(tool_paths) -> None:
        if not os.path.exists(tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + tool_paths.data_model_to_mdl_script + ".")
            
        TesterBase.check_prerequisites(tool_paths)

    
    def run_mdl_to_dm_conversion(self, mcell_args: List[str], main_mdl_file: str):
        cmd = [ self.tool_paths.mcell_binary ]
        cmd += mcell_args
        cmd += [ main_mdl_file ]
        cmd += self.extra_args.mcell_args
        cmd += [ '-mdl2datamodel4' ]
        
        log_name = self.test_name+'.mdl_to_dm.log'
        exit_code = run(cmd, cwd=self.test_work_path, verbose=False, fout_name=log_name, timeout_sec=MCELL_TIMEOUT)
        if (exit_code):
            self.log_test_error("MCell datamodel conversion failed, see '" + os.path.join(self.test_work_path, log_name) + "'.")
            return FAILED_MCELL
        else:
            return PASSED


    def should_be_skipped_for_datamodel_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip_datamodel')):
            self.log_test_skip("SKIP DATAMODEL")
            return True
        else:
            return False


    def is_todo_for_datamodel_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'todo_datamodel')):
            self.log_test_todo("TODO DATAMODEL")
            return True
        else:
            return False
    
            
    def test(self) -> int:
        
        if self.should_be_skipped_for_datamodel_test():
            return SKIPPED
    
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return KNOWN_FAIL
        
        self.clean_and_create_work_dir()
        
        res = self.run_mdl_to_dm_conversion(MCELL_BASE_ARGS, os.path.join(self.test_src_path, MAIN_MDL_FILE))

        if res == PASSED:
            res = self.run_dm_to_mdl_conversion(os.path.join(self.test_work_path, 'data_model.json'), '-data-model-from-mdl')
            
        if res == PASSED:
            self.change_viz_output_to_ascii()
        
        if res == PASSED:
            mcell_args = MCELL_BASE_ARGS.copy()
            if self.mcell4_testing:
                mcell_args.append('-mcell4')
            res = self.run_mcell(mcell_args, os.path.join(self.test_work_path, MAIN_MDL_FILE))
        
        if self.is_todo_test() or self.is_todo_for_datamodel_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec() and not self.is_todo_test():
            return res
        
        res = self.check_reference_data(viz_ref_required=True, fdiff_args_override=self.extra_args.fdiff_datamodel_converter_args)
        return res
