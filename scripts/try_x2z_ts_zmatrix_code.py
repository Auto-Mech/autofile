""" Script for cycling through reactions and testing Yuri's z-matrix code on
them
"""
import automol
from autofile import fs

TMP_PFX = './TMP/'


# for rct_ichs, prd_ichs in [[['InChI=1S/C2H3O/c1-2-3/h1-3H'],
#                             ['InChI=1S/C2H2O/c1-2-3/h1,3H', 'InChI=1S/H']]]:

for rxn_locs, in fs.iterate_locators(TMP_PFX, ['REACTION']):
    (rct_ichs, prd_ichs), _, _, _ = rxn_locs

    rct_geos = list(map(automol.inchi.geometry, rct_ichs))
    prd_geos = list(map(automol.inchi.geometry, prd_ichs))

    rct_gras = list(map(automol.geom.graph, rct_geos))
    prd_gras = list(map(automol.geom.graph, prd_geos))

    rct_gras = list(map(automol.graph.without_stereo_parities, rct_gras))
    prd_gras = list(map(automol.graph.without_stereo_parities, prd_gras))

    rct_gras, _ = automol.graph.standard_keys_for_sequence(rct_gras)
    prd_gras, _ = automol.graph.standard_keys_for_sequence(prd_gras)

    tras, rct_idxs, _, rxn_type = (
        automol.graph.reac.classify(rct_gras, prd_gras))

    # Now, re-sort the reactants according to what the classifier tells us
    rct_geos = list(map(rct_geos.__getitem__, rct_idxs))
    rct_zmas = list(map(automol.geom.zmatrix, rct_geos))
    rct_gras = list(map(rct_gras.__getitem__, rct_idxs))

    # Re-label the graph and the transformation in the new sort order
    rct_gras, rct_atm_key_dcts = (
        automol.graph.standard_keys_for_sequence(rct_gras))

    rct_atm_key_dct = automol.dict_.merge_sequence(rct_atm_key_dcts)

    tras = [automol.graph.trans.relabel(tra, rct_atm_key_dct) for tra in tras]

    assert rxn_type is not None

    rct_gra = automol.graph.union_from_sequence(rct_gras)
    prd_gra = automol.graph.union_from_sequence(prd_gras)
    for tra in tras:
        iso = automol.graph.full_isomorphism(
            automol.graph.trans.apply(tra, rct_gra), prd_gra)
        assert iso

        frm_bnd_keys = automol.graph.trans.formed_bond_keys(tra)

        if len(rct_gras) == 2:
            print(rct_ichs, prd_ichs)
            print(rxn_type)
            print(iso)

            assert len(frm_bnd_keys) <= 1, (
                "For now, this is restricted to one formed bond.")

            frm_bnd_key, = frm_bnd_keys
            print(frm_bnd_key)
