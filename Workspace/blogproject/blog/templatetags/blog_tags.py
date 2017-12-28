from ..models import Post, Category
from django import template
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
	return Category.objects.all()