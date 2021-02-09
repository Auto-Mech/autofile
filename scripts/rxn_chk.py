""" Some examples of how to use the new autofile.fs functions
"""

import os
from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'
# RXN_MANAGERS = fs.manager(
#     PFX, [], 'REACTION')
ZMA_MANAGERS = fs.iterate_managers(
    PFX,
    ['REACTION', 'THEORY', 'TRANSITION STATE', 'CONFORMER'],
    'ZMATRIX'
)


def new_check_rct_gra():
    """  Check zma for trans files
    """

    for _fs in RXN_MANAGERS:
        print(_fs)


def check_rct_gra():
    """  Check zma for trans files
    """

    no_zma_paths = []
    no_gra_paths = []
    for zma_fs in ZMA_MANAGERS:
        if zma_fs is not None:
            zma_path = zma_fs[-1].path([0])
            rct_gra_path = os.path.join(zma_path, 'zmat.g.yaml')
            if not os.path.exists(rct_gra_path):
                no_gra_paths.append(zma_path)
        else:
            no_zma_paths.append(zma_path)

    print('No ZMAs:')
    for path in no_zma_paths:
        print(path)
    print('\n\n\nNo GRAs:')
    for path in no_gra_paths:
        print(path)


if __name__ == '__main__':
    # new_check_rct_gra()
    check_rct_gra()
