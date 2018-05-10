Cookiecutter Geopaparazzi Reference Server
==========================================

Powered by Cookiecutter_, Cookiecutter Geopaparazzi Reference Server is a framework for jumpstarting a
production-ready Django based Geopaparazzi server quickly.  This implementation is based on the excellent Cookiecutter-Django_ release.   The main differences from the original are the use of a PostGIS database and the Profiles app which provides restful services for Geopaparazzi.

* Documentation: https://cookiecutter-django.readthedocs.io/en/latest/
* See Troubleshooting_ for common errors and obstacles
* If you have problems with Cookiecutter Geopaparazzi Server, please open issues_ don't send
  emails to the maintainers.
* Need quick professional paid support? Contact `support@cookiecutter.io`_.
  This includes configuring your servers, fixing bugs, reviewing your code and
  everything in between.

.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django
.. _Troubleshooting: https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html

.. _issues: https://github.com/geoanalytic/cookiecutter-geopaparazzi-server/issues/new
.. _support@cookiecutter.io: support@cookiecutter.io

Features
---------

* For Django 2.0
* Works with Python 3.6
* Renders Django projects with 100% starting test coverage
* Twitter Bootstrap_ v4.0.0 (`maintained Foundation fork`_ also available)
* 12-Factor_ based settings via django-environ_
* Secure by default. We believe in SSL.
* Optimized development and production settings
* Registration via django-allauth_
* Comes with custom user model ready to go
* Grunt build for compass and livereload
* Send emails via Anymail_ (using Mailgun_ by default, but switchable)
* Media storage using Amazon S3
* Docker support using docker-compose_ for development and production (using Caddy_ with LetsEncrypt_ support)
* Procfile_ for deploying to Heroku
* Instructions for deploying to PythonAnywhere_
* Run tests with unittest or py.test

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

Constraints
-----------

* Only maintained 3rd party libraries are used.
* Uses PostGIS/PostgreSQL everywhere
* Environment variables for configuration (This won't work with Apache/mod_wsgi except on AWS ELB).

Usage
------

Let's pretend you want to create a Django project called "geopap-testserver". Rather than using ``startproject``
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter>=1.4.0"

Now run it against this repo::

    $ cookiecutter https://github.com/geoanalytic/cookiecutter-geopaparazzi-server

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'David Currie', 'dave', etc to your own information.

Answer the prompts with your own desired options_. For example::

    Cloning into 'cookiecutter-geopaparazzi-server'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [My Awesome Project]: geopap_testserver
    project_slug [geopap_testserver]: 
    description [Behold My Awesome Project!]: 
    author_name [Daniel Roy Greenfeld]: David Currie
    email [david-currie@example.com]: dave@trailstewards.com
    domain_name [example.com]: trailstewards.com
    version [0.1.0]: 
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 
    timezone [UTC]: 
    windows [n]: 
    use_pycharm [n]: 
    use_docker [n]: y
    postgresql_version [10.3]: 
    Select js_task_runner:
    1 - None
    2 - Gulp
    3 - Grunt
    Choose from 1, 2, 3 [1]: 
    custom_bootstrap_compilation [n]: 
    use_compressor [n]: 
    use_celery [n]: 
    use_mailhog [n]: 
    use_sentry_for_error_reporting [y]: n
    use_whitenoise [y]: 
    use_heroku [n]: 
    use_travisci [n]: 
    keep_local_envs_in_vcs [y]: 
    [SUCCESS]: Project initialized, keep up the good work!

Enter the project and take a look around::

    $ cd geopap_testserver/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:geoanalytic/geopap-testserver.git
    $ git push -u origin mastergeopap_testserver/geopap_testserver/templates/pages

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?

Build and start the local server::

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up -d
    
Create a superuser::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser
    
Connect to the local server at http://127.0.0.1:8000 and you should a default webpage.  You can modify this to your needs by editting the template at geopap_testserver/geopap_testserver/templates/pages/home.html

You can use the admin interface at http://127.0.0.1:8000/admin to view/edit the various database tables.

Alternatively, you can access the RESTful endpoints at these urls (the last two require username/password):

* http://127.0.0.1:8000/projects
* http://127.0.0.1:8000/tags
* http://127.0.0.1:8000/otherfiles
* http://127.0.0.1:8000/spatialitedbs
* http://127.0.0.1:8000/profiles
* http://127.0.0.1:8000/myprofiles
* http://127.0.0.1:8000/userprojects

For local development, see the following:

* `Developing locally`_
* `Developing locally using docker`_

.. _options: http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html
.. _`Developing locally`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html
.. _`Developing locally using docker`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html


