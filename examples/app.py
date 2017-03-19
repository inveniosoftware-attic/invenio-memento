# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Minimal Flask application example for development.

Initialize database

.. code-block:: console

   $ cd examples
   $ flask -a app.py db init
   $ flask -a app.py db create

Create a user (for accessing admin):

   $ flask -a app.py users create info@inveniosoftware.org -a

Load some test data:

   $ flask -a app.py fixtures files

Run example development server:

.. code-block:: console

   $ flask -a app.py --debug run

Run example worker:

.. code-block:: console

   $ celery worker -A app.celery -l info --purge

Administration interface is available on::

   http://localhost:5000/admin/

REST API is available on::

   http://localhost:5000/files/
"""

from __future__ import absolute_import, print_function

import shutil
from os import environ, makedirs
from os.path import dirname, exists, join

from flask import Flask, current_app
from flask_babelex import Babel
from flask_menu import Menu
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as accounts_bp
from invenio_admin import InvenioAdmin
from invenio_celery import InvenioCelery
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, FileInstance, Location, \
    ObjectVersion
from invenio_rest import InvenioREST

from invenio_memento import InvenioMemento
from invenio_memento.converters import ArchivedConverter
from invenio_memento.views import blueprint as memento_bp

# Create Flask application
app = Flask(__name__)
app.config.update(dict(
    CELERY_ALWAYS_EAGER=False,
    CELERY_CACHE_BACKEND='memory',
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND='cache',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI=environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    REST_ENABLE_CORS=True,
    SECRET_KEY='CHANGEME',
    DATADIR=join(dirname(__file__), 'data')
))

Babel(app)
Menu(app)
InvenioDB(app)
InvenioREST(app)
InvenioAdmin(app)
InvenioAccounts(app)
InvenioAccess(app)
InvenioFilesREST(app)
InvenioMemento(app)

app.url_map.converters['archived'] = ArchivedConverter
app.register_blueprint(accounts_bp)
app.register_blueprint(memento_bp)


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def files():
    """Load files."""
    srcroot = dirname(dirname(__file__))
    d = current_app.config['DATADIR']
    if exists(d):
        shutil.rmtree(d)
    makedirs(d)

    # Clear data
    ObjectVersion.query.delete()
    Bucket.query.delete()
    FileInstance.query.delete()
    Location.query.delete()
    db.session.commit()

    # Create location
    loc = Location(name='local', uri=d, default=True)
    db.session.commit()
