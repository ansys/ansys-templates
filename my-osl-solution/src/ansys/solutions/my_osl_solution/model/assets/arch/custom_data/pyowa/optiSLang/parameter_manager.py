""" Converter optiSLang parameter manager

Copyright © 2021 ANSYS, Inc.

"""
from ..containers import (
    SectionVertical,
    TableWithHeader
    )
from ..elements import (
    Label,
    Number,
    Select,
    Text,
    )


class Parameter(dict):

    def load_osl_placeholders(self, parameter):
        deterministic_property = parameter.get('deterministic_property')

        self['Name'] = parameter.get('name')
        self['Value'] = parameter.get('reference_value')
        self['Domain Type'] = deterministic_property.get('domain_type').get('value')
        self['Kind'] = deterministic_property.get('kind')
        if self.is_continuous():
            self['Lower Bound'] = float(deterministic_property.get('lower_bound'))
            self['Upper Bound'] = float(deterministic_property.get('upper_bound'))
            self['Discrete States'] = None
        else:
            self['Lower Bound'] = None
            self['Upper Bound'] = None
            self['Discrete States'] = deterministic_property.get('discrete_states')

    @staticmethod
    def get_value(element):
        data = element.get('data')
        if 'text' in data:
            return data.get('text')
        return data.get('value')

    def load_ows_placeholders(self, row):
        self['Name'] = self.get_value(row[0])
        self['Value'] = self.get_value(row[1])
        self['Domain Type'] = self.get_value(row[2])
        self['Kind'] = self.get_value(row[3])
        self['Lower Bound'] = self.get_value(row[4]) or None
        self['Upper Bound'] = self.get_value(row[5]) or None
        self['Discrete States'] = self.get_value(row[6]) or None

    def is_continuous(self):
        return self['Kind'] == 'continuous'

    def get_column_names(self):
        return [Label(n) for n in self.keys()]

    def get_row_values(self):
        return [
            Label(self['Name']),
            self._get_value_element(),
            Label(self['Domain Type']),
            Label(self['Kind']),
            Label('') if self['Lower Bound'] is None else Number(self['Lower Bound']),
            Label('') if self['Upper Bound'] is None else Number(self['Upper Bound']),
            Label('') if self['Discrete States'] is None else Text(str(self['Discrete States'])),
            ]

    def _get_value_element(self):
        if self.is_continuous():
            value_element = Number(float(self['Value']))
            value_element.set_bounds(self['Lower Bound'], self['Upper Bound'])
        else:
            options = [str(o) for o in self['Discrete States']]
            value_element = Select(str(self['Value']), options)
        return value_element


class ParameterManagerError(Exception):
    pass


class ParameterManager(SectionVertical):

    def __init__(self, placeholder_name):
        super().__init__()
        self.placeholder_name = placeholder_name
        self.parameters = []
        self.pm_table = TableWithHeader()

    def get_placeholder_name(self):
        return self.pm_table.get_placeholder_name()

    def get_placeholder_value(self):
        return self.pm_table.get_placeholder_value()

    def get_parameter_by_name(self, name):
        for p in self.parameters:
            if p['Name'] == name:
                return p
        raise ParameterManagerError(f'Parameter with name "{name} " not found')

    def load_osl_placeholders(self, placeholder_values):
        placeholder_value = placeholder_values.get(self.placeholder_name)
        if placeholder_value is None:
            raise ParameterManagerError(f'Placeholder "{self.placeholder_name}" not found')

        parameter_container = placeholder_value.get('parameter_container')
        for parameter in parameter_container:
            is_const = parameter.get('const')
            type_ = parameter.get('type').get('value')
            if is_const or type_ not in ['deterministic', 'mixed']:
                continue
            p = Parameter()
            p.load_osl_placeholders(parameter)
            self.parameters.append(p)

        self._insert_parameters_to_pm_table()

    def dump_osl_placeholders(self, placeholder_values):
        placeholder_value = placeholder_values.get(self.placeholder_name)
        if placeholder_value is None:
            raise ParameterManagerError(f'Placeholder "{self.placeholder_name}" not found')

        parameter_container = placeholder_value.get('parameter_container')
        for parameter in parameter_container:
            name = parameter.get('name')
            p = self.get_parameter_by_name(name)
            parameter['reference_value'] = p['Value']
        return placeholder_values

    def load_ows_placeholders(self, placeholders):
        placeholder = placeholders.get(self.placeholder_name)
        if placeholder is None:
            raise ParameterManagerError(f'Placeholder "{self.placeholder_name}" not found')

        rows = placeholder.get('value').get('childs')
        for row in rows[1:]:
            p = Parameter()
            p.load_ows_placeholders(row)
            self.parameters.append(p)

    def _insert_parameters_to_pm_table(self):
        for i, p in enumerate(self.parameters, 1):
            if i == 1:
                self.pm_table.insert_row(0, p.get_column_names())
            self.pm_table.insert_row(i, p.get_row_values())

        self.pm_table.hide_columns(2, 3, 4, 5, 6)
        self.pm_table = self.pm_table.to_dynamic_table(self.placeholder_name)
        self.append_child(self.pm_table)
