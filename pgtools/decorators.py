# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import CommandError
from psycopg2 import ProgrammingError


def graceful_db_errors(func):

    def _graceful_db_errors_decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ProgrammingError, e:
            if e.pgcode == '42501':
                raise CommandError(
                    'Permission denied: please check DATABASE_* settings.')
            else:
                raise

    return _graceful_db_errors_decorator
