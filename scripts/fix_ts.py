"""
  Generate
"""

import os
import numpy
import automol
import autofile
from automol.zmatrix._unimol_ts import hydrogen_migration
from automol.zmatrix._unimol_ts import concerted_unimolecular_elimination
from automol.zmatrix._unimol_ts import beta_scission
from automol.zmatrix._bimol_ts import insertion
from automol.zmatrix._bimol_ts import substitution
from automol.zmatrix._bimol_ts import addition
from automol.zmatrix._bimol_ts import hydrogen_abstraction
import tsfails
import sys

CLA = {
    'mig': hydrogen_migration,
    'bsci': beta_scission,
    'ins': insertion,
    'sub': substitution,
    'add': addition,
    'abst': hydrogen_abstraction,
    'elim': concerted_unimolecular_elimination
}

species_csv = autofile.io_.read_file(sys.argv[1]).splitlines()
for idx, entry in enumerate(species_csv[0].split(',')):
    if 'inch' in entry:
        ich_idx = idx
for i, fail in enumerate(tsfails.fails):
    print(fail[0])
    print(fail[1])
    print(fail[2])
#    print(fail[3])
    # cnf_dirs = list(os.walk(fail[3]))[1]
    cnf_dirs = [directory for directory in os.listdir(fail[2]) 
            if directory[0] == 'c' and 'conf' not in directory]

    cnf_parent = fail[2]
    cnf_fs = autofile.fs.conformer(fail[2].replace('CONFS',''))
    inf_obj = cnf_fs[0].file.info.read()
    # nsampd = inf_obj.nsamp

    #cnf_dirs.remove('conf.yaml')
    print('cnf_dirs:', cnf_dirs)
    for adir in cnf_dirs:
        print('dir:', adir)
        path = os.path.join(fail[2], adir)
        print('path:', path)
        zma_fs = autofile.fs.zmatrix(path)
        reacs = fail[0].split('=')[0].split('+')
        prods = fail[0].split('=')[1].split('+')
        reac_ichs = []
        prod_ichs = []
        for species in species_csv[1:]:
            species = species.split("'")
            species_name = species[0].split(',')[0]
            print('species test:', species_name, species, species[0], reacs)
            for i in range(len(reacs)):
                print('reacs test:', reacs[i], i)
                if species_name == reacs[i]:
                    print('ich_idx test:', species[ich_idx-1], ich_idx-1)
                    reacs[i] = species[ich_idx-1]
            for i in range(len(prods)):
                if species_name == prods[i]:
                    prods[i] = species[ich_idx-1]
        print('reacs: ', reacs)
        print('prods: ', prods)
        rct_geos = list(map(automol.inchi.geometry, reacs))#fail[0]))
        prd_geos = list(map(automol.inchi.geometry, prods))#fail[1]))
        rct_zmas = list(map(automol.geom.zmatrix, rct_geos))
        prd_zmas = list(map(automol.geom.zmatrix, prd_geos))
        ret = CLA[fail[1]](rct_zmas, prd_zmas)
        print('ret test:', ret)
        if 'mig' in fail[1]:
            ts_zma, dist_name, frm_key, brk_key, _, tors_names, rcts_gra = ret
        elif 'bsci' in fail[1]:
            ts_zma, dist_name, brk_key, tors_names, rcts_gra = ret
            frm_key = frozenset({})
        elif fail[1] != 'add':
            ts_zma, dist_name, frm_key, brk_key, tors_names, rcts_gra = ret
        else:
            ts_zma, dist_name, frm_key, tors_names, rcts_gra = ret
            brk_key = frozenset({})
        for tors_name in tors_names:
            print('  {}: [0.0, 360.0]'.format( tors_name))

        tra = (frozenset({frm_key}),
            frozenset({brk_key}))
        print(tra)
        print(rcts_gra)
        zma_fs[-1].file.transformation.write(tra, [0])
        zma_fs[-1].file.reactant_graph.write(rcts_gra, [0])
        
        # tors_ranges = list(automol.zmatrix.torsional_sampling_ranges(tors_names))
        tors_ranges = list([0, 360.] for tors in tors_names)
        tors_range_dct = dict(zip(tors_names, tors_ranges))
        inf_obj.tors_ranges = tors_range_dct
        cnf_fs[0].file.info.write(inf_obj)
