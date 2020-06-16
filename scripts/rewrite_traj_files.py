""" Script for re-writing trajectory files in the file system
"""
import itertools
from autofile import fs

SAVE_PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def write_sorted_trajectory_file(fs_):
    """ sort trajectory file according to energies
    """
    locs_lst = fs_[-1].existing()
    if locs_lst:
        enes = [fs_[-1].file.energy.read(locs)
                for locs in locs_lst]
        geos = [fs_[-1].file.geometry.read(locs)
                for locs in locs_lst]
        traj = []
        traj_sort_data = sorted(zip(enes, geos, locs_lst), key=lambda x: x[0])
        for ene, geo, locs in traj_sort_data:
            comment = 'energy: {0:>15.10f} \t {1}'.format(ene, locs[0])
            traj.append((comment, geo))
        traj_path = fs_[0].file.trajectory.path()
        print("Updating trajectory file at {}".format(traj_path))
        fs_[0].file.trajectory.write(traj)


def write_trajectory_file(fs_):
    """ sort trajectory file according to energies
    """
    locs_lst = fs_[-1].existing()
    if locs_lst:
        geos = [fs_[-1].file.geometry.read(locs)
                for locs in locs_lst]

        traj = []
        for geo, locs in zip(geos, locs_lst):
            comment = '{}'.format(locs[0])
            traj.append((comment, geo))

        traj_path = fs_[0].file.trajectory.path()
        print("Updating trajectory file at {}".format(traj_path))
        fs_[0].file.trajectory.write(traj)


# First, write them in the CONFORMER layer
for cnf_fs in itertools.chain(
        fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY'], 'CONFORMER'),
        fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY',
                                       'TRANSITION STATE'], 'CONFORMER')):

    write_sorted_trajectory_file(cnf_fs)


# Then write them in the SYMMETRY layer
for sym_fs in itertools.chain(
        fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY', 'CONFORMER'],
                            'SYMMETRY'),
        fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY',
                                       'TRANSITION STATE', 'CONFORMER'],
                            'SYMMETRY')):

    write_trajectory_file(sym_fs)
