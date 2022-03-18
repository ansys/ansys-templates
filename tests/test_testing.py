import os

from ansys.templates.testing import assert_files_in_baked_project, assert_template_baking_process


def test_assert_files_in_baked_project(tmp_path):
    files_list = ["file_A.txt", "file_B.txt", "file_C.txt"]
    for file in files_list:
        (tmp_path / file).touch()

    assert_files_in_baked_project(files_list, tmp_path)


def test_assert_template_baking_process(tmp_path):
    # Create a tiny family template
    os.mkdir(tmp_path / "common")
    os.mkdir(tmp_path / "common/{{cookiecutter.__project_name_slug}}")
    os.mkdir(tmp_path / "template")
    os.mkdir(tmp_path / "template/{{cookiecutter.__project_name_slug}}")

    # Fill the common cookiecutter file
    with open(tmp_path / "common/cookiecutter.json", "w") as common_file:
        file_content = """
        {
          "__project_name_slug": ""
        }
        """
        common_file.write(file_content)

    # Fill the template cookiecutter file
    with open(tmp_path / "template/cookiecutter.json", "w") as template_file:
        file_content = """
        {
          "project_name_slug": "hello_project",
          "__project_name_slug": "{{ cookiecutter.project_name_slug }}"
        }
        """
        template_file.write(file_content)

    assert_template_baking_process(
        tmp_path / "template", tmp_path, dict(project_name_slug="hello_project")
    )
