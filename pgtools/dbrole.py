# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from django.core.management.base import CommandError
from django.db import connection, transaction


class DatabaseRole(object):
    ROLE_NAME = 'rolname'

    def __init__(self, rolename, create=False, commit=True,
                 db_connection=None, db_transaction=None):
        self.rolename = rolename
        self.connection = (connection if db_connection is None
                                      else db_connection)
        self.transaction = (transaction if db_transaction is None
                                        else db_transaction)
        exists = self.exists(rolename)

        if create:
            if exists:
                raise CommandError("Role already exists: %s" % rolename)

            cursor = self.connection.cursor()
            cursor.execute("CREATE ROLE %s" % rolename)
            if commit:
                self.transaction.commit_unless_managed()
                if not self.exists(rolename):
                    raise CommandError("Role couldn't be created: %s" % rolename)
        elif not exists:
            raise CommandError("Role doesn't exist: %s" % rolename)

    def delete(self, commit=True):
        cursor = self.connection.cursor()
        cursor.execute("DROP ROLE %s" % self.rolename)
        if commit:
            self.transaction.commit_unless_managed()
            if self.exists(self.rolename):
                raise CommandError("Role cannot be deleted: %s" % self.rolename)

    @classmethod
    def exists(cls, rolename, db_connection=None):
        db_connection = connection if db_connection is None else db_connection

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM pg_roles WHERE rolname = %s', (rolename,))
        role = cursor.fetchone()
        return role is not None

    def get_users(self, order_by=ROLE_NAME):
        cursor = self.connection.cursor()
        query = ("SELECT rolname FROM pg_authid "
                 " WHERE oid IN ("
                 "       SELECT member FROM pg_auth_members "
                 "        WHERE roleid = ("
                 "              SELECT oid FROM pg_authid "
                 "               WHERE rolname = %%s)) "
                 "ORDER BY %s" % order_by)
        cursor.execute(query, (self.rolename,))
        users_result = cursor.fetchall()
        users = [result[0] for result in users_result]
        return users

    def grant(self, user, commit=True):
        cursor = self.connection.cursor()
        cursor.execute("GRANT %s TO %s" % (self.rolename, user.username))
        if commit:
            self.transaction.commit_unless_managed()

    def revoke(self, user, commit=True):
        cursor = self.connection.cursor()
        cursor.execute("REVOKE %s FROM %s" % (self.rolename, user.username))
        if commit:
            self.transaction.commit_unless_managed()
            if user.has_role(self):
                raise CommandError("Role cannot be revoked: %s" % self.rolename)
