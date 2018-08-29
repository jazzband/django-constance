# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django import VERSION


from ... import config
from ...admin import ConstanceForm, get_values


def _set_constance_value(key, value):
    """
    Parses and sets a Constance value from a string
    :param key:
    :param value:
    :return:
    """

    form = ConstanceForm(initial=get_values())

    field = form.fields[key]

    clean_value = field.clean(field.to_python(value))
    setattr(config, key, clean_value)


class Command(BaseCommand):
    help = _('Get/Set In-database config settings handled by Constance')

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command')
        # API changed in Django>=2.1. cmd argument was removed.
        parser_list = self._subparsers_add_parser(subparsers, 'list', cmd=self, help='list all Constance keys and their values')

        parser_get = self._subparsers_add_parser(subparsers, 'get', cmd=self, help='get the value of a Constance key')
        parser_get.add_argument('key', help='name of the key to get', metavar='KEY')

        parser_set = self._subparsers_add_parser(subparsers, 'set', cmd=self, help='set the value of a Constance key')
        parser_set.add_argument('key', help='name of the key to get', metavar='KEY')
        # use nargs='+' so that we pass a list to MultiValueField (eg SplitDateTimeField)
        parser_set.add_argument('value', help='value to set', metavar='VALUE', nargs='+')


    def _subparsers_add_parser(self, subparsers, name, **kwargs):
        # API in Django >= 2.1 changed and removed cmd parameter from add_parser
        if VERSION >= (2, 1) and 'cmd' in kwargs:
            kwargs.pop('cmd')
        return subparsers.add_parser(name, **kwargs)


    def handle(self, command, key=None, value=None, *args, **options):

        if command == 'get':
            try:
                self.stdout.write("{}".format(getattr(config, key)), ending="\n")
            except AttributeError as e:
                raise CommandError(key + " is not defined in settings.CONSTANCE_CONFIG")

        elif command == 'set':
            try:
                if len(value) == 1:
                    # assume that if a single argument was passed, the field doesn't expect a list
                    value = value[0]

                _set_constance_value(key, value)
            except KeyError as e:
                raise CommandError(key + " is not defined in settings.CONSTANCE_CONFIG")
            except ValidationError as e:
                raise CommandError(", ".join(e))

        elif command == 'list':
            for k, v in get_values().items():
                self.stdout.write("{}\t{}".format(k, v), ending="\n")
