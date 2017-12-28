from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 要在后台注册我们自己创建的几个模型，这样Django Admin才能知道他们的存在
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)