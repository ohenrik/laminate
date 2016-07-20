"""Laminate is a simple python package that uses Jinja2 and markdown processors
to create beautiful documents for both screens and print.


Usage:
    report.py <input_directory> <input_file> [--output_dir]

"""
from os import path
from docopt import docopt
import laminate

if __name__ == '__main__':
    # pylint: disable=C0103
    arguments = docopt(__doc__)
    print(arguments)

    laminator = laminate.Laminate()

    directory = path.join(path.dirname(__file__),
                          arguments['<input_directory>'])

    laminator.create_html(directory, arguments['<input_file>'],
                          arguments['--output_dir'])
