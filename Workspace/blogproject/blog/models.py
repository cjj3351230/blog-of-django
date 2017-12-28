# 一般该文件中放置与数据库相关的函数
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):	# 一个类对应一个数据库表格，类名即表明
	'''
	Django要求模型必须继承 models.Model 类
	Category 只需要一个简单的分类名name就可以了
	CharField 制定了分类名name的数据类型，CharField为字符型
	CharField的max_length参数指定了最大长度，超过的分类名就不能被存入数据库
	还有其他数据类型如：日期时间类型DateTimeField、整数类型IntegerField等
	'''
	name = models.CharField(max_length=100)		# name为该表格的一个列名，属性名name即列名

	def __str__(self):
		return self.name

class Tag(models.Model):
	'''
	同上
	'''
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Post(models.Model):
	# 文章标题
	title = models.CharField(max_length=70)

	# 正文使用TextField
	# 存储比较短的字符串可以使用CharField，但文章正文为一大段文本，因此使用TextField来存储大段文本。
	body = models.TextField()

	# 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间用DateTimeField类型
	created_time = models.DateTimeField(auto_now_add=True)
	modified_time = models.DateTimeField()

	# 文章摘要，可以没有摘要，但默认情况下Charfield要求必须存入数据，否则会报错
	# 制定CharField的blank=True参数就可以允许空值
	excerpt = models.CharField(max_length=200, blank=True)

	# 这是分类与标签，分类与标签的模型已经定义在上面
	# 这里把文章对应的数据表与分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
	# 我们规定一篇文章只能对应一个分类，但是一个分类下也可以有多篇文章，所以我们使用ForeignKey，即一对多的关联关系
	# 对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以使用ManyToManyField，表明这是多对多关联的关系
	# 同时我们规定文章可以没有标签，因此为标签tags指定了blank=True
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag, blank=True)

	# 文章作者，这里User是从django.contrib.auth.models导入的
	# django.contrib.auth是Django内置应用，专门用于处理网站用户的注册、登录等流程，User是Django为我们已经写好的用户模型
	# 这里通过ForeignKey把文章和User关联起来
	# 因为一篇文章只能有一个作者，而一个作者可能会写很多文章，因此这是一对多的关联关系，和Category类似
	author = models.ForeignKey(User)

	def __str__(self):
		return self.title

	# 自定义get_absolute_url 方法
	# 记得从django.urls中导入reverse函数
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})
		# blog:detail表示blog应用下的name=detail的函数，跟urls.py中的url(...., name='detail')有关
		# 由于通过app_name='blog'告诉django这个url属于blog应用，因此django能找到blog应用下的detail视图函数
		# reverse函数用于解析detail视图函数对应的url

	# Django允许我们再models.Model的子类里定义一个Meta类，这个内部类通过指定一些属性来规定这个类该有的一些特性
	class Meta:
		# 表示先按创建时间逆序排列，如果时间相同则根据title排列，还可以添加其他参数
		ordering = ['-created_time', 'title']