from django.contrib import admin
from django.utils.functional import update_wrapper
from django.conf.urls.defaults import patterns, url
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from constance import config



class ConstanceAdmin(admin.ModelAdmin):

    @property
    def urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.module_name
        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            #url(r'^(.+)/$',
            #    wrap(self.change_view),
            #    name='%s_%s_change' % info),
        )
        return urlpatterns

    def changelist_view(self, request):
        context = {
            'config': [],
            'root_path': self.admin_site.root_path,
            'title': 'Live settings',
            'app_label': 'constance',
            'opts': Config._meta,
        }
        for name, (default, decode, help_text) in settings.CONSTANCE_CONFIG.items():
            context['config'].append({
                'name': name,
                'default': default,
                'decode': decode,
                'help_text': help_text,
                'value': getattr(config, name),
            })
        return render_to_response(
            'admin/constance/change_list.html',
            context,
            context_instance=RequestContext(request)
        )

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return True


class Config(object):
    class Meta(object):
        app_label = 'constance'
        module_name = 'config'
        verbose_name_plural = 'config'
    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
