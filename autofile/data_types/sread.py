""" string readers
    converts properties formatted in strings of externally preferred units
    to properties in internally used units and used data type
"""

from io import StringIO as _StringIO
from numbers import Real as _Real
import numpy
import yaml
import automol
from phydat import phycon
import autoparse.find as apf
import autofile.info


def information(inf_str):
    """ read information (any dict/list combination) from a string
    :param inf_str: info yaml information
    :type inf_str: str
    :return: info object class instance
    :rtype: Info
    """
    inf_obj = autofile.info.from_string(inf_str)
    return inf_obj


def energy(ene_str):
    """ read an energy (hartree) from a string (hartree)
    :param ene_str: energy
    :type inf_str: str
    :return: energy
    :rtype: float
    """
    ene = _float(ene_str)
    return ene


def geometry(xyz_str):
    """ read a geometry (bohr) from a string (angstrom)
    :param xyz_str: geometry in xyz format
    :type xyz_str: str
    :return: goemetry as internally used tuple object
    :rtype: tuple
    """
    geo = automol.geom.from_xyz_string(xyz_str)
    return geo


def trajectory(traj_str):
    """ read a trajectory of geometries (bohr) from a string (angstrom)
    :param traj_str: traj string
    :type traj_str: str
    :return: trajectory as internally used tuple object
    :rtype: tuple
    """
    traj = automol.geom.from_xyz_trajectory_string(traj_str)
    return traj


def zmatrix(zma_str):
    """ read a zmatrix (bohr/radian) from a string (angstrom/degree)
    :param zma_str: zmatrix string
    :type zma_str: str
    :return: zmatrix as internally used tuple object
    :rtype: tuple
    """
    zma = automol.zmatrix.from_string(zma_str)
    return zma


def vmatrix(vma_str):
    """ read a variable zmatrix (bohr/radian) from a string (angstrom/degree)
    :param vma_str: vmatrix string
    :type vma_str: str
    :return: vmatrix as internally used tuple object
    :rtype: tuple
    """
    vma = automol.vmatrix.from_string(vma_str)
    return vma


def gradient(grad_str):
    """ read a gradient (hartree bohr^-1) from a string (hartree bohr^-1)
    :param grad_str: gradient string
    :type grad_str: str
    :return: gradient as internally used tuple object
    :rtype: tuple
    """
    grad_str_io = _StringIO(grad_str)
    grad = numpy.loadtxt(grad_str_io)
    assert grad.ndim == 2 and grad.shape[1] == 3
    return tuple(map(tuple, grad))


def gradient_array(grad_list):
    """convert gradient python list to gradient numpy ndarray
    :param grad_list: gradient list
    :type grad_list: str
    :return: gradient list
    :rtype: numpy array
    """
    return numpy.array(grad_list)


def torsional_names(tors_str):
    """ Write the torsions and their ranges (radian) to a string (degree).

        :param tors_str: names and angle ranges of torsional coordinates
        :type tors_str: str
        :rtype: dict[str: tuple(float)]
    """

    tors_dct = yaml.load(tors_str, Loader=yaml.FullLoader)

    assert all(isinstance(key, str) and len(rng) == 2
               and all(isinstance(x, _Real) for x in rng)
               for key, rng in tors_dct.items())

    for name, rng in tors_dct.items():
        tors_dct[name] = (rng[0] * phycon.DEG2RAD, rng[1] * phycon.DEG2RAD)

    return tors_dct


def hessian(hess_str):
    """ read a hessian (hartree bohr^-2) from a string (hartree bohr^-2)
    :param hess_str: hessian string
    :type hess_str: str
    :return: hessian as 3nx3n tuple
    :rtype: tuple
    """
    hess_str_io = _StringIO(hess_str)
    hess = numpy.loadtxt(hess_str_io)
    assert hess.ndim == 2
    assert hess.shape[0] % 3 == 0 and hess.shape[0] == hess.shape[1]
    return tuple(map(tuple, hess))


def harmonic_frequencies(freq_str):
    """ read harmonic frequencies (cm^-1) from a string (cm^-1)
    :param freq_str: freq string
    :type freq_str: str
    :return: tuple of float frequencies
    :rtype: tuple
    """
    return _frequencies(freq_str)


def anharmonic_frequencies(freq_str):
    """ read anharmonic frequencies (cm^-1) from a string (cm^-1)
    :param freq_str: freq string
    :type freq_str: str
    :return: tuple of float frequencies
    :rtype: tuple
    """
    return _frequencies(freq_str)


def projected_frequencies(freq_str):
    """ read projected frequencies (cm^-1) from a string (cm^-1)
    :param freq_str: freq string
    :type freq_str: str
    :return: tuple of float frequencies
    :rtype: tuple
    """
    return _frequencies(freq_str)


def anharmonic_zpve(anh_zpve_str):
    """ read the anharmonic zpve (hartree) from a string (hartree)
    :param anh_zpve_str: zpve string
    :type anh_zpve_str: str
    :return: zpve as float
    :rtype: float
    """
    anh_zpve = _float(anh_zpve_str)
    return anh_zpve


def anharmonicity_matrix(xmat_str):
    """ read an anharmonicity matrix (cm^-1)
        from a string (cm^-1)
    :param xmat_str: xmat string
    :type xmat_str: str
    :return: anharmonicity xmatrix as nfreqxnfreq tuple
    :rtype: tuple
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
    :param vibro_rot_str: vibro-rot alpha matrix string
    :type vibro_rot_str: str
    :return: matrix as tuple
    :rtype: tuple
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
    :param qcd_consts_str: quartic centrifugal dist const string
    :type qcd_consts_str: str
    :return: constants in a tuple
    :rtype: tuple
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
    :param eps_str: epsilon string
    :type eps_consts_str: str
    :return: epsilon float
    :rtype: float
    """
    eps = _float(eps_str)
    return eps


def lennard_jones_sigma(sig_str):
    """ read a lennard-jones sigma (angstrom) from a string (angstrom)
    :param sig_str: sigma string
    :type sig_consts_str: str
    :return: sigma float
    :rtype: float
    """
    sig = _float(sig_str)
    return sig


def external_symmetry_factor(esf_str):
    """ read an external symmetry factor from a string (dimensionless)
    :param esf_str: external symmetry factor string
    :type esf_consts_str: str
    :return: external symmetry factor float
    :rtype: float
    """
    esf = _float(esf_str)
    return esf


def internal_symmetry_factor(isf_str):
    """ read an internal symmetry factor from a string (dimensionless)
    :param isf_str: internal symmetry factor string
    :type isf_consts_str: str
    :return: internal symmetry factor float
    :rtype: float
    """
    isf = _float(isf_str)
    return isf


def dipole_moment(dip_mom_str):
    """ reads the x,y,z dipole moment vector from a string
    :param dip_mom_str: x,y,z dipole moment vector
    :type dip_mom_str: str
    :return: x, y, z dipole moment tuple
    :rtype: tuple
    """
    dip_mom_str_io = _StringIO(dip_mom_str)
    dip_mom = numpy.loadtxt(dip_mom_str_io)
    assert dip_mom.ndim == 1
    assert dip_mom.shape[0] == 3
    return tuple(dip_mom)


def polarizability(polar_str):
    """ read a polarizability tensor () from a string
    :param polar_str: polarizability tensor
    :type polar_str: str
    :return: polarizability tensor
    :rtype: tuple
    """
    polar_str_io = _StringIO(polar_str)
    polar = numpy.loadtxt(polar_str_io)
    assert polar.ndim == 2
    assert polar.shape[0] == polar.shape[1] == 3
    return tuple(map(tuple, polar))


def graph(gra_str):
    """ read a molecular graph from a string
    :param gra_str: molecular graph
    :type gra_str: str
    :return: molecular graph tuple (autochem format)
    :rtype: tuple
    """
    gra = automol.graph.from_string(gra_str)
    return gra


def transformation(tra_str):
    """ read a chemical transformation from a string
    :param tra_str: trasformation string
    :type tra_str: str
    :return: breaking and forming bonds
    :rtype: tuple
    """
    tra = automol.graph.trans.old_from_string(tra_str)
    return tra


def transformation_new(tra_str):
    """ read a chemical transformation from a string
    """
    tra = automol.graph.trans.from_string(tra_str)
    return tra


def _float(val_str):
    """ str to float
    """
    assert apf.is_number(val_str)
    val = float(val_str)
    return val


def _frequencies(freq_str):
    """ comma seperated string to tuple of floats
    """
    if len(freq_str.split()) == 1:
        freqs = [float(freq) for freq in freq_str.split()]
    else:
        freq_str_io = _StringIO(freq_str)
        freqs = numpy.loadtxt(freq_str_io)
        assert freqs.ndim == 1
    return tuple(freqs)


def _2d_square_matrix(mat_str):
    """ comma seperated string to 2D tuple of floats
    """
    mat_str_io = _StringIO(mat_str)
    mat = numpy.loadtxt(mat_str_io)
    assert mat.ndim == 2
    assert mat.shape[0] == mat.shape[1]
    return tuple(map(tuple, mat))
