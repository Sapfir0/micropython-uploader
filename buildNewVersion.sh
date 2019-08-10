rm -r dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
pip3 install --upgrade micropython_uploader
pip3 install --no-cache-dir micropython_uploader
pip3 install --no-cache-dir micropython_uploader
