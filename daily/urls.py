from django.conf.urls import url

from . import views

app_name = 'daily'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_task/', views.add_task, name='add_task'),
    url(r'^add_interval/', views.add_interval, name='add_interval'),
]