# Spark Equation trial task

This code base serves as the trial task for Python developers.

## Code characteristics

* Tested on Python py38

## Setting up a development environment

We assume that you have `Pipenv` installed.

    pipenv sync --dev


# Adding settings

Copy the `local_settings_example.py` file to `local_settings.py`.

    cp app/local_settings_example.py app/local_settings.py

Edit the `local_settings.py` file.

## Preparing application to run

Set flask app to current application
On Linux run
    
    export FLASK_APP=app

On Windows run

    set FLASK_APP=app


## Initializing the Database

    # Create DB tables and populate the tables
    pipenv python -m flask db upgrade


## Running the app

    # Start the Flask development web server
    pipenv python -m flask run

Point your web browser to http://localhost:5000/products


## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.
