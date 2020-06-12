""" Script for inserting the symmetric-conformer layer into the filesystem

Goal:
    1. Partition each set of conformers into equivalence classes of
       symmetrically equivalent conformers.
    2. Pick one conformer (the one with the largest number of files and
       subdirectories) as class representative.
    3. Store the geometries for the other conformers in the class under the
       symmetric-conformer layer inside the class representative's conformer
       directory.
"""
import itertools
from autofile import fs

SAVE_PFX = '/lcrc/project/PACC/AutoMech/data/save/'


for cnf_fs in itertools.chain(
        fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY'], 'CONFORMER')):

    path = cnf_fs[0].path()
    print(path)

    cnf_locs_lst = cnf_fs[-1].existing()
    print(cnf_locs_lst)
