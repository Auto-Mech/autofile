""" Some examples of how to use the new autofile.fs functions
"""

import os
from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def clean_theory():
    """ Add the zma input files using geo inputs
    """
    thy_managers = fs.iterate_managers(PFX, ['SPECIES'], 'THEORY')
    # cnf_managers = fs.iterate_managers(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE'],
    #                                          'CONFORMER')
    for thy_fs in thy_managers:
        if thy_fs is not None:
            thy_path = thy_fs[0].path()
            print('thy_path', thy_path)
            thy_dirs = os.listdir(thy_path)
            print('dirs', thy_dirs)


def add_tors_names():
    """ Add the zma input files using geo inputs
    """
    cnf_managers = fs.iterate_managers(PFX, ['SPECIES', 'THEORY'],
                                             'CONFORMER')
    # cnf_managers = fs.iterate_managers(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE'],
    #                                          'CONFORMER')
    for cnf_fs in cnf_managers:
        if cnf_fs is not None:

            # Read nsampd and tors range from the info file
            if cnf_fs[0].file.info.exists():
                inf_obj = cnf_fs[0].file.info.read()
                nsampd = inf_obj.nsamp
                tors_ranges = dict(inf_obj.tors_ranges)

                cnf_path = cnf_fs[0].path()
                print('cnf_path', cnf_path)
                print('nsampd', nsampd)
                print('tors', tors_ranges)

            # # Loop over all the Z-Matrices and add the torsional ranges
            # for locs in cnf_fs[-1].existing():
            #     # Set up the ZMA filesys
            #     cnf_path = cnf_fs[-1].path(locs)
            #     zma_fs = fs.manager(cnf_path, 'ZMATRIX')

            #     # Read the frm, brk keys from the transformation file
            #     tra = zma_fs[-1].file.transformation.read([0])

            #     # Write the transformation file with the keys and class
            #     # Determine the reaction class
            #     zma_fs[-1].file.transformation.write(trans)

            #     # Write the tors names
            #     zma_fs[-1].file.torsional_names.write(tors_ranges, [0])


if __name__ == '__main__':
    # clean_theory()
    add_tors_names()
