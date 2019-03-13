events app
=================

Events is a simple app web application where users can log in, create events and RSVP on events.


* Django 1.10
* Python 2.7



Directory layout
================

Events's directory structure looks as follows::

    django-sample-app/
    ├── events
    ├── templates
    ├── README.md
    ├── requirements.txt
    └── tests

Setup
=================

Install ``requirements.txt`` using pip.
To run the app simply hit ``python manage runserver`` in your virtualenv


Templates
---------

The ``templates/`` directory holds all the app templates.
This is set in the ``settings`` module in the `TEMPLATES` conf


App settings
------------

Define you local or custom settings inside the events's directory , just declare them in the ``local_settings.py`` module.

The initial setting to add is the 'SECRET_KEY' , everything else is customizable


Tests
-----

Tests are in the ``tests/`` directory
The ``tests/`` directory structure::

    tests/
    ├── __init__.py
    ├── homepage_tests.py
    ├── login_tests.py