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
