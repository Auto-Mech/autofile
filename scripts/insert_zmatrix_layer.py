""" Script for inserting the z-matrix layer into the filesystem
"""
import os
import shutil
import itertools
import automol
from autofile import fs


RUN_PFX = '/lcrc/project/PACC/AutoMech/data/run/'
SAVE_PFX = '/lcrc/project/PACC/AutoMech/data/save/'

# # First, move the scan file systems over
#
# for path in itertools.chain(
#         fs.iterate_paths(RUN_PFX, ['REACTION', 'THEORY']),
#         fs.iterate_paths(SAVE_PFX, ['REACTION', 'THEORY'])):
#         # fs.iterate_paths(RUN_PFX, ['SPECIES', 'THEORY', 'CONFORMER']),
#         # fs.iterate_paths(RUN_PFX, ['REACTION', 'THEORY',
#         #                            'TRANSITION STATE', 'CONFORMER']),
#         # fs.iterate_paths(SAVE_PFX, ['SPECIES', 'THEORY', 'CONFORMER']),
#         # fs.iterate_paths(SAVE_PFX, ['REACTION', 'THEORY',
#         #                             'TRANSITION STATE', 'CONFORMER'])):
#
#     zma_fs = fs.manager(path, 'ZMATRIX')
#     zma_fs[-1].create([0])
#
#     zma_path = zma_fs[-1].path([0])
#
#     scan_fs = fs.manager(path, 'SCAN')
#     cscan_fs = fs.manager(path, 'CSCAN')
#
#     if scan_fs[0].exists():
#         scan_path = scan_fs[0].path()
#
#         new_path = os.path.join(zma_path, 'SCANS')
#         if os.path.exists(new_path):
#             shutil.rmtree(new_path)
#
#         new_path = shutil.move(scan_path, zma_path)
#         print(new_path)
#
#     if cscan_fs[0].exists():
#         cscan_path = cscan_fs[0].path()
#
#         new_path = os.path.join(zma_path, 'CSCANS')
#         if os.path.exists(new_path):
#             shutil.rmtree(new_path)
#
#         new_path = shutil.move(cscan_path, zma_path)
#         print(new_path)


# # Now, move the .zmat files from the CONFORMER layer into the ZMATRIX layer
# for cnf_fs in itertools.chain(
#         fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY'], 'CONFORMER'),
#         fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY',
#                                        'TRANSITION STATE'], 'CONFORMER')):
#
#     for cnf_locs in cnf_fs[-1].existing():
#         cnf_path = cnf_fs[-1].path(cnf_locs)
#         print(cnf_path)
#
#         zma_df = cnf_fs[-1].file.zmatrix
#
#         if zma_df.exists(cnf_locs):
#             zma = zma_df.read(cnf_locs)
#
#             zma_fs = fs.manager(cnf_path, 'ZMATRIX')
#
#             zma_fs[-1].file.zmatrix.write(zma, [0])
#
#             zma_path = zma_fs[-1].path([0])
#
#             # # Now that we've written the z-matrix to the new location, we can
#             # # remove the old one
#             # zma_df.removable = True
#             # zma_df.remove(cnf_locs)


# Lastly, write the zmatrix files for the z-matrix guess
for zma_fs in itertools.chain(
        fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY'], 'ZMATRIX')):
    path = zma_fs[-1].path([0])
    print(path)

    scan_fs = fs.manager(path, 'SCAN')

    scan_locs_lst = sorted(scan_fs[-1].existing())

    if scan_locs_lst:
        scan_locs = scan_locs_lst[0]
        scan_path = scan_fs[-1].path(scan_locs)
        print(scan_locs)

        zma = scan_fs[-1].file.zmatrix.read(scan_locs)

        zma_fs[-1].file.zmatrix.write(zma, [0])
        print('zmatrix written!')

    print()
