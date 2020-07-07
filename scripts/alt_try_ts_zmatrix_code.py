""" Script for cycling through reactions and testing Yuri's z-matrix code on
them
"""
import automol
from autofile import fs

# PFX = './TMP/'
PFX = '/lcrc/project/PACC/AutoMech/data/save/'

rxn_fs = fs.manager(PFX, 'REACTION')

for rxn_locs, in fs.iterate_locators(PFX, ['REACTION']):
    (rct_ichs, prd_ichs), _, _, _ = rxn_locs

    rct_gras = list(map(automol.inchi.graph, rct_ichs))
    prd_gras = list(map(automol.inchi.graph, prd_ichs))

    rct_gras = list(map(automol.graph.explicit, rct_gras))
    prd_gras = list(map(automol.graph.explicit, prd_gras))

    # Get one z-matrix for this reaction, if there is one
    rxn_path = rxn_fs[-1].path(rxn_locs)
    zma_fs = next(fs.iterate_managers(rxn_path, ['THEORY', 'TRANSITION STATE',
                                                 'CONFORMER'], 'ZMATRIX'), None)
    if zma_fs is not None:
        zma_path = zma_fs[-1].path([0])
        print(zma_path)

        if zma_fs[-1].file.zmatrix.exists([0]):
            zma = zma_fs[-1].file.zmatrix.read([0])
            ts_gra = automol.zmatrix.graph(zma, remove_stereo=True)

            # Here is where we can build the reactant graph and determine the
            # direction.
            # See if the reactant/product graphs are isomoprhic to a subgraph
            # of the TS, then extract that subgraph.

            # First, just see if there is a 
            rct1_iso_dct = automol.graph.full_subgraph_isomorphism(
                ts_gra, rct_gras[0])

            prd1_iso_dct = automol.graph.full_subgraph_isomorphism(
                ts_gra, prd_gras[0])

            if rct1_iso_dct is not None and prd1_iso_dct is None:
                print('forward reaction')
                rct1_atm_keys = rct1_iso_dct.keys()
                rct1_gra = automol.graph.subgraph(ts_gra, rct1_iso_dct.keys())
                print(automol.graph.string(rct1_gra))
            elif rct1_iso_dct is None and prd1_iso_dct is not None:
                print('backward reaction')
                prd1_atm_keys = prd1_iso_dct.keys()
                prd1_gra = automol.graph.subgraph(ts_gra, prd1_iso_dct.keys())
                print(automol.graph.string(prd1_gra))
            elif rct1_iso_dct is not None and prd1_iso_dct is not None:
                print('direction is undecided')
            else:
                print('no subgraph isomorphism was found')

            # TODO: If there is a second reactant, we can determine its graph
            # by taking the keys in ts_gra not in rct1_gra (or prd1_gra) and
            # getting that subgraph. Then we can form a union of these two
            # graphs to get the reactant graph. Furthermore, if we run the
            # classifier on these graphs (in the forward direction), we can get
            # the formed and broken keys.

            print()
