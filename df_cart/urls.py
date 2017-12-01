from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^cart/$', views.cart),
    url(r'^add(\d+)_(\d+)/$', views.add),
    url(r'^edit(\d+)_(\d+)/$', views.edit),
    url(r'^delete(\d+)/$', views.delete),
]
