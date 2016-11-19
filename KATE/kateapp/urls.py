from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personal_page/', views.personal_page, name='personal_page'),
]
