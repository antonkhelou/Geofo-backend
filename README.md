comp-599-project
================
[![Build Status](https://magnum.travis-ci.com/antonkhelou/comp-599-project.svg?token=dJ7Uk3fcs3ZRM6R6XdYv&branch=master)](https://magnum.travis-ci.com/antonkhelou/comp-599-project)

Development
-----------

`virtualenv` should be used to manage dependencies.

To install it: `sudo pip install virtualenv`

Then, to setup a virtual environment:

* In your checked out directory, run

    `virtualenv --no-site-packages proj599_env`

* Enter your virtual environment:

    `source proj599_env/bin/activate`

* Install all the dependencies:
    
    `pip install -r requirements.txt`

If you need to add a dependency, install it with pip and then run: `pip freeze > requirements.txt`

Make sure you commit the requirements file afterwards!

Instructions
------------

* Check out the source with `git clone git@github.com:antonkhelou/comp-599-project.git comp-599-project`
* `cd` into the comp-599-project directory
* `source proj599_env/bin/activate` to setup the virtualenv
* `python manage.py runserver`. Access the site at http://localhost:8000

Project layout
-------------

* `manage.py` - comes with Django. Not modified.
* `readme.md`
* `proj599/`
    * `settings.py` - the project-wide settings. should not need to be changed.
    * `templates/` - all the template files will go under here.
    * `views/` - includes all views which are mapped with the urls patterns specifies in `urls.py`.
    * `urls.py` - includes all the urls.py files for each app