"""
Copyright (C) 2020 by
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
from tester_pymcell4 import TesterPymcell4
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE = False

MCELL_BASE_ARGS = ['-seed', '1']


class TesterDataModelPymcell4(TesterPymcell4):
    def __init___(self, test_src_path: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_src_path, args, tool_paths)
        
    @staticmethod
    def check_prerequisites(tool_paths) -> None:
        if not os.path.exists(tool_paths.data_model_to_pymcell_binary):
            fatal_error("Could not find data model to pymcell conversion tool '" + tool_paths.data_model_to_pymcell_binary + ".")
            
        TesterBase.check_prerequisites(tool_paths)


    def should_be_skipped_for_datamodel_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip_datamodel')):
            self.log_test_skip("SKIP DATAMODEL")
            return True
        else:
            return False


    def should_be_skipped_for_pymcell4_test(self) -> bool:
        if os.path.exists(os.path.join(self.test_src_path, 'skip_pymcell4')):
            self.log_test_skip("SKIP PYMCELL4")
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
    
        if self.should_be_skipped_for_pymcell4_test():
            return SKIPPED
        
        if self.should_be_skipped():
            return SKIPPED
            
        if self.is_known_fail():
            return KNOWN_FAIL
        
        if ARG_CHECKPOINTS in self.args:
            iters = self.load_checkpoint_iters()
            if not iters:
                return IGNORED
            
        self.clean_and_create_work_dir()

        extra_args = ['-t']
        if ARG_CONVERT_W_BNGL in self.args:
            extra_args += ['-b']   
        if ARG_CHECKPOINTS in self.args:
            extra_args += ['-k', ','.join(iters)]               
            
        res = self.run_dm_to_pymcell_conversion(
            os.path.join(self.test_src_path, self.test_name + '.json'), 
            extra_args=extra_args)            
            
        if res == PASSED:
            if ARG_CHECKPOINTS not in self.args:
                # single run
                res = self.run_pymcell4(test_dir=self.test_work_path)
            else:
                # run with checkpoints, run until run has finished
                # TODO: use seed argument 
                res = self.run_pymcell4(test_dir=self.test_work_path)
                while res == PASSED and \
                    not self.run_finished(os.path.join(self.test_work_path, 'reports/run_report_00001.txt')):
                    
                    res = self.run_pymcell4(test_dir=self.test_work_path)
                    
        if self.is_todo_test() or self.is_todo_for_datamodel_test():
            return TODO_TEST
        
        if res != PASSED and not self.expected_wrong_ec() and not self.is_todo_test():
            return res
        
        res = self.check_reference_data(viz_ref_required=False, fdiff_args_override=self.extra_args.fdiff_datamodel_converter_args)
        return res
