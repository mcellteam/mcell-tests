# WARNING: This is an automatically generated file and will be overwritten
#          by CellBlender on the next model export.

import os
import shared
import mcell as m

from parameters import *

# ---- subsystem ----

MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

vm = m.Species(
    name = 'vm',
    diffusion_constant_3d = 5.00000000000000024e-05
)


# ---- create subsystem object and add components ----

subsystem = m.Subsystem()
subsystem.add_species(vm)
