# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Application."""

import os
import tempfile

import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform, NoOutputTransform, TriggerTransform
import dash_uploader as du

app = DashProxy(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    transforms=[NoOutputTransform(), TriggerTransform(), MultiplexerTransform()],
)

# If folder doesn't exist, it will be created later
UPLOAD_DIRECTORY = os.path.join(tempfile.gettempdir(), "GLOW")
du.configure_upload(app, UPLOAD_DIRECTORY)

# !IMPORTANT Keeping the import line here to adapt with dash_uploader config, moving the import above will fail the
# dash uploader configuration
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.ui.pages.page import layout

app.layout = layout
