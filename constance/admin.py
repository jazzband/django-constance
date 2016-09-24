from collections import OrderedDict
from operator import itemgetter

from django import VERSION
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from . import LazyConfig, settings
from .forms import ConstanceForm
from .utils import get_constance_values

config = LazyConfig()


class ConstanceAdmin(admin.ModelAdmin):
    change_list_template = 'admin/constance/change_list.html'
    change_list_form = ConstanceForm

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        return [
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_add' % info),
        ]

    def get_config_value(self, name, options, form, initial):
        default, help_text = options[0], options[1]
        # First try to load the value from the actual backend
        value = initial.get(name)
        # Then if the returned value is None, get the default
        if value is None:
            value = getattr(config, name)
        config_value = {
            'name': name,
            'default': localize(default),
            'help_text': _(help_text),
            'value': localize(value),
            'modified': value != default,
            'form_field': form[name],
        }

        return config_value

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        # First load a mapping between config name and default value
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        initial = get_constance_values()
        form = self.change_list_form(initial=initial)
        if request.method == 'POST':
            form = self.change_list_form(data=request.POST, initial=initial)
            if form.is_valid():
                form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Live settings updated successfully.'),
                )
                return HttpResponseRedirect('.')
        context = {
            'config_values': [],
            'title': _('Constance config'),
            'app_label': 'constance',
            'opts': self.model._meta,
            'form': form,
            'media': self.media + form.media,
            'icon_type': 'gif' if VERSION < (1, 9) else 'svg',
        }
        for name, options in settings.CONFIG.items():
            context['config_values'].append(
                self.get_config_value(name, options, form, initial)
            )

        if settings.CONFIG_FIELDSETS:
            context['fieldsets'] = []
            for fieldset_title, fields_list in settings.CONFIG_FIELDSETS.items():
                fields_exist = all(
                    field in settings.CONFIG.keys() for field in fields_list
                )
                assert fields_exist, "CONSTANCE_CONFIG_FIELDSETS contains fields that does not exist"
                config_values = []

                for name, options in settings.CONFIG.items():
                    if name in fields_list:
                        config_values.append(
                            self.get_config_value(name, options, form, initial)
                        )

                context['fieldsets'].append({
                    'title': fieldset_title,
                    'config_values': config_values
                })

        if not isinstance(settings.CONFIG_FIELDSETS, OrderedDict):
            context['config_values'].sort(key=itemgetter('name'))
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.change_list_template, context)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, request, obj=None):
        if settings.SUPERUSER_ONLY:
            return request.user.is_superuser
        return super(ConstanceAdmin, self).has_change_permission(request, obj)


class Config(object):
    class Meta(object):
        app_label = 'constance'
        object_name = 'Config'
        model_name = module_name = 'config'
        verbose_name_plural = _('config')
        abstract = False
        swapped = False

        def get_ordered_objects(self):
            return False

        def get_change_permission(self):
            return 'change_%s' % self.model_name

    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
