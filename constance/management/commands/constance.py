# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from ... import config
from ...admin import ConstanceForm
from ...utils import get_values


def _set_constance_value(name, value):
    """
    Parses and sets a Constance value from a string
    :param name:
    :param value:
    :return:
    """

    form = ConstanceForm(initial=get_values())

    field = form.fields[name]

    clean_value = field.clean(field.to_python(value))
    setattr(config, name, clean_value)


class Command(BaseCommand):
    help = _('Get/Set In-database config settings handled by Constance')

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command')

        parser_list = subparsers.add_parser('list', cmd=self)

        parser_get = subparsers.add_parser('get', cmd=self)
        parser_get.add_argument('name')

        parser_set = subparsers.add_parser('set', cmd=self)
        parser_set.add_argument('name')
        parser_set.add_argument('value')

    def handle(self, command, name=None, value=None, *args, **options):

        if command == 'get':
            try:
                self.stdout.write("{}".format(getattr(config, name)).encode('utf-8'), ending=b"\n")
            except AttributeError as e:
                raise CommandError(name + " is not defined in settings.CONSTANCE_CONFIG")

        elif command == 'set':
            try:
                _set_constance_value(name, value)
            except KeyError as e:
                raise CommandError(name + " is not defined in settings.CONSTANCE_CONFIG")
            except ValidationError as e:
                raise CommandError(", ".join(e))

        elif command == 'list':
            for k, v in get_values().items():
                self.stdout.write("{}\t{}".format(k, v).encode('utf-8'), ending=b"\n")
