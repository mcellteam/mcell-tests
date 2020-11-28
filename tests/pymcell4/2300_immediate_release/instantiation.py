import mcell as m

from parameters import *
from subsystem import *
from geometry import *

# ---- instantiation ----

# ---- release sites ----

if REF_RUN:
    rel_a = m.ReleaseSite(
        name = 'rel_a',
        complex = a.inst(),
        shape = m.Shape.SPHERICAL,
        location = m.Vec3(0, 0, 0),
        site_diameter = 0,
        number_to_release = 9
    )

# ---- surface classes assignment ----


# ---- compartments assignment ----

# ---- instantiation data ----

instantiation = m.InstantiationData()
instantiation.add_geometry_object(Cube)
if REF_RUN:
    instantiation.add_release_site(rel_a)