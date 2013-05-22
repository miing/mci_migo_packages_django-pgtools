# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

import sys
from getpass import getpass
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from pgtools.dbrole import DatabaseRole
from pgtools.dbuser import DatabaseUser
from pgtools.decorators import graceful_db_errors
from pgtools.utils import check_database_engine, parse_username_and_rolename


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-p', '--password', default=None, dest='password',
            help='Password of the user to be created.'),
        make_option('-P', '--no-password', default=False, dest='no_password',
            action='store_true',
            help='If given, then no password is set up for the user.'),
    )
    help = 'Create a new database user based on an existing role.'
    args = 'username [rolename]'

    def _ask_password(self):
        password = None
        try:
            while True:
                if password is None:
                    password = getpass('Password: ')
                    password2 = getpass('Password (again): ')
                    if password != password2:
                        sys.stderr.write(
                            "Error: Your passwords didn't match.\n")
                        password = None
                        continue
                if password.strip() == '':
                    sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                    password = None
                    continue
                break
        except KeyboardInterrupt:
            raise CommandError('Cancelled.')

        return password

    @graceful_db_errors
    def handle(self, *args, **options):
        check_database_engine()
        username, rolename = parse_username_and_rolename(args)

        password = options.get('password')
        no_password = options.get('no_password')
        if not no_password and password is None:
            self._ask_password()

        role = DatabaseRole(rolename)
        user = DatabaseUser(username, password)
        role.grant(user)

        print "User '%s' created successfully based on role '%s'." % (
            username, rolename)
