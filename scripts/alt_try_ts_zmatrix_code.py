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
            print(automol.zmatrix.string(zma))
            print()
