from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal_page/$', views.personal_page, name='personal_page'),
    url(r'^individual_record/(?P<login>[a-z0-9]+)/$', views.individual_record, name='individual_record'),
    url(r'^timetable/2016/(?P<period_id>[1-7])/(?P<letter_yr>[a-z][0-9])/(?P<login>[a-z0-9]+)/$', views.timetable, name='timetable'),
    url(r'^course/2016/(?P<letter_yr>[a-z][0-9])/$', views.course_list, name='course_list'),
    url(r'^course/2016/(?P<code>[.0-9]+)/$', views.course, name='course'),
    url(r'^exercise_setup/2016/(?P<code>[.0-9]+)/(?P<number>[1-9]+)/$', views.exercise_setup, name='exercise_setup'),
    url(r'^submission/2016/(?P<code>[.0-9]+)/(?P<number>[1-9]+)/$', views.submission, name='submission'),
    url(r'^marking/2016/(?P<code>[.0-9]+)/(?P<number>[1-9]+)/$', views.marking, name='marking'),
    url(r'^grading_scheme/$', views.grading_scheme, name='grading_scheme'),
]
