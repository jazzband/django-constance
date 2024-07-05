from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.management import CommandError
from django.utils.translation import gettext as _

from constance import config
from constance.forms import ConstanceForm
from constance.models import Constance
from constance.utils import get_values


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

    GET = 'get'
    SET = 'set'
    LIST = 'list'
    REMOVE_STALE_KEYS = 'remove_stale_keys'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command')
        subparsers.add_parser(self.LIST, help='list all Constance keys and their values')

        parser_get = subparsers.add_parser(self.GET, help='get the value of a Constance key')
        parser_get.add_argument('key', help='name of the key to get', metavar='KEY')

        parser_set = subparsers.add_parser(self.SET, help='set the value of a Constance key')
        parser_set.add_argument('key', help='name of the key to set', metavar='KEY')
        # use nargs='+' so that we pass a list to MultiValueField (eg SplitDateTimeField)
        parser_set.add_argument('value', help='value to set', metavar='VALUE', nargs='+')

        subparsers.add_parser(
            self.REMOVE_STALE_KEYS,
            help='delete all Constance keys and their values if they are not in settings.CONSTANCE_CONFIG (stale keys)',
        )

    def handle(self, command, key=None, value=None, *args, **options):
        if command == self.GET:
            try:
                self.stdout.write(str(getattr(config, key)), ending='\n')
            except AttributeError as e:
                raise CommandError(f'{key} is not defined in settings.CONSTANCE_CONFIG') from e
        elif command == self.SET:
            try:
                if len(value) == 1:
                    # assume that if a single argument was passed, the field doesn't expect a list
                    value = value[0]
                _set_constance_value(key, value)
            except KeyError as e:
                raise CommandError(f'{key} is not defined in settings.CONSTANCE_CONFIG') from e
            except ValidationError as e:
                raise CommandError(', '.join(e)) from e
        elif command == self.LIST:
            for k, v in get_values().items():
                self.stdout.write(f'{k}\t{v}', ending='\n')
        elif command == self.REMOVE_STALE_KEYS:
            actual_keys = settings.CONSTANCE_CONFIG.keys()
            stale_records = Constance.objects.exclude(key__in=actual_keys)
            if stale_records:
                self.stdout.write('The following record will be deleted:', ending='\n')
            else:
                self.stdout.write('There are no stale records in the database.', ending='\n')
            for stale_record in stale_records:
                self.stdout.write(f'{stale_record.key}\t{stale_record.value}', ending='\n')
            stale_records.delete()
        else:
            raise CommandError('Invalid command')
