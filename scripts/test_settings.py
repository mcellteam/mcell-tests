"""
Copyright (C) 2019 by
The Salk Institute for Biological Studies and
Pittsburgh Supercomputing Center, Carnegie Mellon University

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
"""

"""
This module contains diverse constants used while testing.
"""
import os
import sys
import platform

WORK_DIR_NAME = 'work'

MAX_WIN_PATH_LENGTH = 255

TEST_MCELL4 = False

BUILD_OPTS_USE_LTO = False  # higher performnce but slower build

MAIN_MDL_FILE = 'Scene.main.mdl'
MAIN_MDLR_RULES_FILE = 'Scene.mdlr_rules.xml'

if 'Windows' in platform.system():
    EXE_EXT = '.exe'
else:
    EXE_EXT = ''
    
if 'Windows' in platform.system():
    DLL_EXT = '.pyd'
else:
    DLL_EXT = '.so'

MCELL_BINARY = 'mcell' + EXE_EXT

DATA_MODEL_TO_PYMCELL_PATH = 'bin'
DATA_MODEL_TO_PYMCELL_BINARY = 'data_model_to_pymcell' + EXE_EXT

BNG_ANALYZER_DIR = 'bin'
BNG_ANALYZER_BINARY = 'bng_analyzer' + EXE_EXT

MCELL_PATH_VARIABLE = 'MCELL_PATH'
PYMCELL_MODULE = 'pymcell.py'
PYMCELL_PATH = 'python' 
PYMCELL4_LIB = 'mcell' + DLL_EXT
PYMCELL4_DIR = 'lib'

ARG_MCELL4 = 'mcell4'
ARG_CONVERT_W_BNGL = 'convert_w_bngl'
ARG_CHECKPOINTS = 'checkpoints'

DEFAULT_PYTHON_BINARY = 'python3' + EXE_EXT
DATA_MODEL_TO_MDL_DIR = 'mdl'
DATA_MODEL_TO_MDL_SCRIPT = 'data_model_to_mdl.py'

BNG_DIR = 'bng'
BNGL_TO_DATA_MODEL_SCRIPT = 'bngl_to_data_model.py'

POSTPROCESS_MCELL3R_SCRIPT = 'postprocess_mcell3r.py'

BNG2PL_SCRIPT = 'BNG2.pl'

TEST_FILES_DIR = 'test_files'

MCELL_TIMEOUT=30*60 # in seconds
VALIDATION_TIMEOUT=4*60*60 

DEFAULT_VALIDATION_RUNS = 24

PASSED = 1
SKIPPED = 2
KNOWN_FAIL = 3
TODO_TEST = 4
IGNORED = 5

NUTMEG_UPDATED_REFERENCE = 6 # only for purpose of preparing tests

FAILED_DM_TO_MDL_CONVERSION = 10
FAILED_MCELL = 11
FAILED_DIFF = 12
FAILED_NUTMEG_SPEC = 13
FAILED_EXTERNAL = 14
FAILED_BNG2PL = 15
FAILED_VALIDATION = 16
FAILED_REF_DATA_NOT_FOUND = 16
FAILED_BNGL_TO_DM_CONVERSION = 17

RESULT_NAMES = {
 PASSED:'PASSED',
 SKIPPED:'SKIPPED',
 KNOWN_FAIL:'KNOWN_FAIL',
 TODO_TEST:'TODO_TEST',
 IGNORED:'IGNORED',
 NUTMEG_UPDATED_REFERENCE:'NUTMEG_UPDATED_REFERENCE',
 FAILED_DM_TO_MDL_CONVERSION:'FAILED_DM_TO_MDL_CONVERSION',
 FAILED_MCELL:'FAILED_MCELL',
 FAILED_DIFF:'FAILED_DIFF',
 FAILED_NUTMEG_SPEC:'FAILED_NUTMEG_SPEC',
 FAILED_EXTERNAL:'FAILED_EXTERNAL',
 FAILED_BNG2PL:'FAILED_BNG2PL',
 FAILED_VALIDATION:'FAILED_VALIDATION',
 FAILED_REF_DATA_NOT_FOUND:'FAILED_REF_DATA_NOT_FOUND',
 FAILED_BNGL_TO_DM_CONVERSION:'FAILED_BNGL_TO_DM_CONVERSION'
}

FAIL_CODES = [
    FAILED_MCELL, FAILED_DIFF, FAILED_DM_TO_MDL_CONVERSION, 
    FAILED_NUTMEG_SPEC, FAILED_EXTERNAL, FAILED_VALIDATION, 
    FAILED_REF_DATA_NOT_FOUND, FAILED_BNGL_TO_DM_CONVERSION
]

VIZ_DATA_DIR_3 = 'viz_data'
REF_VIZ_DATA_DIR_3 = 'ref_viz_data_3'
REACT_DATA_DIR_3 = 'react_data'
REF_REACT_DATA_DIR_3 = 'ref_react_data_3'

VIZ_DATA_DIR_4 = 'viz_data'
REF_VIZ_DATA_DIR_4 = 'ref_viz_data_4'
REF_VIZ_DATA_DIR_4_32 = 'ref_viz_data_4_32'
REACT_DATA_DIR_4 = 'react_data'
REF_REACT_DATA_DIR_4 = 'ref_react_data_4'
REF_REACT_DATA_DIR_4_32 = 'ref_react_data_4_32'

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

def get_ref_viz_data_dir(for_mcell4 = False, mcell4_32 = False):
    if for_mcell4:
        if mcell4_32:
            return REF_VIZ_DATA_DIR_4_32
        else:
            return REF_VIZ_DATA_DIR_4
    else:
        assert not mcell4_32
        return REF_VIZ_DATA_DIR_3
    
def get_react_data_dir(for_mcell4 = False):
    if for_mcell4:
        return REACT_DATA_DIR_4
    else:
        return REACT_DATA_DIR_3

def get_ref_react_data_dir(for_mcell4 = False, mcell4_32 = False):
    if for_mcell4:
        if mcell4_32:
            return REF_REACT_DATA_DIR_4_32
        else:
            return REF_REACT_DATA_DIR_4
    else:
        assert not mcell4_32
        return REF_REACT_DATA_DIR_3

TEST_SETTINGS_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MCELL_TOOLS_DIR = os.path.realpath(os.path.join(TEST_SETTINGS_BASE_DIR, '..', '..', 'mcell_tools'))
sys.path.append(os.path.join(MCELL_TOOLS_DIR, 'scripts'))

from build_settings import \
    REPO_NAME_MCELL, REPO_NAME_CELLBLENDER, \
    WORK_DIR_NAME, \
    BUILD_DIR_MCELL, BUILD_DIR_CELLBLENDER
