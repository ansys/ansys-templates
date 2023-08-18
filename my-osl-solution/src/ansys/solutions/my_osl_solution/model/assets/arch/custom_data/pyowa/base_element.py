""" Some metaclasses for elements.

Copyright © 2021 ANSYS, Inc.

"""
import abc
import json
from . import arg


class BaseElementError(Exception):
    pass


class BaseElement:
    """ The base class for all elements.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, id_, type_):
        self.id = id_
        self.type = type_
        self.data = {}

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.id}")'

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    @arg.check_type(path=(str, tuple))
    def add_property(self, path, value):
        """ Add/modify a value of an entry in data.

            Parameter
            ---------
            path: tuple or str
                tuple with elements indicating the path to the entry in data.
            value: any
                value of the entry to be added/modified.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> label_color_property_path = ('style', 'color')
            >>> label_color = 'blue'
            >>> my_label.add_property(label_color_property_path, label_color)
        """

        if not isinstance(path, (list, tuple)):
            path = [path]
        entry_names = path[:-1]
        last_entry_name = path[-1]

        entry = self.data
        for name in entry_names:
            if name not in entry:
                entry[name] = {}
            entry = entry[name]
        entry[last_entry_name] = value

    @arg.check_type(path=(str, tuple))
    def get_property(self, path):
        """ Return a value of an entry in data.

            Parameter
            ---------
            path: tuple, str
                tuple with elements indicating the path to the entry in data.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> label_color_property_path = ('style', 'color')
            >>> label_color = my_label.get_property(label_color_property_path)
        """

        if not isinstance(path, (list, tuple)):
            path = [path]

        entry = self.data
        for name in path:
            if name not in entry:
                return None
            entry = entry[name]
        return entry

    @arg.check_type(color=str)
    def set_color(self, color):
        """ Set the foreground/text color for the element.

            Parameter
            ---------
            color: str
                The required color for the foreground/text. Can be a standard HTML color or the corresponding hex.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label.set_color('blue')
        """
        entry_path = ('style', 'color')
        self.add_property(entry_path, color)

    @arg.check_type(color=str)
    def set_background_color(self, color):
        """ Set the background color for the element.

            Parameter
            ---------
            color: str
                The required color for the background. Can be a standard HTML color or the corresponding hex.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label.set_background_color('blue')
        """
        entry_path = ('style', 'backgroundColor')
        self.add_property(entry_path, color)

    @arg.check_type(top=int, bottom=int, left=int, right=int)
    def set_margin_in_px(self, top=0, bottom=0, left=0, right=0):
        """ Set the margin in pixels for the webpage element.

            Parameter
            --------
            top: int, optional.
                Set the top margin for the element. Default is 0.
            bottom: int, optional.
                Set the bottom margin for the element. Default is 0.
            left: int, optional.
                Set the left margin for the element. Default is 0.
            right: int, optional.
                Set the right margin for the element. Default is 0.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label.set_margin_in_px(top=30, bottom=30, left=50)
        """
        margin = f'{top}px {right}px {bottom}px {left}px'
        self.add_property(('style', 'margin'), margin)

    def show_border(self):
        """ Display the border of the webpage element.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label.show_border()
        """
        self.add_property(('style', 'border'), '2px solid black')

    @arg.check_type(top=int, bottom=int, left=int, right=int)
    def set_padding_in_px(self, top=0, bottom=0, left=0, right=0):
        """ Set the padding in pixels for the webpage element.

            Parameter
            --------
            top: int, optional.
                Set the top padding for the element. Default is 0.
            bottom: int, optional.
                Set the bottom padding for the element. Default is 0.
            left: int, optional.
                Set the left padding for the element. Default is 0.
            right: int, optional.
                Set the right padding for the element. Default is 0.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label.set_padding_in_px(top=30, bottom=30, left=50)
        """
        padding = f'{top}px {right}px {bottom}px {left}px'
        self.add_property(('style', 'padding'), padding)

    def _has_placeholder(self):
        # Check if the element is a placeholder
        return False

    def to_json(self):
        """ Return the json representation of the webpage element.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Label('Hello World!')
            >>> my_label_json = my_label.to_json()
        """
        return {
                'id': self.id,
                'type': self.type,
                'data': self.data,
                }


class BaseElementPlaceholder(BaseElement):
    """ The base class for modifiable elements.

        See Also
        --------
        BaseElement: The base class for all elements.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, id_, type_):
        super().__init__(id_, type_)
        self.placeholder_name = None
        self.placeholder_value = None
        self.placeholder_scripts = []
        self.placeholder_readonly = False
        self.placeholder_table = False
        self.placeholder_hidden = False

    def _has_placeholder(self):
        return self.placeholder_name is not None

    def _set_placeholder(self, name, value=None):
        self.placeholder_name = name
        self.placeholder_value = value

    @arg.check_type(action_script=str)
    def set_action_script(self, action_script):
        """ Assign an python action script to be executed after the element is attached to the webpage

            Parameter
            --------
            action_script: str.
                tail of the python file path.

            Example
            -------
            >>> import pyowa
            >>> result_label = pyowa.ButtonFileUpload()
            >>> result_label.set_action_script('run_me.py')
        """
        self.placeholder_scripts.append(action_script)

    @arg.check_type(action_scripts=list)
    def set_action_scripts(self, action_scripts):
        """ Assign python action scripts to be executed after the element is attached to the webpage

            Parameter
            --------
            action_scripts: list.
                list containing tail of the python file paths.

            Example
            -------
            >>> import pyowa
            >>> result_label = pyowa.ButtonFileUpload()
            >>> result_label.set_action_scripts(['run_me1.py', 'run_me2.py'])
        """
        self.placeholder_scripts.extend(action_scripts)

    @arg.check_type(readonly=bool)
    def set_readonly(self, readonly=True):
        """ Set the element to be modifiable/unmodifiable

            Parameter
            ---------
            readonly: bool, optional.
                True makes the element unmodifiable. False makes the element modifiable. Default is True.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number.set_readonly()
        """
        self.placeholder_readonly = readonly
        return self

    def set_hidden(self):
        """ Hide webpage element.

            Example
            -------
            >>> import pyowa
            >>> my_label = pyowa.Number(5)
            >>> my_label.set_hidden()
        """
        self.placeholder_hidden = True

    def _set_as_table(self, table=True):
        self.placeholder_table = table
        return self

    def get_placeholder_value(self):
        """ Return a dict with the placeholder related information including but not limited to value and readonly of
            the element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number_placeholder_value = number.get_placeholder_value()
        """

        placeholder_value = {'value': self.placeholder_value,
                             'readOnly': self.placeholder_readonly,
                             'hidden': self.placeholder_hidden}
        if self.placeholder_scripts:
            placeholder_value['actions'] = self.placeholder_scripts
        if self.placeholder_table:
            placeholder_value['table'] = self.placeholder_table
        return placeholder_value

    def get_placeholder_name(self):
        """ Return the placeholder name of the element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number_placeholder_name = number.get_placeholder_name()
        """
        return self.placeholder_name

    def to_json(self):
        """ Return the json representation of the webpage element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number_json = number.to_json()
        """
        json_repr = super().to_json()
        json_repr['placeholder'] = self.get_placeholder_name()
        return json_repr


class BaseContainer(BaseElement):
    """ The base class for container elements.

        See Also
        --------
        BaseElement: The base class for all elements.
    """

    def __init__(self, id_, type_):
        super().__init__(id_, type_)
        self.childs = []
        self.placeholders = {}

    def _has_placeholder(self):
        return len(self.placeholders)

    @arg.check_type(child=BaseElement)
    def append_child(self, child):
        """ Append a child element to the container.

            Parameter
            ---------
            child: BaseElement.
                Any element of type BaseElement or a child of BaseElement.

            Example
            -------
            >>> import pyowa
            >>> section_horizontal_bordered = pyowa.SectionHorizontalBordered('MySection')
            >>> section_horizontal_bordered.append_child(pyowa.Label('Label1'))
        """
        self.childs.append(child)
        if not child._has_placeholder():
            return

        if hasattr(child, 'placeholder_name'):
            name = child.get_placeholder_name()
            value = child.get_placeholder_value()
            self.placeholders[name] = value
        else:
            self.placeholders.update(child.placeholders)

    @staticmethod
    def _childs_to_json(childs):
        return [c.to_json() for c in childs]

    def to_json(self):
        """ Return the json representation of the webpage element.

            Example
            -------
            >>> import pyowa
            >>> section_horizontal_bordered = pyowa.SectionHorizontalBordered('MySection')
            >>> section_horizontal_bordered.append_child(pyowa.Label('Label1'))
            >>> section_horizontal_bordered_json = section_horizontal_bordered.to_json()
        """
        json_repr = super().to_json()
        json_repr['childs'] = self._childs_to_json(self.childs)
        return json_repr
