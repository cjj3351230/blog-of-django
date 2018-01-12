from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count
# 表示从上级目录的models.py文件（即数据库模型文件）

# 按照Django将函数注册为模板标签，否则Django在模板中无法使用
register = template.Library()

@register.simple_tag	# simple_tag为简单标签，只有一个参数
def get_recent_posts(num=5):	# 最新文章模板标签
	return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag	
def archives():		# 归档模板标签
	return Post.objects.dates('created_time', 'month', order='DESC')
	# 这里dates方法会返回一个列表，元素为每篇文章（Post）的创建时间，
	# created_time表示创建时间
	# month表示精度，精确到月
	# order='DESC'表明降序排列（即离当前越近的时间越排在前面）

@register.simple_tag
def get_categories(): 	# 分类模板标签
	# 需要在顶部引入Category类，因为该类定义在models.py中
	# 需要在顶部引入Count函数，count计算分类下的文章数，接受的参数为需要技术的模板的名称
	# annotate方法与all类似，返回数据库中Category全部记录，同时会统计返回的Category记录集合中的每条记录下的文章数
	# Count方法接收一个和Category相关联的模型参数名（post),统计与之关联的Post记录的文章数后，把值保存到num_posts属性中
	# 双下划线表示把num_posts.gt属性转化为参数num_posts__gt，这里使用filter过滤掉num_posts值小于1的分类
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
	# 只要是两个model类通过ForeignKey或者ManyToMany关联起来，那么就可以用annotate方法来统计数量

@register.simple_tag
def get_tags():
	# 方法与get_categories相同
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)