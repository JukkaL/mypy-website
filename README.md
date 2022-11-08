# mypy-website

Dependencies:

* Python 3
* `pyyaml` (`pip install pyyaml`)
* `libsass-python` (`pip install libsass`)

To build locally:
```
python build.py
```
Output is in `out`.

To build and update the website:
```
scripts/copy-to-server.sh
```
This runs build.py and then copies everything from `out` to `mypy-lang.org`.
