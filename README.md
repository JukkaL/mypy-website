# mypy-website

Dependencies:

* Python 2
* `pyyaml` (`pip install pyyaml`)
* `sass` (`sudo gem install sass`)

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
