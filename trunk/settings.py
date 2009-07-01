from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
WHERE = os.getcwd()

DJANGO_MEDIA_ROOT= getattr(settings,'DJANGO_MEDIA_ROOT', WHERE+'/django_xmpp/media/')
DJANGO_MEDIA_URL= getattr(settings,'DJANGO_MEDIA_URL','media/')
