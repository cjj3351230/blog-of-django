from django.db import models

# Create your models here.

class Comment(models.Model):
	# forms.py中的4个需要显示的字段要满足数据库中属性的需要，比如这里created_time不需要用户填写，则在forms.py中不用显示created_time
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	url = models.URLField(blank=True)
	text = models.TextField()
	created_time = models.DateTimeField(auto_now_add=True)	# auto_now_add参数作用是：当评论数据保存到数据库是，自动把created_time的值指定为当前时间

	post = models.ForeignKey('blog.Post')  # 表示数据库Comment表的post属性与blog应用的数据库中Post表为多对一关联

	def __str__(self):
		return self.text[:20]

	class Meta:
		ordering = ['-created_time', 'name']