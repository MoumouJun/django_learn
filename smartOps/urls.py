from django.urls import path, re_path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login$', views.login),
    url(r'^index$', views.index),
    url(r'^welcome$', views.welcome),
    url(r'^knowledge_list$', views.knowledge_list),
    url(r'^knowledge_category$', views.knowledge_category),
    url(r'^knowledge_category_add$', views.knowledge_category_add),
    url(r'^knowledge_upload$', views.knowledge_upload),


    # Upload Files Using Model Form
    url(r'file_upload/$', views.file_upload),
    # 下载模板
    url(r'^file_download$', views.file_download),

    # View File List
    path('file/', views.file_list, name='file_list'),

]