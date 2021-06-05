# make and instalg
set -e
echo "Building...."
./scripts/build_pip.sh
echo "(Done)"

echo "Installing..."
python -m  pip install ./dist/music-tag-*.whl
echo "(Done)"

# test
sh ./test/run_tests.sh

# cleaning
echo "Cleaning..."
rm -rf ./dist
echo "(Done)"

# uninstall
echo "Uninstalling..."
python -m pip uninstall -y music-tag
echo "(Done)"
