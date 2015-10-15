# DjangoCon Europe 2016

This is the project for the http://2016.djangocon.eu/ website.

## Run locally

1) Create a virtualenv and activate it
2) `pip install -r requirements/base.txt`
3) `python manage.py migrate`
4) `python manage.py runserver`

## Compile less files

We use less to compile our CSS files. If you've made edits to `style.less`, run
`lessc static/css/style.less > static/css/style.css` to compile the changes (
this assumes that you've already installed a less compiler on your computer).
