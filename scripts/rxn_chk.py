""" Some examples of how to use the new autofile.fs functions
"""

from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'
ZMA_MANAGERS = fs.iterate_managers(
    PFX,
    ['REACTION', 'THEORY', 'TRANSITION STATE', 'CONFORMER'],
    'ZMATRIX'
)


def check_rct_gra():
    """  Check zma for trans files
    """

    no_zma_paths = []
    no_gra_paths = []
    for zma_fs in ZMA_MANAGERS:
        zma_path = zma_fs[-1].path([0])
        if zma_fs is not None:
            if not zma_fs[-1].file.reactant_graph.exists([0]):
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
    check_rct_gra()
