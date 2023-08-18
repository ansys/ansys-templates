""" Definition of the wizard specific optiSLang project starting process.

This file is intended to be used as modifiable template.

Global Parameters
-----------------
projects_dir: str
    Path to the projects directory.
listener_id: str
    Id to register a listener when starting the optiSLang project.
listener_port: int
    Port where optiSLang web service is listening for the started optiSLang project.
optislang_home: str
    Path to optiSLang installation directory.
user: str
    optiSLang web service user name.

"""
import os
import pathlib
import shutil
import socket
import subprocess
import pyowa


def app(working_dirname, osl_project_name, placeholders, remote_location, settings):
    """ Function triggered by optiSLang web service if the user clicks the run button in the ProjectStarter widget.
        Mininum needed functionality is to start an optiSLang project locally.

        Parameters
        ----------
        working_dirname: str
            Name of the unique working directory located in "projects_dir"
        osl_project_name: str
            Name of the optiSLang project.
        placeholders: dict
            The pyowa placeholders object providing the modifiable information from the frontend.
        remote_location: str
            Host name selected in the ProjectStarter widget. Empty if remotes.json doesn't exist.
        settings: dict
            Host settings selected in the ProjectStarter widget. Empty if remotes.json doesn't exist.

        Returns
        -------
        dict
            Supports the following key-value pairs to return:
                'original_working_dir': Local project directory.
                'log_file': Stdout file name.
                'error_log_file': Stderr file name.

    """
    custom_data_dir = pathlib.Path().cwd()
    working_dir = pathlib.Path(projects_dir) / working_dirname

    osl_project_name += '.opf' if not osl_project_name.endswith('.opf') else ''
    reference_project_file = custom_data_dir / osl_project_name
    reference_properties_file = pyowa.find_project_properties_file(osl_project_name)

    working_project_file = working_dir / reference_project_file.name
    working_properties_file = working_dir / reference_properties_file.name

    shutil.copyfile(reference_project_file, working_project_file)

    project_properties = pyowa.optiSLangProjectProperties(reference_properties_file, init_gui=False)
    project_properties.write_updated_properties_file(placeholders, working_properties_file)

    command = [
            str(_get_optislang_executable()),
            str(working_project_file),
            '-b',
            '--force',
            '--restore',
            '--reset',
            '--enable-tcp-server',
            '--blessed-start',
            '--dump-project-state=../project_state.json',
            '--shutdown-on-finished',
            '--tcp-listener-id={}'.format(listener_id),
            '--register-multi-tcp-listeners',
            *_get_tcp_listeners(),
            ]

    if working_properties_file.suffix == '.json':
        command.append(f'--import-project-properties={working_properties_file}')
    else:
        command.append(f'--import-values={working_properties_file}')

    stdout_file = working_dir / 'stdout.txt'
    stderr_file = working_dir / 'stderr.txt'

    with stdout_file.open(mode='wb') as out, stderr_file.open(mode='wb') as err:
        subprocess.Popen(command, stdout=out, stderr=err, cwd=working_dir)

    return {
        'original_working_dir': str(working_dir),
        'log_file': stdout_file.name,
        'error_log_file': stderr_file.name,
    }


def _get_optislang_executable():
    home = pathlib.Path(optislang_home)
    if os.name == 'posix':
        return home / 'optislang'
    return home / 'optislang.com'


def _get_tcp_listeners():
    tcp_listeners = []
    try:
        host_addresses = socket.gethostbyname_ex(socket.getfqdn())[2]
        tcp_listeners = [f'{host_address}:{listener_port}' for host_address in host_addresses]
    except:
        pass
    tcp_listeners.append ("{}:{}".format("127.0.0.1", listener_port))
    return tcp_listeners
