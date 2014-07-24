from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import six
from django.utils.functional import cached_property
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _


class Dashboard(object):
    @cached_property
    def widgets(self):
        return [
            get_object(widget)(**config)
            for widget, config in settings.MKADMIN_DASHBOARD]

    @cached_property
    def urls(self):
        urlpatterns = patterns('')
        for widget in self.widgets:
            urlpatterns += patterns(
                '',
                url(
                    r'^%s/' % widget.__class__.__name__.lower(),
                    include(widget.get_urls()),
                ),
            )
        return urlpatterns


dashboard = Dashboard()


class Widget(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError('Invalid attribute %s for %s' % (
                    key, self.__class__.__name__))
            setattr(self, key, value)

    def get_urls(self):
        return patterns('')

    def get_context(self):
        return {}

    def render(self, context):
        html = render_to_string(
            'mkadmin/%s.html' % self.__class__.__name__.lower(),
            dict(self.get_context(), widget=self),
            context_instance=context)
        return html


class AtAGlance(Widget):
    models = []
    title = _('At a glance')

    def get_context(self):
        models = [apps.get_model(model) for model in self.models]
        models = [{
            'name': model._meta.verbose_name_plural,
            'count': model._default_manager.count(),
            'admin_url': reverse('admin:%s_%s_changelist' % (
                model._meta.app_label, model._meta.model_name)),
        } for model in models]

        versions = []

        import django
        versions.append('Django %s' % django.get_version())

        try:
            import feincms
            versions.append('FeinCMS %s' % feincms.__version__)
        except ImportError:
            pass

        return {
            'models': models,
            'versions': versions,
        }


class Feed(Widget):
    title = _('Feed')
    url = None

    def get_urls(self):
        return patterns(
            '',
            url(r'^mkadmin_feed_feed/$', self.feed, name='mkadmin_feed_feed'),
        )

    def cache_key(self):
        import hashlib
        return 'mkadmin-feed-%s' % hashlib.md5(self.url).hexdigest()

    def feed(self, request):
        from django.http import HttpResponse
        html = cache.get(self.cache_key())
        if html:
            return HttpResponse(html)

        import feedparser
        import socket

        socket.setdefaulttimeout(5)
        try:
            feed = feedparser.parse(self.url)
            context = {
                'feed': feed,
            }
        except:
            context = {}

        html = render_to_string('mkadmin/feed_feed.html', context)
        cache.set(self.cache_key(), html, timeout=300)
        return HttpResponse(html)


class RecentActions(Widget):
    title = _('Recent Actions')


class AllApps(Widget):
    title = _('All apps')


class QuickDraft(Widget):
    title = _('Quick draft')


def get_object(path, fail_silently=False):
    # Return early if path isn't a string (might already be an callable or
    # a class or whatever)
    if not isinstance(path, six.string_types):  # XXX bytes?
        return path

    try:
        return import_module(path)
    except ImportError:
        try:
            dot = path.rindex('.')
            mod, fn = path[:dot], path[dot + 1:]

            return getattr(import_module(mod), fn)
        except (AttributeError, ImportError):
            if not fail_silently:
                raise
