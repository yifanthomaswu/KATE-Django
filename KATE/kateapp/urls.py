from django.conf.urls import url

from . import views

app_name = 'kateapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^timetable/2016/(?P<period_id>[1-7])/(?P<letter_yr>[a-z][0-9])/(?P<login>[a-z0-9]+)/$', views.timetable, name='timetable'),
]
