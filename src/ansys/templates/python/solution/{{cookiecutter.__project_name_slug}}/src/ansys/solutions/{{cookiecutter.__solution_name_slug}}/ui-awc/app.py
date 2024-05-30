# ©2024, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Application."""

import os
import tempfile

from dash_extensions.enrich import DashProxy, MultiplexerTransform, NoOutputTransform, TriggerTransform
import dash_uploader as du

class DashApp(DashProxy):
    def interpolate_index(self, **kwargs):
        return f"""
        <!DOCTYPE html>
        <html >
            <head>
                <title>{{ cookiecutter.__solution_name_slug }}</title>
                {kwargs.get("metas")}
                {kwargs.get("css")}
            </head>
            <body>
                {kwargs.get("app_entry", "")}
                {kwargs.get("config", "")}
                {kwargs.get("scripts", "")}
                {kwargs.get("renderer", "")}
            </body>
        </html>
        """

app = DashApp(
    __name__,
    external_stylesheets=[],
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
