# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Werkzeug URL converters."""

from __future__ import absolute_import, print_function

from datetime import datetime

from werkzeug.routing import BaseConverter, Map, Rule, ValidationError


class ArchivedConverter(BaseConverter):
    """Parse archivation datetime."""

    def __init__(self, url_map, format=None, regex=None):
        """Default constructor for 'YYYYmmddHHMMSS' datetime format."""
        super(ArchivedConverter, self).__init__(url_map)
        self.format = format or '%Y%m%d%H%M%S'
        self.regex = regex or '([^/]*)'

    def to_python(self, value):
        """Convert URL value to Python object."""
        return datetime.strptime(value, self.format).replace(microsecond=0)

    def to_url(self, value):
        """Format datetime with ``self.format``."""
        return value.strftime(self.format)
