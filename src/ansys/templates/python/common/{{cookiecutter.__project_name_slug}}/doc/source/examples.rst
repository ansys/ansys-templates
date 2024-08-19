Examples
########

{%- if cookiecutter.__product_name_slug != "" %}
These examples demonstrate the behavior and usage of Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }}.
{%- elif cookiecutter.__template_name != "solution" %}
These examples demonstrate the behavior and usage of {{ cookiecutter.project_name }}.
{%- else %}
These examples demonstrate the behavior and usage of {{ cookiecutter.solution_name }}.
{%- endif %}

{{ '.. Provide links to the files in doc/source/examples below:' }}