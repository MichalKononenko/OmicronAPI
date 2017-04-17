.. image:: https://badge.waffle.io/MichalKononenko/OmicronServer.png?label=ready&title=Ready 
 :target: https://waffle.io/MichalKononenko/OmicronServer
 :alt: 'Stories in Ready'
Welcome to OmicronServer
========================

**OmicronServer** is the back end for Omicron Web Services, a project that aims
 to automate much of the process engineering and experimentation

Badges
------

.. image:: https://travis-ci.org/OmicronProject/OmicronServer.svg?branch=master
  :target: https://travis-ci.org/OmicronProject/OmicronServer
  :alt: Build Status

.. image:: https://coveralls.io/repos/MichalKononenko/OmicronServer/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/MichalKononenko/OmicronServer?branch=master

.. image:: https://img.shields.io/badge/License-GNU%20GPL%20v3-blue.svg

.. image:: https://readthedocs.org/projects/omicron-server/badge/?version=latest
    :target: http://omicron-server.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://requires.io/github/MichalKononenko/OmicronServer/requirements.svg?branch=master
     :target: https://requires.io/github/MichalKononenko/OmicronServer/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codeclimate.com/github/MichalKononenko/OmicronServer/badges/gpa.svg
   :target: https://codeclimate.com/github/MichalKononenko/OmicronServer
   :alt: Code Climate

.. image:: https://badge.waffle.io/MichalKononenko/OmicronServer.png?label=ready&title=Ready
   :target: https://waffle.io/MichalKononenko/OmicronServer
   :alt: 'Stories in Ready'


Installation
------------

A stable version of **OmicronServer** has not yet been released. TravisCI builds
are run on all branches and pull requests with every commit, but features may be
lacking in these builds. See the issues and project milestones for a timeline
of future releases.

``$ git clone https://github.com/MichalKononenko/OmicronServer.git``
 

Packages and Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~

Dependencies are outlined in ``requirements.txt``. In order to install dependencies, run 

``pip install -r requirements.txt``

TravisCI uses this file to install all its dependencies, and Heroku uses this
to identify **OmicronServer** as a `Python <https://docs.python.org/3.5/>`_ project.

Since Travis runs on Linux, it has the advantage of using ``gcc`` to compile
some of the packages listed here. your machine may not have this luxury, and so
you may have to find binaries for the `psycopg2 <http://initd.org/psycopg/>`_
package, in order to connect to PostgreSQL

Supported Versions
~~~~~~~~~~~~~~~~~~

This project is currently supported for Python versions
    - 2.7
    - 3.4
    - 3.5


Supported Databases
~~~~~~~~~~~~~~~~~~~
OmicronServer currently supports PostgreSQL and SQLite.

Running the Program
-------------------

To run the server, run

    .. code-block:: bash
        
        $ python run_server.py

from the command line. 
By default, the server will run on ``localhost:5000``. The address can be specified by
setting the ``IP_ADDRESS`` and ``PORT`` environment variables in your command line.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The file ``config.py`` will adjust its settings depending on the value of several
environment variables. These are

- ``IP_ADDRESS``: The IP address at which the server is to be hosted
- ``PORT``: The port number at which the server is to be hosted
- ``BASE_DIRECTORY``: The base directory where ``run_server.py`` is kept. By default, this is the current directory of the ``config.py`` file
- ``TOKEN_SECRET_KEY``: The secret key used as a salt to generate authentication tokens for the user. Tokens are not stored on
    the back end, but are generated from user data, and the value of ``TOKEN_SECRET_KEY``. If this value is changed, the user's
    token will no longer work.
- ``DATABASE_URL``: The URL at which the database sits. This is the database to be used by the server
- ``DEBUG``: If ``TRUE``, then stack traces will be displayed when **in the browser** if the server throws a 500 error
- ``STATE``: A generic flag for specifying between ``DEV``, ``CI``, and ``PROD`` machines. Currently not wired to anything
- ``LOGFILE``: The file to which the log should be written. If this is not
    defined, the application log will be written to ```sys.stdout```.

Command Line Parsing
~~~~~~~~~~~~~~~~~~~~

Unfortunately, the values above must be set as environment variables as OmicronServer does not currently support parsing
these arguments in the command line

License
-------


This project and all files in this repository are licensed under the GNU General Public License (GPL) version 3.
A copy of this license can be found in the ``LICENSE`` file
