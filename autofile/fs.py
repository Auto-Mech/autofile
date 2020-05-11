"""
autofile.fs
***********

Each function in this module returns a tuple of autofile.model.DataSeries
objects for interacting with successive layers in a file system. Below is a
tutorial script that you may want to follow along with to get a grasp of how it
works.

Create a species filesystem at the prefix '.' (current directory).
>>> import autofile
>>> fs = autofile.fs.species('.')

`fs` is simply a tuple of two directory managers, one for the trunk directory
and one for the leaf directory.

To begin, check whether the trunk directory exists.
>>> fs[0].exists([])
False

Since it doesn't exist, create it.
>>> fs[0].create([])

Now, we will find that it does exist.
>>> fs[0].exists([])
True

The empty list argument to each of these functions is the sequence of "locator
values" for accessing this directory.  The species trunk directory doesn't take
any locator values, so the list is empty.

We can print the path the this trunk directory as follows.
>>> fs[0].path([])
'/home/avcopan/SPC'

Obviously, the path on your system will be different.

Now, we can create the species leaf directories, which go inside the trunk
directory.  The manager for the leaf directories is the second (and final)
element of the tuple.

Let's create some directories for atoms.
>>> fs[-1].create(['InChI=1S/H', 0, 2])
>>> fs[-1].create(['InChI=1S/He', 0, 1])
>>> fs[-1].create(['InChI=1S/O', 0, 3])
>>> fs[-1].create(['InChI=1S/O', 0, 1])

We can see that the species leaf directory takes three locator values: 1. the
inchi, 2. the charge, and 3. the multiplicity.  We need these three values
every time we want to access the file for a particular species.

Note that since fs is simply a tuple of two elements, we can access the last
element as either fs[1] or fs[-1].

Let's take a look at the paths for each leaf directory:
>>> fs[-1].path(['InChI=1S/H', 0, 2])
'/home/avcopan/SPC/H/YZCKVEUIGOORGS/0/2/UHFFFAOYSA-N'
>>> fs[-1].path(['InChI=1S/He', 0, 1])
'/home/avcopan/SPC/He/SWQJXJOGLNCZEY/0/1/UHFFFAOYSA-N'
>>> fs[-1].path(['InChI=1S/O', 0, 3])
'/home/avcopan/SPC/O/QVGXLLKOCUKJST/0/3/UHFFFAOYSA-N'
>>> fs[-1].path(['InChI=1S/O', 0, 1])
'/home/avcopan/SPC/O/QVGXLLKOCUKJST/0/1/UHFFFAOYSA-N'

Note that there is no correspondence between the number of locators and the
number of directories.

Finally, we can create a theory directory manager inside a given species
directory.
>>> pfx = fs[-1].path(['InChI=1S/H', 0, 2])
>>> pfx
'/home/avcopan/SPC/H/YZCKVEUIGOORGS/0/2/UHFFFAOYSA-N'
>>> tfs = autofile.fs.theory(pfx)

The theory filesystem has only one layer, which can be accessed using either 0
or -1 for the index, and takes method, basis, and orbital type as its locator
values.
>>> tfs[-1].create(['b3lyp', '6-31g*', 'U'])
>>> tfs[-1].create(['b3lyp', '6-31g*', 'R'])
>>> tfs[-1].path(['b3lyp', '6-31g*', 'U'])
'/home/avcopan/SPC/H/YZCKVEUIGOORGS/0/2/UHFFFAOYSA-N/ezvlpJU'
>>> tfs[-1].path(['b3lyp', '6-31g*', 'R'])
'/home/avcopan/SPC/H/YZCKVEUIGOORGS/0/2/UHFFFAOYSA-N/ezvlpJR'

The theory directory manager allows for the reading and writing of various
files within a given directory. One does this through the file attribute.
>>> tfs[-1].file
namespace(energy=<...>, geometry=<...>, hessian=<...>, zmatrix=<...>)

The file attribute is a namespace of several file I/O managers. I have cut out
the object identifiers above to make the printed value more readable, but they
are all autofile.system.model.DataSeriesFile objects.

Tip: If you want a readable print-out of what the files are in a given layer,
you can use the following.
>>> tfs[-1].file.__dict__.keys()
dict_keys(['energy', 'geometry', 'hessian', 'zmatrix'])

Otherwise, the files for each layer are also listed in the function docstrings
for this module.

As an example, let us do some I/O with an energy file.

First, we'll check that the file doesn't exist yet.
>>> tfs[-1].file.energy.exists(['b3lyp', '6-31g*', 'U'])
False

Notice that we need the same three specifiers! The argument doesn't change.

Let's write a made-up energy value to the file.
>>> tfs[-1].file.energy.write(5.7, ['b3lyp', '6-31g*', 'U'])

Now the file exists.
>>> tfs[-1].file.energy.exists(['b3lyp', '6-31g*', 'U'])
True

The path to this file is as follows.
>>> tfs[-1].file.energy.path(['b3lyp', '6-31g*', 'U'])
'/home/avcopan/SPC/H/YZCKVEUIGOORGS/0/2/UHFFFAOYSA-N/ezvlpJU/geom.ene'

We can confirm that our made-up value was correctly stored by reading it back
out.
>>> tfs[-1].file.energy.read(['b3lyp', '6-31g*', 'U'])
5.7
"""
from autofile.system import file_
from autofile.system import info
from autofile.system import dir_


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
    IRC = 'irc'


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
    IRC_INFO = 'irc_info'
    GEOM_INPUT = 'geometry_input'
    GRAD_INPUT = 'gradient_input'
    HESS_INPUT = 'hessian_input'
    VPT2_INPUT = 'vpt2_input'
    IRC_INPUT = 'irc_input'
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
    """ construct the species filesystem (2 layers)

    specifiers:
        0 - []
                (no files)
        1 - [ich, chg, mul]
                (no files)

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.species_trunk(prefix)
    leaf_ds = dir_.species_leaf(prefix, root_ds=trunk_ds)
    return (trunk_ds, leaf_ds)


def theory(prefix):
    """ construct the theory filesystem (1 layer)

    specifiers:
        0 - [method, basis, orb_type]
                files:
                - energy
                - geometry
                - hessian
                - zmatrix

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
    """ construct the conformer filesystem (2 layers)

    specifiers:
        0 - []
                files:
                - vmatrix
                - info
                - energy
                - trajectory
        1 - [cid]
                files:
                - geometry_info
                - gradient_info
                - hessian_info
                - geometry_input
                - gradient_input
                - hessian_input
                - energy
                - geometry
                - zmatrix
                - gradient
                - hessian
                - harmonic_frequencies
                - vpt2_info
                - vpt2_input
                - anharmonic_frequencies
                - anharmonic_zpve
                - anharmonicity_matrix
                - vibro_rot_alpha_matrix
                - quartic_centrifugal_dist_consts

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
    # need addl vpt2 info file, one for job status and other for fermi
    vpt2_inf_dfile = file_.information(_FilePrefix.VPT2, function=info.vpt2)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    vpt2_inp_dfile = file_.input_file(_FilePrefix.VPT2)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    grad_dfile = file_.gradient(_FilePrefix.GRAD)
    hess_dfile = file_.hessian(_FilePrefix.HESS)
    hfreq_dfile = file_.harmonic_frequencies(_FilePrefix.HESS)
    anhfreq_dfile = file_.anharmonic_frequencies(_FilePrefix.VPT2)
    anhzpve_dfile = file_.anharmonic_zpve(_FilePrefix.VPT2)
    xmat_dfile = file_.anharmonicity_matrix(_FilePrefix.VPT2)
    vibrot_mat_dfile = file_.vibro_rot_alpha_matrix(_FilePrefix.VPT2)
    centrif_dist_dfile = file_.quartic_centrifugal_dist_consts(
        _FilePrefix.VPT2)

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
    """ construct the single-point filesystem (2 layers)

    specifiers:
        0 - []
                (no files)
        1 - [method, basis, orb_type]
                files:
                - info
                - input
                - energy

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
    """ construct the high-spin, single-point filesystem (2 layers)

    specifiers:
        0 - []
                (no files)
        1 - [method, basis, orb_type]
                files:
                - info
                - input
                - energy

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
    """ construct the scan filesystem (3 layers)

    three layers with the following specifiers:
        0 - []
                files:
                - vmatrix
        1 - [coo_names]
                files:
                - info
                - trajectory
        2 - [coo_names, coo_vals]
                files:
                - geometry_info
                - gradient_info
                - hessian_info
                - irc_info
                - geometry_input
                - gradient_input
                - hessian_input
                - irc_input
                - energy
                - geometry
                - zmatrix
                - gradient
                - hessian
                - harmonic_frequencies

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

    # Need an irc file in the branch!
    # Need an run irc file in the forward and backward direction

    geom_inf_dfile = file_.information(_FilePrefix.GEOM, function=info.run)
    grad_inf_dfile = file_.information(_FilePrefix.GRAD, function=info.run)
    hess_inf_dfile = file_.information(_FilePrefix.HESS, function=info.run)
    irc_inf_dfile = file_.information(_FilePrefix.IRC, function=info.run)
    geom_inp_dfile = file_.input_file(_FilePrefix.GEOM)
    grad_inp_dfile = file_.input_file(_FilePrefix.GRAD)
    hess_inp_dfile = file_.input_file(_FilePrefix.HESS)
    irc_inp_dfile = file_.input_file(_FilePrefix.IRC)
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
        _FileAttributeName.IRC_INFO: irc_inf_dfile,
        _FileAttributeName.GEOM_INPUT: geom_inp_dfile,
        _FileAttributeName.GRAD_INPUT: grad_inp_dfile,
        _FileAttributeName.HESS_INPUT: hess_inp_dfile,
        _FileAttributeName.IRC_INPUT: irc_inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile,
        _FileAttributeName.GRAD: grad_dfile,
        _FileAttributeName.HESS: hess_dfile,
        _FileAttributeName.HFREQ: hfreq_dfile})

    return (trunk_ds, branch_ds, leaf_ds)


def cscan(prefix):
    """ construct the constrained scan filesystem (4 layers)

    specifiers:
        0 - []
                files:
                - vmatrix
        1 - [coo_names]
                files:
                - info
                - trajectory
        2 - [coo_names, coo_vals]
        3 - [coo_names, coo_vals, cons_coo_val_dct]
                files:
                - geometry_info
                - gradient_info
                - hessian_info
                - geometry_input
                - gradient_input
                - hessian_input
                - energy
                - geometry
                - zmatrix
                - gradient
                - hessian
                - harmonic_frequencies

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
    """ construct the tau filesystem (2 layers)

    specifiers:
        0 - []
                files:
                - vmatrix
                - info
                - trajectory
        0 - [tid]
                files:
                - geometry_info
                - gradient_info
                - hessian_info
                - geometry_input
                - gradient_input
                - hessian_input
                - energy
                - geometry
                - zmatrix
                - gradient
                - hessian
                - harmonic_frequencies

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
    """ construct the energy transfer filesystem (3 layers)

    specifiers:
        0 - []
                files:
                - info
        1 - [ich, chg, mul]
                (no files)
        2 - [ich, chg, mul, method, basis, orb_type]
                files:
                - energy
                - lennard_jones_epsilon
                - lennard_jones_sigma
                - trajectory

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
    """ construct the reaction filesystem (2 layers)

    specifiers:
        0 - []
                (no files)
        1 - [rxn_ichs, rxn_chgs, rxn_muls, ts_mul]
                (no files)

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.reaction_trunk(prefix)
    leaf_ds = dir_.reaction_leaf(prefix, root_ds=trunk_ds)

    return (trunk_ds, leaf_ds)


def transition_state(prefix):
    """ construct the ts filesystem (1 layer)

    specifiers:
        0 - []
                files:
                - energy
                - geometry
                - zmatrix

    :param prefix: sets the path where this filesystem will sit
    :type prefix: str
    """
    trunk_ds = dir_.transition_state_trunk(prefix)

    geom_dfile = file_.geometry(_FilePrefix.GEOM)
    ene_dfile = file_.energy(_FilePrefix.GEOM)
    zmat_dfile = file_.zmatrix(_FilePrefix.GEOM)
    trunk_ds.add_data_files({
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile})

    return (trunk_ds,)


def direction(prefix):
    """ filesystem object for reaction direction (1 layer)

    specifiers:
        0 - [forw]
                files:
                - geometry_info
                - geometry_input
                - energy
                - geometry
                - zmatrix

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
        _FileAttributeName.GEOM_INFO: inf_dfile,
        _FileAttributeName.GEOM_INPUT: inp_dfile,
        _FileAttributeName.ENERGY: ene_dfile,
        _FileAttributeName.GEOM: geom_dfile,
        _FileAttributeName.ZMAT: zmat_dfile})

    return (leaf_ds,)


def run(prefix):
    """ construct the run filesystem (2 layers)

    specifiers:
        0 - []
                files:
                - info
        1 - [job]
                files:
                - info
                - input
                - output

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
    """ construct the subrun filesystem (1 layer)

    specifiers:
        0 - [macro_idx, micro_idx]
                files:
                - info
                - input
                - output

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
    """ construct the build filesystem (2 layers)

    specifiers:
        0 - [head]
                (no files)
        1 - [head, num]
                files:
                - input
                - output

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
