# pylint: disable=C0111,W0621,C0103
import os
import re
import pytest
from laminate.laminate import Laminate

@pytest.fixture()
def create_file(tmpdir):
    def file_creator(content='**test**'):
        md_file = tmpdir.mkdir("laminate").join("markdown.md")
        md_file.write(content, 'w')
        return str(md_file)
    return file_creator

@pytest.fixture()
def build_dir(tmpdir):
    return str(tmpdir.mkdir("build"))

def test_parse_markdown(create_file, build_dir):
    input_file = create_file("**test**")
    laminator = Laminate(input_file, build_dir)
    result = laminator.parse_markdown()
    assert result == '<p><strong>test</strong></p>'

def test_parse_jinja(create_file, build_dir):
    content = "{{% filter markdown %}}**Something else**{{% endfilter %}}".format()
    input_file = create_file(content=content)
    laminator = Laminate(input_file, build_dir)
    result = laminator.parse_jinja()
    assert result == '<p><strong>Something else</strong></p>'

def test_parse_jinja_uses_default_template(create_file, build_dir):
    content = """
    {{% extends 'index.html' %}}
    {{% block content %}}
        Uses template
    {{% endblock %}}
    """.format()
    input_file = create_file(content=content)
    laminator = Laminate(input_file, build_dir)
    result = laminator.parse_jinja()
    assert re.search('<meta template-name="laminate_default">', result) is not None
    assert re.search(r'Uses template\n', result) is not None

def test_create_html_does_creates_a_html_file(create_file, build_dir):
    content = """
    {{% extends 'index.html' %}}
    {{% block content %}}
        Uses template
    {{% endblock %}}
    """.format()
    input_file = create_file(content=content)
    laminator = Laminate(input_file, build_dir)
    file_path = laminator.create_html()
    assert os.access(file_path['html'], os.F_OK) is True,\
            "Could not find html output file"

def test_create_html_copies_resources(create_file, build_dir):
    input_file = create_file()
    laminator = Laminate(input_file, build_dir)
    file_path = laminator.create_html()
    assert os.access(file_path['assets'], os.F_OK) is True,\
            "Could not find assets directory"
