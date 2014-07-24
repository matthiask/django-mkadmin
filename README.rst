Django-mkadmin
==============

Modifies the stock Django-Administration interface to fit my ideas a little
bit better.


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
