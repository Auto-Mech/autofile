""" Script for cycling through reactions and testing Yuri's z-matrix code on
them
"""
import automol
from autofile import fs

# PFX = './TMP/'
PFX = '/lcrc/project/PACC/AutoMech/data/save/'

RXN_FS = fs.manager(PFX, 'REACTION')

FORWARD_COUNT = 0
BACKWARD_COUNT = 0
OVERLAP_COUNT = 0
FAIL_COUNT = 0

fails = []
for rxn_locs, in fs.iterate_locators(PFX, ['REACTION']):
    # print('HERE')
    (rct_ichs, prd_ichs), _, _, _ = rxn_locs

    rct_gras = list(map(automol.inchi.graph, rct_ichs))
    prd_gras = list(map(automol.inchi.graph, prd_ichs))

    rct_gras = list(map(automol.graph.without_stereo_parities, rct_gras))
    prd_gras = list(map(automol.graph.without_stereo_parities, prd_gras))

    rct_gras = list(map(automol.graph.explicit, rct_gras))
    prd_gras = list(map(automol.graph.explicit, prd_gras))

    rct_smis = list((automol.inchi.smiles(ich) for ich in rct_ichs))
    prd_smis = list((automol.inchi.smiles(ich) for ich in prd_ichs))

    # print('ichs')
    # print(rct_ichs)
    # print(prd_ichs)
    # print('smi')
    # print(list((automol.inchi.smiles(ich) for ich in rct_ichs)))
    # print(list((automol.inchi.smiles(ich) for ich in prd_ichs)))

    # Get one z-matrix for this reaction, if there is one
    rxn_path = RXN_FS[-1].path(rxn_locs)
    zma_fs = next(fs.iterate_managers(rxn_path, ['THEORY', 'TRANSITION STATE',
                                                 'CONFORMER'], 'ZMATRIX'), None)
    if zma_fs is not None:
        zma_path = zma_fs[-1].path([0])
        # print([rct_ichs, prd_ichs])
        print(zma_path)

        if zma_fs[-1].file.zmatrix.exists([0]):
            # Read out the z-matrix
            ts_zma = zma_fs[-1].file.zmatrix.read([0])

            # Note that the keys in rct_gras and prd_gras at this point are
            # arbitrary. The following work determines the transformation and
            # the reactant graph *in terms of the z-matrix keys*.

            # Attempt to determine the transformation in the forward direction
            forw_tra, forw_rct_gra = automol.zmat.ts.zmatrix_reaction_info(
                ts_zma, rct_gras, prd_gras)

            # Attempt to determine the transformation in the backward direction
            back_tra, back_rct_gra = automol.zmat.ts.zmatrix_reaction_info(
                ts_zma, rct_gras=prd_gras, prd_gras=rct_gras)

            # The transformations (formed/broken keys) returned by the above
            # function are aligned to the z-matrix and *should* correspond to
            # the correct atoms in the z-matrix. Since there are many
            # transformations possible between rct_gras and prd_gras, I have
            # chosen the one in which the bonds formed and broken are
            # *shortest* in the TS z-matrix, which should correspond to the
            # ones that were actually used to generate it.

            # If we have found a correctly-aligned transformation, we can now
            # use it to determine the correctly-aligned reactant graph, with
            # keys corresponding to those in the TS z-matrix.

            if forw_tra is not None:
                # print("Found transformation in the forward direction")

                # print("Reactant graph, with keys aligned to zmatrix:")
                # print(automol.graph.string(forw_rct_gra))

                # print("Reaction transformation, with keys aligned to zmatrix:")
                # print(automol.graph.trans.string(forw_tra))
                fails.append(
                    [rct_smis, prd_smis, rct_ichs, prd_ichs, 'rxn', zma_path]
                )

                FORWARD_COUNT += 1

            if back_tra is not None:
                BACKWARD_COUNT += 1
                # print("Found transformation in the backward direction")

                # print("Reactant graph, with keys aligned to zmatrix:")
                # print(automol.graph.string(back_rct_gra))

                # print("Reaction transformation, with keys aligned to zmatrix:")
                # print(automol.graph.trans.string(back_tra))
                fails.append(
                    [rct_smis, prd_smis, rct_ichs, prd_ichs, 'rxn', zma_path]
                )

            # If the formed and broken bonds are both too long in the TS to be
            # considered connected, we may not dect a transformation in either
            # direction. I could imagine a hacky fix for this, in which we add
            # connections between the next closest atoms.
            if forw_tra is None and back_tra is None:
                # print("No TS subgraph match")
                # print(automol.zmat.string(ts_zma))
                # print(automol.geom.string(automol.zmat.geometry(ts_zma)))
                # print('ichs')
                # print(rct_ichs)
                # print(prd_ichs)
                # print('smi')
                # print(list((automol.inchi.smiles(ich) for ich in rct_ichs)))
                # print(list((automol.inchi.smiles(ich) for ich in prd_ichs)))
                # print(zma_path)
                fails.append(
                    [rct_smis, prd_smis, rct_ichs, prd_ichs, 'rxn', zma_path]
                )

                FAIL_COUNT += 1

            if forw_tra is not None and back_tra is not None:
                # print("Overlap match")
                # print(automol.zmat.string(ts_zma))
                # print('ichs')
                # print(rct_ichs)
                # print(prd_ichs)
                # print('smi')
                # print(list((automol.inchi.smiles(ich) for ich in rct_ichs)))
                # print(list((automol.inchi.smiles(ich) for ich in prd_ichs)))
                # print(zma_path)
                # print(automol.geom.string(automol.zmat.geometry(ts_zma)))
                OVERLAP_COUNT += 1
                # fails.append(
                    # [rct_ichs, prd_ichs, 'rxn', zma_path]
                # )

# print('forward count:', FORWARD_COUNT)
# print('backward count:', BACKWARD_COUNT)
# print('overlap count:', OVERLAP_COUNT)
# print('fail count:', FAIL_COUNT)

print('fails = ')
for fail in fails:
    print('[')
    for i, x in enumerate(fail):
        if i in (0, 1):
            print('     #', x, ',')
        elif i in (2, 3):
            z = [elm for elm in x]
            print('    ', z, ',')
        else:
            print('    ', "'"+x+"'", ',')
    print(']')
print(']')
