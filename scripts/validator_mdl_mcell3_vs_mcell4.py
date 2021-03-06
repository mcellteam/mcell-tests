"""
Copyright (C) 2020 by
The Salk Institute for Biological Studies 

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

import os
import sys
import shutil
import glob
import random
import multiprocessing
import re
from typing import List, Dict

from test_settings import *
from tester_base import TesterBase
from validator_bng_vs_pymcell4 import ValidatorBngVsPymcell4
from tool_paths import ToolPaths

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

class ValidatorMcell3VsMcell4Mdl(ValidatorBngVsPymcell4):
    def __init___(self, test_dir: str, args: List[str], tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, args, tool_paths)
    
    
    @staticmethod
    def check_prerequisites(tool_paths: ToolPaths) -> None:
        TesterBase.check_prerequisites(tool_paths)   
            
           
    def run_validation_mcell4(self, seed):
        res = self.run_mcell(
            ['-mcell4'], 
            os.path.join(self.test_src_path, MAIN_MDL_FILE), 
            seed=seed,            
            timeout_sec=VALIDATION_TIMEOUT)
        
        return res
    
    
    def run_validation_mcell3(self, seed):
        res = self.run_mcell(
            [], 
            os.path.join(self.test_src_path, MAIN_MDL_FILE), 
            seed=seed,            
            timeout_sec=VALIDATION_TIMEOUT)

        return res    
    
    
    def move_output_dirs(self, suffix):
        # MCell4 generates viz_output dir as well, we need to distinguish it from mcell3 run
        viz_dir = os.path.join(self.test_work_path, 'viz_data')
        shutil.move(viz_dir, viz_dir + suffix)
        
        react_dir = os.path.join(self.test_work_path, 'react_data')
        if os.path.exists(react_dir):
            shutil.move(react_dir, react_dir + suffix)
    
    
    def get_molecule_counts_for_multiple_mdl_runs(self, mcell4, seeds):
        
        # Set up the parallel task pool to use all available processors
        cpu_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cpu_count)
        
        # Run the jobs
        if mcell4:
            suffix = '4'
            res_codes = pool.map(self.run_validation_mcell4, seeds)
            self.move_output_dirs(suffix)
        else:
            suffix = '3'
            res_codes = pool.map(self.run_validation_mcell3, seeds)
            self.move_output_dirs(suffix)
    
        if os.path.exists(os.path.join(self.test_src_path, 'molecule_counts')): 
            # use observables from react_output
            counts = self.get_molecule_counts(seeds, res_codes, suffix)
        else:
            # use molecule counts
            counts = self.get_species_counts(seeds, res_codes, suffix)

    
        # unify the counts, return None on error
        if counts is not None:
            if not mcell4:
                unified_counts = self.unify_counts_with_bng_analyzer(counts, mcell4)
            else:
                unified_counts = dict(counts)
            return unified_counts
        else:
            return None
    
    
    def test(self) -> int:
        if self.should_be_skipped():
            return SKIPPED
        
        if self.is_known_fail():
            return SKIPPED
        
        self.clean_and_create_work_dir()
        
        print("Report will be printed to " + os.path.join(self.test_work_path, "validation_report.txt"))
        
        num_runs = self.tool_paths.opts.validation_runs
        seeds = self.generate_seeds(num_runs)


        mcell4_counts = self.get_molecule_counts_for_multiple_mdl_runs(True, seeds)
        if not mcell4_counts:
            print("MCell4 runs failed")
            return FAILED_MCELL
        else:
            print("MCell4 runs finished")
        mcell4_counts_per_run = { key:cnt/num_runs for key,cnt in mcell4_counts.items() }

        NO_MCELL3 = self.check_no_mcell3()
                
        if not NO_MCELL3:
            mcell3_counts = self.get_molecule_counts_for_multiple_mdl_runs(False, seeds)
            if not mcell3_counts:
                print("MCell3 runs failed")
                return FAILED_MCELL
            else:
                print("MCell3 runs finished")
            mcell3_counts_per_run = { key:cnt/num_runs for key,cnt in mcell3_counts.items() }
        else:
            mcell3_counts_per_run = {}
                                    
        tolerance = self.get_tolerance()
        
        res = self.validate_mcell_output(mcell3_counts_per_run, mcell4_counts_per_run, {}, tolerance)

        if self.is_todo_test():
            return TODO_TEST
       
        return res
