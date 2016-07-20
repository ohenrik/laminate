# -*- coding: utf-8 -*-
# pylint: disable=R0913, R0201
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

    def create_html(self, input_dir=None, input_file='index.md',
                    build_dir='build', templates_dir=None, template_name=None):
        """Create the complete report as an html document

        Parameters:
            input_dir : (str)
                Path to directory containing the mardownfiles

            input_file : (str)
                Name of the index markdownfile. **default:** index.md

            build_dir : (str)
                Path to output directory. **default: build**

            templates_dir : (array)
                Path to custom template directory

            template_name : (str)
                Name of template that should be used. Name
                must match template folder name. (e.g. my_template) inside a
                template directory.

        Returns:
            None:
                Creates a new html document in the directory
                spesified by build_dir
        """
        parsed_md = self.parse_markdown(input_dir, input_file)
        full_html = self.parse_jinja(parsed_md, templates_dir, template_name)

        filename = self._output_filename(input_dir, build_dir, 'index.html')

        self._write_result(full_html, filename)

    def _write_result(self, content, output_file):
        makedirs(path.dirname(output_file), exist_ok=True)
        with open(output_file, 'wt') as f:
            f.write(content)

    def _output_filename(self, input_dir, build_dir, filename):
        output_dir_name = input_dir.split('/')[-1]
        return path.join(build_dir, output_dir_name, filename)

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

    def parse_jinja(self, html, templates_dir=None, template_name=None):
        # pylint: disable=E1101
        """Combines a string of html with the jinja2 templates.

        Parameters:
            doc_html : (str)
                HTML as a string

            templates_dir : (array)
                Path to custom template directory

            template_name : (str)
                Name of template that should be used. Name
                must match template folder name. (e.g. my_template) inside a
                template directory.

        Returns:
            str:
                The complete html document parsed by jinja as a string.
        """
        if templates_dir is None:
            env = Environment(loader=PackageLoader('laminate', 'templates'))
        else:
            loaded_templates = FileSystemLoader(templates_dir, followlinks=True)
            loaders = [loaded_templates, PackageLoader('laminate', 'templates'),]
            env = Environment(loader=ChoiceLoader(loaders))


        if template_name is None:
            template = env.get_template('default/index.html')
        else:
            template = env.get_template('{}/index.html'.format(template_name))

        return template.render(content=html, **self._config)
