Cookiecutter Geopaparazzi Reference Server
==========================================

Based on Cookiecutter-Django_, Cookiecutter Geopaparazzi Reference Server is a framework for quickly jumpstarting
production-ready web servers to manage Geopaparazzi data.

.. _issues: https://github.com/geoanalytic/cookiecutter-geopaparazzi-server/issues/new


Features
---------

* For Django 2.0
* Works with Python 3.6
* Twitter Bootstrap_ v4.0.0 (`maintained Foundation fork`_ also available)
* 12-Factor_ based settings via django-environ_
* Secure by default. We believe in SSL.
* Optimized development and production settings
* User registration via django-allauth_
* Comes with custom user model ready to go
* Grunt build for compass and LiveReload
* Send emails via Anymail_ (using Mailgun_ by default, but switchable)
* Media storage using Amazon S3 or DigitalOcean Spaces
* Docker support using docker-compose_ for development and production (using Caddy_ with LetsEncrypt_ support)
* Procfile_ for deploying to Heroku
* Instructions for deploying to PythonAnywhere_
* Run tests with unittest or py.test
* Uses PostGIS/PostgreSQL for spatial database functionality

.. _`maintained Foundation fork`: https://github.com/Parbhat/cookiecutter-django-foundation


Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Serve static files from Amazon S3 or Whitenoise_
* Configuration for Celery_
* Integration with MailHog_ for local email testing
* Integration with Sentry_ for error logging

.. _Bootstrap: https://github.com/twbs/bootstrap
.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-avatar: https://github.com/grantmcconnaughey/django-avatar
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Mailgun: http://www.mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.io/
.. _Celery: http://www.celeryproject.org/
.. _Anymail: https://github.com/anymail/django-anymail
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://sentry.io/welcome/
.. _docker-compose: https://github.com/docker/compose
.. _PythonAnywhere: https://www.pythonanywhere.com/
.. _Caddy: https://caddyserver.com/
.. _LetsEncrypt: https://letsencrypt.org/


Prerequisites
-------------

* Docker-compose_
* Python_ (including Pip_, note that if you are using Windows its easiest to just install Anaconda_)
* Git_

.. _Docker-compose: https://github.com/docker/compose
.. _Python: https://www.python.org/
.. _Pip: https://pip.pypa.io/en/stable/installing/
.. _Anaconda: https://www.anaconda.com/
.. _Git: https://git-scm.com/

Usage
------

Here are the basic instructions for setting up a local development system, discussed in more detail in this `blog
post <https://geoanalytic.github.io/a-reference-server-for-geopaparazzi-cloud-profiles/>`__.
Before you begin, open a console window and create a directory to hold
the project source code and demo data you will download (we use "grs" as an example below, but you can use choose your own directory name)

::

    $ mkdir /grs
    $ cd /grs

1. Install cookiecutter

::

    $ pip install "cookiecutter>=1.4.0"

2. Use cookiecutter to get the latest source code from the geopaparazzi reference server repository

::

    $ cookiecutter https://github.com/geoanalytic/cookiecutter-geopaparazzi-server

You will be asked a number of questions, some of which are only
applicable to production systems. For development purposes, you should
enter ‘y’ to the following choices (these should be the defaults):

-  docker
-  celery
-  whitenoise

3) Change directory into the directory created by the cookiecutter process and then
   build and run the containers:

::

    $ cd geopaparazzi_reference_server
    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up -d
    $ docker-compose -f local.yml ps

If everything is working, the last command should result in a report
like this:

::

                        Name                                  Command               State           Ports
    --------------------------------------------------------------------------------------------------------------
    geopaparazzi_reference_server_celerybeat_1     /entrypoint /start-celerybeat    Up
    geopaparazzi_reference_server_celeryworker_1   /entrypoint /start-celeryw ...   Up
    geopaparazzi_reference_server_django_1         /entrypoint /start               Up      0.0.0.0:8000->8000/tcp
    geopaparazzi_reference_server_flower_1         /entrypoint /start-flower        Up      0.0.0.0:5555->5555/tcp
    geopaparazzi_reference_server_postgres_1       /bin/sh -c /docker-entrypo ...   Up      5432/tcp
    geopaparazzi_reference_server_redis_1          docker-entrypoint.sh redis ...   Up      6379/tcp

What you see is six containers running within an isolated network that
allows the containers to communicate among themselves. Only the django
and flower containers are open to outside connections. Each container
does one thing:

-  django … provides the python based web framework
-  postgres … provides a PostgreSQL/PostGIS database
-  redis … provides a message broker and in memory cache for performance
   and to support celery tasks
-  celeryworker … provides an on demand asysnchronous processing
   capability
-  celerybeat … provides scheduled background processing capability
-  flower … provides a real-time monitoring tool for the celery tasks

4) Setup the database and static assets, create a superuser

::

    $ docker-compose -f local.yml run --rm django python manage.py collectstatic
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

The second command will prompt you to enter a username, email and
password for the superuser. You will need those credentials to access
the system so write them down!

5)  Run the tests

::

    $ docker-compose -f local.yml run --rm django py.test

    Starting geotabloid_postgres_1 ... done
    PostgreSQL is available
    Test session starts (platform: linux, Python 3.6.5, pytest 3.8.0, pytest-sugar 0.9.1)
    Django settings: config.settings.test (from ini file)
    rootdir: /app, inifile: pytest.ini
    plugins: sugar-0.9.1, django-3.4.3, celery-4.2.1

        geotabloid/users/tests/test_forms.py ✓                  2% ▎
        geotabloid/users/tests/test_models.py ✓                 4% ▍
        geotabloid/users/tests/test_urls.py ✓✓✓✓               11% █▏
        geotabloid/users/tests/test_views.py ✓✓✓               16% █▋
        gp_projects/tests/test_models.py ✓✓✓                   21% ██▏
        profiles/tests/test_api.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓     61% ██████▎
        profiles/tests/test_models.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓  100% ██████████

    Results (6.31s):
          57 passed


6) Now load the demo data

Download the demo data from
`here <https://drive.google.com/open?id=12HwGhqdFNvZwS5Y6iO1dC81HWZQbsPnu>`__.
Note that you need to install `Httpie <https://httpie.org/>`__ and edit
the load_local.sh file, replacing ``user:password`` with the values you
provided for the superuser and your server IP address for the
``uploadurl`` entries.  No other values (e.g. path=. etc) need to be changed.

::

    $ pip install httpie
    $ cd location/of/demo/data
    $ ./load_local.sh

Next, point your browser at http://localhost:8000/admin, login with your
superuser credentials and edit the Profiles and create Profilesets for
your superuser as described in the `original
post <https://geoanalytic.github.io/a-reference-server-for-geopaparazzi-cloud-profiles/>`__.

6) Connect Geopaparazzi to your server

You will need to figure out the IP address of the computer the server is
running on. On Linux, use the command ``hostname -I``. On Windows, the
command ``ipconfig`` should work. On your mobile, start the app and
select the settings (gear) icon, then select Cloud Server Settings and
fill in the user, password and Cloud Profiles URL as shown:

7) Download the cloud profiles, collect some tracks and notes, then upload your user project data.


Cookiecutter-Django Stuff
-------------------------

As noted, this project is derived from the Cookiecutter-Django_
You can find lots of helpful documentation there, here are some of the essential links:

* `Developing locally`_
* `Developing locally using docker`_


.. _options: http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html
.. _`Developing locally`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html
.. _`Developing locally using docker`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html


* Documentation: https://cookiecutter-django.readthedocs.io/en/latest/
* See Troubleshooting_ for common errors and obstacles
* If you have problems with Cookiecutter Geopaparazzi Server, please open issues_ don't send
  emails to the maintainers.

.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django

.. _Troubleshooting: https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html


"Your Stuff"
-------------

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

