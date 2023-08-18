# © 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.

""" Description of the wizard page.

This file is intended to be used as modifiable template.

"""
import pyowa


MARGIN = 20
WIZARD_NAME = "hook optimization"
OSL_PROJECT_NAME = "hook_optimization"
DESCRIPTION_TEXT = "An optiSLang web application for the optimization of a steel hook"


def app():
#    static_line0 = '.'
    static_line1 = 'Loading force F = 6000N'
    static_line2 = 'Cylindrical support, tangential direction is free (which requires weak springs to stabilize the numerical analysis).'
    static_line3 = 'Optimization is based on MOP, the best design is validated.'
    static_line4 = 'Please enter below the bounds of the geometric parameters as well the stress constraint and define the number of solver runs to generate the MOP.'

    image1 = pyowa.ImageFromWizardDir('GeomParameter.png')
    image1.set_size_in_px(300, 300)
    image2 = pyowa.ImageFromWizardDir('loading.png')
    image2.set_size_in_px(280, 280)
    image3 = pyowa.ImageFromWizardDir('scenery.png')
    image3.set_size_in_px(600, 600)

    properties_file = pyowa.find_project_properties_file(OSL_PROJECT_NAME)

    project_description = _get_project_description()
    project_properties = pyowa.optiSLangProjectProperties(properties_file)
    project_starter = pyowa.ProjectStarter('run_project.py', OSL_PROJECT_NAME)

    page = pyowa.PageWizard(WIZARD_NAME)
    page.append_child(project_description)

    page.append_child(pyowa.Empty())
    list_unordered = pyowa.ListUnordered()
    list_unordered.append_child(pyowa.Label(static_line1))
    list_unordered.append_child(pyowa.Label(static_line2))
    list_unordered.append_child(pyowa.Label(static_line3))
    page.append_child(list_unordered)

    page.append_child(pyowa.Empty())
    page.append_child(image1)
    page.append_child(image2)
    page.append_child(pyowa.Empty())
    page.append_child(image3)
    page.append_child(pyowa.Empty())
    page.append_child(pyowa.Label(static_line4))


    page.append_child(pyowa.Empty())
    page.append_child(pyowa.Empty())
    page.append_child(project_properties)
    page.append_child(project_starter)

    return page.to_json()


def _get_project_description():
    description_text = DESCRIPTION_TEXT

    description_table = pyowa.Table()
    description_table.set_margin_in_px(top=MARGIN)
    description_table.set_col_width_in_percent([50, 50])
    description_table.append_child(0, pyowa.Label(description_text))
    description_table.append_child(0, pyowa.Empty())
    return description_table
