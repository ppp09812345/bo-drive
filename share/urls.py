# lib/urls.py

from django.urls import path
from . import views
from share.views import HomeView #视图里的对象
from django.contrib import admin
from django.conf.urls import include,url

app_name = 'share'
urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^$', HomeView.as_view(),name="home"), #引用视图对象需要调用对象的as.view().以对象的形式去调用，所以加括号
   #path('detail/', views.detail, name='detail'),
]

