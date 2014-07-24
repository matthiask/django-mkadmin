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
        ('mkweb.mkadmin.AtAGlance', {
            'models': ['blog.Post', 'chet.Album', 'chet.Photo'],
        }),
        ('mkweb.mkadmin.AllApps', {
        }),
        ('mkweb.mkadmin.RecentActions', {
        }),
        ('mkweb.mkadmin.QuickDraft', {
        }),
        ('mkweb.mkadmin.Feed', {
            'url': 'http://www.feinheit.ch/news/feed/',
        }),
    ]
