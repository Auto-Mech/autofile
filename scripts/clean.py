""" Some examples of how to use the new autofile.fs functions
"""

import os
import subprocess
import shutil
import tempfile
import automol

import projrot_io
from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def write_freqs():
    """ write the harm freqs using ProjRot
    """

    # Build tmp dir to run ProjRot
    prefix = tempfile.mkdtemp()
    print(prefix)
    start_path = os.getcwd()

    # ini = ['REACTION', 'THEORY', 'TRANSITION STATE']
    ini = ['SPECIES', 'THEORY']

    saddle = bool('REACTION' in ini)

    managers = fs.iterate_managers(
        PFX, ini, 'CONFORMER'
    )

    bad_path = []
    for cnf_fs in managers:
        # print(cnf_fs[-1].existing())
        for locs in cnf_fs[-1].existing():
            cnf_path = cnf_fs[-1].path(locs)
            print(cnf_path)
            if cnf_fs[-1].file.hessian.exists(locs):
                print('RUNNING HESS')

                # Read the info
                geom = cnf_fs[-1].file.geometry.read(locs)
                # grad = cnf_fs[-1].file.gradient.read(locs)
                grad = []
                hess = cnf_fs[-1].file.hessian.read(locs)

                # Write the ProjRot input file
                inp_str = projrot_io.writer.rpht_input(
                    [geom], [grad], [hess], rotors_str='')
                in_path = os.path.join(prefix, 'RPHt_input_data.dat')
                with open(in_path, 'w') as proj_file:
                    proj_file.write(inp_str)

                os.chdir(prefix)
                subprocess.check_call(['RPHt.exe'])
                os.chdir(start_path)

                # Read the harmonic frequencies
                out_path = os.path.join(prefix, 'RTproj_freq.dat')
                with open(out_path, 'r') as proj_file:
                    out_str = proj_file.read()
                freqs, imag = projrot_io.reader.rpht_output(
                    out_str)

                # Combine freqs
                if saddle:
                    if len(imag) == 1:
                        wfreqs = freqs + [-1.0*x for x in imag]
                    else:
                        wfreqs = []
                        bad_path.append(cnf_path)
                        print('bad_freqs')
                        print(freqs)
                        print(imag)
                else:
                    if len(imag) == 0:
                        wfreqs = freqs
                    else:
                        wfreqs = []
                        bad_path.append(cnf_path)
                        print('bad_freqs')
                        print(freqs)
                        print(imag)

                # Write the freqs
                if wfreqs:
                    print('FREQS GOOD')
                    print(wfreqs)
                    cnf_fs[-1].file.harmonic_frequencies.write(sorted(wfreqs), locs)


def check_r():
    """ Add the zma input files using geo inputs
    """
    cnf_managers = fs.iterate_managers(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE'],
                                             'CONFORMER')
    for cnf_fs in cnf_managers:
        if cnf_fs is not None:
            print()
            gra = None
            for locs in cnf_fs[-1].existing():
                cnf_path = cnf_fs[-1].path(locs)
                zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                zma_path = zma_fs[-1].path([0])
                # if zma_fs[-1].file.transformation.exists([0]):
                #     tra = zma_fs[-1].file.transformation.read([0])
                #     print('FOUND TRA')
                #     print(zma_path)
                #     break
                if zma_fs[-1].file.reactant_graph.exists([0]):
                    gra = zma_fs[-1].file.reactant_graph.read([0])
                    print('FOUND GRAPH')
                    print(zma_fs[-1].path([0]))
                    break
            print('---')
            print()
            for locs in cnf_fs[-1].existing():
                cnf_path = cnf_fs[-1].path(locs)
                zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                zma_path = zma_fs[-1].path([0])
                # if not zma_fs[-1].file.transformation.exists([0]):
                if not zma_fs[-1].file.reactant_graph.exists([0]):
                    print('WRITING GRA AT CONF')
                    print(zma_path)
                    zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                    # zma_fs[-1].file.transformation.write(tra, [0])
                    zma_fs[-1].file.reactant_graph.write(gra, [0])
                else:
                    print('GRA GOOD')
                    print(zma_path)


def add_zma_inp():
    """ Add the zma input files using geo inputs
    """
    cnf_managers = fs.iterate_managers(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE'],
                                             'CONFORMER')
    for cnf_fs in cnf_managers:
        if cnf_fs is not None:
            print()
            for locs in cnf_fs[-1].existing():
                cnf_path = cnf_fs[-1].path(locs)
                # zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                if cnf_fs[-1].file.geometry_input.exists(locs):
                    inp_str = cnf_fs[-1].file.geometry_input.read(locs)
                    print('FOUND INPUT')
                    print(cnf_fs[-1].path(locs))
                    break
            for locs in cnf_fs[-1].existing():
                cnf_path = cnf_fs[-1].path(locs)
                zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                zma_path = zma_fs[-1].path([0])
                if not zma_fs[-1].file.geometry_input.exists([0]):
                    print('WRITING INPUT')
                    print(zma_path)
                    # zma_fs = fs.manager(cnf_path, 'ZMATRIX')
                    zma_fs[-1].file.geometry_input.write(inp_str, [0])
                else:
                    print('INPUT GOOD')
                    print(zma_path)


def add_ene_yaml():
    """ Add the energy files
    """
    ini = ['SPECIES', 'THEORY']

    # saddle = bool('REACTION' in ini)

    # managers = fs.iterate_managers(
    #     PFX, ini, 'CONFORMER'
    # )
    managers = fs.iterate_managers(
        PFX, ['SPECIES', 'THEORY'], 'CONFORMER')

    for cnf_fs in managers:
        for cnf_locs in cnf_fs[-1].existing():
            cnf_path = cnf_fs[-1].path(cnf_locs)
            sp_fs = fs.single_point(cnf_path)
            sp_locs = fs.iterate_locators(cnf_path, ['SINGLE POINT'])
            for locs in sp_locs:
                sp_fs = fs.single_point(cnf_path)
                if not sp_fs[-1].file.info.exists(locs):
                    print('BAD')

    # method = sp_lst[1]
    # basis = sp_lst[2]
    # if 'ccsd' not in method:
    #     prog = 'gaussian09'
    # inf_obj = autofile.schema.info_objects.run(
    #     job='optimization', prog=prog, version='e.01',
    #     method=method, basis=basis, status=status)
    # inf_obj.utc_start_time = autofile.schema.utc_time()
    # inf_obj.utc_end_time = autofile.schema.utc_time()
    # sp_fs[-1].file.info.write(inf_obj, thy_info[1:4])


def add_ene_to_sp():
    """ Add the energy files
    """
    ini = ['SPECIES', 'THEORY']

    # saddle = bool('REACTION' in ini)

    # managers = fs.iterate_managers(
    #     PFX, ini, 'CONFORMER'
    # )
    managers = fs.iterate_managers(
        PFX, ['SPECIES'], 'THEORY'
    )

    for thy_fs in managers:
        if thy_fs is not None:
            for thy_locs in thy_fs[-1].existing():
                thy_path = thy_fs[-1].path(thy_locs)
                print('thy', thy_path)
                cnf_fs = fs.conformer(thy_path)
                for cnf_locs in cnf_fs[-1].existing():
                    cnf_path = cnf_fs[-1].path(cnf_locs)
                    print('cnf', cnf_path)
                    sp_locs = fs.iterate_locators(cnf_path, ['SINGLE POINT'])
                    sp_lst = list(sp_locs)
                    print('thy_locs', thy_locs)
                    print('sp_locs', sp_lst)
                    if sp_lst:
                        if (thy_locs,) not in sp_lst:
                            if cnf_fs[-1].file.energy.exists(cnf_locs):
                                print('ADD SP FILES')
                                sp_fs = fs.single_point(cnf_path)
                                sp_fs[-1].create(thy_locs)
                                inp_str = cnf_fs[-1].file.geometry_input.read(cnf_locs)
                                ene = cnf_fs[-1].file.energy.read(cnf_locs)
                                sp_fs[-1].file.input.write(inp_str, thy_locs)
                                sp_fs[-1].file.energy.write(ene, thy_locs)
                            else:
                                print('NEED SP FILE')
                    else:
                        print('ADD SP DIR AND FILES')
                        sp_fs = fs.single_point(cnf_path)
                        sp_fs[-1].create(thy_locs)
                        inp_str = cnf_fs[-1].file.geometry_input.read(cnf_locs)
                        ene = cnf_fs[-1].file.energy.read(cnf_locs)
                        sp_fs[-1].file.input.write(inp_str, thy_locs)
                        sp_fs[-1].file.energy.write(ene, thy_locs)



                # method = sp_lst[1]
                # basis = sp_lst[2]
                # if 'ccsd' not in method:
                #     prog = 'gaussian09'
                # inf_obj = autofile.schema.info_objects.run(
                #     job='optimization', prog=prog, version='e.01',
                #     method=method, basis=basis, status=status)
                # inf_obj.utc_start_time = autofile.schema.utc_time()
                # inf_obj.utc_end_time = autofile.schema.utc_time()
                # sp_fs[-1].file.info.write(inf_obj, thy_info[1:4])



def check_zma_for_trans():
    """  Check zma for trans files
    """
    zma_managers = fs.iterate_managers(PFX, ['REACTION', 'THEORY', 'TRANSITION STATE',
                                             'CONFORMER'], 'ZMATRIX')
    BAD = 0
    for zma_fs in zma_managers:
        zma_path = zma_fs[-1].path([0])
        print(zma_path)
        if zma_fs is not None:
            if zma_fs[-1].file.transformation.exists([0]):
                print('GOOD')
            else:
                print('NO TRANS')
                BAD += 1
        else:
            print('zma none')
        print()

    print('\nBAD CNT', BAD)


def add_tors_names_file():
    """ add torsional files
    """




if __name__ == '__main__':
    # add_zma_trans()
    # add_zma_inp()
    # check_zma_for_trans()
    # remove_empty_thy_spc_dirs()
    # remove_empty_thy_ts_dirs()
    # remove_pf_dirs_from_save()
    # ts_keys()
    # write_freqs()
    add_ene_yaml()
    # add_ene_to_sp()
