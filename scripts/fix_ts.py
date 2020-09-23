"""
  Generate
"""

import os
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


CLA = {
    'mig': hydrogen_migration,
    'bsci': beta_scission,
    'ins': insertion,
    'sub': substitution,
    'add': addition,
    'abst': hydrogen_abstraction,
    'elim': concerted_unimolecular_elimination
}

for i, fail in enumerate(tsfails.fails):
    print(fail[0])
    print(fail[1])
    print(fail[2])
    print(fail[3])
    # cnf_dirs = list(os.walk(fail[3]))[1]
    cnf_dirs = [directory for directory in os.listdir(fail[3]) 
            if directory[0] == 'c' and 'conf' not in directory]
    #cnf_dirs.remove('conf.yaml')
    print('cnf_dirs:', cnf_dirs)
    for adir in cnf_dirs:
        print('dir:', adir)
        path = os.path.join(fail[3], adir)
        print('path:', path)
        zma_fs = autofile.fs.manager(path, 'ZMATRIX')
        rct_geos = list(map(automol.inchi.geometry, fail[0]))
        prd_geos = list(map(automol.inchi.geometry, fail[1]))
        rct_zmas = list(map(automol.geom.zmatrix, rct_geos))
        prd_zmas = list(map(automol.geom.zmatrix, prd_geos))
        ret = CLA[fail[2]](rct_zmas, prd_zmas)
        if fail[2] != 'add':
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
