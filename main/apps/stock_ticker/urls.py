from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^index$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^result$', views.result),
    url(r'^dashboard/update$', views.update),
    url(r'^login$', views.login), 
    url(r'^register$', views.register), 
    url(r'^logout$', views.logout)
    ]