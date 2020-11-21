import sys
import os

MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

s1 = m.Subsystem()
s1.load_bngl_molecule_types_and_reaction_rules('test1.bngl')

s2 = m.Subsystem()
s2.load_bngl_molecule_types_and_reaction_rules('test2.bngl')

assert len(s1.reaction_rules) == 1
assert len(s2.reaction_rules) == 1

assert s1.reaction_rules[0] == s2.reaction_rules[0]
