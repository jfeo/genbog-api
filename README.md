# Backend for the GenBog project

A Flask REST API that is used to keep track of books by their ISBN numbers.

## Requirements & dependencies


The project is developed for python 3.7.

The only direct dependencies are `Flask`, and `pytest`

## Setup


To get started initialize a virtual environment in the project directory, and
activate it - substitute the `python3.7` command with the corresponding on your
system.

    $ python3.7 -m venv venv
    $ source venv/bin/activate

With the virtual environment active, install the required packages in the
environment

    (venv) $ pip install -r requirements.txt

## Running


To run a development version of the application, run the following `flask`
command in the virtual environment

    (venv) $ FLASK_APP=genbog/app.py flask run

## Tests


Run the tests simply by executing `pytest` in the virtual environment.

    (venv) $ pytest
