## Update PyPI package
Here is a reminder for the steps to follow to update the dsf-python package on PyPI (https://pypi.org/project/dsf-python/)

#### Prerequisite :
`setuptools`, `wheel` and `twine` must be installed on the system
```
pip3 install setuptools wheel twine
```

#### Clone current version from Github
```
git clone https://github.com/Duet3D/dsf-python.git
cd dsf-python
```

#### Test in development
```
pip install -e .
```

#### Create distribution packages on your local machine
```
python3 setup.py sdist bdist_wheel
```

#### Upload the distribution files to pypi
```
twine upload dist/*
```

#### Reference
* [Uploading your Project to PyPI](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi)
* [Updating a package on pypi](https://widdowquinn.github.io/coding/update-pypi-package/)
* [Update existing Python package in Pypi](https://gist.github.com/arsho/fc651bfadd8a0f42be72156fd21bd8a9)