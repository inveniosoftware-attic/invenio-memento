# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module makes your site Memento compliant."""

from __future__ import absolute_import, print_function

from . import config
from .cli import memento as memento_cmd
from .views import blueprint


class InvenioMemento(object):
    """Invenio-Memento extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        if hasattr(app, 'cli'):
            app.cli.add_command(memento_cmd)
        app.extensions['invenio-memento'] = self

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            'MEMENTO_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_memento/base.html'))
        # Set default configuration
        for k in dir(config):
            if k.startswith('MEMENTO_'):
                app.config.setdefault(k, getattr(config, k))
