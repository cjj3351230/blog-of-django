from django.shortcuts import render, get_object_or_404, redirect	# 重定向函数在django.shortcuts中
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_comment(request, post_pk):
	
	# 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
	# 使用Django提供的一个快捷函数get_object_or_404
	# 这个函数的作用是当获取的文章（Post）存在时，则获取，否则返回404页面给用户
	post = get_object_or_404(Post, pk=post_pk)
	
	# HTTP请求有get和post两种，一般用户通过表单提交数据都是通过post请求，且提交的数据存在request.POST这个类字典对象中
	# 只有当用户的请求为post时需要处理表单数据
	if request.method == 'POST':
	
		# 用户提交的数据存在request.method中，为类字典对象
		# 利用这些数据构造CommentForm的实例，生成Django表单
		form = CommentForm(request.POST)

		# 当调用form.is_valid()方法时，django自动检查表单数据是否符合格式要求（即是否满足models.py中Comment表的格式要求（如不能有未填写项等）
		if form.is_valid():

			# 检查数据为合法，则调用表单的save方法保存数据到数据库
			# commit=False作用为，利用表单的数据生成Comment模型类的实例，但先不保存评论到数据库
			comment = form.save(commit=False)

			# 将评论和被评论的文章关联起来
			# 因为comment为Comment模型类的实例，则comment有post属性，这里把获取到pk值对应的文章赋给post变量，之后传给comment的post属性
			comment.post = post

			# 最终将评论数据保存进数据库，调用模型实例的save方法
			comment.save()

			# 重定向到post详情页，实际上当redirect函数接收一个模型实例时，他会调用这个模型实例的get_absolute_url
			# 然后重定向到get_absolute_url 方法返回的URL
			return redirect(post)	# redirect即可接受URL又可接受模型实例作为参数，接受实例则该实例必须实现get_absolute_url方法

		else:
			# 检查到数据不合法，将重新渲染详情页，并渲染表单的错误
			# 因此传了三个模板变量给detail.html
			# 分别问文章（Post），评论列表，表单form
			# 这里用到了post.comment_set.all()方法，该用法类似于Post.objects.all()
			# 该方法用于获取这篇文章（Post）下的所有评论
			# 因为Post和Comment是ForeignKey关联的（一对多）
			# 因此使用post.comment_set.all()反向查询全部评论
			comment_list = post.comment_set.all()	# 等价于Comment.objects.filter(post=post)，其中_set属性表示获取类似于objects的模型管理器
													# 因为一个post对应多个comment且Comment与Post关联，则使用post的关联模型类名comment来进行选择评论内容
			context = {'post': post,
						'form':form,
						'comment_list': comment_list
						}
			return render(request, 'blog/detail.html', context=context)

		# 不是post请求，说明用户没有提交数据，重定向到文章详情页
		return redirect(post)

