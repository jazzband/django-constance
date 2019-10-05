
from django.conf import settings
from django.core import checks
from django.utils.translation import ugettext_lazy as _


DUPE_ERROR = _('Duplicate Key found in Constance Config Fieldset: %r')
DUPE_ERROR_HINT = _('Remove the duplicate key %r from CONFIG_FIELDSETS')
DUPE_ERROR_ID = _('constance.E001')

EXTRA_IN_FIELDSET = _('Extra Key found in Constance Config Fieldset not in CONFIG: %r')
EXTRA_IN_FIELDSET_HINT = _('Remove the extra key %r from CONFIG_FIELDSETS')
EXTRA_IN_FIELDSET_ID = _('constance.E003')

MISSING_IN_FIELDSET = _('Key missing from Constance Config Fieldset: %r')
MISSING_IN_FIELDSET_HINT = _('Add the missing key %r to CONFIG_FIELDSETS')
MISSING_IN_FIELDSET_ID = _('constance.E003')

NO_CONSTANCE_CONFIG = _('Constance is loaded, but CONSTANCE_CONFIG is not setup in settings')
NO_CONSTANCE_CONFIG_HINT = _('If you wish to use constance, create a CONSTANCE_CONFIG in settings, see https://django-constance.readthedocs.io/en/latest/')
NO_CONSTANCE_CONFIG_ID = _('constance.E004')


@checks.register()
def constance_config_check(app_configs, **kwargs):
    errors = []
    if hasattr(settings, 'CONFIG'):
        errors.append(
            checks.Warning(
                NO_CONSTANCE_CONFIG,
                hint=NO_CONSTANCE_CONFIG_HINT,
                obj='settings.CONSTANCE_CONFIG',
                id=NO_CONSTANCE_CONFIG_ID,
            )
        )
        return errors
    if not hasattr(settings, 'CONSTANCE_CONFIG_FIELDSETS'):
        return errors

    existing_keys = set(settings.CONSTANCE_CONFIG.keys())
    field_set_keys = set()
    for fields_list in settings.CONSTANCE_CONFIG_FIELDSETS.values():
        fields_list = set(fields_list)
        overlap = field_set_keys.intersection(fields_list)
        for field_name in overlap:
            errors.append(
                checks.Warning(
                    DUPE_ERROR % field_name,
                    hint=DUPE_ERROR_HINT % field_name,
                    obj='Constance config (settings.CONFIG)',
                    id=DUPE_ERROR_ID,
                )
            )
        field_set_keys.update(set(fields_list))

    for field_name in field_set_keys.difference(existing_keys):
        errors.append(
            checks.Error(
                EXTRA_IN_FIELDSET % field_name,
                hint=EXTRA_IN_FIELDSET_HINT % field_name,
                obj='Constance config (settings.CONFIG)',
                id=EXTRA_IN_FIELDSET_ID,
            )
        )

    for field_name in existing_keys.difference(field_set_keys):
        errors.append(
            checks.Error(
                MISSING_IN_FIELDSET % field_name,
                hint=MISSING_IN_FIELDSET_HINT % field_name,
                obj='Constance config (settings.CONFIG)',
                id=MISSING_IN_FIELDSET_ID,
            )
        )

    return errors


