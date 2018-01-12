"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.feeds import AllPostsRssFeed # RSS订阅方法

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'', include('blog.urls')), # 利用include函数，把blog中urls.py文件包含进来，则实际正则匹配为r''+r'^$'
	url(r'', include('comments.urls')),		# 评论部分
	url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
	url(r'^search/', include('haystack.urls')), # 使用haystack搜索引擎
]
