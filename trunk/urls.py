# -*- coding: utf-8 -*-
#
#  Copyright (c) 2009 Marcello Bontempo Salgueiro and contributors
#
#  This file is part of Django XMPP.
#
#  Django XMPP is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#


from django.conf.urls.defaults import *
from settings import DJANGO_MEDIA_ROOT, DJANGO_MEDIA_URL
urlpatterns = patterns('',
    (r'login/$', 'django_xmpp.views.login'),
	(r'(?P<uuid>\w+)/logout/$','django_xmpp.views.logout'),
	(r'(?P<uuid>\w+)/msg/$', 'django_xmpp.views.recive_message'),
	(r'(?P<uuid>\w+)/send/$', 'django_xmpp.views.send_message'),
	(r'(?P<uuid>\w+)/roster/$','django_xmpp.views.view_roster'),
	(r'(?P<uuid>\w+)/status/$','django_xmpp.views.set_status'),
	(r'(?P<uuid>\w+)/auth/$','django_xmpp.views.authorize_view'),
	(r'^%s(?P<path>.*)$' % DJANGO_MEDIA_URL, 'django.views.static.serve',
		{'document_root': DJANGO_MEDIA_ROOT}),
    )
print DJANGO_MEDIA_ROOT

