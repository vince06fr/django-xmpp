from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
WHERE = os.path.abspath(os.path.dirname(__file__))

XMPP_MEDIA_ROOT= getattr(settings,'XMPP_MEDIA_ROOT', WHERE+'/media/')
XMPP_MEDIA_URL= getattr(settings,'XMPP_MEDIA_URL','/media/')
