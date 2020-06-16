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
import os
import itertools
import automol
from autofile import fs

SAVE_PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def equivalent_geometry_and_energy(geo_ene1, geo_ene2):
    """ Based on their coulomb spectrum and energy, are these two structures
        equivalent?
    """
    etol = 2e-5
    rtol = 1e-2

    geo1, ene1 = geo_ene1
    geo2, ene2 = geo_ene2

    return (abs(ene1 - ene2) < etol and
            automol.geom.almost_equal_coulomb_spectrum(geo1, geo2, rtol=rtol))


def equivalence_class_indices(iterable, eq_):
    """ Determine indices for the equivalence classes in this list
    """
    rep_lst = []
    idxs_lst = []
    for idx, item in enumerate(iterable):
        is_in_a_class = False

        for rep, idxs in zip(rep_lst, idxs_lst):
            if eq_(item, rep):
                idxs.append(idx)
                is_in_a_class = True
                break

        if not is_in_a_class:
            rep_lst.append(item)
            idxs_lst.append([idx])

    return idxs_lst


def conformer_rep_selector(_cnf_fs):
    """ Returns a function to select a conformer representative
    (Selected based on the total number of items in the directory)
    """

    def _select(_locs_lst):
        func = lambda locs: len(os.listdir(_cnf_fs[-1].path(locs)))
        return max(_locs_lst, key=func)

    return _select


for cnf_fs in itertools.chain(
        fs.iterate_managers(SAVE_PFX, ['SPECIES', 'THEORY'], 'CONFORMER'),
        fs.iterate_managers(SAVE_PFX, ['REACTION', 'THEORY',
                                       'TRANSITION STATE'], 'CONFORMER')):

    print(cnf_fs[0].path())

    locs_lst = cnf_fs[-1].existing()

    geos = [cnf_fs[-1].file.geometry.read(locs) for locs in locs_lst]
    enes = [cnf_fs[-1].file.energy.read(locs) for locs in locs_lst]
    geo_ene_lst = list(zip(geos, enes))

    cls_idxs_lst = (
        equivalence_class_indices(geo_ene_lst, equivalent_geometry_and_energy))

    cls_locs_lsts = [
        list(map(locs_lst.__getitem__, cls_idxs)) for cls_idxs in cls_idxs_lst]

    rep_locs_lst = list(map(conformer_rep_selector(cnf_fs), cls_locs_lsts))

    for rep_locs, cls_locs_lst in zip(rep_locs_lst, cls_locs_lsts):
        rep_path = cnf_fs[-1].path(rep_locs)
        print(rep_path)

        sym_fs = fs.manager(rep_path, 'SYMMETRY')
        print(sym_fs[0].path())

        for locs in cls_locs_lst:
            print(locs)
            geo = cnf_fs[-1].file.geometry.read(locs)

            sym_fs[-1].create(locs)
            sym_fs[-1].file.geometry.write(geo, locs)

            # WARNING!! THIS PART IS REMOVING STUFF!!
            # (Removes conformer directories that are now redundant)
            if locs != rep_locs:
                print('removing ...')
                cnf_fs[-1].removable = True
                cnf_fs[-1].remove(locs)

    print()
