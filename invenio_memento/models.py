# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Define relation between Mementos and buckets."""

from __future__ import absolute_import

from invenio_db import db
from invenio_files_rest.models import Bucket
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import validates
from sqlalchemy_utils.types import UUIDType


class MementoArchives(db.Model):
    """Relationship between Memento and Buckets."""

    __tablename__ = 'memento_archives'

    archived = db.Column(
        db.DateTime,
        primary_key=True,
    )
    """The archivation date and time."""

    key = db.Column(
        db.Text().with_variant(mysql.VARCHAR(255), 'mysql'),
        primary_key=True,
    )
    """Key identifying the archived object."""

    bucket_id = db.Column(
        UUIDType,
        db.ForeignKey(Bucket.id),
        nullable=False,
    )
    """The bucket with archived files related to the ``key``.

    .. note:: There must be a ``ObjectVersion`` with same key.
    """

    bucket = db.relationship(Bucket)

    def __repr__(self):
        """Return representation of Memento."""
        return '{0.archived}/{0.key}:{0.bucket_id}'.format(self)

    @validates('archived')
    def validate_archived(self, key, value):
        """Remove microseconds from the value."""
        return value.replace(microsecond=0) if value else value
