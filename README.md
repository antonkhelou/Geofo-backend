Geofo-backend
================
[![Build Status](https://travis-ci.com/antonkhelou/Geofo-backend.svg?token=dJ7Uk3fcs3ZRM6R6XdYv&branch=master)](https://travis-ci.com/antonkhelou/Geofo-backend)

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

* Install RabbitMQ:

    `brew install rabbitmq`

If you need to add a dependency, install it with pip and then run: `pip freeze > requirements.txt`

Make sure you commit the requirements file afterwards!

Instructions
------------

* Check out the source with `git clone git@github.com:antonkhelou/comp-599-project.git comp-599-project`
* `cd` into the comp-599-project directory
* `source proj599_env/bin/activate` to setup the virtualenv
* `python manage.py syncdb`. This will generate a db.sqlite file containing the database.
* `python manage.py runserver`. Access the site at http://localhost:8000
* `sudo rabbitmq-server`. Make sure you have `PATH=$PATH:/usr/local/sbin` added to your path. The broker responsible for holding and sending tasks.
* `python manage.py celery beat -S djcelery.schedulers.DatabaseScheduler`. This is to launch the beat process which will look for changes inside the database and run tasks periodically
* `python manage.py celery worker --loglevel=info`. This is the worker which will receive the tasks from the RabbitMQ broker.
* An additional changes need to be made to proj_599/lib/site-packages/djcelery/schedulers.py at line 54. Replace `self.args = loads(model.args or '[]')` with `self.args = ast.literal_eval(model.args or '[]')`. Make sure to `import ast`
* Adjust period task rate of execution inside proj599/settings.py for local development

Project layout
--------------

* `manage.py` - comes with Django. Not modified.
* `readme.md`
* `proj599/`
    * `settings.py` - the project-wide settings. should not need to be changed.
    * `templates/` - all the template files will go under here.
    * `views.py` - includes all views which are mapped with the urls patterns specifies in `urls.py`.
    * `tasks.py` -  holds the tasks that can be used to run as messages inside the AMQP pipeline.
    * `models.py` - includes all models that we will work with in this project.
    * `permissions.py` - contains custom permissions used for our RESTful API.
    * `serializers.py` - specifies the way the model data should be handled through the RESTful interface.
    * `urls.py` - includes all the urls.py files for each app.


REST API
-------------
Once the database is created and the server is running (the other components AMQP components are not required for this)

* `localhost:8000/threads/`
* `localhost:8000/threads/<pk>/`
* `localhost:8000/threads/<pk>/comments/`
* `localhost:8000/threadupvote/`
* `localhost:8000/comments/`
* `localhost:8000/comments/<pk>/`
* `localhost:8000/commentupvote/`
* `localhost:8000/users/`
* `localhost:8000/users/<pk>/`

The above are all the standard API hooks for the models. Full HTTP methods support. If you want raw JSON data, add `?format=json` to the end of the url.

* `localhost:8000/api-token-auth/`

The above supports POST only and requires, `username` and `password` attributes and returns the API authentication token.

* `localhost:8000/admin/`

To view the admin page and the PeriodicTasks.
