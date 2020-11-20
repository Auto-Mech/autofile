""" A script to wipe out all cscan directories
"""
import itertools
from autofile import fs

RUN_PFX = '/lcrc/project/PACC/AutoMech/data/run/'
SAVE_PFX = '/lcrc/project/PACC/AutoMech/data/save/'

for sca_fs in itertools.chain(
        fs.iterate_managers(RUN_PFX, ['SPECIES', 'THEORY', 'CONFORMER',
                                      'ZMATRIX'], 'CSCAN'),
        fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY', 'CONFORMER',
                                       'ZMATRIX'], 'CSCAN'),
        fs.iterate_managers(RUN_PFX, ['REACTION', 'THEORY', 'TRANSITION STATE',
                                      'CONFORMER', 'ZMATRIX'], 'CSCAN'),
        fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY', 'TRANSITION STATE',
                                       'CONFORMER', 'ZMATRIX'], 'CSCAN')):
    if sca_fs[0].exists():
        print(sca_fs[0].path())
        sca_fs[0].removable = True
        sca_fs[0].remove()
        print('removing...')
