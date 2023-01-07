from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login$', views.login),
    url(r'^index$', views.index),
    url(r'^welcome$', views.welcome),
    url(r'^product-list$', views.product_list),
]