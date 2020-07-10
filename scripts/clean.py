""" Some examples of how to use the new autofile.fs functions
"""

import os
import tempfile
import automol
import projrot_io
from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'


def remove_empty_thy_dirs():
    """ Get rid of the empty theory directories
    """
    paths = fs.iterate_paths(
        PFX, ['REACTION', 'THEORY']
    )

    for path in paths:
        thy_dirs = os.listdir(path)
        if 'CONFS' not in thy_dirs:
            print(path)
            print(thy_dirs)
            # put in a remove command for the path


def remove_pf_dirs_from_save():
    """ Get rid of the empty theory directories
    """
    spc_paths = fs.iterate_paths(
        PFX, ['SPECIES', 'THEORY']
    )
    ts_paths = fs.iterate_paths(
        PFX, ['REACTION', 'THEORY', 'TRANSITION STATE']
    )
    paths = list(spc_paths) + list(ts_paths)

    bad_dirs = ['PF', 'PROJ']

    for path in paths:
        for bad_dir in bad_dirs:
            bad_path = os.path.join(path, bad_dir)
            if os.path.exists(bad_path):
                print(bad_path)
                # put in a remove command for the path


def write_freqs():
    """ write the harm freqs using ProjRot
    """

    # Build tmp dir to run ProjRot
    prefix = tempfile.mkdtemp()
    print(prefix)

    ini = ['REACTION', 'THEORY', 'TRANSITION STATE']
    # ini = ['SPECIES', 'THEORY']

    saddle = bool('REACTION' in ini)

    managers = fs.iterate_managers(
        PFX, ini, 'CONFORMER'
    )

    bad_path = []
    for cnf_fs in managers:
        for locs in cnf_fs[-1].existing():
            if cnf_fs[-1].file.hessian.exists(locs):
                cnf_path = cnf_fs[-1].path(locs)
                print(cnf_path)

                # Read the info
                geom = cnf_fs[-1].file.geometry.read(locs)
                grad = cnf_fs[-1].file.gradient.read(locs)
                hess = cnf_fs[-1].file.hessian.read(locs)

                # Write the ProjRot input file
                inp_str = projrot_io.writer.rpht_input(
                    [geom], [grad], [hess], rotors_str='')
                in_path = os.path.join(prefix, 'RPHt_input_data.dat')
                with open(in_path, 'w') as proj_file:
                    proj_file.write(inp_str)

                # Read the harmonic frequencies
                out_path = os.path.join(prefix, 'RTproj_freq.dat')
                with open(out_path, 'r') as proj_file:
                    out_str = proj_file.read()
                freqs, imag = projrot_io.reader.rpht_output(
                    out_str)

                # Combine freqs
                if saddle:
                    if len(imag) == 1:
                        wfreqs = freqs + imag
                    else:
                        wfreqs = []
                        bad_path.append(cnf_path)
                else:
                    if len(imag) == 0:
                        wfreqs = freqs
                    else:
                        wfreqs = []
                        bad_path.append(cnf_path)

                # Write the freqs
                if wfreqs:
                    cnf_fs[-1].file.harmonic_frequencies.write(wfreqs, locs)


if __name__ == '__main__':
    # remove_empty_thy_dirs()
    # remove_pf_dirs_from_save()
    # ts_keys()
    write_freqs()
