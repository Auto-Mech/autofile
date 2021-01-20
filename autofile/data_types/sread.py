""" string readers
"""
from io import StringIO as _StringIO
import numpy
import automol
import autoparse.find as apf
import autofile.info


def information(inf_str):
    """ read information (any dict/list combination) from a string
    """
    inf_obj = autofile.info.from_string(inf_str)
    return inf_obj


def energy(ene_str):
    """ read an energy (hartree) from a string (hartree)
    """
    ene = _float(ene_str)
    return ene


def geometry(xyz_str):
    """ read a geometry (bohr) from a string (angstrom)
    """
    geo = automol.geom.from_xyz_string(xyz_str)
    return geo


def trajectory(traj_str):
    """ read a trajectory of geometries (bohr) from a string (angstrom)
    """
    traj = automol.geom.from_xyz_trajectory_string(traj_str)
    return traj


def zmatrix(zma_str):
    """ read a zmatrix (bohr/radian) from a string (angstrom/degree)
    """
    zma = automol.zmatrix.from_string(zma_str)
    return zma


def vmatrix(vma_str):
    """ read a variable zmatrix (bohr/radian) from a string (angstrom/degree)
    """
    vma = automol.vmatrix.from_string(vma_str)
    return vma


def gradient(grad_str):
    """ read a gradient (hartree bohr^-1) from a string (hartree bohr^-1)
    """
    grad_str_io = _StringIO(grad_str)
    grad = numpy.loadtxt(grad_str_io)
    assert grad.ndim == 2 and grad.shape[1] == 3
    return tuple(map(tuple, grad))


def gradient_array(grad_list):
    """convert gradient python list to gradient numpy ndarray
    """
    return numpy.array(grad_list)


def hessian(hess_str):
    """ read a hessian (hartree bohr^-2) from a string (hartree bohr^-2)
    """
    hess_str_io = _StringIO(hess_str)
    hess = numpy.loadtxt(hess_str_io)
    assert hess.ndim == 2
    assert hess.shape[0] % 3 == 0 and hess.shape[0] == hess.shape[1]
    return tuple(map(tuple, hess))


def harmonic_frequencies(freq_str):
    """ read harmonic frequencies (cm^-1) from a string (cm^-1)
    """
    return _frequencies(freq_str)


def anharmonic_frequencies(freq_str):
    """ read anharmonic frequencies (cm^-1) from a string (cm^-1)
    """
    return _frequencies(freq_str)


def projected_frequencies(freq_str):
    """ read projected frequencies (cm^-1) from a string (cm^-1)
    """
    return _frequencies(freq_str)


def anharmonic_zpve(anh_zpve_str):
    """ read the anharmonic zpve (hartree) from a string (hartree)
    """
    anh_zpve = _float(anh_zpve_str)
    return anh_zpve


def anharmonicity_matrix(xmat_str):
    """ read an anharmonicity matrix (cm^-1)
        from a string (cm^-1)
    """
    mat_str_io = _StringIO(xmat_str)
    mat = numpy.loadtxt(mat_str_io)
    assert mat.ndim == 2 or mat.ndim == 0
    if mat.ndim == 2:
        assert mat.shape[0] == mat.shape[1]
        xmat = tuple(map(tuple, mat))
    else:
        xmat = ((mat,),)
    return xmat


def vibro_rot_alpha_matrix(vibro_rot_str):
    """ read an vibro-rot alpha matrix (cm^-1)
        from a string (cm^-1)
    """
    mat_str_io = _StringIO(vibro_rot_str)
    mat = numpy.loadtxt(mat_str_io)
    assert mat.ndim == 2 or mat.ndim == 0
    if mat.ndim == 2:
        assert mat.shape[0] == mat.shape[1]
    return tuple(map(tuple, mat))


def quartic_centrifugal_dist_consts(qcd_consts_str):
    """ write the quartic centrifugal distortion constant
        labels and values (cm^-1) to a string (cm^-1)
    """
    qcd_consts_lines = qcd_consts_str.splitlines()
    qcd_consts = []
    for line in qcd_consts_lines:
        const = line.strip().split()
        qcd_consts.append([const[0], float(const[1])])
    qcd_consts = tuple(tuple(x) for x in qcd_consts)
    return qcd_consts


def lennard_jones_epsilon(eps_str):
    """ read a lennard-jones epsilon (waveunmbers) from a string (wavenumbers)
    """
    eps = _float(eps_str)
    return eps


def lennard_jones_sigma(sig_str):
    """ read a lennard-jones sigma (angstrom) from a string (angstrom)
    """
    sig = _float(sig_str)
    return sig


def external_symmetry_factor(esf_str):
    """ read an external symmetry factor from a string (dimensionless)
    """
    esf = _float(esf_str)
    return esf


def internal_symmetry_factor(isf_str):
    """ read an internal symmetry factor from a string (dimensionless)
    """
    isf = _float(isf_str)
    return isf


def dipole_moment(dip_mom_str):
    """ reads the x,y,z dipole moment vector from a string
    """
    dip_mom_str_io = _StringIO(dip_mom_str)
    dip_mom = numpy.loadtxt(dip_mom_str_io)
    assert dip_mom.ndim == 1
    assert dip_mom.shape[0] == 3
    return map(tuple, dip_mom)


def polarizability(polar_str):
    """ read a polarizability tensor () from a string
    """
    polar_str_io = _StringIO(polar_str)
    polar = numpy.loadtxt(polar_str_io)
    assert polar.ndim == 2
    assert polar.shape[0] == polar.shape[1] == 3
    return tuple(map(tuple, polar))


def graph(gra_str):
    """ read a molecular graph from a string
    """
    gra = automol.graph.from_string(gra_str)
    return gra


def transformation(tra_str):
    """ read a chemical transformation from a string
    """
    tra = automol.graph.trans.old_from_string(tra_str)
    return tra


def transformation_old(tra_str):
    """ read a chemical transformation from a string
    """
    tra = automol.graph.trans.from_string(tra_str)
    return tra


def _float(val_str):
    assert apf.is_number(val_str)
    val = float(val_str)
    return val


def _frequencies(freq_str):
    if len(freq_str.split()) == 1:
        freqs = [float(freq) for freq in freq_str.split()]
    else:
        freq_str_io = _StringIO(freq_str)
        freqs = numpy.loadtxt(freq_str_io)
        assert freqs.ndim == 1
    return tuple(freqs)


def _2d_square_matrix(mat_str):
    mat_str_io = _StringIO(mat_str)
    mat = numpy.loadtxt(mat_str_io)
    assert mat.ndim == 2
    assert mat.shape[0] == mat.shape[1]
    return tuple(map(tuple, mat))
