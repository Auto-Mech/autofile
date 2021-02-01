""" Some examples of how to use the new autofile.fs functions
"""

import itertools
import automol
from autofile import fs


PFX = '/lcrc/project/PACC/AutoMech/data/save/'

CNF_MANAGERS = itertools.chain(
    fs.iterate_managers(PFX, ['SPECIES', 'THEORY'], 'CONFORMER'),
    fs.iterate_managers(PFX, ['SPECIES', 'THEORY', 'TRANSITION_STATE'], 'CONFORMER'))
# sca_fs[0].removable = True
# sca_fs[0].remove()
# print('removing...')


def fix_tors():
    """ Add the zma input files using geo inputs
    """

    for cnf_fs in CNF_MANAGERS:
        if cnf_fs is not None:

            # Read nsampd and tors range from the info file
            if cnf_fs[0].file.info.exists():
                inf_obj = cnf_fs[0].file.info.read()
                nsampd = inf_obj.nsamp
                tors_ranges = dict(inf_obj.tors_ranges)

                cnf_path = cnf_fs[0].path()
                print('cnf_path', cnf_path)
                print('nsampd', nsampd)
                print('tors', tors_ranges)

                # Build zma obj
                zma_fs = fs.zmatrix(cnf_path)

                # Read the zma and build the zma object
                zma = zma_fs[-1].file.zmatrix.read([0])
                rotors = automol.rotor.from_zma(zma)

                new_names = automol.rotor.names(rotors, flat=True)
                assert set(tors_ranges.keys()) == set(new_names)

                # zma_fs[-1].file.torsions.write(rotors, [0])

            else:
                print('no cnf yaml')


if __name__ == '__main__':
    fix_tors()
