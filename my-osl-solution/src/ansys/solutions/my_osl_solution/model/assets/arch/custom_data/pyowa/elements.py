""" This module contains all elements which can be added to the webpage, e.g. to interact with the user.

Copyright © 2021 ANSYS, Inc.

"""
import os
import pathlib
from .base_element import (
        BaseElement,
        BaseElementPlaceholder
        )
from . import arg


HTML_ESCAPE_SEQUENCE = {
    '#': '%23',
}


# -------------------------------------------------------------------------------------------------
### static elements
# -------------------------------------------------------------------------------------------------

class Empty(BaseElement):
    """ A line break that can be used as a filler.
        The html element tag is "<br>".

        Example
        -------
        >>> import pyowa
        >>> invisible_element = pyowa.Empty()

        >>> table = pyowa.Table()
        >>> table.append_child(0, pyowa.Label('Label1'))
        >>> table.append_child(1, invisible_element)
        >>> table.append_child(2, pyowa.Label('Label2'))

        See Also
        --------
        BaseElement: The base class for all elements.
    """

    def __init__(self):
        type_ = 'empty'
        super().__init__(type_, type_)


class Label(BaseElement):
    """ A static text without newline.
        The html element tag is "<span>".

        Parameter
        ---------
        text: str
            Text to be visualized.

        Example
        -------
        >>> import pyowa
        >>> simple_label = pyowa.Label('SimpleLabel')

        >>> styled_label = pyowa.Label('StyledLabel')
        >>> styled_label.set_color('white')
        >>> styled_label.set_background_color('black')
        >>> styled_label.add_property(('style', 'fontSize'), '24px')

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(text=str)
    def __init__(self, text):
        Label._cnt += 1
        type_ = 'label'
        id_ = f'{type_}_{Label._cnt}'
        super().__init__(id_, type_)
        self.set_text(text)

    @arg.check_type(text=str)
    def set_text(self, text):
        self.add_property('text', text)

    def set_bold(self):
        """ Style the text using bold font."""
        self.add_property(('style', 'fontWeight'), 'bold')
        return self


class Paragraph(BaseElement):
    """ A static text with newline.
        The html element tag is "<p>".

        Parameter
        ---------
        text: str
            Text to be visualized on the webpage.

        Example
        -------
        >>> import pyowa
        >>> paragraph = pyowa.Paragraph('MyText')
        >>> paragraph.set_color('white')
        >>> paragraph.set_background_color('black')
        >>> paragraph.add_property(('style', 'fontSize'), '24px')

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(text=str)
    def __init__(self, text):
        Paragraph._cnt += 1
        type_ = 'paragraph'
        id_ = f'{type_}_{Paragraph._cnt}'
        super().__init__(id_, type_)
        self.add_property('text', text)


class HeadingError(Exception):
    pass


class Heading(BaseElement):
    """ A static heading of level X.
        The html element tag is "<hX>".

        Parameter
        ---------
        text: str
            Text to be visualized on the webpage.
        level: int
            The heading level, which can have a value from 1 to 6.

        Example
        -------
        >>> import pyowa
        >>> header_2 = pyowa.Heading('Header of size 2', 2)
        >>> header_4 = pyowa.Heading('Header of size 4', 4)
        >>> header_6 = pyowa.Heading('Header of size 6', 6)

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(text=str, level=int)
    def __init__(self, text, level=1):
        if not 1 <= level <= 6:
            raise HeadingError('Heading level can have value from 1 to 6.')
        Heading._cnt += 1
        type_ = 'heading'
        id_ = f'{type_}_{Heading._cnt}'
        super().__init__(id_, type_)
        self.add_property('text', text)
        self.add_property('level', level)


class ImageFileError(Exception):
    pass


class ImageFromWizardDir(BaseElement):
    """ Visualize an image which is located in the wizard directory.
        The html element tag is "<img>".
        Supported Formats: gif, png, svg, jpg, jpeg.

        Parameter
        ---------
        tail: str
            The image path relative to the wizard directory.

        Example
        -------
        >>> import pyowa
        >>> image = pyowa.ImageFromWizardDir('my_file.png')
        >>> image.set_size_in_px(300, 300)

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0
    _supported_formats = ['.gif', '.png', '.svg', '.jpg', '.jpeg']

    @arg.check_type(tail=str)
    def __init__(self, tail):
        self._check_support(tail)
        ImageFromWizardDir._cnt += 1
        type_ = 'image_wizard_dir'
        id_ = f'{type_}_{ImageFromWizardDir._cnt}'
        super().__init__(id_, type_)
        self.add_property('src', tail)

    def _check_support(self, file):
        ext = os.path.splitext(file)[1]
        if ext.lower() not in self._supported_formats:
            msg = f'Image file with extension {ext} not supported'
            raise ImageFileError(msg)

    @arg.check_type(width=int, height=int)
    def set_size_in_px(self, width, height):
        """ Set image size in pixel.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property(('style', 'width'), f'{width}px')
        self.add_property(('style', 'heigth'), f'{height}px')

    @arg.check_type(width=int, height=int)
    def set_size_in_percent(self, width, height):
        """ Set image size in percent.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property(('style', 'width'), f'{width}%')
        self.add_property(('style', 'heigth'), f'{height}%')


class ImageFromRegisteredFiles(ImageFromWizardDir):
    """ Visualize an image which is registered in optiSLang as output file.
        The html element tag is "<img>".
        Supported Formats: gif, png, svg, jpg, jpeg.

        Parameter
        ---------
        id_: str
            The registered file id.

        Example
        -------
        >>> import pyowa
        >>> image = pyowa.ImageFromRegisteredFiles('my_file.png')
        >>> image.set_size_in_px(300, 300)

        See Also
        --------
        ImageFromWizardDir: An image which is located in the wizard directory.
    """
    _cnt = 0

    @arg.check_type(registered_file_id=str)
    def __init__(self, registered_file_id):
        ImageFromRegisteredFiles._cnt += 1
        type_ = 'file_preview'
        id_ = f'{type_}_{ImageFromRegisteredFiles._cnt}'
        BaseElement.__init__(self, id_, type_)
        self.add_property('filename', registered_file_id)


class HTMLFromRegisteredFiles(BaseElement):
    """ Visualize an html file which is registered in optiSLang as output file.
        The html element tag is "<iframe>".

        Parameter
        ---------
        registered_file_id: str
            The registered file id.

        Example
        -------
        >>> import pyowa
        >>> html = pyowa.HTMLFromRegisteredFiles('my_file.png')
        >>> html.set_size_in_px(300, 300)

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(registered_file_id=str)
    def __init__(self, registered_file_id):
        HTMLFromRegisteredFiles._cnt += 1
        type_ = 'file_preview'
        id_ = f'{type_}_{HTMLFromRegisteredFiles._cnt}'
        super().__init__(id_, type_)
        self.add_property('filename', registered_file_id)

    @arg.check_type(title=str)
    def set_title(self, title):
        """ Set a title for the html iframe window

            Parameter
            ---------
            title: str
                The title for the html iframe window
        """
        self.add_property('title', title)

    @arg.check_type(width=int, height=int)
    def set_size_in_px(self, width, height):
        """ Set iframe window size in pixel.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property('width', f'{width}px')
        self.add_property('height', f'{height}px')

    @arg.check_type(width=int, height=int)
    def set_size_in_percent(self, width, height):
        """ Set iframe window size in percent.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property('width', f'{width}%')
        self.add_property('height', f'{height}%')


class TextFromRegisteredFiles(BaseElement):
    """ Visualize a text file which is registered in optiSLang as output file.
        The html element tag is "<pre>".

        Parameter
        ---------
        registered_file_id: str
            The registered file id.

        Example
        -------
        >>> import pyowa
        >>> txt = pyowa.TextFromRegisteredFiles('my_file.txt')

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(registered_file_id=str)
    def __init__(self, registered_file_id):
        TextFromRegisteredFiles._cnt += 1
        type_ = 'file_preview'
        id_ = f'{type_}_{TextFromRegisteredFiles._cnt}'
        super().__init__(id_, type_)
        self.add_property('filename', registered_file_id)


class VideoFileError(Exception):
    pass


class VideoFromWizardDir(BaseElement):
    """ Visualze a video which is located in the wizard directory.
        The html element tag is "<video>".
        Supported Formats: mp4, ogv, webm.

        Parameter
        ---------
        tail: str
            The video path relative to the wizard directory.

        Example
        -------
        >>> import pyowa
        >>> video = pyowa.VideoFromWizardDir('drone_owa_in_minerva.mp4')
        >>> video.set_autoplay_on()
        >>> video.set_controls_on()
        >>> video.set_loop_on()
        >>> video.set_muted()
        >>> video.set_size_in_px(300, 300)

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0
    _supported_formats = ['.mp4', '.ogv', '.webm']

    @arg.check_type(tail=str)
    def __init__(self, tail):
        self._check_support(tail)
        VideoFromWizardDir._cnt += 1
        type_ = 'video_wizard_dir'
        id_ = f'{type_}_{VideoFromWizardDir._cnt}'
        super().__init__(id_, type_)
        self.add_property('src', tail)

    def _check_support(self, file):
        ext = os.path.splitext(file)[1]
        if ext.lower() not in self._supported_formats:
            msg = f'Video file with extension {ext} not supported'
            raise VideoFileError(msg)

    @arg.check_type(width=int, height=int)
    def set_size_in_px(self, width, height):
        """ Set video size in pixel.

            Parameter
            ---------
            width: int
                The video width.
            height: int
                The video height.
        """
        self.add_property(('style', 'width'), f'{width}px')
        self.add_property(('style', 'heigth'), f'{height}px')

    def set_autoplay_on(self):
        """ Set the video to autoplay on page load
        """
        self.add_property('autoplay', 1)

    def set_controls_on(self):
        """ Display the video controls (play, pause, mute, etc.)
        """
        self.add_property('controls', 1)

    def set_loop_on(self):
        """ Play the video in loop
        """
        self.add_property('loop', 1)

    def set_muted(self):
        """ Play the video without audio
        """
        self.add_property('muted', 1)

    @arg.check_type(src=str)
    def set_poster(self, src):
        """ Set a thumbnail image for the video

            Parameter
            ---------
            src:
                tail of the image path located in the wizard directory
        """
        self.add_property('poster', src)

    def set_preload_none(self):
        """ The browser should NOT load the video when the page loads
        """
        self.add_property('preload', 'none')

    def set_preload_metadata(self):
        """ The browser should load only metadata when the page loads
        """
        self.add_property('preload', 'metadata')

    def set_preload_auto(self):
        """ The browser should load the entire video when the page loads
        """
        self.add_property('preload', 'auto')


class VideoFromRegisteredFiles(VideoFromWizardDir):
    """ Visualze a video which is registered in optiSLang as output file.
        The html element tag is "<video>".
        Supported Formats: mp4, ogv, webm.

        Parameter
        ---------
        registered_file_id: str
            The registered file id.

        Example
        -------
        >>> import pyowa
        >>> video = pyowa.VideoFromRegisteredFiles('my_file.mp4')
        >>> video.set_size_in_px(300, 300)

        See Also
        --------
        VideoFromWizardDir: An video which is located in the wizard directory.
    """
    _cnt = 0

    @arg.check_type(registered_file_id=str)
    def __init__(self, registered_file_id):
        self._check_support(registered_file_id)
        VideoFromRegisteredFiles._cnt += 1
        type_ = 'file_preview'
        id_ = f'{type_}_{VideoFromRegisteredFiles._cnt}'
        BaseElement.__init__(self, id_, type_)
        self.add_property('filename', registered_file_id)


class ButtonDownloadRegisteredFile(BaseElement):
    """ A button to open/download a file which is registered in optiSLang as output file.
        The html element tag is "<button>".

        Parameter
        ---------
        text: str
            The button text. Can also be an empty string.
        registered_file_id: str
            The registered file id.

        Example
        -------
        >>> import pyowa
        >>> download_csv = pyowa.ButtonDownloadRegisteredFile('Download me', 'my_file.csv')
        >>> open_pdf = pyowa.ButtonDownloadRegisteredFile('Open me', 'my_file.pdf')

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    @arg.check_type(registered_file_id=str)
    def __init__(self, text, registered_file_id):
        ButtonDownloadRegisteredFile._cnt += 1
        type_ = 'button_download_reg_file'
        id_ = f'{type_}_{ButtonDownloadRegisteredFile._cnt}'
        super().__init__(id_, type_)
        self.add_property('filename', registered_file_id)
        self.add_property('buttonText', text)
        # will stay disabled until the file content is available
        self.add_property('disabled', True)

    @arg.check_type(tail=str)
    def set_icon(self, tail):
        """ Add an icon which is located the wizard directory.
        """
        self.add_property('icon', tail)

    @arg.check_type(width=int)
    def set_width(self, width):
        """ Set the width of the button.

            Parameter
            ---------
            width: int
                Required width of the button in pixels.

            Example
            -------
            >>> import pyowa
            >>> download_csv = pyowa.ButtonLinkedToWizardDir('Download me', 'my_file.csv')
            >>> download_csv.set_width(200)
        """
        width_in_px = f'{width}px'
        self.add_property(('style', 'width'), width_in_px)


class LineHorizontal(BaseElement):
    """ A static horizontal line.
        The html element tag is "<hr>".

        Example
        -------
        >>> import pyowa
        >>> line = pyowa.LineHorizontal()

        See Also
        --------
        BaseElement: The base class for all elements.
    """
    _cnt = 0

    def __init__(self):
        LineHorizontal._cnt += 1
        type_ = 'line_horizontal'
        id_ = f'{type_}_{LineHorizontal._cnt}'
        super().__init__(id_, type_)


class ProjectStarter(BaseElementPlaceholder):
    """ The optiSLang project starter element.

        It can provide an user-depended host selection as well as host settings.
        This can be defined via "remotes.json" file located in the wizard directory.
        See web_service/doc/spec/remotes.json for the json-schema.

        On run it starts the python script given with "script_name" located in custom_data.
        See wizard directory "run_project.py" for more details.

        Parameter
        ---------
        script_name: str
            The python scipt name to run the project.
        project_name: str
            The optiSLang project name (opf).
        name: str. optional. Default is an upcounting expression.
            The placeholder name.

        Example
        -------
        >>> import pyowa
        >>> starter = pyowa.ProjectStarter('run_project.py', 'overview_project.opf', 'MyStarter')

        See Also
        --------
        BaseElement: The base class for all elements.
    """

    @arg.check_type(script_name=str, project_name=str, name=str)
    def __init__(self, script_name, project_name, name=''):
        type_ = 'project_starter'
        id_ = type_
        super().__init__(id_, type_)
        self.add_property('scriptName', script_name)
        self.add_property('projectName', project_name)

        self._set_placeholder(name or id_, '')
        self.set_return_to_overview()

    def set_return_to_overview(self):
        self.add_property('forwardToMonitoring', False)
        self.add_property('returnToOverview', True)

    def set_forward_to_monitoring(self):
        self.add_property('forwardToMonitoring', True)
        self.add_property('returnToOverview', False)

# -------------------------------------------------------------------------------------------------
### modifiable elements
# -------------------------------------------------------------------------------------------------
class NumberError(Exception):
    pass


class Number(BaseElementPlaceholder):
    """ A modifiable number.
        The html element tag is "<input[type=number]>".
        If value is of type int: stepsize is 1.
        If value is of type float: stepsize is "any".

        Parameter
        ---------
        value: int or float
            The default value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> number = pyowa.Number(1.0, 'MyNumber')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=(int, float, type(None)), name=str)
    def __init__(self, value, name=''):
        Number._cnt += 1
        type_ = 'number'
        id_ = f'{type_}_{Number._cnt}'
        super().__init__(id_, type_)

        step_size = self._get_stepsize(value)
        self.set_stepsize(step_size)
        self._set_placeholder(name or id_, value)

    @staticmethod
    def _get_stepsize(value):
        if isinstance(value, int):
            return 1
        return 'any'

    @arg.check_type(stepsize=(int, float, str))
    def set_stepsize(self, stepsize):
        """ Set the step size for the modifiable number element.

            Parameter
            ---------
            stepsize: int/float.
                Step size for the number element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number.set_stepsize(0.001)
        """
        if isinstance(stepsize, str):
            if stepsize != 'any':
                msg = 'Expected {} or {}. Got {}'.format(type(1), type(0.1), type(''))
                raise NumberError(msg)
        self.add_property('step', stepsize)

    @arg.check_type(min_value=(int, float))
    def set_min_value(self, min_value):
        """ Set the minimum bound for the modifiable number element.

            Parameter
            ---------
            min_value: int, float.
                Value of the minimum bound for the number element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number.set_min_value(-20)
        """
        self.add_property('min', min_value)

    @arg.check_type(max_value=(int, float))
    def set_max_value(self, max_value):
        """ Set the maximum bound for the modifiable number element.

            Parameter
            ---------
            max_value: int, float.
                Value of the maximum bound for the number element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number.set_max_value(20)
        """
        self.add_property('max', max_value)

    @arg.check_type(min_value=(int, float), max_value=(int, float))
    def set_bounds(self, min_value, max_value):
        """ Set the bounds for the modifiable number element.

            Parameter
            ---------
            min_value: int, float.
                Value of the minimum bound for the number element.
            max_value: int, float.
                Value of the maximum bound for the number element.

            Example
            -------
            >>> import pyowa
            >>> number = pyowa.Number(1.0, 'MyNumber')
            >>> number.set_bounds(-20, 20)
        """
        self.set_min_value(min_value)
        self.set_max_value(max_value)
        return self


class IFrame(BaseElementPlaceholder):
    """ Visualize a html file which is located in the wizard directory or plain html source code.
        The html element tag is "<iframe>".

        Parameter
        ---------
        value: str
            The html file path relative to the wizard direcory or html source code.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa

        >>> # see my_file.html:
        >>> html_file = pyowa.IFrame('my_file.html')
        >>> html_file.set_size_in_px(300, 300)

        >>> html_code = pyowa.IFrame('<span>MyHTML</span>')
        >>> html_code.set_size_in_px(300, 300)

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=str, name=str)
    def __init__(self, value, name=''):
        IFrame._cnt += 1
        type_ = 'iframe'
        id_ = f'{type_}_{IFrame._cnt}'
        super().__init__(id_, type_)
        self._set_placeholder(name or id_, value)
        self._set_value_type(value)

    def _set_value_type(self, value):
        if self._is_file(value):
            self.add_property('isFile', True)
        else:
            self.add_property('isFile', False)

    @staticmethod
    def _is_file(value):
        path = pathlib.Path(value)
        if path.suffix == '.html':
            return True
        return False

    @arg.check_type(title=str)
    def set_title(self, title):
        """ Set a title for the html iframe window

            Parameter
            ---------
            title: str
                The title for the html iframe window
        """
        self.add_property('title', title)

    @arg.check_type(width=int, height=int)
    def set_size_in_px(self, width, height):
        """ Set iframe window size in pixel.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property('width', f'{width}px')
        self.add_property('height', f'{height}px')

    @arg.check_type(width=int, height=int)
    def set_size_in_percent(self, width, height):
        """ Set iframe window size in percent.

            Parameter
            ---------
            width: int
                The image width.
            height: int
                The image height.
        """
        self.add_property('width', f'{width}%')
        self.add_property('height', f'{height}%')


class HTMLFromWizardDir(IFrame):
    """ Visualize a html file which is located in the wizard directory or plain html source code.
        The html element tag is "<iframe>".

        Parameter
        ---------
        value: str
            The html file path relative to the wizard direcory or html source code.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa

        >>> # see my_file.html:
        >>> html_file = pyowa.HTMLFromWizardDir('my_file.html')
        >>> html_file.set_size_in_px(300, 300)

        >>> html_code = pyowa.HTMLFromWizardDir('<span>MyHTML</span>')
        >>> html_code.set_size_in_px(300, 300)

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    pass


class TextArea(BaseElementPlaceholder):
    """ A modifiable text area.
        The html element tag is "<textarea>".

        Parameter
        ---------
        value: str
            The default text.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> text_area = pyowa.TextArea('This is an example comment to indicate the usage of Text Area', 'CommentArea1')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=str, name=str)
    def __init__(self, value, name=''):
        TextArea._cnt += 1
        type_ = 'text_area'
        id_ = f'{type_}_{TextArea._cnt}'
        super().__init__(id_, type_)
        self._set_placeholder(name or id_, value)

    def set_required(self):
        """ Make the input for the text area mandatory
        """
        self.add_property('required', True)

    @arg.check_type(width=int, height=int)
    def set_size(self, width, height):
        """ Set the size of the text area.

            Parameters
            ----------
            width: int
                visible width of the text area
            height: int
                visible number of lines in the text area
        """

        self.add_property('cols', width)
        self.add_property('rows', height)

    @arg.check_type(placeholder_text=str)
    def set_placeholder(self, placeholder_text):
        """ Set a placeholder text for the text field

            Parameters
            ----------
            placeholder_text: str
                the placeholder text to be displayed in the text area
        """

        self.add_property('placeholder', placeholder_text)

    @arg.check_type(max_length=int)
    def set_max_length(self, max_length):
        """ Set the maximum number of characters allowed in the text area

            Parameters
            ----------
            max_length: int
                maximum number of characters allowed in the text area
        """
        self.add_property('maxlength', max_length)

    def set_spell_check_false(self):
        self.add_property('spellcheck', False)


class Select(BaseElementPlaceholder):
    """ Select an option from a dropdown box.
        The html element tag is "<select>".

        Parameter
        ---------
        value: int, float, str
            The default value.
        options: list
            The options to select.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> select_letter = pyowa.Select('A', ['A', 'B', 'C'], 'SelectLetter')
        >>> select_letter.set_action_script('action_Select.py')

        >>> select_numbered_letter = pyowa.Select('', [''], 'SelectNumberedLetter')

        >>> # action script start: action_Select.py
        >>> def app(name, placeholders, project_info):
        >>>    # do nothing if action is not comming from "SelectLetter"
        >>>    if name != 'SelectLetter':
        >>>        return placeholders
        >>>    # set options in dependecy from currenly selected letter
        >>>    letter = placeholders['SelectLetter']['value']
        >>>    options = [''] + [f'{letter}{i}' for i in range(5)]
        >>>    placeholders['SelectNumberedLetter']['options'] = options
        >>>
        >>>    return placeholders
        >>> # action script stop

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=str, options=list, name=str)
    def __init__(self, value, options, name=''):
        Select._cnt += 1
        type_ = 'select'
        id_ = f'{type_}_{Select._cnt}'
        super().__init__(id_, type_)

        if value not in options:
            options.insert(0, value)

        self.placeholder_options = options
        self._set_placeholder(name or id_, value)

    def get_placeholder_value(self):
        """ Return the value and possible options of the dropdown box.
        """
        placeholder_value = super().get_placeholder_value()
        placeholder_value['options'] = self.placeholder_options
        return placeholder_value

    # def allow_multiple_selections(self):  # ows site element Select does not support this yet
    #     """ Allow multiple options from the list to be selected
    #     """
    #     self.add_property('multiple', True)

    def allow_sort(self):
        """ Allow the options to be sorted alphabetically
        """
        self.add_property('sort', True)

    # @arg.check_type(text=str)
    # def set_default_display_text(self, text):
    #     """ Display a default text in case no options are available

    #     Parameter
    #     ---------
    #         text: str
    #             The deault text to be displayed
    #     """
    #     self.add_property('defaultText', text)


class SelectProject(BaseElementPlaceholder):
    """ A dropdown box to select a project from all projects owned by the logged in user.
        The selected project's path becomes the value of this element's placeholder.
        The html element tag is "<select>".

        Parameter
        ---------
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> select_project = pyowa.SelectProject('MyProjectSelector')
        >>> select_project.set_action_script('update_label.py')
        >>> table = pyowa.Table()
        >>> table.insert_row(0, [pyowa.Label('Path: '), pyowa.LabelDynamic(None, 'MyLabel')])
        >>>
        >>> # action script start: update_label.py
        >>> def app(name, placeholders, project_info):
        >>>     project_path = placeholders['MyProjectSelector']['value']
        >>>     placeholders['MyLabel']['value'] = project_path
        >>>     return placeholders
        >>> # action script stop
        >>>

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(name=str)
    def __init__(self, name=''):
        SelectProject._cnt += 1
        type_ = 'select_project'
        id_ = f'{type_}_{SelectProject._cnt}'
        super().__init__(id_, type_)
        self._set_placeholder(name or id_, '')


class RadioButton(BaseElementPlaceholder):
    """ Select an option from a group of radio buttons.
        The html element tag is "<input[type=radio]>".

        Parameter
        ---------
        options: list
            The options to select.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> radio_button = pyowa.RadioButton(['A', 'B', 'C'], 'MyRadioButton')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(options=list, name=str)
    def __init__(self, options, name=''):
        RadioButton._cnt += 1
        type_ = 'radio_button'
        id_ = f'{type_}_{RadioButton._cnt}'
        super().__init__(id_, type_)

        self.placeholder_options = options
        self._set_placeholder(name or id_, None)

    def get_placeholder_value(self):
        """ Return the value and possible options of the dropdown box.
        """
        placeholder_value = super().get_placeholder_value()
        placeholder_value['options'] = self.placeholder_options
        return placeholder_value


class Checkbox(BaseElementPlaceholder):
    """ Turn something on or off using a checkbox.
        The html element tag is "<input[type=checkbox]>".

        Parameter
        ---------
        value: bool
            The default value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> table = pyowa.Table()
        >>> table.append_child(0, pyowa.Checkbox(True, 'MyCheckBox'))
        >>> table.append_child(0, pyowa.Label('Checklist item'))

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=bool, name=str)
    def __init__(self, value, name=''):
        Checkbox._cnt += 1
        type_ = 'checkbox'
        id_ = f'{type_}_{Checkbox._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, value)


class Toggle(BaseElementPlaceholder):
    """ Turn something on or off using a toggle button.

        Parameter
        ---------
        value: bool
            The default value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> toggle = pyowa.Toggle(True, 'MyToggle')
        >>> toggle.set_action_script('action_Toggle.py')

        >>> label = pyowa.LabelDynamic('On', 'MyLabel')

        >>> # action script start: action_Toggle.py
        >>> def app(name, placeholders, project_info):
        >>>     toggle_value = placeholders['MyToggle']['value']
        >>>     placeholders['MyLabel']['value'] = 'On' if toggle_value else 'Off'
        >>>     return placeholders
        >>> # action script stop


        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=bool, name=str)
    def __init__(self, value, name=''):
        Toggle._cnt += 1
        type_ = 'toggle'
        id_ = f'{type_}_{Toggle._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, value)


class Text(BaseElementPlaceholder):
    """ A modifiable text field.
        The html element tag is "<input[type=text]>".

        Parameter
        ---------
        value: str
            The default value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> text = pyowa.Text('MyContent', 'MyText')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=str, name=str)
    def __init__(self, value, name=''):
        Text._cnt += 1
        type_ = 'text'
        id_ = f'{type_}_{Text._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, value)


class BarPlot(BaseElementPlaceholder):
    """ A bar plot to visualize data from a list of dictionaries.
        For example, the following data which is in csv form:

            GraphType, Likes, Dislikes
            BarCharts, 5, 5
            PieGraphs, 2, 8
            Histograms, 3, 7

        should be organized as:

            [{'GraphType': 'BarCharts', 'Likes': 5, 'Dislikes': 5},
            {'GraphType': 'PieGraphs', 'Likes': 2, 'Dislikes': 8},
            {'GraphType': 'Histograms', 'Likes': 3, 'Dislikes': 7}]

        Parameter
        ---------
        value: list of dict
            Plotting data. Plotting data should be organized as a list of dictionaries.
        name: str, optional
            the placeholder name. Default is an upcounting expression

        Example
        -------
        >>> import pyowa
        >>> plotting_data = [{'GraphType': 'BarCharts', 'Likes': 5, 'Dislikes': 5},
        >>>                  {'GraphType': 'PieGraphs', 'Likes': 2, 'Dislikes': 8},
        >>>                  {'GraphType': 'Histograms', 'Likes': 3, 'Dislikes': 7},]
        >>> bar_plot = pyowa.BarPlot(plotting_data, 'awesome_bar_plot')
    """

    _cnt = 0

    @arg.check_type(value=(list, type(None)), name=str)
    def __init__(self, value, name=''):
        BarPlot._cnt += 1
        type_ = 'bar_plot'
        id_ = f'{type_}_{BarPlot._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, value)

    def set_bar_colors(self, colors):
        """ Set the colors for the bars in the plot

            Parameters
            ----------
            colors: list
                list of HTML color names or color hex
        """
        self.add_property('barColors', colors)


class ButtonLinkedToWizardDir(BaseElementPlaceholder):
    """ Open/download a file located the wizard directory.
        The html element tag is "<button>".

        Parameter
        ---------
        text: str
            The button text. Can also be an empty string.
        tail: str
            The tail of the filepath.

        Example
        -------
        >>> import pyowa
        >>> download_csv = pyowa.ButtonLinkedToWizardDir('Download me', 'my_file.csv')
        >>> open_pdf = pyowa.ButtonLinkedToWizardDir('Open me', 'my_file.pdf')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(text=str, tail=str)
    def __init__(self, text, tail):
        ButtonLinkedToWizardDir._cnt += 1
        type_ = 'button_linked_wizard_dir'
        id_ = f'{type_}_{ButtonLinkedToWizardDir._cnt}'
        super().__init__(id_, type_)
        self.add_property('href', tail)

        self._set_placeholder(id_, text)

    @arg.check_type(tail=str)
    def set_icon(self, tail):
        """ Add an icon which is located the wizard directory.
        """
        self.add_property('icon', tail)

    @arg.check_type(width=int)
    def set_width(self, width):
        """ Set the width of the button.

            Parameter
            ---------
            width: int
                Required width of the button in pixels.

            Example
            -------
            >>> import pyowa
            >>> download_csv = pyowa.ButtonLinkedToWizardDir('Download me', 'my_file.csv')
            >>> download_csv.set_width(200)
        """
        width_in_px = f'{width}px'
        self.add_property(('style', 'width'), width_in_px)


class ButtonDownloadTextData(BaseElementPlaceholder):
    """ Download a file containing given text data.
        The html element tag is "<button>".

        Parameter
        ---------
        downloadable_text: str
            The text data that will be contained within the downloaded file.
        button_text: str
            The button text. Can also be an empty string.
        out_file_name: str
            Tha name of the file that will be downloaded.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> download_csv = pyowa.ButtonDownloadTextData('Show this text', 'Download me', 'my_file.csv')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(downloadable_text=(str, type(None)), button_text=str, out_file_name=str, name=str)
    def __init__(self, downloadable_text, button_text, out_file_name, name=''):
        ButtonDownloadTextData._cnt += 1
        type_ = 'button_download_text'
        id_ = f'{type_}_{ButtonDownloadTextData._cnt}'
        super().__init__(id_, type_)

        if downloadable_text:
            for symbol, escape_seq in HTML_ESCAPE_SEQUENCE.items():
                downloadable_text = downloadable_text.replace(symbol, escape_seq)

        self.add_property('outFile', out_file_name)
        self.add_property('buttonText', button_text)
        self._set_placeholder(name or id_, downloadable_text)


class ButtonFileUpload(BaseElementPlaceholder):
    """ Upload a file into the project directory.
        The html element tag is "<button>".

        Parameter
        ---------
        name: str
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> upload = pyowa.ButtonFileUpload()

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
   """
    _cnt = 0

    @arg.check_type(name=str)
    def __init__(self, name=''):
        ButtonFileUpload._cnt += 1
        type_ = 'button_file_upload'
        id_ = f'{type_}_{ButtonFileUpload._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, '')


class ButtonAction(BaseElementPlaceholder):
    """ A button that calls a python action script on click.
        The html element tag is "<button>".

        Parameter
        ---------
        text: str
            The button text. Can also be an empty string.
        action_script: str
            The tail of the python action script located in custom_data.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> button_count = pyowa.ButtonAction('Count', 'action_ButtonAction.py', 'MyCounter')
        >>> progress_count = pyowa.Progress(0, 100, 'MyProgress')

        >>> # action script start: action_ButtonAction.py
        >>> def app(name, placeholders, project_info):
        >>>    # do nothing if action is not comming from "MyCounter"
        >>>    if name != 'MyCounter':
        >>>        return placeholders
        >>>
        >>>    # add "+10" to the "value" of "MyProgress" on every "MyCounter" click
        >>>    placeholders['MyProgress']['value'] += 10
        >>>
        >>>    return placeholders
        >>> # action script stop

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(text=str, action_script=str, name=str)
    def __init__(self, text, action_script, name=''):
        ButtonAction._cnt += 1
        type_ = 'button_action'
        id_ = f'{type_}_{ButtonAction._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, text)
        self.set_action_script(action_script)

    @arg.check_type(icon=str)
    def set_icon(self, icon):
        """ Add an icon which is located the wizard directory.

            Parameter
            ---------
            icon: image file in the wizard folder.
                The icon that is to be displayed on the button.

            Example
            -------
            >>> import pyowa
            >>> progress = pyowa.Progress(0, 100, 'MyProgress')
            >>> progress_counter = pyowa.ButtonAction('Count', 'on_click_count.py', 'MyCounter')
            >>> progress_counter.set_icon('my_icon.png')
        """
        self.add_property('icon', icon)

    @arg.check_type(confirm_question=str)
    def set_confirm_question(self, confirm_question):
        """ Set a confirmation question to be posed before the action script is run.

            Parameter
            ---------
            confirm_question: str.
                The question to be posed to the user.

            Example
            -------
            >>> import pyowa
            >>> progress = pyowa.Progress(0, 100, 'MyProgress')
            >>> progress_counter = pyowa.ButtonAction('Count', 'on_click_count.py', 'MyCounter')
            >>> progress_counter.set_confirm_question('Confirm button click')
        """
        self.add_property('confirmQuestion', confirm_question)

    @arg.check_type(width=int)
    def set_width(self, width):
        """ Set the width of the button.

            Parameter
            ---------
            width: int
                Required width of the button in pixels.

            Example
            -------
            >>> import pyowa
            >>> progress = pyowa.Progress(0, 100, 'MyProgress')
            >>> progress_counter = pyowa.ButtonAction('Count', 'on_click_count.py', 'MyCounter')
        """
        width_in_px = f'{width}px'
        self.add_property(('style', 'width'), width_in_px)


class ButtonWidget(BaseElementPlaceholder):
    """ A button widget to run an action defined as another python script similar to ButtonAction.
        The button widget resembles a widget in the optiSLang webservice.

        Parameter
        ---------
        text: str
            The widget text.
        action_script: str
            The tail of the python filepath.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> button_widget = pyowa.ButtonWidget('My App', 'build_my_app.py', 'my_app')
        >>> button_widget.add_property(('style', 'width'), '250px')

        See Also
        --------
        ButtonAction: A button that calls a python action script on click.
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(text=str, action_script=str, name=str)
    def __init__(self, text, action_script, name=''):
        ButtonWidget._cnt += 1
        type_ = 'button_widget'
        id_ = f'{type_}_{ButtonWidget._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, text)
        self.set_action_script(action_script)

    @arg.check_type(text=str)
    def set_button_text(self, text):
        """ Set an in-button text for the widget

            Parameter
            ---------
            text:  str.
                The text to be displayed on the button in the widget
        """
        self.add_property('buttonText', text)

    def set_description(self, description):
        """ Set an description for the widget

            Parameter
            ---------
            description:  str.
                A short description about what the widget does.
        """
        self.add_property('description', description)


class Progress(BaseElementPlaceholder):
    """ A progress bar.
        The html element tag is "<progress>".

        Parameter
        ---------
        value: int
            The default value.
        max_value: int
            The maximum value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> progress = pyowa.Progress(25, 100, 'MyProgress')

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=int, max_value=int, name=str)
    def __init__(self, value, max_value, name=''):
        Progress._cnt += 1
        type_ = 'progress'
        id_ = f'{type_}_{Progress._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, value)
        self.add_property('max', max_value)

    @arg.check_type(width=int)
    def set_width_in_px(self, width):
        """ Set the width of the progress bar in pixels

            Parameter
            ---------
            width: int
                width of the progress bar in pixels.

            Example
            -------
            >>> import pyowa
            >>> progress = pyowa.Progress(0, 100, 'MyProgress')
            >>> progress.set_width_in_px(200)
        """
        width_in_px = f'{width}px'
        self.add_property(('style', 'width'), width_in_px)


class LabelDynamic(BaseElementPlaceholder):
    """ A modifiable label.
        The html element tag is "<span>".

        Parameter
        ---------
        value: str or None
            The default value.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> result_label = pyowa.LabelDynamic(None, 'MyResultLabel')
        >>> button_action = pyowa.ButtonAction('Click To Update', 'action_LabelDynamic.py', 'ex_button_action')
        >>>
        >>> # action script start: action_LabelDynamic.py
        >>> def app(name, placeholders, project_info):
        >>>     placeholders['MyResultLabel']['value'] = 'Updated Label'
        >>>     return placeholders
        >>> # action script stop

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(value=(str, type(None)), name=str)
    def __init__(self, value, name=''):
        LabelDynamic._cnt += 1
        type_ = 'label_dynamic'
        id_ = f'{type_}_{LabelDynamic._cnt}'
        super().__init__(id_, type_)
        self._set_placeholder(name or id_, value)
        self.set_readonly()

    def get_placeholder_value(self):
        """ Return the placeholder value with the options.
        """
        placeholder_value = super().get_placeholder_value()
        placeholder_value['style'] = {
                'backgroundColor': None,
                'color': None,
                }
        return placeholder_value


class LabelStatus(BaseElementPlaceholder):
    """ A label that calls a python action script if its status text changes.
        The html element tag is "<span>".

        Parameter
        ---------
        status: str
            The status text. Can also be an empty string.
        action_script: str
            The tail of the python filepath.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> status = pyowa.LabelStatus('Idle', 'action_LabelStatus.py', 'MyStatus')
        >>> # uncomment to hide the status:
        >>> #status.set_hidden()

        >>> progress = pyowa.Progress(0, 100, 'MyProgressBar')
        >>> button_action = pyowa.ButtonAction('Start', 'action_LabelStatus.py', 'MyButtonAction')

        >>> # action script start: action_LabelStatus.py
        >>> import time
        >>> def app(name, placeholders, project_info):
        >>>     status = placeholders['MyStatus']['value']
        >>>     if status == 'Idle':
        >>>         placeholders['MyProgressBar']['value'] = 50
        >>>         placeholders['MyStatus']['value'] = 'Starting'
        >>>     elif status == 'Starting':
        >>>         time.sleep(2)
        >>>         placeholders['MyProgressBar']['value'] = 100
        >>>         placeholders['MyStatus']['value'] = 'Completed'
        >>>     return placeholders
        >>> # action script stop

        See Also
        --------
        BaseElementPlaceholder: The base class for modifiable elements.
    """
    _cnt = 0

    @arg.check_type(status=str, action_script=str, name=str)
    def __init__(self, status, action_script, name=''):
        LabelStatus._cnt += 1
        type_ = 'label_status'
        id_ = f'{type_}_{LabelStatus._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, status)
        self.set_action_script(action_script)


class LabelAction(BaseElementPlaceholder):
    """ A label that run a python action script on click.
        The html element tag is "<span>".

        Parameter
        ---------
        text: str
            The label text.
        action_script: str
            The tail of the python filepath.
        name: str, optional
            The placeholder name. Default is an upcounting expression.

        Example
        -------
        >>> import pyowa
        >>> new_label_action = pyowa.LabelAction('Click Me!', 'action_LabelAction.py', 'my_label_action')
        >>>
        >>> # action script start: action_LabelAction.py
        >>> def app(name, placeholders, project_info):
        >>>     label = placeholders[name]['value']
        >>>     placeholders[name]['value'] = 'You clicked me!' if label == 'Click Me!' else 'Click Me!'
        >>>     return placeholders
        >>> # action script stop
    """
    _cnt = 0

    def __init__(self, text, action_script, name=None):
        LabelAction._cnt += 1
        type_ = 'label_action'
        id_ = f'{type_}_{LabelAction._cnt}'
        super().__init__(id_, type_)

        self._set_placeholder(name or id_, text)
        self.set_action_script(action_script)
        self.add_property(('style', 'cursor'), 'pointer')
        self.set_mouse_over_color('blue')

    def set_confirm_question(self, confirm_question):
        self.add_property('confirmQuestion', confirm_question)

    def set_mouse_over_color(self, mouse_over_color):
        self.add_property('mouseOverColor', mouse_over_color)
