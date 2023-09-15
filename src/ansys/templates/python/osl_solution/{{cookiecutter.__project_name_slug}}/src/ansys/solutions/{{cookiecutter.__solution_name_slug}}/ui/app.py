# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Application."""

import dash_bootstrap_components as dbc
import dash_uploader as du
import os
import tempfile

from dash_extensions.enrich import DashProxy, MultiplexerTransform, NoOutputTransform, TriggerTransform


class Dash(DashProxy):
    """Custom Dash class."""
    def interpolate_index(self, **kwargs):

        # Get the original index content (including default Dash CSS styles) from the parent class
        index_str = super().interpolate_index(**kwargs)

        # Combine the original index content and your custom CSS
        modified_index = index_str.replace('</html>', f'<html class="light">')

        return modified_index

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
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
