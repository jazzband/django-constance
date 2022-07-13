from django.core import checks
from django.utils.translation import gettext_lazy as _


@checks.register("constance")
def check_fieldsets(*args, **kwargs):
    """
    A Django system check to make sure that, if defined, CONFIG_FIELDSETS accounts for
    every entry in settings.CONFIG.
    """
    from . import settings

    if hasattr(settings, "CONFIG_FIELDSETS") and settings.CONFIG_FIELDSETS:
        inconsistent_fieldnames = get_inconsistent_fieldnames()
        if inconsistent_fieldnames:
            return [
                checks.Warning(
                    _(
                        "CONSTANCE_CONFIG_FIELDSETS is missing "
                        "field(s) that exists in CONSTANCE_CONFIG."
                    ),
                    hint=", ".join(sorted(inconsistent_fieldnames)),
                    obj="settings.CONSTANCE_CONFIG",
                    id="constance.E001",
                )
            ]
    return []


def get_inconsistent_fieldnames():
    """
    Returns a set of keys from settings.CONFIG that are not accounted for in
    settings.CONFIG_FIELDSETS.
    If there are no fieldnames in settings.CONFIG_FIELDSETS, returns an empty set.
    """
    from . import settings

    if isinstance(settings.CONFIG_FIELDSETS, dict):
        fieldset_items = settings.CONFIG_FIELDSETS.items()
    else:
        fieldset_items = settings.CONFIG_FIELDSETS

    field_name_list = []
    for fieldset_title, fields_list in fieldset_items:
        # fields_list can be a dictionary, when a fieldset is defined as collapsible
        # https://django-constance.readthedocs.io/en/latest/#fieldsets-collapsing
        if isinstance(fields_list, dict) and 'fields' in fields_list:
            fields_list = fields_list['fields']
        field_name_list += list(fields_list)
    if not field_name_list:
        return {}
    return set(set(settings.CONFIG.keys()) - set(field_name_list))
