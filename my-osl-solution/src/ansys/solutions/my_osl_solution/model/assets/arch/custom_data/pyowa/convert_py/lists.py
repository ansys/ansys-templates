""" This file contains methods to convert simple python things into pyowa elemnts.

Copyright © 2021 ANSYS, Inc.

"""
from .. import (
        Empty,
        Number,
        Label,
        Text,
        Select,
        Checkbox,
        Table,
        )


class PyowaConvertError(Exception):
    pass


def convert_pydef_list_to_pyowa_table(rows, TableType=Table):
    """ Convert a list of list of python objects into a pyowa.Table containing pyowa elements.

        Parameters
        ----------
        rows: list
            A list of list of python classes.
            See convert_pydef_to_pyowa_element function to get more information.
        TableType: table type, optional
            The pyowa table type. Default is pyowa.Table.

        Returns
        -------
        pobject of type TableType

    """
    table = TableType()
    for i, row in enumerate(rows):
        for pydef in row:
            pyowa_element = convert_pydef_to_pyowa_element(pydef)
            table.append_child(i, pyowa_element)
    return table


def convert_pydef_to_pyowa_element(pydef):
    """ Converts a python object into a pyowa element according to the following rules:

        >>> ''            # str   -> pyowa.Empty()
        >>> 'my_label'    # str   -> pyowa.Label('my_label')
        >>> b'my_label'   # str   -> pyowa.Label('my_label').set_bold()
        >>> ['A', 'B']    # list  -> pyowa.Selection('A', ['A', 'B'])
        >>> (True,)       # tuple -> pyowa.Checkbox(True)
        >>> (1,)          # tuple -> pyowa.Number(1)
        >>> (2.2,)        # tuple -> pyowa.Number(2.2)
        >>> ('my_text',)  # tuple -> pyowa.Text('my_text')
        >>> (20, 0, 100)  # tuple -> pyowa.Number(20).set_bounds(0, 100)s

    """
    if isinstance(pydef, str):
        if not len(pydef):
            return Empty()
        return Label(pydef)
    elif _is_binary_str(pydef):
        text = pydef.decode()
        return Label(text).set_bold()
    elif isinstance(pydef, list):
        return Select(pydef[0], pydef)
    elif isinstance(pydef, tuple):
        return _pydef_tuple_to_pyowa_element(pydef)
    else:
        raise PyowaConvertError(str(pydef))


def _pydef_tuple_to_pyowa_element(pydef):
    if len(pydef) == 1:
        value = pydef[0]
        if _is_bool(value):
            return Checkbox(value)
        elif isinstance(value, int):
            return Number(pydef)
        elif isinstance(value, float):
            return Number(pydef)
        elif isinstance(value, str):
            return Text(pydef)
        else:
            raise PyowaConvertError(str(pydef))
    elif len(pydef) == 3:
        value, lb, ub = pydef
        # TODO: they have to be int or float
        return Number(value).set_bounds(lb, ub)
    else:
        raise PyowaConvertError(str(pydef))


def _is_bool(value):
    return str(value).lower() in ['true', 'false']


def _is_binary_str(value):
    return isinstance(value, (bytes, bytearray))
