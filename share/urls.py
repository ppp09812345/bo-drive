# share/urls.py

from django.urls import path
from . import views
from share.views import HomeView,DisplayView,MyView,SearchView #视图里的对象
from django.contrib import admin
from django.conf.urls import include,url

app_name = 'share'

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^$', HomeView.as_view(),name="home"), #引用视图对象需要调用对象的as.view().以对象的形式去调用，所以加括号
    url(r'^s/(?P<code>\d+)/$',DisplayView.as_view(),name="icode"),
    #/s/(?P<code>\d+ 使用了组匹配的方式 匹配code任意长度的数字，如/s/123456，将123456传给 DisplayView,这里的 code 必须和视图函数的 code 保持一致。
    url(r'^search/',SearchView.as_view(),name="search"),
    url(r'^my/$',MyView.as_view(),name="MY"),
]

