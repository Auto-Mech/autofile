""" molecular graph transformations (representing reactions)
"""
import numbers
import yaml
from automol.graph._graph import full_isomorphism
from automol.graph._graph import add_bonds
from automol.graph._graph import remove_bonds


# old
def old_from_data(frm_bnd_keys, brk_bnd_keys):
    """ define a transformation from data
    """
    frm_bnd_keys = frozenset(map(frozenset, frm_bnd_keys))
    brk_bnd_keys = frozenset(map(frozenset, brk_bnd_keys))
    assert all(map(_is_bond_key, frm_bnd_keys))
    assert all(map(_is_bond_key, brk_bnd_keys))
    assert not frm_bnd_keys & brk_bnd_keys
    return (frm_bnd_keys, brk_bnd_keys)


def old_formed_bond_keys(tra):
    """ keys for bonds that are formed in the transformation
    """
    frm_bnd_keys, _ = tra
    return frm_bnd_keys


def old_broken_bond_keys(tra):
    """ keys for bonds that are broken in the transformation
    """
    _, brk_bnd_keys = tra
    return brk_bnd_keys


def old_string(tra):
    """ write the transformation to a string
    """
    def _encode_bond(bnd_key):
        atm1_key, atm2_key = bnd_key
        bnd_str = '{}-{}'.format(atm1_key+1, atm2_key+1)
        return bnd_str

    frm_bnd_keys = sorted(map(sorted, old_formed_bond_keys(tra)))
    brk_bnd_keys = sorted(map(sorted, old_broken_bond_keys(tra)))

    if any(frm_bnd_keys):
        frm_bnd_strs = list(map(_encode_bond, frm_bnd_keys))
    else:
        frm_bnd_strs = None

    if any(brk_bnd_keys):
        brk_bnd_strs = list(map(_encode_bond, brk_bnd_keys))
    else:
        brk_bnd_strs = None

    tra_dct = {'bonds formed': frm_bnd_strs,
               'bonds broken': brk_bnd_strs}

    tra_str = yaml.dump(tra_dct, default_flow_style=None, sort_keys=False)
    return tra_str


def old_from_string(tra_str):
    """ read the transformation from a string
    """
    def _decode_bond(bnd_str):
        atm1_key, atm2_key = map(int, bnd_str.split('-'))
        bnd_key = frozenset({atm1_key-1, atm2_key-1})
        return bnd_key

    tra_dct = yaml.load(tra_str, Loader=yaml.FullLoader)
    frm_bnd_strs = tra_dct['bonds formed']
    brk_bnd_strs = tra_dct['bonds broken']

    if frm_bnd_strs is not None:
        frm_bnd_keys = frozenset(map(_decode_bond, frm_bnd_strs))
    else:
        frm_bnd_keys = frozenset({})

    if brk_bnd_strs is not None:
        brk_bnd_keys = frozenset(map(_decode_bond, brk_bnd_strs))
    else:
        brk_bnd_keys = frozenset({})

    tra = old_from_data(frm_bnd_keys, brk_bnd_keys)

    return tra


# New
def from_data(rxn_class, frm_bnd_keys, brk_bnd_keys):
    """ define a transformation from data
    """
    frm_bnd_keys = frozenset(map(frozenset, frm_bnd_keys))
    brk_bnd_keys = frozenset(map(frozenset, brk_bnd_keys))
    assert all(map(_is_bond_key, frm_bnd_keys))
    assert all(map(_is_bond_key, brk_bnd_keys))
    assert not frm_bnd_keys & brk_bnd_keys
    return (rxn_class, frm_bnd_keys, brk_bnd_keys)


def reaction_class(tra):
    """ string describing the reaction class
    """
    rxn_class, _, _ = tra
    # assert par.is_reaction_class(rxn_class), (
    #     '{} is not an allowed reaction class'.format(rxn_class)
    # )
    return rxn_class


def formed_bond_keys(tra):
    """ keys for bonds that are formed in the transformation
    """
    _, frm_bnd_keys, _ = tra
    return frm_bnd_keys


def broken_bond_keys(tra):
    """ keys for bonds that are broken in the transformation
    """
    _, _, brk_bnd_keys = tra
    return brk_bnd_keys


def string(tra):
    """ write the transformation to a string
    """
    def _encode_bond(bnd_key):
        atm1_key, atm2_key = bnd_key
        bnd_str = '{}-{}'.format(atm1_key+1, atm2_key+1)
        return bnd_str

    rxn_class = reaction_class(tra)
    frm_bnd_keys = sorted(map(sorted, formed_bond_keys(tra)))
    brk_bnd_keys = sorted(map(sorted, broken_bond_keys(tra)))

    if any(frm_bnd_keys):
        frm_bnd_strs = list(map(_encode_bond, frm_bnd_keys))
    else:
        frm_bnd_strs = None

    if any(brk_bnd_keys):
        brk_bnd_strs = list(map(_encode_bond, brk_bnd_keys))
    else:
        brk_bnd_strs = None

    tra_dct = {'reaction class': rxn_class,
               'bonds formed': frm_bnd_strs,
               'bonds broken': brk_bnd_strs}

    tra_str = yaml.dump(tra_dct, sort_keys=False)
    return tra_str


def from_string(tra_str):
    """ read the transformation from a string
    """
    def _decode_bond(bnd_str):
        atm1_key, atm2_key = map(int, bnd_str.split('-'))
        bnd_key = frozenset({atm1_key-1, atm2_key-1})
        return bnd_key

    tra_dct = yaml.load(tra_str, Loader=yaml.FullLoader)
    rxn_class = tra_dct['reaction class']
    frm_bnd_strs = tra_dct['bonds formed']
    brk_bnd_strs = tra_dct['bonds broken']

    if frm_bnd_strs is not None:
        frm_bnd_keys = frozenset(map(_decode_bond, frm_bnd_strs))
    else:
        frm_bnd_keys = frozenset({})

    if brk_bnd_strs is not None:
        brk_bnd_keys = frozenset(map(_decode_bond, brk_bnd_strs))
    else:
        brk_bnd_keys = frozenset({})

    tra = from_data(rxn_class, frm_bnd_keys, brk_bnd_keys)

    return tra


def relabel(tra, atm_key_dct):
    """ relabel the atom keys in the transformation
    """
    def _relabel_bond_key(bnd_key):
        return frozenset(map(atm_key_dct.__getitem__, bnd_key))

    rxn_class = reaction_class(tra)
    frm_bnd_keys = list(map(_relabel_bond_key, formed_bond_keys(tra)))
    brk_bnd_keys = list(map(_relabel_bond_key, broken_bond_keys(tra)))

    return from_data(rxn_class, frm_bnd_keys, brk_bnd_keys)


def apply(tra, xgr):
    """ apply this transformation to a graph
    """
    brk_bnd_keys = old_broken_bond_keys(tra)
    frm_bnd_keys = old_formed_bond_keys(tra)
    # in case some bonds are broken *and* formed, we subtract the other set
    xgr = remove_bonds(xgr, brk_bnd_keys - frm_bnd_keys)
    xgr = add_bonds(xgr, frm_bnd_keys - brk_bnd_keys)
    return xgr


def _is_bond_key(obj):
    return (isinstance(obj, frozenset) and len(obj) == 2 and
            all(map(_is_atom_key, obj)))


def _is_atom_key(obj):
    return isinstance(obj, numbers.Integral)
