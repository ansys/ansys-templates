""" pyowa wrapper for optiSLang project properties.

Copyright © 2021 ANSYS, Inc.

"""
import pyowa


TABLE_COLUMN_SIZE = [20, 30, 50]


class BorderedSection(pyowa.SectionHorizontalBordered):

    def __init__(self, name):
        super().__init__(name)
        self.main_table = pyowa.Table()
        self.main_table.set_col_width_in_percent([50, 50])

    def append_child(self, child):
        row = self.main_table.get_num_rows()
        self.main_table.append_child(row, child)
        self.main_table.append_child(row, pyowa.Empty())

    def create(self):
        super().append_child(self.main_table)
        return self


class TableInputFiles(pyowa.TableWithHeader):

    def __init__(self):
        super().__init__()
        self.set_col_width_in_percent(TABLE_COLUMN_SIZE)

    def read(self, registered_files):
        self.append_child(0, pyowa.Label('ID'))
        self.append_child(0, pyowa.Label('Upload'))
        self.append_child(0, pyowa.Label('Comment'))

        for i, registered_file in enumerate(registered_files, 1):
            if not registered_file['usage'] == 'Input file':
                continue

            ident = registered_file['ident']
            comment = registered_file['comment']
            # tail = registered_file['local_location']['split_path']['tail']

            self.append_child(i, pyowa.Label(ident))
            self.append_child(i, pyowa.ButtonFileUpload(ident))  # TODO: add an action to activate run button
            self.append_child(i, pyowa.Label(comment))


class TablePlaceholdersError(Exception):
    pass


class TablePlaceholders(pyowa.SectionVertical):

    def __init__(self):
        super().__init__()
        self.placeholder_definitions = {}

        self.num_added_tables = 0

        self.table_placeholders = pyowa.TableWithHeader()
        self.table_placeholders.set_col_width_in_percent(TABLE_COLUMN_SIZE)

    def create(self):
        self.append_child(self.table_placeholders)
        return self

    def get_num_rows(self):
        return self.table_placeholders.get_num_rows() + self.num_added_tables

    def append_element(self, name, element, description):
        row = self.table_placeholders.get_num_rows()
        if not row:
            self.table_placeholders.append_child(0, pyowa.Label('Name'))
            self.table_placeholders.append_child(0, pyowa.Label('Value'))
            self.table_placeholders.append_child(0, pyowa.Label('Description'))
            row += 1

        self.table_placeholders.append_child(row, pyowa.Label(name))
        self.table_placeholders.append_child(row, element)
        self.table_placeholders.append_child(row, pyowa.Label(description))

    def append_table(self, table):
        self.append_child(table)
        self.num_added_tables += 1

    def read(self, placeholders):
        self.placeholder_definitions = placeholders.get('placeholder_definitions')
        placeholder_values = placeholders.get('placeholder_values')
        for name, value in placeholder_values.items():
            if not is_user_level_computation_enginieer(name, self.placeholder_definitions):
                continue

            definition = self.placeholder_definitions.get(name)
            definition_type = get_definition_type(definition)
            description = definition['description']

            if definition_type == 'unknown':
                if is_variant_bool(value):
                    element = ElementVariantBool(name, value, definition)
                    self.append_element(name, element, description)
                elif is_variant_scalar(value):
                    element = ElementVariantScalar(name, value, definition)
                    self.append_element(name, element, description)
                elif is_startdesigns(value):
                    table = TableStartDesigns(name, placeholders)
                    self.append_table(table)
                # elif is_parameter_manager(value):
                #     table = pyowa.ParameterManager(name)
                #     table.load_osl_placeholders(placeholder_values)
                #     self.append_table(table)
                # else:
                #     raise TablePlaceholdersError(f'Unhandled optislang type "{name}"')
            elif definition_type == 'string':
                element = ElementString(name, value, definition)
                self.append_element(name, element, description)
            elif definition_type == 'uint':
                element = ElementUInt(name, value, definition)
                self.append_element(name, element, description)
            elif definition_type == 'int':
                element = ElementInt(name, value, definition)
                self.append_element(name, element, description)
            elif definition_type == 'real':
                element = ElementReal(name, value, definition)
                self.append_element(name, element, description)
            elif definition_type == 'bool':
                element = ElementBool(name, value, definition)
                self.append_element(name, element, description)
            else:
                raise TablePlaceholdersError(f'Unhandled type "{definition_type}"')


class PropertiesFileSyntaxError(Exception):
    pass


def _get_user_level(name, placeholder_definitions):
    if name not in placeholder_definitions:
        raise PropertiesFileSyntaxError(f'Placeholder definition "{name}" not found.')

    definition = placeholder_definitions[name]
    user_level = definition['user_level']
    if 'value' in user_level:  # >= osl21R1
        user_level = user_level['value']
    return user_level


def is_user_level_computation_enginieer(name, placeholder_definitions):
    user_level = _get_user_level(name, placeholder_definitions)
    return user_level == 'computation_engineer'


def is_user_level_flow_engineer(name, placeholder_definitions):
    user_level = _get_user_level(name, placeholder_definitions)
    return user_level == 'flow_engineer'


def get_definition_type(definition):
    definition_type = definition['type']
    if 'value' in definition_type:  # >= osl21R1
        definition_type = definition_type['value']
    return definition_type


def _get_variant_kind(value):
    NOT_A_VARIANT = ''
    if not isinstance(value, dict):
        return NOT_A_VARIANT
    kind = value.get('kind')
    if kind is None:
        return False
    if 'value' in kind:  # >= osl21R1
        kind = kind['value']
    return kind


def is_variant_bool(value):
    kind = _get_variant_kind(value)
    return kind == 'bool'


def is_variant_scalar(value):
    kind = _get_variant_kind(value)
    return kind == 'scalar'


def is_parameter_manager(value):
    if not isinstance(value, dict):
        return False
    return 'parameter_container' in value


def is_startdesigns(value):
    if not isinstance(value, list):
        return False
    if not value:
        return False
    d = value[0]
    return 'id' in d and 'parameters' in d


class ElementBool(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        element = pyowa.Checkbox(value, name)
        self.append_child(element)


class ElementReal(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        r = definition['range'].lstrip('[').rstrip(']')
        if r.count(';'):
            options = r.split(';')
            element = pyowa.Select(str(value), options, name)
        else:
            element = pyowa.Number(float(value), name)
            bounds = _extract_bounds(r, float)
            if bounds:
                element.set_bounds(*bounds)
        self.append_child(element)


class ElementInt(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        r = definition['range'].lstrip('[').rstrip(']')
        if r.count(';'):
            options = r.split(';')
            element = pyowa.Select(str(value), options, name)
        else:
            element = pyowa.Number(int(value), name)
            bounds = _extract_bounds(r, int)
            if bounds:
                element.set_bounds(*bounds)
        self.append_child(element)


def _extract_bounds(r, ValueType):
    if not r.strip():
        return []
    r = r.split('-')
    if r[0] and r[1]:  # '1-3' -> ['1', '3']
        return [ValueType(r[0]), ValueType(r[1])]
    elif r[1] and r[2]:  # '-1-3' -> ['', '1', '3']
        return [-ValueType(r[0]), ValueType(r[1])]
    elif r[0] and r[2]:  # '1--3' -> ['1', '', '3']
        return [ValueType(r[0]), -ValueType(r[1])]
    elif r[1] and r[3]:  # '-1--3' -> ['', '1', '', '3']
        return [-ValueType(r[1]), -ValueType(r[3])]
    return []


class ElementUInt(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        element = pyowa.Number(value, name)
        element.set_min_value(0)
        self.append_child(element)


class ElementString(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        r = definition['range'].lstrip('[').rstrip(']')
        if r.count(';'):
            options = r.split(';')
            element = pyowa.Select(str(value), options, name)
        else:
            element = pyowa.Text(value, name)
        self.append_child(element)


class ElementVariantScalar(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        value = value['scalar']['real']
        element = ElementReal(name, value, definition)
        self.append_child(element)


class ElementVariantBool(pyowa.SectionHorizontal):

    def __init__(self, name, value, definition):
        super().__init__()
        value = value['bool']
        element = ElementBool(name, value, definition)
        self.append_child(element)


class TableStartDesigns(pyowa.SectionHorizontal):

    def __init__(self, name, placeholders):
        super().__init__()
        placeholder_values = placeholders.get('placeholder_values')
        start_designs = placeholder_values.get(name)

        table_start_designs = self._generate_table_start_designs(start_designs, name)
        table_start_designs = table_start_designs.to_dynamic_table(name)

        self.append_child(pyowa.Heading(name, 4))
        self.append_child(table_start_designs)

    @staticmethod
    def _generate_table_start_designs(start_designs, name):
        table_start_designs = pyowa.TableWithHeader()

        names = _get_design_parameter_names(start_designs)
        for n in names:
            table_start_designs.append_child(0, pyowa.Label(n))

        for i, start_design in enumerate(start_designs, 1):
            sequence = start_design.get('parameters').get('sequence')
            for entry in sequence:
                value = entry.get('Second')
                table_start_designs.append_child(i, pyowa.Number(value))

        return table_start_designs


def _get_design_parameter_names(start_designs):
    sequence = start_designs[0].get('parameters').get('sequence')
    return [entry.get('First') for entry in sequence]
