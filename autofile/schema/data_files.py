""" DataFiles
"""
from autofile import model
import autofile.data_types
import autofile.info


def information(file_prefix, function=None):
    """ information DataFile

    :param function: optional information-generator function, for checking the
        function signature against the information object
    :type function: callable
    """
    def writer_(inf_obj):
        if function is not None:
            assert autofile.info.matches_function_signature(inf_obj, function)
        inf_str = autofile.data_types.swrite.information(inf_obj)
        return inf_str

    def reader_(inf_str):
        inf_obj = autofile.data_types.sread.information(inf_str)
        if function is not None:
            assert autofile.info.matches_function_signature(inf_obj, function)
        return inf_obj

    name = autofile.data_types.name.information(file_prefix)
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def locator(file_prefix, map_dct_, loc_keys):
    """ locator DataFile

    Specifiers are stored in information files according to `map_dct_` and read
    back out according to `loc_keys_`. The file may contain auxiliary
    information (such as SMILES along with InChI), but for the read to work it
    must contain each locator value.

    :param map_dct_: Maps on the locator list to the values stored in the
        information file, by key.
    :type map_dct_: dict[key: callable]
    :param loc_keys: Keys to the original locator values.
    :type loc_keys: tuple[str]
    """
    def writer_(locs):
        inf_dct = {key: map_(locs) for key, map_ in map_dct_.items()}
        inf_obj = autofile.info.object_(inf_dct)
        return autofile.data_types.swrite.information(inf_obj)

    def reader_(inf_str):
        inf_obj = autofile.data_types.sread.information(inf_str)
        inf_dct = dict(inf_obj)
        return list(map(inf_dct.__getitem__, loc_keys))

    name = autofile.data_types.name.information(file_prefix)
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def input_file(file_prefix):
    """ generate input file DataFile
    """
    name = autofile.data_types.name.input_file(file_prefix)
    return model.DataFile(name=name)


def output_file(file_prefix):
    """ generate output file DataFile
    """
    name = autofile.data_types.name.output_file(file_prefix)
    return model.DataFile(name=name)


def energy(file_prefix):
    """ generate energy DataFile
    """
    name = autofile.data_types.name.energy(file_prefix)
    writer_ = autofile.data_types.swrite.energy
    reader_ = autofile.data_types.sread.energy
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def geometry(file_prefix):
    """ generate geometry DataFile
    """
    name = autofile.data_types.name.geometry(file_prefix)
    writer_ = autofile.data_types.swrite.geometry
    reader_ = autofile.data_types.sread.geometry
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def gradient(file_prefix):
    """ generate gradient DataFile
    """
    name = autofile.data_types.name.gradient(file_prefix)
    writer_ = autofile.data_types.swrite.gradient
    reader_ = autofile.data_types.sread.gradient
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def hessian(file_prefix):
    """ generate hessian DataFile
    """
    name = autofile.data_types.name.hessian(file_prefix)
    writer_ = autofile.data_types.swrite.hessian
    reader_ = autofile.data_types.sread.hessian
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def harmonic_frequencies(file_prefix):
    """ generate harmonic_frequencies DataFile
    """
    name = autofile.data_types.name.harmonic_frequencies(file_prefix)
    writer_ = autofile.data_types.swrite.harmonic_frequencies
    reader_ = autofile.data_types.sread.harmonic_frequencies
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def anharmonic_frequencies(file_prefix):
    """ generate anharmonic_frequencies DataFile
    """
    name = autofile.data_types.name.anharmonic_frequencies(file_prefix)
    writer_ = autofile.data_types.swrite.anharmonic_frequencies
    reader_ = autofile.data_types.sread.anharmonic_frequencies
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def anharmonic_zpve(file_prefix):
    """ generate anharmonic_zpve DataFile
    """
    name = autofile.data_types.name.anharmonic_zpve(file_prefix)
    writer_ = autofile.data_types.swrite.anharmonic_zpve
    reader_ = autofile.data_types.sread.anharmonic_zpve
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def anharmonicity_matrix(file_prefix):
    """ generate anharmonicity matrix DataFile
    """
    name = autofile.data_types.name.anharmonicity_matrix(file_prefix)
    writer_ = autofile.data_types.swrite.anharmonicity_matrix
    reader_ = autofile.data_types.sread.anharmonicity_matrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def vibro_rot_alpha_matrix(file_prefix):
    """ generate vibro_rot_alpha matrix DataFile
    """
    name = autofile.data_types.name.vibro_rot_alpha_matrix(file_prefix)
    writer_ = autofile.data_types.swrite.vibro_rot_alpha_matrix
    reader_ = autofile.data_types.sread.vibro_rot_alpha_matrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def quartic_centrifugal_dist_consts(file_prefix):
    """ generate vibro_rot_alpha matrix DataFile
    """
    name = (
        autofile.data_types.name.quartic_centrifugal_dist_consts(file_prefix))
    writer_ = autofile.data_types.swrite.quartic_centrifugal_dist_consts
    reader_ = autofile.data_types.sread.quartic_centrifugal_dist_consts
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def zmatrix(file_prefix):
    """ generate zmatrix DataFile
    """
    name = autofile.data_types.name.zmatrix(file_prefix)
    writer_ = autofile.data_types.swrite.zmatrix
    reader_ = autofile.data_types.sread.zmatrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def vmatrix(file_prefix):
    """ generate vmatrix DataFile
    """
    name = autofile.data_types.name.vmatrix(file_prefix)
    writer_ = autofile.data_types.swrite.vmatrix
    reader_ = autofile.data_types.sread.vmatrix
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def trajectory(file_prefix):
    """ generate trajectory DataFile
    """
    name = autofile.data_types.name.trajectory(file_prefix)
    writer_ = autofile.data_types.swrite.trajectory
    reader_ = _not_implemented
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def transformation(file_prefix):
    """ generate transformation DataFile
    """
    name = autofile.data_types.name.transformation(file_prefix)
    writer_ = autofile.data_types.swrite.transformation
    reader_ = autofile.data_types.sread.transformation
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def lennard_jones_epsilon(file_prefix):
    """ generate lennard_jones_epsilon DataFile
    """
    name = autofile.data_types.name.lennard_jones_epsilon(file_prefix)
    writer_ = autofile.data_types.swrite.lennard_jones_epsilon
    reader_ = autofile.data_types.sread.lennard_jones_epsilon
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


def lennard_jones_sigma(file_prefix):
    """ generate lennard_jones_sigma DataFile
    """
    name = autofile.data_types.name.lennard_jones_sigma(file_prefix)
    writer_ = autofile.data_types.swrite.lennard_jones_sigma
    reader_ = autofile.data_types.sread.lennard_jones_sigma
    return model.DataFile(name=name, writer_=writer_, reader_=reader_)


# helpers
def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError
