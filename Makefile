SOURCES=$(wildcard clustice/*.py)
PKGNAME=clustice

all: README.md $(patsubst %.scad, %.stl, $(wildcard *.scad))
	echo Hello.


test-deploy:
	poetry publish --build -r testpypi
test-install:
	pip install --index-url https://test.pypi.org/simple/ $(PKGNAME)
uninstall:
	-pip uninstall -y $(PKGNAME)
build: README.md
	poetry build
deploy:
	poetry publish --build
check:
	poetry check
# prepare-auto-versioning:
# 	poetry self add "poetry-dynamic-versioning[plugin]"

doc: README.md # CITATION.cff 
	pdoc -o docs ./clustice --docformat google

%: temp_% replacer.py pyproject.toml
	python replacer.py < $< > $@


%.stl: %.scad
	openscad $< -o $@

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
