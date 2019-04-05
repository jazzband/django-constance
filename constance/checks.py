from django.core import checks
from django.utils.translation import ugettext_lazy as _

from . import settings


@checks.register("constance")
def check_fieldsets(*args, **kwargs):
    """
    A Django system check to make sure that, if defined, CONFIG_FIELDSETS accounts for
    every entry in settings.CONFIG.
    """
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
    field_name_list = []
    for fieldset_title, fields_list in settings.CONFIG_FIELDSETS.items():
        for field_name in fields_list:
            field_name_list.append(field_name)
    if not field_name_list:
        return {}
    return set(set(settings.CONFIG.keys()) - set(field_name_list))
