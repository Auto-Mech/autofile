""" Some examples of how to use the new autofile.fs functions
"""
import automol
from autofile import fs

PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def example1():
    """
    Example 1: Get the path to a specific part of the file system

    """

    path = fs.path(PFX, [('SPECIES', ['InChI=1S/HO2/c1-2/h1H', 0, 2]),
                         ('THEORY', ['wb97xd', '6-31g*', 'U']),
                         ('CONFORMER', ['cel7a4s_k6Ay5'])])
    print(path)


def example2():
    """
    Example 2: Get the manager for a specific part of the file system

    """

    cnf_fs = fs.manager(path, [('SPECIES', ['InChI=1S/HO2/c1-2/h1H', 0, 2]),
                               ('THEORY', ['wb97xd', '6-31g*', 'U'])])
                        'CONFORMER')

    # Read out the z-matrix for this conformer and print it
    zma = cnf_fs[-1].file.zmatrix.read(['cel7a4s_k6Ay5'])
    print(automol.zmatrix.string(zma))


def example3():
    """
    Example 3: Iterate over all SPECIES/THEORY/CONFORMER paths

    """

    for path in fs.iterate_paths(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE',
                                       'CONFORMER']):
        print(path)


def example4():
    """
    Example 4: Iterate over locs for all SPECIES/THEORY/CONFORMER paths

    """

    for locs_lst in fs.iterate_locators(
            PFX, ['SPECIES', 'THEORY', 'CONFORMER']):
        print(locs_lst)


def example5():
    """
    Example 5: Iterate over CONFORMER managers under SPECIES/THEORY paths

    """

    for cnf_fs in fs.iterate_managers(PFX, ['SPECIES', 'THEORY'], 'CONFORMER'):

        print(cnf_fs[0].path())

        # If it has an energy file, print the value
        for locs in cnf_fs[-1].existing():
            path = cnf_fs[-1].path(locs)
            print(path)
            # ene = cnf_fs[-1].file.energy.read(locs)
            # print(ene)

        print()


def example6():
    """
    Example 6: Iterate over CSCANS managers
    """

    for scn_fs in fs.iterate_managers(
            PFX,
            ['REACTION', 'THEORY', 'TRANSITION STATE', 'CONFORMER', 'ZMATRIX'],
            'CSCAN'):
        if scn_fs[0].exists():
            print(scn_fs[0].path())

            # Note that the following loops all do the same thing

            # Combined loop over scan coordinates, coordinate values, and
            # constraints
            for locs in scn_fs[-1].existing():
                print(locs)

            print()

            # Loop over all directories for a given set of scan coordinates
            for root_locs in scn_fs[1].existing():
                print('root: {}'.format(root_locs))
                for locs in scn_fs[3].existing(root_locs):
                    print(locs)

            print()

            # Loop over all directories for a given set of scan coordinates and
            # values
            for root_locs in scn_fs[2].existing():
                print('root: {}'.format(root_locs))
                for locs in scn_fs[3].existing(root_locs):
                    print(locs)

            print()

            # Completely split out the loop
            for root_locs1 in scn_fs[1].existing():
                print('root1: {}'.format(root_locs1))
                for root_locs2 in scn_fs[2].existing(root_locs1):
                    print('root2: {}'.format(root_locs2))
                    for locs in scn_fs[3].existing(root_locs2):
                        print(locs)
            print()

# example1()
# example2()
# example3()
# example4()
# example5()
# example6()
