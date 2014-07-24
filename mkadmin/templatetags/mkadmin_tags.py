from __future__ import unicode_literals

from django import template
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import NoReverseMatch, reverse
from django.templatetags.static import static
from django.utils import six
from django.utils.text import capfirst

from mkadmin.dashboard import dashboard


register = template.Library()


@register.assignment_tag(takes_context=True)
def mkadmin_topbar(context, site=admin.site):
    # Almost an exact copy of the code in django.contrib.admin.sites
    request = context['request']

    app_dict = {}
    user = request.user
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'name_singular': capfirst(model._meta.verbose_name),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse(
                            'admin:%s_%s_changelist' % info,
                            current_app=site.name)
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse(
                            'admin:%s_%s_add' % info,
                            current_app=site.name)
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': apps.get_app_config(app_label).verbose_name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=site.name),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    # Sort the apps alphabetically.
    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    create_models = [
        apps.get_model(model) for model in settings.MKADMIN_CREATE]

    return {
        'app_list': app_list,
        'create': [
            {
                'name': capfirst(model._meta.verbose_name),
                'perms': {'add': True},  # FIXME
                'add_url': reverse(
                    'admin:%s_%s_add' % (
                        model._meta.app_label, model._meta.model_name),
                    current_app=site.name),
            } for model in create_models],
    }


@register.simple_tag(takes_context=True)
def mkadmin_dashboard(context, site=admin.site):
    html = ''.join(
        widget.render(context=context) for widget in dashboard.widgets)

    return '<script src="%s"></script>%s' % (
        static('admin/js/jquery.min.js'),
        html)
