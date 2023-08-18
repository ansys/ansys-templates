""" The main wizard page..

Copyright © 2021 ANSYS, Inc.

"""
import os
import json

from .base_element import BaseContainer


PYOWA_VERSION = "21.R1.1"


class PageWizard(BaseContainer):
    """ The <div> main page container class.

        Parameters
        ----------
        title: str, optional
            The page title. Default value is no title.

        Example
        -------
        >>> import pyowa
        >>> my_label = pyowa.Label('A first label')
        >>> my_page = pyowa.Page('My page title')
        >>> my_page.append_child(my_label)

        See Also
        --------
        BaseContainer: The base class for container elements.
    """

    def __init__(self, title=''):
        super().__init__('page', 'page')
        self.add_property('version', PYOWA_VERSION)
        self.add_property('title', title)
        self.placeholder_scripts = []

    def to_json(self):
        """ Return the json representation of the
        """
        placeholders = self.placeholders
        placeholders['page'] = {'actions': self.placeholder_scripts}

        json_repr = super().to_json()
        json_repr['placeholders'] = placeholders
        return json_repr

    def write_pyowa_file(self, pyowa_filename):
        """ Write the json representation of a page as a json file

            Parameter
            ---------
            pyowa_filename: str
                name for the json file where the json representation of the page will be dumped.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('A first label')
            >>> my_page = pyowa.Page('My page title')
            >>> my_page.append_child(my_label)
            >>> my_page.write_pyowa_file('my_page.json')
        """
        wizard_path = os.path.join(os.getcwd(), pyowa_filename)
        with open(wizard_path, 'w') as f:
            json.dump(self.to_json(), f, indent=4)

    def set_action_script(self, action_script):
        """ Set a python script that will be run after the page is loaded.

            Parameter
            ---------
            action_script: str.
                The tail of the python file path saved in the wizard directory.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('A first label')
            >>> my_page = pyowa.Page('My page title')
            >>> my_page.append_child(my_label)
            >>> my_page.set_action_script('my_python_script.py')
        """
        self.placeholder_scripts.append(action_script)

    def set_action_scripts(self, action_scripts):
        """ Set python scripts that will be run after the page is loaded.

            Parameter
            ---------
            action_script: list.
                list of tail of the python file paths saved in the wizard directory.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('A first label')
            >>> my_page = pyowa.Page('My page title')
            >>> my_page.append_child(my_label)
            >>> my_page.set_action_script(['my_python_script1.py', 'my_python_script2.py'])
        """
        self.placeholder_scripts.extend(action_scripts)


class PageMonitoring(PageWizard):
    pass
