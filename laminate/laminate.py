# -*- coding: utf-8 -*-
# pylint: disable=R0913, R0201
"""Laminate - Create beatifull yet simple html and pdf documents
from markdown"""
from os import path, makedirs
from shutil import copyfile, copytree, rmtree
from jinja2 import Environment, FileSystemLoader
import markdown
import laminate_default # pylint: disable=E0401

class Laminate():
    """This class parses markdown and combines the result with
    jinja templates and config variables provided by the user."""

    def __init__(self, **config):
        self._config = config
        self._toc = ""

    def create_html(self, input_file, build_dir='build', custom_template=None):
        """Create the complete report as an html document

        Parameters:
            input_file : (str)
                Path to the index markdownfile.

            build_dir : (str)
                Path to output directory. **default: build**

            custom_template : (str)
                Path to custom template directory

        Returns:
            None:
                Creates a new html document in the directory
                spesified by build_dir
        """
        input_dir = path.dirname(path.abspath(input_file))
        self._clean_up_build_dir(build_dir, input_dir)
        parsed_html = self.parse_jinja(input_file, custom_template)
        filename = self._output_filename(input_dir, build_dir, 'index.html')
        self._write_result(parsed_html, filename)

        if custom_template is None:
            template_dir = path.join(list(laminate_default.__path__)[0], 'templates')
        else:
            template_dir = custom_template[0]

        copyfile(path.join(template_dir, 'index.css'),
                 path.join(build_dir, input_dir.split('/')[-1], 'index.css'))
        copytree(path.join(template_dir, 'fonts/'),
                 path.join(build_dir, input_dir.split('/')[-1], 'fonts/'))
        copytree(path.join(template_dir, 'images/'),
                 path.join(build_dir, input_dir.split('/')[-1], 'images/'))

    def _clean_up_build_dir(self, build_dir, input_dir):
        if path.exists(path.join(build_dir, input_dir.split('/')[-1])):
            rmtree(path.join(build_dir, input_dir.split('/')[-1]))

    def _write_result(self, content, output_file):
        makedirs(path.dirname(output_file), exist_ok=True)
        with open(output_file, 'wt') as f:
            f.write(content)

    def _output_filename(self, input_dir, build_dir, filename):
        output_dir_name = input_dir.split('/')[-1]
        return path.join(build_dir, output_dir_name, filename)

    def parse_markdown(self, text, extentions=()):
        # pylint: disable=R0201
        """Parse markdown to html

        Parameters:
            text : (str)
                text to be converted to markdown

        Returns:
            str:
                String containing the parsed mardown as html
        """
        # Read morea about these features here:
        # https://pythonhosted.org/Markdown/extensions/index.html
        markdown_extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.headerid',
        ]
        markdown_extensions += list(extentions)
        return markdown.markdown(text, extensions=markdown_extensions)

    def parse_jinja(self, input_file,
                    custom_template=None):
        # pylint: disable=E1101
        """Combines a string of html with the jinja2 templates.

        Parameters:
            input_file : (str)
                Path to the index markdownfile.

            custom_template : (array)
                Path to custom template directory

        Returns:
            str:
                The complete html document parsed by jinja as a string.
        """
        if custom_template is not None:
            theme = custom_template
        else:
            theme = path.join(list(laminate_default.__path__)[0], 'templates')

        # Initialize the Jinja environment
        input_directory = path.dirname(path.abspath(input_file))
        loaders = FileSystemLoader([theme, input_directory])
        env = Environment(loader=loaders)

        # Add custom markdown filter
        env.filters['markdown'] = self.parse_markdown

        # Get the index markdown file
        input_filename = input_file.split('/')[-1]
        template = env.get_template(input_filename)

        return template.render(**self._config)
