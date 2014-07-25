Django-mkadmin
==============

Modifies the stock Django-Administration interface to fit my ideas a little
bit better.

Add ``django-mkadmin`` to your requirements file. Currently there is no release,
therefore you can add the following line to install the latest version::

    -e git+git://github.com/matthiask/django-mkadmin.git#egg=mkadmin-dev

Add ``mkadmin`` to ``INSTALLED_APPS``. The entry has to be before
``django.contrib.admin`` because ``mkadmin`` overrides ``admin/base_site.html``
and ``admin/index.html``.

Add ``django.core.context_processors.request`` to
``TEMPLATE_CONTEXT_PROCESSORS``.

Add an entry to your URLconf::

    from django.conf.urls import patterns, url, include
    from django.contrib import admin
    from mkadmin.dashboard import dashboard

    admin.autodiscover()

    urlpatterns = patterns(
        '',
        url(r'^admin/mkadmin/', include(dashboard.urls)),
        url(r'^admin/' include(admin.site.urls)),
    )

Configuration of the Create menu::

    MKADMIN_CREATE = [
        'blog.Post',
        # 'blog',  # Take all models from the blog app, does not work yet.
        'chet.Album',
    ]

Dashboard configuration::

    MKADMIN_DASHBOARD = [
        ('mkadmin.dashboard.AtAGlance', {
            'models': ['blog.Post', 'chet.Album', 'chet.Photo'],
        }),
        ('mkadmin.dashboard.AllApps', {
        }),
        ('mkadmin.dashboard.RecentActions', {
        }),
        ('mkadmin.dashboard.QuickDraft', {
        }),
        ('mkadmin.dashboard.Feed', {
            'url': 'http://www.feinheit.ch/news/feed/',
        }),
    ]
