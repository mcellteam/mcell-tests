import os
import sys
import shutil


def update_dir(work_data_dir, test_data_dir):
    files = os.listdir(test_data_dir)
    for fname in files:
        print("  - updating " + fname)
        shutil.copy(os.path.join(work_data_dir, fname), os.path.join(test_data_dir, fname))

def update_ref_data(work_dir, test_dir):
    print("Updating MCell3 ref data in " + test_dir + " using data from " + work_dir)

    work_viz_seed = os.path.join(work_dir, 'viz_data', 'seed_00001');
    test_viz_seed = os.path.join(test_dir, 'ref_viz_data_3', 'seed_00001');

    work_react_seed = os.path.join(work_dir, 'react_data', 'seed_00001');
    test_react_seed = os.path.join(test_dir, 'ref_react_data_3', 'seed_00001');

    work_gdat = work_dir
    test_gdat = os.path.join(test_dir, 'ref_mcellr_gdat_3');
    
    update_dir(work_viz_seed, test_viz_seed)
    
    if (os.path.exists(test_react_seed)):
        update_dir(work_react_seed, test_react_seed)

    if (os.path.exists(test_gdat)):
        update_dir(work_gdat, test_gdat)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Expecting work directory and test directory")
        sys.exit(1)
    
    update_ref_data(sys.argv[1], sys.argv[2])
