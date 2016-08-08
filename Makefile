watch-tests:
	py.test -f -v --color=yes --cov=laminate --cov-report=html

show-cov:
	open htmlcov/index.html
