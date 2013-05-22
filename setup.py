#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from distutils.core import setup, Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the project tests."""

        import django
        from django.conf import settings
        from django.core.management import call_command

        config = {
            'SITE_ID': 1,
            'ROOT_URLCONF': '',
            'INSTALLED_APPS': [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'pgtools',
            ],
        }

        django_version = django.VERSION[:2]
        if django_version > (1,1):
            config.update({
                'DATABASES': {
                    'default': {
                        'NAME': 'pgtools',
                        'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'USER': 'postgres',
                    }
                }
            })
        if django_version < (1,4):
            config.update({
                'DATABASE_ENGINE': 'django.db.backends.postgresql_psycopg2',
                'DATABASE_NAME': 'pgtools',
                'DATABASE_USER': 'postgres',
            })

        settings.configure(**config)

        call_command('test', interactive=False)


setup(
    name='django-pgtools',
    version='0.1',
    description="Set of Django management commands for handling various aspects of managing PostgreSQL database.",
    url='https://launchpad.net/django-pgtools',
    author='Canonical ISD',
    author_email='canonical-isd@lists.launchpad.net',
    packages=['pgtools', 'pgtools/management', 'pgtools/management/commands'],
    license='AGPLv3',
    cmdclass = {'test': TestCommand},
)
