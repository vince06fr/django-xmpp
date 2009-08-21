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

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
WHERE = os.path.abspath(os.path.dirname(__file__))

XMPP_MEDIA_ROOT= getattr(settings,'XMPP_MEDIA_ROOT', WHERE+'/media/')
XMPP_MEDIA_URL= getattr(settings,'XMPP_MEDIA_URL','/media/')
