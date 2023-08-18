""" This module contains all container elements, which can hold other elements.

Copyright © 2021 ANSYS, Inc.

"""
from .base_element import BaseContainer, BaseElementPlaceholder, BaseElement
from .elements import Label, Number
from . import arg


class SectionHorizontal(BaseContainer):
    """ An invisible section <div> to add elements from left to right.

        Example
        -------
        >>> import pyowa
        >>> section_horizontal = pyowa.SectionHorizontal()
        >>> section_horizontal.append_child(pyowa.Label('Label1'))
        >>> section_horizontal.append_child(pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        SectionHorizontal._cnt += 1
        type_ = 'section_horizontal'
        id_ = f'{type_}_{SectionHorizontal._cnt}'
        super().__init__(id_, type_)

    def set_hidden(self):
        self.add_property(('style', 'display'), 'none')


class SectionVertical(BaseContainer):
    """ An invisible section <div> to add elements from top to bottom.

        Example
        -------
        >>> import pyowa
        >>> section_vertical = pyowa.SectionVertical()
        >>> section_vertical.append_child(pyowa.Label('Label1'))
        >>> section_vertical.append_child(pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        SectionVertical._cnt += 1
        type_ = 'section_vertical'
        id_ = f'{type_}_{SectionVertical._cnt}'
        super().__init__(id_, type_)

    def set_hidden(self):
        self.add_property(('style', 'display'), 'none')


class SectionHorizontalBordered(BaseContainer):
    """ A visible section inside a <div> to add elements from left to right.

        Parameter
        ---------
        name: str, optional
            The name of the section. Default is no name.

        Example
        -------
        >>> import pyowa
        >>> section_horizontal_bordered = pyowa.SectionHorizontalBordered('MySection')
        >>> section_horizontal_bordered.append_child(pyowa.Label('Label1'))
        >>> section_horizontal_bordered.append_child(pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    @arg.check_type(name=str)
    def __init__(self, name=''):
        SectionHorizontalBordered._cnt += 1
        type_ = 'section_horizontal_bordered'
        id_ = f'{type_}_{SectionHorizontalBordered._cnt}'
        super().__init__(id_, type_)
        # self.add_property('accented', True)
        if name:
            self.add_property('title', name)

    def set_hidden(self):
        self.add_property(('style', 'display'), 'none')


class SectionExpandable(BaseContainer):
    """ A hidden container with/without title that can be expanded/collapsed with a click

        Parameter
        ---------
            title: str, optional. Default is no title
                the title for the expandable container
            initial_state: bool, optional. Default is False
                intial state of the container. false --> collapsed, true --> expanded

        Example
        -------
            >>> import pyowa
            >>> new_expandable = pyowa.SectionExpandable()
            >>> new_expandable.append_child(pyowa.Label('Label1'))
            >>> new_expandable.append_child(pyowa.Label('Label2'))
    """

    _cnt = 0

    def __init__(self, title='', intitial_state=False):
        SectionExpandable._cnt += 1
        type_ = 'section_expandable'
        id_ = f'{type_}_{SectionExpandable._cnt}'
        super().__init__(id_, type_)
        self.add_property('initial_state', intitial_state)
        if title:
            self.set_title(title)

    def set_title(self, title):
        self.add_property('title', title)


class ListOrdered(BaseContainer):
    """ An ordered list <ol> to add elements.

        Example
        -------
        >>> import pyowa
        >>> list_ordered = pyowa.ListOrdered()
        >>> list_ordered.append_child(pyowa.Label('Label1'))
        >>> list_ordered.append_child(pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        ListOrdered._cnt += 1
        type_ = 'list_ordered'
        id_ = f'{type_}_{ListOrdered._cnt}'
        super().__init__(id_, type_)

    @arg.check_type(list_style_type=str)
    def set_list_style_type(self, list_style_type):
        """ Set the marker type.

            Parameter
            ---------
            list_style_type: str
                The list style type, e.g. 1|a|A|i|I.

            Example
            -------
            >>> import pyowa
            >>> list_ordered = pyowa.ListOrdered()
            >>> list_ordered.append_child(pyowa.Label('Label1'))
            >>> list_ordered.set_list_style_type('i')
        """
        entry_path = ('style', 'listStyleType')
        self.add_property(entry_path, list_style_type)


class ListUnordered(BaseContainer):
    """ An unordered list <ul> to add elements.

        Example
        -------
        >>> import pyowa
        >>> list_unordered = pyowa.ListUnordered()
        >>> list_unordered.append_child(pyowa.Label('Label1'))
        >>> list_unordered.append_child(pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        ListUnordered._cnt += 1
        type_ = 'list_unordered'
        id_ = f'{type_}_{ListUnordered._cnt}'
        super().__init__(id_, type_)

    @arg.check_type(list_style_type=str)
    def set_list_style_type(self, list_style_type):
        """ Set the marker type.

            Parameter
            ---------
            list_style_type: str
                The list style type, e.g. disc|circle|square|decimal.

            Example
            -------
            >>> import pyowa
            >>> list_unordered = pyowa.ListUnordered()
            >>> list_unordered.append_child(pyowa.Label('Label1'))
            >>> list_unordered.set_list_style_type('disc')
        """
        entry_path = ('style', 'listStyleType')
        self.add_property(entry_path, list_style_type)


class TabBar(BaseContainer):
    """ A tab bar <div> to add elements.

        Example
        -------
        >>> import pyowa
        >>> tab_bar = pyowa.TabBar()
        >>> tab_bar.append_child('First Tab', pyowa.Label('Label1'))
        >>> tab_bar.append_child('Second Tab', pyowa.Label('Label2'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        TabBar._cnt += 1
        type_ = 'tab_bar'
        id_ = f'{type_}_{TabBar._cnt}'
        super().__init__(id_, type_)

    @arg.check_type(tab_name=str, child=BaseElement)
    def append_child(self, tab_name, child):
        """ Append a tab to the page.

            Parameter
            ---------
            tab_name: str.
                The name of the tab to be displayed.
            child: object.
                An instance of a pyowa.BaseElement.
        """
        child.data['tab_name'] = tab_name
        super().append_child(child)


class TableError(Exception):
    pass


class Table(BaseContainer):
    """ An table <table> without any header to add elements.

        Example
        -------
        >>> import pyowa
        >>> table = pyowa.Table()
        >>> table.append_child(0, pyowa.Label('Label11'))
        >>> table.append_child(0, pyowa.Label('Label12'))
        >>> table.append_child(1, pyowa.Label('Label21'))
        >>> table.append_child(1, pyowa.Label('Label22'))

        See Also
        --------
        BaseContainer: The base class for container elements.
    """
    _cnt = 0

    def __init__(self):
        Table._cnt += 1
        type_ = 'table'
        id_ = f'{type_}_{Table._cnt}'
        super().__init__(id_, type_)
        self._export_placeholder_values = False

    @arg.check_type(row=int, child=BaseElement)
    def append_child(self, row, child):
        """ Append a child to a row.

            Parameter
            ---------
            row: int
                The row number to append the child to.
            child: object
                An instance of a pyowa.BaseElement.
        """
        if not self._row_exists(row):
            self._add_row(row)
        self._append_to_row(row, child)

    def get_num_rows(self):
        """ Return the number of rows in a table.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> n_rows = table.get_num_rows()
        """
        return len(self.childs)

    def get_num_cols(self):
        """ Return the number of columns in a table.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> n_columns = table.get_num_cols()
        """
        return max([len(row) for row in self.childs])

    @arg.check_type(index=int, row_elements=list)
    def insert_row(self, index, row_elements):
        """ Insert a new row of childs.

            Parameter
            ---------
            index: int
                The row number to insert the childs to.
            child: list
                A list of of a pyowa.BaseElements.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> row_1 = [pyowa.Label('This'), pyowa.Label('is'), pyowa.Label('row'), pyowa.Label('1')]
            >>> table.insert_row(0, row_1)
        """
        self.childs.insert(index, row_elements)

        for child in row_elements:
            if not child._has_placeholder():
                continue

            if hasattr(child, 'placeholder_name'):
                name = child.get_placeholder_name()
                value = child.get_placeholder_value()
                self.placeholders[name] = value
            else:
                self.placeholders.update(child.placeholders)

    def _row_exists(self, row):
        return row + 1 <= len(self.childs)

    def _add_row(self, row):
        while row >= len(self.childs):
            self.childs.append([])

    def _append_to_row(self, row, child):
        self.childs[row].append(child)
        if not child._has_placeholder():
            return

        if hasattr(child, 'placeholder_name'):
            name = child.get_placeholder_name()
            value = child.get_placeholder_value()
            self.placeholders[name] = value
        else:
            self.placeholders.update(child.placeholders)

    def transpose(self):
        """ Transpose the table to switch rows to columns.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(0, pyowa.Label('Label12'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> table.append_child(1, pyowa.Label('Label22'))
            >>> table.transpose()
        """
        num_rows = self.get_num_rows()
        num_cols = self.get_num_cols()
        transposed_childs = []

        for c in range(num_cols):
            row = []
            for r in range(num_rows):
                row.append(self.childs[r][c])
            transposed_childs.append(row)
        self.childs = transposed_childs

    @arg.check_type(col_width=list)
    def set_col_width_in_percent(self, col_width):
        """ Set the width of the columns in percentage.

            Parameter
            ---------
            col_width: list of int.
                list of column widths in percentage.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> row_1 = [pyowa.Label('This'), pyowa.Label('is'), pyowa.Label('row'), pyowa.Label('1')]
            >>> table.insert_row(0, row_1)
            >>> col_width = [25, 25, 25, 25]
            >>> table.set_col_width_in_percent(col_width)
        """
        self.add_property('colWidth', col_width)

    @arg.check_type(label_convert=dict)
    def modify_labels(self, label_convert):
        """ Rename existing lables.

            Parameter
            ---------
            label_convert: dict.
                Key is the old label and value the new one.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> row_1 = [pyowa.Label('This'), pyowa.Label('is'), pyowa.Label('row'), pyowa.Label('1')]
            >>> table.insert_row(0, row_1)
            >>> label_modifications = {'This': 'Updating', 'is': 'the'}
            >>> table.modify_labels(label_modifications)
        """
        for old_label, new_label in label_convert.items():
            label = self._find_child(Label, 'text', old_label)
            if label is None:
                raise TableError(f'No label with text "{old_label}" found.')
            label.set_text(new_label)

    @arg.check_type(number_convert=dict)
    def modify_stepsize(self, number_convert):
        """ Change the step size for specified numbers.

            Parameter
            ---------
            number_convert: dict.
                key is the placeholder name of the number and value is the new step size.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> row_1 = [pyowa.Number(1, 'number_one'), pyowa.Number(2, 'number_two')]
            >>> table.insert_row(0, row_1)
            >>> stepsize = {'number_one': 0.1, 'number_two': 0.001}
            >>> table.modify_stepsize(stepsize)
        """

        for name, stepsize in number_convert.items():
            number = self._find_child_by_name(Number, name)
            if number is None:
                raise TableError(f'No number with name "{name}" found.')
            number.set_stepsize(stepsize)

    def set_table_layout_fixed(self):
        self.add_property('tableLayoutFixed', True)

    def set_cell_overflow_hidden(self):
        self.add_property('cellOverflowHidden', True)

    def allow_cell_word_break(self):
        self.add_property('cellWordBreak', True)

    @arg.check_type(args=(int, tuple))
    def hide_columns(self, *args):
        hiddenCols = list(args)
        self.add_property('hiddenCols', hiddenCols)

    @arg.check_issubclass(type_=BaseElement)
    def get_childs_by_type(self, type_):
        """ Return all the children of a particular type from a table.

            Parameter
            ---------
            type_: any pyowa.BaseElement.
                type of the pyowa element to search for in a table.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> row_1 = [pyowa.Label('Column 1'), pyowa.Label('Column 2')]
            >>> row_2 = [pyowa.Number(1), pyowa.Number(2)]
            >>> table.insert_row(0, row_1)
            >>> table.insert_row(1, row_2)
            >>> number_children = table.get_childs_by_type(pyowa.Number)
        """
        return [e for row in self.childs for e in row if isinstance(e, type_)]

    def _find_child(self, type_, path, exp_value):
        typed_childs = self.get_childs_by_type(type_)
        for element in typed_childs:
            value = element.get_property(path)
            if value == exp_value:
                return element
        return None

    def _find_child_by_name(self, type_, name):
        typed_childs = self.get_childs_by_type(type_)
        for element in typed_childs:
            if name == element.placeholder_name:
                return element
        return None

    def _childs_to_json(self):
        return [super(Table, self)._childs_to_json(child) for child in self.childs]

    def to_json(self):
        """ Return the json representation of the table.
        """
        json_repr = {
            'id': self.id,
            'type': self.type,
            'data': self.data,
            'childs': self._childs_to_json(),
        }
        if self._export_placeholder_values:
            json_repr['placeholders'] = self.placeholders
        return json_repr

    @arg.check_type(name=str)
    def to_dynamic_table(self, name=''):
        """ Convert the Table container into a Table placeholder.

            Parameter
            ---------
            name: str, optional.
                the name for the placeholder. Default is an up-counting expression.

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.Table()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(0, pyowa.Label('Label12'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> table.append_child(1, pyowa.Label('Label22'))
            >>> table = table.to_dynamic_table('new_dynamic_table')
        """

        self._export_placeholder_values = True
        json_repr = self.to_json()
        return TableDynamic(self.id, self.type, json_repr, name)

    @arg.check_type(placeholders=dict, dyn_table_name=str)
    def update_dynamic_table(self, placeholders, dyn_table_name):
        """ Update the Table placeholder in a placeholders collection

            Parameter
            --------
            placeholders: dict.
                placeholders dict for/from the web page.
            dyn_table_name: str.
                the name of the table placeholder that needs to be updated.
        """

        dyn_table = self.to_dynamic_table()
        dyn_table_value = dyn_table.get_placeholder_value()
        child_placeholders = dyn_table_value['value']['placeholders']
        child_placeholders_old = placeholders[dyn_table_name]['value']['placeholders']

        for placeholder_name in child_placeholders_old:
            if placeholder_name not in placeholders:
                continue
            placeholders.pop(placeholder_name)

        for placeholder_name in child_placeholders:
            if placeholder_name not in placeholders:
                continue
            msg = 'Placeholder with name {} already exists.'
            raise TableError(msg.format(placeholder_name))

        placeholders[dyn_table_name].update(dyn_table_value)
        placeholders.update(child_placeholders)

        return placeholders


class TableWithHeader(Table):
    """ An visible table <table> with first row as header to add elements.

        Example
        -------
        >>> import pyowa
        >>> table = pyowa.TableWithHeader()
        >>> table.append_child(0, pyowa.Label('Label11'))
        >>> table.append_child(0, pyowa.Label('Label12'))
        >>> table.append_child(1, pyowa.Label('Label21'))
        >>> table.append_child(1, pyowa.Label('Label22'))

        See Also
        --------
        Table: An table <table> without any header to add elements.
    """
    _cnt = 0

    def __init__(self):
        TableWithHeader._cnt += 1
        super().__init__()
        type_ = 'table_with_header'
        id_ = f'{type_}_{TableWithHeader._cnt}'
        BaseContainer.__init__(self, id_, type_)

    def allow_sort(self):
        """ Add the sort functionality to the table with header

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.TableWithHeader()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(0, pyowa.Label('Label12'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> table.append_child(1, pyowa.Label('Label22'))
            >>> table.allow_sort()
        """
        self.add_property('sort', True)

    def allow_filter(self):
        """ Add the sort functionality to the table with header

            Example
            -------
            >>> import pyowa
            >>> table = pyowa.TableWithHeader()
            >>> table.append_child(0, pyowa.Label('Label11'))
            >>> table.append_child(0, pyowa.Label('Label12'))
            >>> table.append_child(1, pyowa.Label('Label21'))
            >>> table.append_child(1, pyowa.Label('Label22'))
            >>> table.allow_filter()
        """
        self.add_property('filter', True)


class TableDynamic(BaseElementPlaceholder):
    """ A table placeholder created using a Table object.
    """

    def __init__(self, id_, type_, value, name=None):
        super().__init__(id_, type_)
        self._set_placeholder(name or id_, value)
        self._set_as_table()
