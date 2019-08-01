# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module makes your site Memento compliant."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template

blueprint = Blueprint(
    'invenio_memento',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/archive',
)


@blueprint.route('/<archived:archived>/<path:key>')
def archive(archived, key):
    """Retrun basic view."""
    from .models import MementoArchives

    memento = MementoArchives.query.filter_by(
        archived=archived, key=key
    ).first_or_404()
    return render_template('invenio_memento/index.html', memento=memento)
