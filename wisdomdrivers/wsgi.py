import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wisdomdrivers.settings")

application = get_wsgi_application()

#Use whitenoise package to serve static files on Heroku
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
