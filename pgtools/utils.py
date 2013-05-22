# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.conf import settings
from django.core.management.base import CommandError
from django.db.utils import load_backend


def check_database_engine():
    all_psql = True
    postgresql_psycopg2_engine = load_backend('django.db.backends.postgresql_psycopg2')
    if getattr(settings, 'DATABASES', None):
        # Django 1.2+ style
        for db in settings.DATABASES.values():
            engine = load_backend(db['ENGINE'])
            if not issubclass(engine.DatabaseWrapper,
                              postgresql_psycopg2_engine.DatabaseWrapper):
                all_psql = False
    else:
        # Django -1.1 style
        engine = load_backend(settings.DATABASE_ENGINE)
        if not issubclass(engine.DatabaseWrapper,
                          postgresql_psycopg2_engine.DatabaseWrapper):
            all_psql = False
    if not all_psql:
        raise CommandError(
            'Only the postgresql_psycopg2 database engine is supported.')


def get_rolename_from_settings():
    rolename = getattr(settings, 'PG_BASE_ROLE', None)
    if rolename is None:
        raise CommandError(
            'Please provide a role name, or set the PG_BASE_ROLE setting.')
    return rolename


def parse_username_and_rolename(args):
    username = None
    rolename = None
    arg_count = len(args)

    if arg_count == 2:
        username, rolename = args
    else:
        if arg_count > 2:
            raise CommandError('Too many arguments provided.')
        elif arg_count < 1:
            raise CommandError(
                'Please provide both a username and a role name.')
        username = args[0]
        rolename = get_rolename_from_settings()

    return (username, rolename)
