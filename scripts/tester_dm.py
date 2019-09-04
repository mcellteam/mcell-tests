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
from test_utils import ToolPaths, report_test_error, report_test_success, replace_in_file

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(THIS_DIR, '..', 'mcell_tools', 'scripts'))
from utils import run, log, fatal_error

UPDATE_REFERENCE = False

MCELL_ARGS = ['-seed', '1']
SEED_DIR = 'seed_00001'


class TesterDm(TesterBase):
    def __init___(self, test_dir: str, tool_paths: ToolPaths):
        super(TesterMdl, self).__init__(test_dir, tool_paths)
    
    
    def check_prerequisites(self): 
        if not os.path.exists(self.tool_paths.mcell_binary):
            fatal_error("Could not find executable '" + self.tool_paths.mcell_binary + ".")
            
        if not os.path.exists(self.tool_paths.data_model_to_mdl_script):
            fatal_error("Could not find data model conversion script '" + self.tool_paths.data_model_to_mdl_script + ".")
        
         
    def run_dm_to_mdl_conversion(self):
        # the conversion python script is considered a separate utility, 
        # we run it through bash 
        cmd = [ 
            PYTHON_BINARY, self.tool_paths.data_model_to_mdl_script, 
            os.path.join(self.test_set_dir, self.test_name, self.test_name + '.json'), MAIN_MDL_FILE ]
        log_name = self.test_name+'.dm_to_mdl.log'
        exit_code = run(cmd, cwd=os.getcwd(), verbose=False, fout_name=log_name)
        if exit_code != 0:
            report_test_error(self.test_name, "JSON to mdl conversion failed, see '" + os.path.join(self.test_name, log_name) + "'.")
            return FAILED_DM_TO_MDL_CONVERSION
        else:
            return PASSED
        
        
    def change_viz_output_to_ascii(self):
        fname = os.path.join(self.test_work_dir, 'Scene.viz_output.mdl')
        replace_in_file(fname, 'CELLBLENDER', 'ASCII')
        return PASSED
            

    def update_reference(self):
        viz_reference = os.path.join(self.test_dir, REF_VIZ_DATA_DIR, SEED_DIR)
        viz_res = os.path.join(self.test_work_dir, VIZ_DATA_DIR, SEED_DIR)

        if os.path.exists(viz_res):
            # remove whole directory
            if os.path.exists(viz_reference):
                log("Cleaning old data in " + viz_reference)
                shutil.rmtree(viz_reference)
                
            # copy the first and the last viz data file
            log("New reference from " + viz_res)
            files = os.listdir(viz_res)
            if not files:
                fatal_error("There are no reference data in " + viz_res)
                  
            files.sort()
    
            log("Updating reference " + viz_reference + " with data from " + viz_res)
            log("  File 1:" + files[0])
            log("  File 1:" + files[-1])
            
            if not os.path.exists(viz_reference):
                os.makedirs(viz_reference)
            shutil.copyfile(os.path.join(viz_res, files[0]), os.path.join(viz_reference, files[0]))
            shutil.copyfile(os.path.join(viz_res, files[-1]), os.path.join(viz_reference, files[-1]))
            
        # copy the whole react data files 
        react_reference = os.path.join(self.test_dir, REF_REACT_DATA_DIR, SEED_DIR)
        react_res = os.path.join(self.test_work_dir, REACT_DATA_DIR, SEED_DIR)
        
        if os.path.exists(react_res):
            # remove whole directory
            if os.path.exists(react_reference):
                log("Cleaning old data in " + react_reference)
                shutil.rmtree(react_reference)
    
            # and update all files
            log("Updating reference " + react_reference + " with data from " + react_res)
            shutil.copytree(react_res, react_reference)

        # copy the whole dyn_geom data files 
        dyn_geom_reference = os.path.join(self.test_dir, REF_DYN_GEOM_DATA_DIR)
        dyn_geom_res = os.path.join(self.test_work_dir, DYN_GEOM_DATA_DIR)
        
        if os.path.exists(dyn_geom_res):
            # remove whole directory
            if os.path.exists(dyn_geom_reference):
                log("Cleaning old data in " + dyn_geom_reference)
                shutil.rmtree(dyn_geom_reference)
    
            # and use every 100th file
            files = os.listdir(dyn_geom_res)
            if not files:
                fatal_error("There are no reference data in " + dyn_geom_res)
            files.sort()   
            
            if not os.path.exists(dyn_geom_reference):
                os.makedirs(dyn_geom_reference)
                
            log("Updating reference " + dyn_geom_reference + " with data from " + dyn_geom_res)
            for i in range(0, len(files), 50):
                log("Updating reference file '" + files[i] + '"')
                shutil.copyfile(os.path.join(dyn_geom_res, files[i]), os.path.join(dyn_geom_reference, files[i]))

        # and also check the .gdat files generated with mcellr mode
        mcellr_gdat_reference = os.path.join(self.test_dir, REF_MCELLR_GDAT_DATA_DIR)
        mcellr_gdat_res = os.path.join(self.test_work_dir, MCELLR_GDAT_DATA_DIR)
        
        print("PATH:" + mcellr_gdat_res)
        gdat_files = os.listdir(mcellr_gdat_res) 
        print("F1:" + str(gdat_files))
        gdat_files = [ f for f in gdat_files if f.endswith('.gdat')]
        print("F2:" + str(gdat_files))
        if gdat_files:
            # remove whole directory
            if os.path.exists(mcellr_gdat_reference):
                log("Cleaning old data in " + mcellr_gdat_reference)
                shutil.rmtree(mcellr_gdat_reference)
                
            log("Updating reference .gdat files " + mcellr_gdat_reference + " with data from " + mcellr_gdat_res)
            if not os.path.exists(mcellr_gdat_reference):
                os.makedirs(mcellr_gdat_reference)
            for f in gdat_files:
                log("Updating reference file '" + f + "'")
                shutil.copyfile(os.path.join(mcellr_gdat_res, f), os.path.join(mcellr_gdat_reference, f))
                 

    def test(self):
        self.check_prerequisites()

        if self.should_be_skipped():
            return SKIPPED

        self.clean_and_create_work_dir()
        
        res = self.run_dm_to_mdl_conversion()
        if res != PASSED:
            return res
        
        res = self.change_viz_output_to_ascii()
        if res != PASSED:
            return res
         
        res = self.run_mcell(MCELL_ARGS, os.path.join(self.test_work_dir, MAIN_MDL_FILE))
    
        if not UPDATE_REFERENCE:
            res = self.check_reference_data(SEED_DIR)
        else:
            if res != PASSED:
                fatal_error("Tried to update reference data but mcell execution failed!")
                
            self.update_reference()
        
        return res