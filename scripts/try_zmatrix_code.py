""" Script for cycling through reactions and testing Yuri's z-matrix code on
them
"""
import automol
import automol.sym_num
from autofile import fs

TMP_PFX = './TMP/'

COUNT2 = 0
COUNT3 = 0

MISSED2 = []
MISSED3 = []

for spc_locs, in fs.iterate_locators(TMP_PFX, ['SPECIES']):
    ich, _, _ = spc_locs

    geo = automol.inchi.geometry(ich)

    if not automol.geom.is_linear(geo):
        print(ich)
        # zma = automol.geom.zmatrix(geo)
        # names = automol.geom.zmatrix_torsion_coordinate_names(geo)
        # idxs = automol.geom.zmatrix_atom_ordering(geo)
        sym_num1 = automol.sym_num.external_symmetry_factor1(geo)
        sym_num2 = automol.sym_num.external_symmetry_factor2(geo)
        sym_num3 = automol.sym_num.external_symmetry_factor3(geo)

        if sym_num2 != sym_num1:
            print('sym_num2', '{} != {}'.format(sym_num1, sym_num2))
            MISSED2.append(sym_num1)
            COUNT2 += 1

        if sym_num3 != sym_num1:
            print('sym_num3', '{} != {}'.format(sym_num1, sym_num3))
            MISSED3.append(sym_num1)
            COUNT3 += 1

print('COUNT2', COUNT2)
print('COUNT3', COUNT3)
print('MISSED2', MISSED2)
print('MISSED3', MISSED3)
