""" Some examples of how to use the new autofile.fs functions
"""

import os
import subprocess
import tempfile

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
                    cnf_fs[-1].file.harmonic_frequencies.write(
                        sorted(wfreqs), locs)


if __name__ == '__main__':
    write_freqs()
