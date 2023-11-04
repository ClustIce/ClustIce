SOURCES=$(wildcard clustice/*.py)

all: README.md
	echo Hello.


# pep8:
# 	autopep8 -r -a -a -i clustice/
test-deploy: build
	-pip install twine
	twine upload -r pypitest dist/*
test-install: requirements.txt
	pip install -r $<
	pip install --index-url https://test.pypi.org/simple/ clustice


install:
	./setup.py install
uninstall:
	-pip uninstall -y clustice
build: $(SOURCES) README.md doc
	python3 -m build


deploy: build
	twine upload dist/*
check:
	./setup.py check


doc: README.md CITATION.cff 
	pdoc3 --html -o docs-tmp --force genice_core
	-rm -rf docs
	mv docs-tmp/genice_core docs

%: temp_% replacer.py pyproject.toml
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
