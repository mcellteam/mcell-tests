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
This module contains diverse constants used while testing.
"""
import os
import sys
import platform

WORK_DIR_NAME = 'work'

TEST_MCELL4 = False

BUILD_OPTS_USE_LTO = False  # higher performnce but slower build

MAIN_MDL_FILE = 'Scene.main.mdl'
MAIN_MDLR_RULES_FILE = 'Scene.mdlr_rules.xml'

if 'Windows' in platform.system():
    EXE_EXT = '.exe'
else:
    EXE_EXT = ''
    
if 'Windows' in platform.system():
    DLL_EXT = '.dll'
elif 'Darwin' == platform.system():
    DLL_EXT = '.so' # mcell.so is used on MacOS as well, python does not find it otherwise
else:
    DLL_EXT = '.so'

MCELL_BINARY = 'mcell' + EXE_EXT

DATA_MODEL_TO_PYMCELL_DIR = os.path.join('utils', 'data_model_to_pymcell')
DATA_MODEL_TO_PYMCELL_BINARY = 'data_model_to_pymcell' + EXE_EXT

MCELL_DIR_VARIABLE = 'MCELL_DIR'
PYMCELL_MODULE = 'pymcell.py'
PYMCELL_DIR = 'python' 
PYMCELL4_LIB = 'mcell' + DLL_EXT
PYMCELL4_DIR = 'lib'


DEFAULT_PYTHON_BINARY = 'python3' + EXE_EXT
DATA_MODEL_TO_MDL_DIR = 'mdl'
DATA_MODEL_TO_MDL_SCRIPT = 'data_model_to_mdl.py'

BNG_DIR = 'bng'
BNGL_TO_DATA_MODEL_SCRIPT = 'bngl_to_data_model.py'

BNG2PL_SCRIPT = 'BNG2.pl'

TEST_FILES_DIR = 'test_files'

MCELL_TIMEOUT=1500 # 20 min

DEFAULT_VALIDATION_RUNS = 24

PASSED = 1
SKIPPED = 2
KNOWN_FAIL = 3
TODO_TEST = 4

NUTMEG_UPDATED_REFERENCE = 5 # only for purpose of preparing tests

FAILED_DM_TO_MDL_CONVERSION = 10
FAILED_MCELL = 11
FAILED_DIFF = 12
FAILED_NUTMEG_SPEC = 13
FAILED_EXTERNAL = 14
FAILED_BNG2PL = 15
FAILED_VALIDATION = 16

RESULT_NAMES = {
 PASSED:'PASSED',
 SKIPPED:'SKIPPED',
 KNOWN_FAIL:'KNOWN_FAIL',
 TODO_TEST:'TODO_TEST',
 NUTMEG_UPDATED_REFERENCE:'NUTMEG_UPDATED_REFERENCE',
 FAILED_DM_TO_MDL_CONVERSION:'FAILED_DM_TO_MDL_CONVERSION',
 FAILED_MCELL:'FAILED_MCELL',
 FAILED_DIFF:'FAILED_DIFF',
 FAILED_NUTMEG_SPEC:'FAILED_NUTMEG_SPEC',
 FAILED_EXTERNAL:'FAILED_EXTERNAL',
 FAILED_BNG2PL:'FAILED_BNG2PL',
 FAILED_VALIDATION:'FAILED_VALIDATION'
}

FAIL_CODES = [
    FAILED_MCELL, FAILED_DIFF, FAILED_DM_TO_MDL_CONVERSION, 
    FAILED_NUTMEG_SPEC, FAILED_EXTERNAL, FAILED_VALIDATION
]

VIZ_DATA_DIR_3 = 'viz_data'
REF_VIZ_DATA_DIR_3 = 'ref_viz_data_3'
REACT_DATA_DIR_3 = 'react_data'
REF_REACT_DATA_DIR_3 = 'ref_react_data_3'

VIZ_DATA_DIR_4 = 'viz_data'
REF_VIZ_DATA_DIR_4 = 'ref_viz_data_4'
REACT_DATA_DIR_4 = 'react_data'
REF_REACT_DATA_DIR_4 = 'ref_react_data_4'

# not used by mcell4 testing yet
DYN_GEOM_DATA_DIR = 'dynamic_geometry'
REF_DYN_GEOM_DATA_DIR = 'ref_dynamic_geometry_3'
MCELLR_GDAT_DATA_DIR = '.'
REF_MCELLR_GDAT_DATA_DIR = 'ref_mcellr_gdat_3'
REF_NUTMEG_DATA_DIR = 'ref_data_3'
    

def get_viz_data_dir(for_mcell4 = False):
    if for_mcell4:
        return VIZ_DATA_DIR_4
    else:
        return VIZ_DATA_DIR_3

def get_ref_viz_data_dir(for_mcell4 = False):
    if for_mcell4:
        return REF_VIZ_DATA_DIR_4
    else:
        return REF_VIZ_DATA_DIR_3
    
def get_react_data_dir(for_mcell4 = False):
    if for_mcell4:
        return REACT_DATA_DIR_4
    else:
        return REACT_DATA_DIR_3

def get_ref_react_data_dir(for_mcell4 = False):
    if for_mcell4:
        return REF_REACT_DATA_DIR_4
    else:
        return REF_REACT_DATA_DIR_3

TEST_SETTINGS_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MCELL_TOOLS_DIR = os.path.realpath(os.path.join(TEST_SETTINGS_BASE_DIR, '..', '..', 'mcell_tools'))
sys.path.append(os.path.join(MCELL_TOOLS_DIR, 'scripts'))

from build_settings import \
    REPO_NAME_MCELL, REPO_NAME_CELLBLENDER, \
    WORK_DIR_NAME, \
    BUILD_DIR_MCELL, BUILD_DIR_CELLBLENDER
