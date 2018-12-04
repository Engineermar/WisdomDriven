# urls.py
from django.conf.urls import patterns, include, url

from .views import TimeSeriesView
urlpatterns = patterns('',
    url(r'^data', TimeSeriesView.as_view()),
)

# This is only required to support extension-style formats (e.g. /data.csv)
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
