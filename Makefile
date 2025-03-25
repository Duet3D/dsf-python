SHELL := /bin/bash
verbosity=1

#########################################
# bumpversion Usage
#########################################
# `bumpversion [major|minor|patch|build|post]`
# `bumpversion --tag release

update_dist:
	python -m pytest
	rm dist/* -f
	python setup.py sdist bdist_wheel

check_dist: update_dist
	python -m twine check dist/*

build_deb:
	rm -rf deb_dist/
	sed -i -E '/forced-upstream-version/ s/([0-9]+)\.([0-9]+)\.([0-9]+)-([a-z]+)([0-9]+)/\1.\2.\3~\4\5/' setup.cfg
	python3 setup.py --command-packages=stdeb.command bdist_deb
	sed -i -E '/forced-upstream-version/ s/([0-9]+)\.([0-9]+)\.([0-9]+)~([a-z]+)([0-9]+)/\1.\2.\3-\4\5/' setup.cfg
	dpkg-deb -I deb_dist/*.deb