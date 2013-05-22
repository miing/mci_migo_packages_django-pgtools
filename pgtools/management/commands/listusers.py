# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import BaseCommand, CommandError

from pgtools.dbrole import DatabaseRole
from pgtools.decorators import graceful_db_errors
from pgtools.utils import check_database_engine, get_rolename_from_settings


class Command(BaseCommand):
    help = 'List database users with access to given role.'
    args = 'rolename'

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()
        if len(args) < 1:
            rolename = get_rolename_from_settings()
        elif len(args) == 1:
            rolename = args[0]
        else:
            raise CommandError('Too many arguments.')

        role = DatabaseRole(rolename)
        roles = role.get_users()
        if not roles:
            print "No users exist for role: %s" % rolename
        else:
            for role in roles:
                print role
