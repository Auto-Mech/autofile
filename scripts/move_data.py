""" Rearrange files in the file system according to a new schema
"""
from autofile import fs

# Let's test things on the RUN file system, in case something goes wrong
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

    path = fs.path(PFX, [('SPECIES', ['InChI=1S/HO2/c1-2/h1H', 0, 2]),
                         ('THEORY', ['wb97xd', '6-31g*', 'U'])])
    cnf_fs = fs.manager(path, 'CONFORMER')

    # Print the trunk path
    print(cnf_fs[0].path())

    # Print one of the leaf paths
    print(cnf_fs[-1].path(['cel7a4s_k6Ay5']))


def example3():
    """
    Example 3: Iterate over all SPECIES/THEORY/CONFORMER paths

    """

    for path in fs.iterate_paths(PFX, keys=['SPECIES', 'THEORY', 'CONFORMER']):
        print(path)


def example4():
    """
    Example 4: Iterate over specs for all SPECIES/THEORY/CONFORMER paths

    """

    for specs_lst in fs.iterate_specifiers(
            PFX, keys=['SPECIES', 'THEORY', 'CONFORMER']):
        print(specs_lst)


def example5():
    """
    Example 5: Get the manager for a specific part of the file system

    """


# example1()
example2()
# example3()
