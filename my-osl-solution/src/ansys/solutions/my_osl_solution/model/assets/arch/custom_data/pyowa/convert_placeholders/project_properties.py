""" Convert project properties into pyowa objects and vice-versa.

Copyright © 2021 ANSYS, Inc.

"""
import json
import pathlib
import copy

from .osl_pyowa_wrapper import (
    TableInputFiles,
    BorderedSection,
    TablePlaceholders,
    is_user_level_computation_enginieer,
    get_definition_type,
    is_variant_bool,
    is_variant_scalar,
    )
from .. import SectionVertical


class ProjectPropertiesError(Exception):
    pass


class ProjectProperties:

    def __init__(self):
        self._json_content = None
        self._placeholders = {}
        self._registered_files = {}
        self._settings = {}
        self._parameter_manager = {}
        self._criteria = {}

    def read_file(self, file):
        with open(file) as f:
            self._json_content = json.load(f)
        if 'placeholders' in self._json_content:
            self._placeholders = self._json_content['placeholders']
            self._registered_files = self._json_content['registered_files']
            self._settings = self._json_content['settings']
            self._parameter_manager = self._json_content['parameter_manager']
            self._criteria = self._json_content['criteria']
        else:
            self._placeholders = self._json_content

    def to_pyowa_sections(self):
        pyowa_sections = []
        pyowa_sections.append(self.registered_files_to_pyowa_section())
        pyowa_sections.append(self.criteria_to_pyowa_section())
        pyowa_sections.append(self.parameter_manager_to_pyowa_section())
        pyowa_sections.append(self.placeholders_to_pyowa_section())
        pyowa_sections.append(self.settings_to_pyowa_section())
        return [s for s in pyowa_sections if s is not None]

    def registered_files_to_pyowa_section(self):
        input_files_table = TableInputFiles()
        input_files_table.read(self._registered_files)

        if not input_files_table.get_num_rows() > 1:
            return None

        section = BorderedSection('Input files')
        section.append_child(input_files_table)
        return section.create()

    def criteria_to_pyowa_section(self):
        return None

    def parameter_manager_to_pyowa_section(self):
        return None

    def placeholders_to_pyowa_section(self):
        placeholder_table = TablePlaceholders()
        placeholder_table.read(self._placeholders)

        if not placeholder_table.get_num_rows() > 0:
            return None

        section = BorderedSection('Placeholders')
        section.append_child(placeholder_table.create())
        return section.create()

    def settings_to_pyowa_section(self):
        return None

    def update_values(self, ui_placeholders):
        ui_values = {n: v['value'] for n, v in ui_placeholders.items() if 'value' in v}
        self._update_registered_files(ui_values)
        self._update_placeholders(ui_values)

    def _update_registered_files(self, ui_values):
        for registered_file in self._registered_files:
            if registered_file.get('usage') != 'Input file':
                continue
            ident = registered_file.get('ident')
            uploaded_file = ui_values.get(ident)
            uploaded_file = pathlib.Path(uploaded_file)

            local_location = registered_file.get('local_location')
            split_path = local_location.get('split_path')
            base_path_mode = local_location.get('base_path_mode')
            if 'value' in base_path_mode:
                base_path_mode = base_path_mode.get('value')

            base_path_mode = 'PROJECT_RELATIVE'
            split_path['head'] = str(uploaded_file.parent)
            split_path['tail'] = str(uploaded_file.name)

    def _update_placeholders(self, ui_values):
        placeholder_values = self._placeholders.get('placeholder_values')
        placeholder_definitions = self._placeholders.get('placeholder_definitions')

        for name, old_value in placeholder_values.items():
            if not is_user_level_computation_enginieer(name, placeholder_definitions):
                continue

            definition = placeholder_definitions.get(name)
            definition_type = get_definition_type(definition)
            new_value = ui_values.get(name)

            if definition_type == 'unknown':
                if is_variant_bool(old_value):
                    placeholder_values[name] = update_variant_bool(old_value, new_value)
                elif is_variant_scalar(old_value):
                    placeholder_values[name] = update_variant_scalar(old_value, new_value)
                elif name.startswith('StartDesigns'):
                    placeholder_values[name] = update_start_designs(old_value, new_value)
                # elif is_parameter_manager(new_value):
                #   placeholder_values[name] = update_parameter_manager(old_value, new_value)
                # else:
                #     raise ProjectPropertiesError(f'Unhandled optislang type "{name}")
            elif definition_type == 'string':
                placeholder_values[name] = new_value
            elif definition_type == 'uint':
                placeholder_values[name] = new_value
            elif definition_type == 'int':
                placeholder_values[name] = new_value
            elif definition_type == 'real':
                placeholder_values[name] = new_value
            elif definition_type == 'bool':
                placeholder_values[name] = new_value
            else:
                raise ProjectPropertiesError(f'Unhandled type "{definition_type}"')

    def get_properties(self):
        # placeholders only
        if 'placeholders' not in self._json_content:
            return self._placeholders
        # project properties
        properties = {
            'criteria': self._criteria,
            'parameter_manager': self._parameter_manager,
            'placeholders': self._placeholders,
            'registered_files': self._registered_files,
            'settings': self._settings,
            }
        return properties


def update_variant_bool(old_value, new_value):
    old_value['bool'] = new_value
    return old_value


def update_variant_scalar(old_value, new_value):
    old_value['scalar']['real'] = new_value
    return old_value


def update_start_designs(old_value, new_value):
    designs = _get_table_content(new_value)

    start_designs = []
    for i, design in enumerate(designs, 1):
        start_design = copy.deepcopy(old_value[0])
        sequence = [{'First': n, 'Second': v} for n, v in design.items()]
        start_design['id'] = i
        start_design['parameters']['sequence'] = sequence
        start_designs.append(start_design)
    return start_designs


def update_parameter_manager(old_value, new_value):
    pass


def _get_table_content(ui_value):
    childs = ui_value.get('childs')
    column_names = [v['data']['text'] for v in childs[0]]

    table_content = []
    for row in childs[1:]:
        row_values = [v['data']['value'] for v in row]
        row_data = dict(zip(column_names, row_values))
        table_content.append(row_data)
    return table_content


def convert_properties_file_to_pyowa_sections(properties_file):
    pp = ProjectProperties()
    pp.read_file(properties_file)
    pyowa_sections = pp.to_pyowa_sections()
    return pyowa_sections


def apply_placeholders_to_properties_file(ui_placeholders, properties_file):
    pp = ProjectProperties()
    pp.read_file(properties_file)
    pp.update_values(ui_placeholders)
    properties = pp.get_properties()
    return properties


def write_properties_file(properties, properties_file):
    with properties_file.open(mode='w') as f:
        json.dump(properties, f, indent=4)


def find_project_properties_file(properties_file_name):
    project = pathlib.Path().cwd() / properties_file_name

    properties_file = project.with_suffix('.json')
    if properties_file.exists():
        return properties_file

    placeholders_file = project.with_suffix('.placeholders')
    if placeholders_file.exists():
        return placeholders_file

    raise FileNotFoundError(f'Unable to find properties file to "{project}.opf".')


class optiSLangProjectProperties(SectionVertical):
    """ Visualize an optiSLang project property (or placeholders) file.

        Parameter
        ---------
        project_properties_file: str
            Path to the project properties file.

        Example
        -------
        >>> import pyowa
        >>> # for more details please have a look into overview_project.opf and overview_project.json
        >>> table = pyowa.optiSLangProjectProperties('overview_project.json')
        >>> starter = pyowa.ProjectStarter('run_project.py', 'overview_project.opf', 'ExampleStarter')

    """

    def __init__(self, project_properties_file, init_gui=True):
        self._project_properties_file = project_properties_file
        super().__init__()
        if init_gui:
            self._init_gui()

    def _init_gui(self):
        sections = convert_properties_file_to_pyowa_sections(self._project_properties_file)
        for section in sections:
            self.append_child(section)

    def write_updated_properties_file(self, ui_placeholders, working_properties_file):
        properties = apply_placeholders_to_properties_file(ui_placeholders, self._project_properties_file)
        write_properties_file(properties, working_properties_file)
