# © 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

"""This script is called by the pyowa wizard to run an action.
"""

def app(name, placeholders, project_info):
    """Action running e.g. on value change or button push.

    Parameters
    ----------
    name : str
        Name of the object triggering the action.
    placeholders : dict
        Modifiable object values.
    project_info : dict
        Information about the optiSLang project (if available).

    Returns
    -------
    dict
        Modified placeholders object.
    """
    return placeholders
