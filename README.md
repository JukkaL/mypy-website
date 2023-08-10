# mypy-website

## Dependencies:

```
python3 -m pip install -r requirements.txt
```

## To update news items

Edit `news.yaml` and add an entry to the new news item at the top.

## To build locally:
```
python3 build.py
```
Output is in `out`.

## To build and update the website:
```
scripts/copy-to-server.sh
```
This runs build.py and then copies everything from `out` to `mypy-lang.org`.
