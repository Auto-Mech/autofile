""" Some examples of how to use the new autofile.fs functions
"""
import automol
from autofile import fs

PFX = '/lcrc/project/PACC/AutoMech/data/run/'


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

    path = fs.path(PFX, [('SPECIES', ['InChI=1S/HO2/c1-2/h1H', 0, 2]),
                         ('THEORY', ['wb97xd', '6-31g*', 'U'])])

    cnf_fs = fs.manager(path, 'CONFORMER')

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
            ene = cnf_fs[-1].file.energy.read(locs)
            print(ene)

        print()


# example1()
# example2()
example3()
# example4()
# example5()
