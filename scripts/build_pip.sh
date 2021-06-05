# install needed pip packages
python3 -m pip install --user --upgrade setuptools wheel twine

# build
python3 setup.py sdist bdist_wheel

# clean build files
rm -rf build fmdpy.egg-info
