# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import VERSION
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from ...utils import get_values
from ...forms import set_constance_value
from ... import LazyConfig


config = LazyConfig()


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
                    set_constance_value(raw_name, raw_value)
                except KeyError as e:
                    raise CommandError(raw_name + " is not defined in settings.CONSTANCE_CONFIG")
                except ValidationError as e:
                    raise CommandError(", ".join(e))

        elif options.get('list'):
            for k, v in get_values().items():
                self.stdout.write("{}\t{}".format(k, v))