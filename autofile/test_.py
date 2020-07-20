""" test autofile.fs
"""
import os
import tempfile
import autofile.fs
import automol

PREFIX = tempfile.mkdtemp()
print(PREFIX)


def test__species():
    """ test autofile.fs.species
    """
    prefix = os.path.join(PREFIX, 'species')
    os.mkdir(prefix)

    locs = ['InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 0, 1]
    spc_fs = autofile.fs.species(prefix)
    print(spc_fs[-1].path(locs))

    assert not spc_fs[-1].exists(locs)
    spc_fs[-1].create(locs)
    assert spc_fs[-1].exists(locs)


def test__reaction():
    """ test autofile.fs.reaction
    """
    prefix = os.path.join(PREFIX, 'reaction')
    os.mkdir(prefix)

    locs = [
        [['InChI=1S/C2H5O2/c1-2-4-3/h3H,1-2H2'],
         ['InChI=1S/C2H4/c1-2/h1-2H2', 'InChI=1S/HO2/c1-2/h1H']],
        [[0], [0, 0]],
        [[2], [1, 2]],
        2
    ]
    rxn_fs = autofile.fs.reaction(prefix)
    print(rxn_fs[-1].path(locs))

    assert not rxn_fs[-1].exists(locs)
    rxn_fs[-1].create(locs)
    assert rxn_fs[-1].exists(locs)


def test__transition_state():
    """ test autofile.fs.transition_state
    """
    prefix = os.path.join(PREFIX, 'ts')
    os.mkdir(prefix)

    ts_fs = autofile.fs.transition_state(prefix)
    print(ts_fs[0].path())

    assert not ts_fs[0].exists()
    ts_fs[0].create()
    assert ts_fs[0].exists()


def test__theory():
    """ test autofile.fs.theory
    """
    prefix = os.path.join(PREFIX, 'theory')
    os.mkdir(prefix)

    thy_fs = autofile.fs.theory(prefix)
    locs = ['hf', 'sto-3g', 'U']
    print(thy_fs[-1].path(locs))

    ref_ene = 5.7
    print(thy_fs[-1].file.energy.path(locs))
    thy_fs[-1].create(locs)
    thy_fs[-1].file.energy.write(ref_ene, locs)
    assert thy_fs[-1].file.energy.read(locs) == ref_ene


def test__conformer():
    """ test autofile.fs.conformer
    """
    prefix = os.path.join(PREFIX, 'conformer')
    os.mkdir(prefix)

    locs = [autofile.schema.generate_new_conformer_id()]
    cnf_fs = autofile.fs.conformer(prefix)
    print(cnf_fs[-1].path(locs))

    assert not cnf_fs[-1].exists(locs)
    cnf_fs[-1].create(locs)
    assert cnf_fs[-1].exists(locs)


def test__single_point():
    """ test autofile.fs.single_point
    """
    prefix = os.path.join(PREFIX, 'single_point')
    os.mkdir(prefix)

    sp_fs = autofile.fs.single_point(prefix)
    locs = ['hf', 'sto-3g', 'U']
    print(sp_fs[-1].path(locs))

    ref_ene = 5.7
    print(sp_fs[-1].file.energy.path(locs))
    sp_fs[-1].create(locs)
    sp_fs[-1].file.energy.write(ref_ene, locs)
    assert sp_fs[-1].file.energy.read(locs) == ref_ene


def test__zmatrix():
    """ test autofile.fs.zmatrix
    """
    prefix = os.path.join(PREFIX, 'zmatrix')
    os.mkdir(prefix)

    zma_fs = autofile.fs.zmatrix(prefix)
    locs = [0]
    print(zma_fs[-1].path(locs))

    ref_zma = ((('O', (None, None, None), (None, None, None)),
                ('H', (0, None, None), ('R1', None, None))),
               {'R1': 1.84779})

    print(zma_fs[-1].file.zmatrix.path(locs))
    zma_fs[-1].create(locs)
    zma_fs[-1].file.zmatrix.write(ref_zma, locs)
    assert automol.zmatrix.almost_equal(
        zma_fs[-1].file.zmatrix.read(locs), ref_zma)

    ref_tra = (frozenset({frozenset({10, 7})}),
               frozenset({frozenset({0, 10})}))

    zma_fs[-1].file.transformation.write(ref_tra, locs)
    tra = zma_fs[-1].file.transformation.read(locs)

    print(tra)
    assert tra == ref_tra

    ref_gra = ({0: ('C', 0, None), 1: ('C', 0, None), 2: ('C', 0, None),
                3: ('C', 0, None), 4: ('C', 0, None), 5: ('C', 0, None),
                6: ('C', 0, None), 8: ('H', 0, None), 9: ('H', 0, None),
                10: ('H', 0, None), 11: ('H', 0, None), 12: ('H', 0, None),
                13: ('H', 0, None), 14: ('H', 0, None), 15: ('H', 0, None),
                16: ('H', 0, None), 17: ('H', 0, None), 18: ('H', 0, None),
                19: ('H', 0, None), 20: ('H', 0, None), 21: ('H', 0, None),
                22: ('H', 0, None), 7: ('O', 0, None)},
               {frozenset({4, 6}): (1, None), frozenset({21, 6}): (1, None),
                frozenset({0, 2}): (1, None), frozenset({2, 4}): (1, None),
                frozenset({5, 6}): (1, None), frozenset({17, 4}): (1, None),
                frozenset({3, 5}): (1, None), frozenset({1, 3}): (1, None),
                frozenset({20, 6}): (1, None), frozenset({0, 10}): (1, None),
                frozenset({1, 12}): (1, None), frozenset({2, 14}): (1, None),
                frozenset({18, 5}): (1, None), frozenset({1, 13}): (1, None),
                frozenset({0, 8}): (1, None), frozenset({0, 9}): (1, None),
                frozenset({3, 15}): (1, None), frozenset({1, 11}): (1, None),
                frozenset({19, 5}): (1, None), frozenset({16, 3}): (1, None),
                frozenset({22, 7}): (1, None)})

    zma_fs[-1].file.reactant_graph.write(ref_gra, locs)
    rct_gra = zma_fs[-1].file.reactant_graph.read(locs)

    rct_atm_keys_lst = automol.graph.connected_components_atom_keys(rct_gra)
    print(rct_atm_keys_lst)

    # this is how we can get the product graph
    prd_gra = automol.graph.trans.apply(tra, rct_gra)
    prd_atm_keys_lst = automol.graph.connected_components_atom_keys(prd_gra)
    print(prd_atm_keys_lst)

    assert rct_gra == ref_gra


def test__scan():
    """ test autofile.fs.scan
    """
    prefix = os.path.join(PREFIX, 'scan')
    os.mkdir(prefix)

    scn_fs = autofile.fs.scan(prefix)
    locs = [['d3', 'd4'], [2, 3]]
    print(scn_fs[-1].path(locs))

    ref_inp_str = '<input string>'
    print(scn_fs[-1].file.geometry_input.path(locs))
    scn_fs[-1].create(locs)
    scn_fs[-1].file.geometry_input.write(ref_inp_str, locs)
    assert scn_fs[-1].file.geometry_input.read(locs) == ref_inp_str


def test__cscan():
    """ test autofile.fs.cscan
    """
    prefix = os.path.join(PREFIX, 'cscan')
    os.mkdir(prefix)

    scn_fs = autofile.fs.cscan(prefix)
    # the dictionary at the end specifies the constraint values
    locs = [{'r1': 1., 'a2': 2.3}, ['d3', 'd4'], [1.2, 2.9]]
    print(scn_fs[-1].path(locs))

    ref_inp_str = '<input string>'
    print(scn_fs[-1].file.geometry_input.path(locs))
    scn_fs[-1].create(locs)
    scn_fs[-1].file.geometry_input.write(ref_inp_str, locs)
    assert scn_fs[-1].file.geometry_input.read(locs) == ref_inp_str


def test__tau():
    """ test autofile.fs.tau
    """
    prefix = os.path.join(PREFIX, 'tau')
    os.mkdir(prefix)

    locs = [autofile.schema.generate_new_tau_id()]
    tau_fs = autofile.fs.tau(prefix)
    print(tau_fs[-1].path(locs))

    assert not tau_fs[-1].exists(locs)
    tau_fs[-1].create(locs)
    assert tau_fs[-1].exists(locs)


# def test__energy_transfer():
#     """ test autofile.fs.energy_transfer
#     """
#     prefix = os.path.join(PREFIX, 'etrans')
#     os.mkdir(prefix)
#
#  #   spc_fs = autofile.fs.species(prefix)
#  #   spc_locs = ['InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 0, 1]
#  #   spc_fs[-1].create(spc_locs)
#  #   spc_path = spc_fs[-1].path(spc_locs)
#  #   print(spc_fs[-1].path(spc_locs))
#
#     etrans_fs = autofile.fs.energy_transfer(prefix)
#     spc_locs = [['InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 0, 1],[],[]]
#     etrans_fs[-1].create(spc_locs)
#     etrans_spc_path = etrans_fs[-1].path(spc_locs)
#     print(etrans_spc_path)
#     thy_locs = [ 'hf', 'sto-3g', True]
#     etrans_thy_fs = autofile.fs.theory(etrans_spc_path)
#     etrans_thy_fs[-1].create(thy_locs)
#     etrans_thy_path = etrans_thy_fs[-1].path(thy_locs)
#     print(etrans_thy_path)
#     spc_path = print(etrans_spc_s[-1].path(spc_locs))
#     print(etrans_spc_s[-1].path(spc_locs))
#     locs = ['InChI=1S/C2H2F2/c3-1-2-4/h1-2H/b2-1+', 0, 1]
#     etrans_fs[-1].create(locs)
#     print(etrans_fs[-1].path(locs))
#
#     ref_eps = 300.0
#     ref_sig = 3.50
#     print(etrans_fs[-1].file.lennard_jones_epsilon.path(locs))
#     print(etrans_fs[-1].file.lennard_jones_sigma.path(locs))
#     # etrans_fs[-1].create(locs)
#     etrans_fs[-1].file.lennard_jones_epsilon.write(ref_eps, locs)
#     etrans_fs[-1].file.lennard_jones_sigma.write(ref_sig, locs)
#     assert etrans_fs[-1].file.lennard_jones_epsilon.read(locs) == ref_eps
#     assert etrans_fs[-1].file.lennard_jones_sigma.read(locs) == ref_sig


def test__run():
    """ test autofile.fs.run
    """
    prefix = os.path.join(PREFIX, 'run')
    os.mkdir(prefix)

    run_fs = autofile.fs.run(prefix)
    print(run_fs[-1].path(['gradient']))

    ref_inp_str = '<input string>'
    print(run_fs[-1].file.input.path(['gradient']))
    run_fs[-1].create(['gradient'])
    run_fs[-1].file.input.write(ref_inp_str, ['gradient'])
    assert run_fs[-1].file.input.read(['gradient']) == ref_inp_str


def test__build():
    """ test autofile.fs.build
    """
    prefix = os.path.join(PREFIX, 'build')
    os.mkdir(prefix)

    build_fs = autofile.fs.build(prefix)
    print(build_fs[-1].path(['MESS', 0]))

    ref_inp_str = '<input string>'
    print(build_fs[-1].file.input.path(['MESS', 0]))
    build_fs[-1].create(['MESS', 0])
    build_fs[-1].file.input.write(ref_inp_str, ['MESS', 0])
    assert build_fs[-1].file.input.read(['MESS', 0]) == ref_inp_str


if __name__ == '__main__':
    # test__species()
    # test__reaction()
    # test__transition_state()
    # test__theory()
    # test__conformer()
    # test__tau()
    # test__single_point()
    # test__energy_transfer()
    # test__scan()
    # test__run()
    # test__build()
    test__cscan()
    # test__zmatrix()
