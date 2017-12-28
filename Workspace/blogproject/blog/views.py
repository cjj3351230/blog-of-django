from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm # 评论部分。从comments文件的forms.py文件中引入CommentForm类
import markdown

# Create your views here.
def index(request):
	# all方法返回一个QuerySet（可以理解为类似于列表的数据结构）；之后调用order_by方法对queryset进行排序，排序依据的字段是created_time；"-"表示逆序，不加则为正序
	post_list = Post.objects.all()
	return render(request, 'blog/index.html', context={
			'post_list': post_list
		})

def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# 根据从URL捕获的文章id(即pk)获取数据库中文章id为该值的记录，然后传递给模板
	# get_object_or_404方法用于，当传入的pk对应的Post在数据库存在，则返回对应的post，否则会返回404错误
	post_directory = Post.objects.all()
	# 用于在detail.html中显示文章目录，参数与index函数中的post_list参数一样，只是改了名字减少冲突
	post.body = markdown.markdown(post.body,
								  extensions=[		# 给markdown渲染函数传递了额外参数extensions，该参数时对Markdown语法的拓展 
								  	'markdown.extensions.extra',	# extra本身包含很多拓展	
								  	'markdown.extensions.codehilite',	# codehilite是语法高亮拓展，为后面实现代码高亮功能提供基础
								  	'markdown.extensions.toc',		# toc允许自动生成目录
								  ])
	# 使用前需要引入CommentForm
	form = CommentForm()
	# 获取这篇post下的全部评论
	comment_list = post.comment_set.all()

	# 将文章、表单、以及文章下的评论列表作为模板变量传给detail.html模板，以便渲染相应数据
	context = {
				'post': post,	# 文章部分
				'form': form,	# 用户填写的表单部分
				'comment_list': comment_list,	# 获取文章下的全部评论的部分
				'post_directory': post_directory	# 文章目录部分
				}
	return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
# 归档视图函数
	post_list = Post.objects.filter(created_time__year=year,	# Python中类实例调用属性的方法通常是created_time.year，但这里作为函数的参数列表
									created_time__month=month 	# 所以将点替换成两个下划线
									).order_by('-created_time')
	return render(request,'blog/index.html', context={'post_list':post_list})

def category(request, pk):
# 需要导入Category类
	cate = get_object_or_404(Category,pk=pk)
	# 首先根据pk值（即分类的id值）来从数据库中获取该分类并赋值给cate变量。
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	# 通过filter过滤出分类为所获取分类的全部文章并按创建时间倒序排列
	return render(request, 'blog/index.html', context={'post_list':post_list})