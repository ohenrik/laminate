# -*- coding: utf-8 -*-
"""Laminate - Create beatifull yet simple html and pdf documents
from markdown"""
from os import path, makedirs
from jinja2 import Environment, PackageLoader, ChoiceLoader, FileSystemLoader
import markdown
from markdown.extensions.toc import TocExtension
from markdown_include.include import MarkdownInclude

class Laminate():
    """This class parses markdown and combines the result with
    jinja templates and config variables provided by the user."""

    def __init__(self, **config):
        self._config = config

    def create_html(self, input_directory, input_file='index.md',
                    output_dir=None):
        """Create the complete report as an html document

        Parameters:
            input_directory : (str)
                Path to directory containing the mardownfiles

            input_file : (str)
                Name of the index markdownfile. **Default:** index.md

            output_dir : (str)
                Path to output directory

        Returns:
            None:
                Creates a new html document in the directory
                spesified by output_dir
        """
        parsed_md = self.parse_markdown(input_directory, input_file)
        full_html = self.parse_jinja(parsed_md)

        # if output_dir is False or None:
        #     output_dir = path.join(path.dirname(__file__), 'build')

        destination_file = path.join(output_dir, 'index.html')

        makedirs(path.dirname(destination_file), exist_ok=True)
        with open(destination_file, 'wt') as f:
            f.write(full_html)

    def parse_markdown(self, input_directory, input_file='index.md'):
        # pylint: disable=R0201
        """Parse markdown to html

        Parameters:
            input_directory : (str)
                Path to directory containing the mardownfiles for the report

            input_file : (str)
                Name of the index markdownfile. Default: index.md

        Returns:
            str:
                String containing the parsed mardown as html
        """
        mrkd = path.join(input_directory, input_file)
        md_text = open(mrkd, 'rt').read()

        # Markdown include extension
        markdown_include = MarkdownInclude(
            configs={'base_path': input_directory, 'encoding': 'iso-8859-1'}
        )

        # Read morea about these features here:
        # https://pythonhosted.org/Markdown/extensions/index.html
        markdown_extensions = [
            markdown_include,
            TocExtension(baselevel=1),
            'markdown.extensions.extra',
            'markdown.extensions.headerid',
        ]

        return markdown.markdown(md_text, extensions=markdown_extensions)

    def parse_jinja(self, html, template_path=None):
        # pylint: disable=E1101
        """Combines a string of html with the jinja2 templates.

        Parameters:
            doc_html : (str)
                HTML as a string

        Returns:
            str:
                The complete html document parsed by jinja as a string.
        """
        loaded_templates = FileSystemLoader(template_path, followlinks=True)
        loaders = [loaded_templates, PackageLoader('laminate', 'templates'),]
        env = Environment(loader=ChoiceLoader(loaders))

        template = env.get_template('default/index.html')

        return template.render(content=html, **self._config)
