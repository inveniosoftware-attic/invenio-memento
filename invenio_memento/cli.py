# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Click command-line interface for memento management."""

from __future__ import absolute_import, print_function

from datetime import datetime

import click
from flask.cli import with_appcontext
from invenio_db import db


#
# Memento management commands
#


@click.group()
def memento():
    """File management commands."""


@memento.command()
@click.argument('source', type=click.Path(exists=True, resolve_path=True))
@click.argument('key')
@click.option('--checksum/--no-checksum', default=False)
@click.option('--key-prefix', default='')
@with_appcontext
def cp(source, key, checksum, key_prefix):
    """Create new Memento from all files in directory."""
    from invenio_files_rest.models import Bucket
    from invenio_files_rest.helpers import populate_from_path

    from .models import MementoArchives

    bucket = Bucket.create()
    memento = MementoArchives(
        archived=datetime.now(), key=key, bucket=bucket
    )
    for object_version in populate_from_path(
            bucket, source, checksum=checksum,
            key_prefix=key_prefix):
        click.secho(str(object_version))

    db.session.add(memento)
    db.session.commit()
    click.secho(str(memento), fg='green')
