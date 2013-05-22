# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import BaseCommand

from pgtools.dbrole import DatabaseRole
from pgtools.dbuser import DatabaseUser
from pgtools.decorators import graceful_db_errors
from pgtools.utils import check_database_engine, parse_username_and_rolename


class Command(BaseCommand):
    help = 'Delete an existing database user based on given role.'
    args = 'username [rolename]'

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()
        username, rolename = parse_username_and_rolename(args)

        role = DatabaseRole(rolename)
        user = DatabaseUser(username, create=False)

        role.revoke(user)
        user.delete()

        print "User '%s' deleted successfully." % username
