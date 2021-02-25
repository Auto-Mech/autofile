""" test the autofile.file module
"""
import os
import tempfile
import numpy
import automol
import autofile.info
import autofile.data_types

TMP_DIR = tempfile.mkdtemp()
print(TMP_DIR)


def test__information():
    """ test the information read/write functions
    """
    ref_inf_obj = autofile.info.Info(a=['b', 'c', 'd', 'e'],
                                     x=autofile.info.Info(y=1, z=2))

    inf_file_name = autofile.data_types.name.information('test')
    inf_file_path = os.path.join(TMP_DIR, inf_file_name)
    inf_str = autofile.data_types.swrite.information(ref_inf_obj)

    assert not os.path.isfile(inf_file_path)
    autofile.io_.write_file(inf_file_path, inf_str)
    assert os.path.isfile(inf_file_path)

    inf_str = autofile.io_.read_file(inf_file_path)
    inf_obj = autofile.data_types.sread.information(inf_str)
    assert inf_obj == ref_inf_obj


def test__file():
    """ test the file read/write functions
    """
    inp_str = '<input file contents>'
    out_str = '<output file contents>'
    scr_str = '<shell script contents>'

    inp_file_name = autofile.data_types.name.input_file('test')
    out_file_name = autofile.data_types.name.output_file('test')
    scr_file_name = autofile.data_types.name.run_script('test')

    inp_file_path = os.path.join(TMP_DIR, inp_file_name)
    out_file_path = os.path.join(TMP_DIR, out_file_name)
    scr_file_path = os.path.join(TMP_DIR, scr_file_name)

    assert not os.path.isfile(inp_file_path)
    assert not os.path.isfile(out_file_path)
    assert not os.path.isfile(scr_file_path)
    autofile.io_.write_file(inp_file_path, inp_str)
    autofile.io_.write_file(out_file_path, out_str)
    autofile.io_.write_file(scr_file_path, scr_str)


def test__energy():
    """ test the energy read/write functions
    """
    ref_ene = -75.00613628303537

    ene_file_name = autofile.data_types.name.energy('test')
    ene_file_path = os.path.join(TMP_DIR, ene_file_name)
    ene_str = autofile.data_types.swrite.energy(ref_ene)

    assert not os.path.isfile(ene_file_path)
    autofile.io_.write_file(ene_file_path, ene_str)
    assert os.path.isfile(ene_file_path)

    ene_str = autofile.io_.read_file(ene_file_path)
    ene = autofile.data_types.sread.energy(ene_str)
    assert numpy.isclose(ref_ene, ene)


def test__geometry():
    """ test the geometry read/write functions
    """
    ref_geo = (('C', (-0.70116587131, 0.0146227007587, -0.016166607003)),
               ('O', (1.7323365056, -0.9538524899, -0.5617192010)),
               ('H', (-0.9827048283, 0.061897979239, 2.02901783816)),
               ('H', (-0.8787925682, 1.91673409124, -0.80019507919)),
               ('H', (-2.12093033745, -1.21447973767, -0.87411360631)),
               ('H', (2.9512589894, 0.17507745634, 0.22317665541)))

    geo_file_name = autofile.data_types.name.geometry('test')
    geo_file_path = os.path.join(TMP_DIR, geo_file_name)
    geo_str = autofile.data_types.swrite.geometry(ref_geo)

    assert not os.path.isfile(geo_file_path)
    autofile.io_.write_file(geo_file_path, geo_str)
    assert os.path.isfile(geo_file_path)

    geo_str = autofile.io_.read_file(geo_file_path)
    geo = autofile.data_types.sread.geometry(geo_str)
    assert automol.geom.almost_equal(ref_geo, geo)


def test__trajectory():
    """ test the trajectory read/rwrite functions
    """
    ref_geo_lst = [
        (('C', (0.0, 0.0, 0.0)),
         ('O', (0.0, 0.0, 2.699694868173)),
         ('O', (0.0, 2.503038629201, -1.011409768236)),
         ('H', (-1.683942509299, -1.076047850358, -0.583313101501)),
         ('H', (1.684063451772, -0.943916309940, -0.779079279468)),
         ('H', (1.56980872050, 0.913848877557, 3.152002706027)),
         ('H', (-1.57051358834, 3.264399836517, -0.334901043405))),
        (('C', (0.0, 0.0, 0.0)),
         ('O', (0.0, 0.0, 2.70915105770)),
         ('O', (0.0, 2.55808068205, -0.83913477573)),
         ('H', (-1.660164085463, -1.04177010816, -0.73213470306)),
         ('H', (1.711679909369, -0.895873802652, -0.779058492481)),
         ('H', (0.0238181080852, -1.813377410537, 3.16912929390)),
         ('H', (-1.36240560905, 3.348313125118, 0.1732746576216)))]
    ref_comments = [
        'energy: -187.38941054878092',
        'energy: -187.3850624381528']
    traj = tuple(zip(ref_geo_lst, ref_comments))

    traj_file_name = autofile.data_types.name.trajectory('test')
    traj_file_path = os.path.join(TMP_DIR, traj_file_name)
    traj_str = autofile.data_types.swrite.trajectory(traj)

    assert not os.path.isfile(traj_file_path)
    autofile.io_.write_file(traj_file_path, traj_str)
    assert os.path.isfile(traj_file_path)


def test__zmatrix():
    """ test the zmatrix read/write functions
    """
    ref_zma = (
        ('C', (None, None, None), (None, None, None),
         (None, None, None)),
        ('O', (0, None, None), ('r1', None, None),
         (2.67535, None, None)),
        ('H', (0, 1, None), ('r2', 'a1', None),
         (2.06501, 1.9116242, None)),
        ('H', (0, 1, 2), ('r3', 'a2', 'd1'),
         (2.06501, 1.9116242, 2.108497362)),
        ('H', (0, 1, 2), ('r4', 'a3', 'd2'),
         (2.06458, 1.9020947, 4.195841334)),
        ('H', (1, 0, 2), ('r5', 'a4', 'd3'),
         (1.83748, 1.8690905, 5.228936625))
    )

    zma_file_name = autofile.data_types.name.zmatrix('test')
    zma_file_path = os.path.join(TMP_DIR, zma_file_name)
    zma_str = autofile.data_types.swrite.zmatrix(ref_zma)

    assert not os.path.isfile(zma_file_path)
    autofile.io_.write_file(zma_file_path, zma_str)
    assert os.path.isfile(zma_file_path)

    zma_str = autofile.io_.read_file(zma_file_path)
    zma = autofile.data_types.sread.zmatrix(zma_str)
    assert automol.zmat.almost_equal(ref_zma, zma)


def test__vmatrix():
    """ test the vmatrix read/write functions
    """
    ref_vma = (('C', (None, None, None), (None, None, None)),
               ('O', (0, None, None), ('r1', None, None)),
               ('H', (0, 1, None), ('r2', 'a1', None)),
               ('H', (0, 1, 2), ('r3', 'a2', 'd1')),
               ('H', (0, 1, 2), ('r4', 'a3', 'd2')),
               ('H', (1, 0, 2), ('r5', 'a4', 'd3')))

    vma_file_name = autofile.data_types.name.vmatrix('test')
    vma_file_path = os.path.join(TMP_DIR, vma_file_name)
    vma_str = autofile.data_types.swrite.vmatrix(ref_vma)

    assert not os.path.isfile(vma_file_path)
    autofile.io_.write_file(vma_file_path, vma_str)
    assert os.path.isfile(vma_file_path)

    vma_str = autofile.io_.read_file(vma_file_path)
    vma = autofile.data_types.sread.vmatrix(vma_str)
    assert vma == ref_vma


# def test__torsions():
#     """ test the torsion names read/write functions
#     """
# 
#     zma = automol.geom.zmatrix(automol.inchi.geometry(
#             automol.smiles.inchi('CCO')))
#     ref_tors_lst = automol.rotor.from_zmatrix(zma)
# 
#     tors_file_name = autofile.data_types.name.torsions('test')
#     tors_file_path = os.path.join(TMP_DIR, tors_file_name)
#     tors_str = autofile.data_types.swrite.torsions(ref_tors_lst)
# 
#     assert not os.path.isfile(tors_file_path)
#     autofile.io_.write_file(tors_file_path, tors_str)
#     assert os.path.isfile(tors_file_path)
# 
#     tors_str = autofile.io_.read_file(tors_file_path)
#     tors_lst = autofile.data_types.sread.torsions(tors_str)
#     for tors, tors_ref in zip(tors_lst, ref_tors_lst):
#         assert tors.name == tors_ref.name
#         assert tors.symmetry == tors_ref.symmetry
# 

def test__gradient():
    """ test the gradient read/write functions
    """
    ref_grad = (
        (-6.687065494e-05, -2.087360475e-05, -2.900518464e-05),
        (2.091815312e-05, -2.162539565e-05, 2.097302071e-05),
        (-9.17712798e-06, -2.97043797e-05, -1.378883952e-05),
        (2.244858355e-05, 6.0265176e-06, 1.00733398e-06),
        (4.676018254e-05, 5.473937899e-05, 1.744549e-05),
        (-1.407913705e-05, 1.143748381e-05, 3.3681804e-06))

    grad_file_name = autofile.data_types.name.gradient('test')
    grad_file_path = os.path.join(TMP_DIR, grad_file_name)
    grad_str = autofile.data_types.swrite.gradient(ref_grad)

    assert not os.path.isfile(grad_file_path)
    autofile.io_.write_file(grad_file_path, grad_str)
    assert os.path.isfile(grad_file_path)

    grad_str = autofile.io_.read_file(grad_file_path)
    grad = autofile.data_types.sread.gradient(grad_str)
    assert numpy.allclose(ref_grad, grad)


def test__hessian():
    """ test the hessian read/write functions
    """
    ref_hess = (
        (0.70455411073336, -0.08287472697212, 0.0, -0.0798647434566,
         0.05385932364624, 0.0, -0.62468936727659, 0.02901540332588, 0.0),
        (-0.08287472697212, 0.73374800936533, 0.0, -0.06694564915575,
         -0.63928635896955, 0.0, 0.14982037612785, -0.09446165039567, 0.0),
        (0.0, 0.0, 0.00019470176975, 0.0, 0.0, -9.734161519e-05, 0.0, 0.0,
         -9.736015438e-05),
        (-0.0798647434566, -0.06694564915575, 0.0, 0.08499297871932,
         -0.02022391947876, 0.0, -0.00512823526272, 0.0871695686345, 0.0),
        (0.05385932364624, -0.63928635896955, 0.0, -0.02022391947876,
         0.65384367318451, 0.0, -0.03363540416748, -0.01455731421496, 0.0),
        (0.0, 0.0, -9.734161519e-05, 0.0, 0.0, 4.370597581e-05, 0.0, 0.0,
         5.363563938e-05),
        (-0.62468936727659, 0.14982037612785, 0.0, -0.00512823526272,
         -0.03363540416748, 0.0, 0.6298176025393, -0.11618497196038, 0.0),
        (0.02901540332588, -0.09446165039567, 0.0, 0.0871695686345,
         -0.01455731421496, 0.0, -0.11618497196038, 0.10901896461063, 0.0),
        (0.0, 0.0, -9.736015438e-05, 0.0, 0.0, 5.363563938e-05, 0.0, 0.0,
         4.3724515e-05)
    )

    hess_file_name = autofile.data_types.name.hessian('test')
    hess_file_path = os.path.join(TMP_DIR, hess_file_name)
    hess_str = autofile.data_types.swrite.hessian(ref_hess)

    assert not os.path.isfile(hess_file_path)
    autofile.io_.write_file(hess_file_path, hess_str)
    assert os.path.isfile(hess_file_path)

    hess_str = autofile.io_.read_file(hess_file_path)
    hess = autofile.data_types.sread.hessian(hess_str)
    assert numpy.allclose(ref_hess, hess)


def test__anharmonic_frequencies():
    """ test the anharmonic frequencies read/write functions
    """
    ref_freqs = sorted([3123.20334, 2013.56563, 1830.34050, 745.33024,
                        23.049560, 1.2344])

    freqs_file_name = autofile.data_types.name.anharmonic_frequencies('test')
    freqs_file_path = os.path.join(TMP_DIR, freqs_file_name)
    freqs_str = autofile.data_types.swrite.anharmonic_frequencies(ref_freqs)

    assert not os.path.isfile(freqs_file_path)
    autofile.io_.write_file(freqs_file_path, freqs_str)
    assert os.path.isfile(freqs_file_path)

    freqs_str = autofile.io_.read_file(freqs_file_path)
    freqs = autofile.data_types.sread.anharmonic_frequencies(freqs_str)
    assert numpy.allclose(ref_freqs, freqs, atol=1e00)


def test__anharmonic_zpve():
    """ test the anharmonic ZPVE read/write functions
    """
    ref_anh_zpve = -25.123455

    anh_zpve_file_name = autofile.data_types.name.anharmonic_zpve('test')
    anh_zpve_file_path = os.path.join(TMP_DIR, anh_zpve_file_name)
    anh_zpve_str = autofile.data_types.swrite.anharmonic_zpve(ref_anh_zpve)

    assert not os.path.isfile(anh_zpve_file_path)
    autofile.io_.write_file(anh_zpve_file_path, anh_zpve_str)
    assert os.path.isfile(anh_zpve_file_path)

    anh_zpve_str = autofile.io_.read_file(anh_zpve_file_path)
    anh_zpve = autofile.data_types.sread.anharmonic_zpve(anh_zpve_str)
    assert numpy.isclose(ref_anh_zpve, anh_zpve)


def test__anharmonicity_matrix():
    """ test the anharmonicity matrix read/write functions
    """

    ref_xmat = ((1.123, 2.451, 7.593),
                (3.321, 4.123, 9.382),
                (5.342, 6.768, 8.392))

    xmat_file_name = autofile.data_types.name.anharmonicity_matrix('test')
    xmat_file_path = os.path.join(TMP_DIR, xmat_file_name)
    xmat_str = autofile.data_types.swrite.anharmonicity_matrix(ref_xmat)

    assert not os.path.isfile(xmat_file_path)
    autofile.io_.write_file(xmat_file_path, xmat_str)
    assert os.path.isfile(xmat_file_path)

    xmat_str = autofile.io_.read_file(xmat_file_path)
    xmat = autofile.data_types.sread.anharmonicity_matrix(xmat_str)
    assert numpy.allclose(ref_xmat, xmat)


def test__vibro_rot_alpha_matrix():
    """ test the vibro-rot alpha matrix read/write functions
    """

    ref_vibro_rot_mat = ((1.123, 2.451, 7.593),
                         (3.321, 4.123, 9.382),
                         (5.342, 6.768, 8.392))

    vibro_rot_mat_file_name = (
        autofile.data_types.name.vibro_rot_alpha_matrix('test'))
    vibro_rot_mat_file_path = os.path.join(TMP_DIR, vibro_rot_mat_file_name)
    vibro_rot_mat_str = autofile.data_types.swrite.vibro_rot_alpha_matrix(
        ref_vibro_rot_mat)

    assert not os.path.isfile(vibro_rot_mat_file_path)
    autofile.io_.write_file(vibro_rot_mat_file_path, vibro_rot_mat_str)
    assert os.path.isfile(vibro_rot_mat_file_path)

    vibro_rot_mat_str = autofile.io_.read_file(
        vibro_rot_mat_file_path)
    vibro_rot_mat = autofile.data_types.sread.vibro_rot_alpha_matrix(
        vibro_rot_mat_str)
    assert numpy.allclose(ref_vibro_rot_mat, vibro_rot_mat)


def test__quartic_centrifugal_distortion_constants():
    """ test the quartic centrifugal distortion constants read/write functions
    """

    ref_qcds = (('aaaa', 1.123), ('bbbb', 2.451), ('cccc', 4.123))

    qcds_file_name = (
        autofile.data_types.name.quartic_centrifugal_dist_consts('test'))
    qcds_file_path = os.path.join(TMP_DIR, qcds_file_name)
    qcds_str = (
        autofile.data_types.swrite.quartic_centrifugal_dist_consts(ref_qcds))

    assert not os.path.isfile(qcds_file_path)
    autofile.io_.write_file(qcds_file_path, qcds_str)
    assert os.path.isfile(qcds_file_path)

    qcds_str = autofile.io_.read_file(qcds_file_path)
    qcds = autofile.data_types.sread.quartic_centrifugal_dist_consts(qcds_str)
    assert ref_qcds[0][0] == qcds[0][0]
    assert ref_qcds[1][0] == qcds[1][0]
    assert ref_qcds[2][0] == qcds[2][0]
    assert numpy.isclose(ref_qcds[0][1], qcds[0][1])
    assert numpy.isclose(ref_qcds[1][1], qcds[1][1])
    assert numpy.isclose(ref_qcds[2][1], qcds[2][1])


def test__lennard_jones_epsilon():
    """ test the epsilon read/write functions
    """
    ref_eps = 247.880866746988

    eps_file_name = autofile.data_types.name.lennard_jones_epsilon('test')
    eps_file_path = os.path.join(TMP_DIR, eps_file_name)
    eps_str = autofile.data_types.swrite.lennard_jones_epsilon(ref_eps)

    assert not os.path.isfile(eps_file_path)
    autofile.io_.write_file(eps_file_path, eps_str)
    assert os.path.isfile(eps_file_path)

    eps_str = autofile.io_.read_file(eps_file_path)
    eps = autofile.data_types.sread.lennard_jones_epsilon(eps_str)
    assert numpy.isclose(ref_eps, eps)


def test__lennard_jones_sigma():
    """ test the sigma read/write functions
    """
    ref_sig = 3.55018590361446

    sig_file_name = autofile.data_types.name.lennard_jones_sigma('test')
    sig_file_path = os.path.join(TMP_DIR, sig_file_name)
    sig_str = autofile.data_types.swrite.lennard_jones_sigma(ref_sig)

    assert not os.path.isfile(sig_file_path)
    autofile.io_.write_file(sig_file_path, sig_str)
    assert os.path.isfile(sig_file_path)

    sig_str = autofile.io_.read_file(sig_file_path)
    sig = autofile.data_types.sread.lennard_jones_sigma(sig_str)
    assert numpy.isclose(ref_sig, sig)


def test__external_symmetry_number():
    """ test the symmetry number read/write functions
    """
    ref_num = 1.500

    num_file_name = autofile.data_types.name.external_symmetry_factor('test')
    num_file_path = os.path.join(TMP_DIR, num_file_name)
    num_str = autofile.data_types.swrite.external_symmetry_factor(ref_num)

    assert not os.path.isfile(num_file_path)
    autofile.io_.write_file(num_file_path, num_str)
    assert os.path.isfile(num_file_path)

    num_str = autofile.io_.read_file(num_file_path)
    num = autofile.data_types.sread.external_symmetry_factor(num_str)
    assert numpy.isclose(ref_num, num)


def test__internal_symmetry_number():
    """ test the symmetry number read/write functions
    """
    ref_num = 1.500

    num_file_name = autofile.data_types.name.internal_symmetry_factor('test')
    num_file_path = os.path.join(TMP_DIR, num_file_name)
    num_str = autofile.data_types.swrite.internal_symmetry_factor(ref_num)

    assert not os.path.isfile(num_file_path)
    autofile.io_.write_file(num_file_path, num_str)
    assert os.path.isfile(num_file_path)

    num_str = autofile.io_.read_file(num_file_path)
    num = autofile.data_types.sread.internal_symmetry_factor(num_str)
    assert numpy.isclose(ref_num, num)


def test__polarizability():
    """ test the vibro-rot alpha matrix read/write functions
    """

    ref_polar_mat = ((1.00, 2.00, 3.00),
                     (4.00, 5.00, 6.00),
                     (7.00, 8.00, 9.00))

    polar_mat_file_name = (
        autofile.data_types.name.polarizability('test'))
    polar_mat_file_path = os.path.join(TMP_DIR, polar_mat_file_name)
    polar_mat_str = autofile.data_types.swrite.polarizability(
        ref_polar_mat)

    assert not os.path.isfile(polar_mat_file_path)
    autofile.io_.write_file(polar_mat_file_path, polar_mat_str)
    assert os.path.isfile(polar_mat_file_path)

    polar_mat_str = autofile.io_.read_file(
        polar_mat_file_path)
    polar_mat = autofile.data_types.sread.polarizability(
        polar_mat_str)
    assert numpy.allclose(ref_polar_mat, polar_mat)


def test__dipole_moment():
    """ test the dipole_moment tensor read/write functions
    """

    ref_dip_mom_vec = (1.00, 2.00, 3.00)

    dip_mom_vec_file_name = (
        autofile.data_types.name.dipole_moment('test'))
    dip_mom_vec_file_path = os.path.join(TMP_DIR, dip_mom_vec_file_name)
    dip_mom_vec_str = autofile.data_types.swrite.dipole_moment(
        ref_dip_mom_vec)

    assert not os.path.isfile(dip_mom_vec_file_path)
    autofile.io_.write_file(dip_mom_vec_file_path, dip_mom_vec_str)
    assert os.path.isfile(dip_mom_vec_file_path)

    dip_mom_vec_str = autofile.io_.read_file(
        dip_mom_vec_file_path)
    dip_mom_vec = autofile.data_types.sread.dipole_moment(
        dip_mom_vec_str)
    assert numpy.allclose(ref_dip_mom_vec, dip_mom_vec)


def test__reaction():
    """ test the reaction read/write functions
    """
    ref_rxn = automol.reac.Reaction(
        rxn_cls=automol.par.ReactionClass.HYDROGEN_ABSTRACTION,
        forw_tsg=(
            {0: ('C', 0, None), 1: ('H', 0, None), 2: ('H', 0, None),
             3: ('H', 0, None), 4: ('H', 0, None), 5: ('O', 0, None),
             6: ('H', 0, None)},
            {frozenset({5, 6}): (1, None), frozenset({0, 3}): (1, None),
             frozenset({4, 5}): (0.1, None),
             frozenset({0, 1}): (1, None), frozenset({0, 2}): (1, None),
             frozenset({0, 4}): (0.9, None)}),
        back_tsg=(
            {0: ('O', 0, None), 1: ('H', 0, None), 2: ('H', 0, None),
             3: ('C', 0, None), 4: ('H', 0, None), 5: ('H', 0, None),
             6: ('H', 0, None)},
            {frozenset({0, 2}): (0.9, None),
             frozenset({2, 3}): (0.1, None),
             frozenset({3, 6}): (1, None), frozenset({0, 1}): (1, None),
             frozenset({3, 4}): (1, None), frozenset({3, 5}): (1, None)}),
        rcts_keys=((0, 1, 2, 3, 4), (5, 6)),
        prds_keys=((0, 1, 2), (3, 4, 5, 6)),
    )

    rxn_file_name = autofile.data_types.name.reaction('test')
    rxn_file_path = os.path.join(TMP_DIR, rxn_file_name)
    rxn_str = autofile.data_types.swrite.reaction(ref_rxn)

    assert not os.path.isfile(rxn_file_path)
    autofile.io_.write_file(rxn_file_path, rxn_str)
    assert os.path.isfile(rxn_file_path)

    rxn_str = autofile.io_.read_file(rxn_file_path)
    rxn = autofile.data_types.sread.reaction(rxn_str)
    assert rxn == ref_rxn


if __name__ == '__main__':
    # test__energy()
    # test__geometry()
    # test__zmatrix()
    # test__file()
    # test__information()
    # test__gradient()
    # test__hessian()
    # test__trajectory()
    # test__vmatrix()
    test__torsions()
    # test__anharmonic_frequencies()
    # test__anharmonic_zpve()
    # test__anharmonicity_matrix()
    # test__vibro_rot_alpha_matrix()
    # test__quartic_centrifugal_distortion_constants()
    # test__lennard_jones_epsilon()
    # test__lennard_jones_sigma()
    # test__external_symmetry_number()
    # test__internal_symmetry_number()
    # test__dipole_moment()
    # test__polarizability()
    # test__graph()
    # test__reaction()
