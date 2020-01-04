"""
autofile.fs
***********

Generate autofile.model.FileSystem objects for generating and interacting with
a filesystem.
"""
from autofile.system import file_
from autofile.system import info
from autofile.system import dir_
from autofile.system import model


class _FilePrefix():
    """ file prefixes """
    RUN = 'run'
    BUILD = 'build'
    CONF = 'conf'
    TAU = 'tau'
    SP = 'sp'
    HS = 'hs'
    SCAN = 'scan'
    GEOM = 'geom'
    GRAD = 'grad'
    HESS = 'hess'
    MIN = 'min'
    VPT2 = 'vpt2'
    LJ = 'lj'


class _FileAttributeName():
    """ DataFile attribute names """
    INFO = 'info'
    INPUT = 'input'
    OUTPUT = 'output'
    VMATRIX = 'vmatrix'
    GEOM_INFO = 'geometry_info'
    GRAD_INFO = 'gradient_info'
    HESS_INFO = 'hessian_info'
    VPT2_INFO = 'vpt2_info'
    GEOM_INPUT = 'geometry_input'
    GRAD_INPUT = 'gradient_input'
    HESS_INPUT = 'hessian_input'
    VPT2_INPUT = 'vpt2_input'
    ENERGY = 'energy'
    GEOM = 'geometry'
    ZMAT = 'zmatrix'
    GRAD = 'gradient'
    HESS = 'hessian'
    HFREQ = 'harmonic_frequencies'
    TRAJ = 'trajectory'
    ANHFREQ = 'anharmonic_frequencies'
    ANHZPVE = 'anharmonic_zpve'
    XMAT = 'anharmonicity_matrix'
    VIBROT_MAX = 'vibro_rot_alpha_matrix'
    CENTIF_DIST = 'quartic_centrifugal_dist_consts'
    LJ_EPS = 'lennard_jones_epsilon'
    LJ_SIG = 'lennard_jones_sigma'


def species(prefix):
    """ construct the species filesystem [trunk/leaf]

    two layers with the following specifiers:
    1. []
    2. [ich, chg, mul]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.species_trunk(prefix)
    leaf_ds = dir_.species_leaf(prefix, root_ds=trunk_ds)
    return (trunk_ds, leaf_ds)


def theory(prefix):
    """ construct the theory filesystem [leaf]

    one layer with the following specifiers: [method, basis, orb_type]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    leaf_ds = dir_.theory_leaf(prefix)

    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    leaf_ds.add_data_files({
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.ZMAT: zmat_dfile})

    return (leaf_ds,)


def conformer(prefix):
    """ construct the conformer filesystem [trunk/leaf]

    two layers with the following specifiers:
    1. []
    2. [cid]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.conformer_trunk(prefix)
    leaf_ds = dir_.conformer_leaf(prefix, root_ds=trunk_ds)

    min_ene_dfile = file_.energy(_FilePrefix.MIN)
    vma_dfile = file_.vmatrix(_FilePrefix.CONF)
    inf_dfile = file_.information(_FilePrefix.CONF,
                                  function=info.conformer_trunk)
    traj_dfile = file_.trajectory(_FilePrefix.CONF)
    trunk_ds.add_data_files({
        _FileAttributeName.VMATRIX: vma_dfile,
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.ENERGY: min_ene_dfile,
        _FileAttributeName.TRAJ: traj_dfile})

    geom_inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    grad_inf_dfile = file_.information(_FilePrefix.GRAD, function=info.run)
    hess_inf_dfile = file_.information(_FilePrefix.HESS, function=info.run)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    grad_dfile = file_.gradient(_FilePrefix.GRAD)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    hfreq_dfile = file_.harmonic_frequencies(_FilePrefix.HESS)
    vpt2_inf_dfile = file_.information(
        _FilePrefix.VPT2, function=info.vpt2_trunk)
    vpt2_inp_dfile = file_.input_file(_FilePrefix.VPT2)
    anhfreq_dfile = file_.anharmonic_frequencies(_FilePrefix.VPT2)
    anhzpve_dfile = file_.anharmonic_zpve(_FilePrefix.VPT2)
    xmat_dfile = file_.anharmonicity_matrix(_FilePrefix.VPT2)
    vibrot_mat_dfile = file_.vibro_rot_alpha_matrix(_FilePrefix.VPT2)
    centrif_dist_dfile = file_.quartic_centrifugal_dist_consts(_FilePrefix.VPT2)

    leaf_ds.add_data_files({
        _FileAttributeName.GEOM_INFO: geom_inf_dfile,
        _FileAttributeName.GRAD_INFO: grad_inf_dfile,
        _FileAttributeName.HESS_INFO: hess_inf_dfile,
        _FileAttributeName.GEOM_INPUT: geom_inp_dfile,
        _FileAttributeName.GRAD_INPUT: grad_inp_dfile,
        _FileAttributeName.HESS_INPUT: hess_inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile,
        _FileAttributeName.GRAD: grad_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.HFREQ: hfreq_dfile,
        _FileAttributeName.VPT2_INFO: vpt2_inf_dfile,
        _FileAttributeName.VPT2_INPUT: vpt2_inp_dfile,
        _FileAttributeName.ANHFREQ: anhfreq_dfile,
        _FileAttributeName.ANHZPVE: anhzpve_dfile,
        _FileAttributeName.XMAT: xmat_dfile,
        _FileAttributeName.VIBROT_MAX: vibrot_mat_dfile,
        _FileAttributeName.CENTIF_DIST: centrif_dist_dfile})

    return (trunk_ds, leaf_ds)


def single_point(prefix):
    """ construct the single-point filesystem [trunk/leaf]

    two layers with the following specifiers:
    1. []
    2. [method, basis, orb_type]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.single_point_trunk(prefix)
    leaf_ds = dir_.single_point_leaf(prefix, root_ds=trunk_ds)

    inp_dfile = file_.input_file(_FilePrefix.SP)
    inf_dfile = file_.information(_FilePrefix.SP, function=info.run)
    ene_dfile = file_.energy(_FilePrefix.SP)
    leaf_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.INPUT: inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile})

    return (trunk_ds, leaf_ds)


def high_spin(prefix):
    """ construct the high-spin, single-point filesystem [trunk/leaf]

    two layers with the following specifiers:
    1. []
    2. [method, basis, orb_type]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.high_spin_trunk(prefix)
    leaf_ds = dir_.high_spin_leaf(prefix, root_ds=trunk_ds)

    inp_dfile = file_.input_file(_FilePrefix.HS)
    inf_dfile = file_.information(_FilePrefix.HS, function=info.run)
    ene_dfile = file_.energy(_FilePrefix.HS)
    leaf_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.INPUT: inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile})

    return (trunk_ds, leaf_ds)


def scan(prefix):
    """ construct the scan filesystem

    three layers with the following specifiers:
    1. []
    2. [coo_names]
    3. [coo_names, coo_vals]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.scan_trunk(prefix)
    branch_ds = dir_.scan_branch(prefix, root_ds=trunk_ds)
    leaf_ds = dir_.scan_leaf(prefix, root_ds=branch_ds)

    vma_dfile = file_.vmatrix(_FilePrefix.SCAN)
    trunk_ds.add_data_files({
        _FileAttributeName.VMATRIX: vma_dfile})

    inf_dfile = file_.information(_FilePrefix.SCAN, function=info.scan_branch)
    traj_dfile = file_.trajectory(_FilePrefix.SCAN)
    branch_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.TRAJ: traj_dfile})

    geom_inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    grad_inf_dfile = file_.information(_FilePrefix.GRAD, function=info.run)
    hess_inf_dfile = file_.information(_FilePrefix.HESS, function=info.run)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    grad_dfile = file_.gradient(_FilePrefix.GRAD)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    hfreq_dfile = file_.harmonic_frequencies(_FilePrefix.HESS)
    leaf_ds.add_data_files({
        _FileAttributeName.GEOM_INFO: geom_inf_dfile,
        _FileAttributeName.GRAD_INFO: grad_inf_dfile,
        _FileAttributeName.HESS_INFO: hess_inf_dfile,
        _FileAttributeName.GEOM_INPUT: geom_inp_dfile,
        _FileAttributeName.GRAD_INPUT: grad_inp_dfile,
        _FileAttributeName.HESS_INPUT: hess_inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile,
        _FileAttributeName.GRAD: grad_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.HFREQ: hfreq_dfile})

    return (trunk_ds, branch_ds, leaf_ds)


def cscan(prefix):
    """ construct the constrained scan filesystem

    four layers with the following specifiers:
    1. []
    2. [coo_names]
    3. [coo_names, coo_vals]
    4. [coo_names, coo_vals, cons_coo_val_dct]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.cscan_trunk(prefix)
    branch1_ds = dir_.cscan_branch1(prefix, root_ds=trunk_ds)
    branch2_ds = dir_.cscan_branch2(prefix, root_ds=branch1_ds)
    leaf_ds = dir_.cscan_leaf(prefix, root_ds=branch2_ds)

    vma_dfile = file_.vmatrix(_FilePrefix.SCAN)
    trunk_ds.add_data_files({
        _FileAttributeName.VMATRIX: vma_dfile})

    inf_dfile = file_.information(_FilePrefix.SCAN, function=info.scan_branch)
    traj_dfile = file_.trajectory(_FilePrefix.SCAN)
    branch1_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.TRAJ: traj_dfile})

    geom_inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    grad_inf_dfile = file_.information(_FilePrefix.GRAD, function=info.run)
    hess_inf_dfile = file_.information(_FilePrefix.HESS, function=info.run)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    grad_dfile = file_.gradient(_FilePrefix.GRAD)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    hfreq_dfile = file_.harmonic_frequencies(_FilePrefix.HESS)
    leaf_ds.add_data_files({
        _FileAttributeName.GEOM_INFO: geom_inf_dfile,
        _FileAttributeName.GRAD_INFO: grad_inf_dfile,
        _FileAttributeName.HESS_INFO: hess_inf_dfile,
        _FileAttributeName.GEOM_INPUT: geom_inp_dfile,
        _FileAttributeName.GRAD_INPUT: grad_inp_dfile,
        _FileAttributeName.HESS_INPUT: hess_inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile,
        _FileAttributeName.GRAD: grad_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.HFREQ: hfreq_dfile})

    return (trunk_ds, branch1_ds, branch2_ds, leaf_ds)


def tau(prefix):
    """ construct the tau filesystem

    two layers with the following specifiers:
    1. []
    4. [tid]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.tau_trunk(prefix)
    leaf_ds = dir_.tau_leaf(prefix, root_ds=trunk_ds)

    vma_dfile = file_.vmatrix(_FilePrefix.TAU)
    inf_dfile = file_.information(_FilePrefix.TAU,
                                  function=info.tau_trunk)
    traj_dfile = file_.trajectory(_FilePrefix.TAU)
    trunk_ds.add_data_files({
        _FileAttributeName.VMATRIX: vma_dfile,
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.TRAJ: traj_dfile})

    geom_inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    grad_inf_dfile = file_.information(_FilePrefix.GRAD, function=info.run)
    hess_inf_dfile = file_.information(_FilePrefix.HESS, function=info.run)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    grad_dfile = file_.gradient(_FilePrefix.GRAD)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    hfreq_dfile = file_.harmonic_frequencies(_FilePrefix.HESS)
    leaf_ds.add_data_files({
        _FileAttributeName.GEOM_INFO: geom_inf_dfile,
        _FileAttributeName.GRAD_INFO: grad_inf_dfile,
        _FileAttributeName.HESS_INFO: hess_inf_dfile,
        _FileAttributeName.GEOM_INPUT: geom_inp_dfile,
        _FileAttributeName.GRAD_INPUT: grad_inp_dfile,
        _FileAttributeName.HESS_INPUT: hess_inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile,
        _FileAttributeName.GRAD: grad_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.HFREQ: hfreq_dfile})

    return (trunk_ds, leaf_ds)


def energy_transfer(prefix):
    """ construct the energy transfer filesystem [trunk/leaf]

    three layers with the following specifiers:
    1. []
    2. [ich, chg, mul]
    3. [ich, chg, mul, method, basis, orb_type]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.energy_transfer_trunk(prefix)
    branch_ds = dir_.energy_transfer_branch(prefix, root_ds=trunk_ds)
    leaf_ds = dir_.energy_transfer_leaf(prefix, root_ds=branch_ds)

    # inp_dfile = file_.input_file(_FilePrefix.LJ)
    inf_dfile = file_.information(
        _FilePrefix.LJ, function=info.lennard_jones)
    ene_dfile = file_.energy(_FilePrefix.LJ)
    eps_dfile = file_.lennard_jones_epsilon(_FilePrefix.LJ)
    sig_dfile = file_.lennard_jones_sigma(_FilePrefix.LJ)
    traj_dfile = file_.trajectory(_FilePrefix.LJ)

    trunk_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile})

    leaf_ds.add_data_files({
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.LJ_EPS: eps_dfile,
        _FileAttributeName.LJ_SIG: sig_dfile,
        _FileAttributeName.TRAJ: traj_dfile})

    return (trunk_ds, branch_ds, leaf_ds)


def reaction(prefix):
    """ construct the reaction filesystem

    two layers with the following specifiers:
    1. []
    2. [rxn_ichs, rxn_chgs, rxn_muls, ts_mul]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.reaction_trunk(prefix)
    leaf_ds = dir_.reaction_leaf(prefix, root_ds=trunk_ds)

    return (trunk_ds, leaf_ds)


def ts(prefix):
    """ construct the ts filesystem

    one layer without specifiers

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.ts_trunk(prefix)

    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    trunk_ds.add_data_files({
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile})

    return (trunk_ds,)


def direction(prefix):
    """ filesystem object for reaction direction

    one layer with the following specifiers: [forw]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    leaf_ds = dir_.direction_leaf(prefix)

    inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    inp_dfile = file_.input_file(_FilePrefix.GEOM)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)

    leaf_ds.add_data_files({
        _FileAttributeName.GEOM_INPUT: inp_dfile,
        _FileAttributeName.GEOM_INFO: inf_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile})

    return (leaf_ds,)


def run(prefix):
    """ construct the run filesystem

    two layers with the following specifiers:
    1. []
    2. [job]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.run_trunk(prefix)
    leaf_ds = dir_.run_leaf(prefix, root_ds=trunk_ds)

    inf_dfile = file_.information(_FilePrefix.RUN, function=info.run)
    inp_dfile = file_.input_file(_FilePrefix.RUN)
    out_dfile = file_.output_file(_FilePrefix.RUN)
    trunk_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile})
    leaf_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.INPUT: inp_dfile,
        _FileAttributeName.OUTPUT: out_dfile})

    return (trunk_ds, leaf_ds)


def subrun(prefix):
    """ construct the subrun filesystem

    one layer with the following specifiers: [macro_idx, micro_idx]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    leaf_ds = dir_.subrun_leaf(prefix)

    inf_dfile = file_.information(_FilePrefix.RUN, function=info.run)
    inp_dfile = file_.input_file(_FilePrefix.RUN)
    out_dfile = file_.output_file(_FilePrefix.RUN)
    leaf_ds.add_data_files({
        _FileAttributeName.INFO: inf_dfile,
        _FileAttributeName.INPUT: inp_dfile,
        _FileAttributeName.OUTPUT: out_dfile})

    return (leaf_ds,)


def build(prefix):
    """ construct the build filesystem

    two layers with the following specifiers:
    1. [head]
    2. [head, num]

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.build_trunk(prefix)
    leaf_ds = dir_.build_leaf(prefix, root_ds=trunk_ds)

    inp_dfile = file_.input_file(_FilePrefix.BUILD)
    out_dfile = file_.output_file(_FilePrefix.BUILD)
    leaf_ds.add_data_files({
        _FileAttributeName.INPUT: inp_dfile,
        _FileAttributeName.OUTPUT: out_dfile})

    return (trunk_ds, leaf_ds)


def _process_root_args(root_fs=None, top_ds_name=None):
    if root_fs is not None:
        root_fs = dict(root_fs)
        assert top_ds_name in root_fs
        top_dsdir = root_fs[top_ds_name].dir
    else:
        root_fs = {}
        top_dsdir = None
    return root_fs, top_dsdir
