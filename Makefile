SOURCES=$(wildcard clustice/*.py)
PKGNAME=clustice

all: README.md
	echo Hello.


test-deploy:
	poetry publish --build -r testpypi
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)
uninstall:
	-pip uninstall -y $(PKGNAME)
build: README.md $(wildcard cycles/*.py)
	poetry build
deploy:
	poetry publish --build
check:
	poetry check


doc: README.md # CITATION.cff 
	pdoc -o docs ./clustice --docformat google

%: %.j2 replacer.py pyproject.toml
	python replacer.py < $< > $@


clean:
	-rm -rf build dist
distclean:
	-rm *.scad *.yap @*
	-rm -rf build dist
	-rm -rf *.egg-info
	-rm .DS_Store
	find . -name __pycache__ | xargs rm -rf
	find . -name \*.pyc      | xargs rm -rf
	find . -name \*~         | xargs rm -rf
