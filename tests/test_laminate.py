# pylint: disable=C0111
import pytest
from laminate import laminate

@pytest.fixture()
def create_file(tmpdir):
    def file_creator(content='**test**', add_filter=False):
        if add_filter:
            content = ("{{% filter markdown %}}{content}{{% endfilter %}}"
                            .format(content=content))
        md_file = tmpdir.mkdir("laminate").join("markdown.txt")
        md_file.write(content, 'w')
        return str(md_file)
    return file_creator


def test_parse_markdown(create_file):
    input_file = create_file()
    lm = laminate.Laminate(input_file)
    result = lm.parse_markdown()
    assert result == '<p><strong>test</strong></p>'

def test_parse_jinja(create_file):
    input_file = create_file(content="**Something else**", add_filter=True)
    lm = laminate.Laminate(input_file)
    result = lm.parse_jinja()
    assert result == '<p><strong>Something else</strong></p>'
