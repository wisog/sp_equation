#!/usr/bin/env python

"""This file sets up a command line manager.

Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for a list of runserver options.
"""

from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import create_app
from app import db

cli = FlaskGroup(create_app)

migrate = Migrate(create_app, db)
migrate.init_app(create_app, db)

