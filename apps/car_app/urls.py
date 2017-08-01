from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),       #login/reg page
  url(r'^home$', views.home, name="home"),    #main homepage
  url(r'^register/process$', views.register_process),
  url(r'^login$', views.login),
  #url(r'^logout$', views.logout, name='logout'),
  #url(r'^new_user$', views.register_process)#login post request
]