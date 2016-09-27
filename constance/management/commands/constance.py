# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from ...admin import ConstanceForm
from ...utils import get_values
from ... import config


def _set_constance_value(raw_name, raw_value):
    """
    Parses and sets a Constance value
    :param raw_name:
    :param raw_value:
    :return:
    """

    form = ConstanceForm(initial=get_values())

    field = form.fields[raw_name]

    value = field.clean(field.to_python(raw_value))
    setattr(config, raw_name, value)


class Command(BaseCommand):
    help = _('Get/Set In-database config settings handled by Constance')

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--list", action="store_true",
                           help=_("List all Constance settings"))
        group.add_argument("--get", dest='setting', nargs=1)
        group.add_argument("--set", dest='setting', nargs=2, metavar=('SETTING', 'VALUE',))

    def handle(self, *args, **options):

        if options.get('setting'):
            raw_name = options.get('setting')[0]

            if len(options.get('setting')) == 1:
                # get
                try:
                    print(getattr(config, raw_name))
                except AttributeError as e:
                    raise CommandError(raw_name + " is not defined in settings.CONSTANCE_CONFIG")
            else:
                # set
                raw_value = options.get('setting')[1]

                try:
                    _set_constance_value(raw_name, raw_value)
                except KeyError as e:
                    raise CommandError(raw_name + " is not defined in settings.CONSTANCE_CONFIG")
                except ValidationError as e:
                    raise CommandError(", ".join(e))

        elif options.get('list'):
            for k, v in get_values().items():
                self.stdout.write("{}\t{}".format(k, v).encode('utf-8'))
