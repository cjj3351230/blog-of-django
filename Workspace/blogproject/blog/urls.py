from django.conf.urls import url

from . import views

app_name = 'blog'
# 告诉Django这个urls.py模块属于blog应用
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),	# 这里[0-9]+表示至少有一个数字
    																# 这里name='detail'与models.py中的'blog:detail'有关
    																# ?P<pk>表示命名捕获组，用于从用户访问的URL里把括号内匹配的字符串捕获并作为关键字参数传给其对应的视图函数detail
   	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})', views.archives, name='archives'),
   	url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category')
   	# 括号括起来的地方为两个命名组参数（year和month部分）
   	# django会从用户访问的URL中自动提取这两个参数值，然后传递给其对应的视图函数（即archives函数）
   	# 例如：用户查看2017年3月的文章，访问url为/archives/2017/3，那么archives函数调用为archives(request, year=2017, month=3)。
]
