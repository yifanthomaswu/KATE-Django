from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal_page/$', views.personal_page, name='personal_page'),
    url(r'^timetable/2016/(?P<period_id>[1-7])/(?P<letter_yr>[a-z][0-9])/(?P<login>[a-z0-9]+)/$', views.timetable, name='timetable'),
]
