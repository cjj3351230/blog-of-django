from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm # 评论部分。从comments文件的forms.py文件中引入CommentForm类
import markdown
from django.views.generic import ListView, DetailView 	# 类视图需要引入
# 下面两个引入用于美化目录锚
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# 下面这个函数用于搜索
from django.db.models import Q

# 将index视图函数改写为类视图
class IndexView(ListView):
	model = Post 	# 将model指定为Post,告诉django要获取的模型为Post，即获取Post模型的全部内容
	template_name = 'blog/index.html'	# 指定这个视图渲染的模板
	context_object_name = 'post_list'	# 将获得的模型数据列表保存到post_list里传递给blog/index.html模板文件

	# 制定paginate_by属性后开启分页功能，其值代表没营业包含多少篇文章
	# ListView类视图已经写好分页逻辑，即为paginate_by属性
	paginate_by = 3

	def get_context_data(self, **kwargs):
		'''
		在视图函数中将模板变量传递给模板是通过给render函数的context参数传递一个字典实现的
		例如render(request, 'blog/index.html', context={'post_list': post_list})
		在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的，所以覆写该方法一遍能够自己插入一些自定义的模板变量进去
		'''

		# 首先获得父类生成的传递给模板的字典
		context = super().get_context_data(**kwargs)

		# 父类生成的字典中已有paginator、page_obj、is_paginated这三个模板变量
		# paginator是Poginator的一个实例，page_obj是Page的一个实例,is_paginated是一个布尔变量，用于指示是否已分页
		# 例如如果规定每页10个数据，而本身只有5个数据，则不用分页，此时is_paginated=False
		# 由于context是一个字典，所以调用get方法从中取出某个键对应的值
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		# 调用自己写的pagination_data方法获得显示分页导航条需要的数据，方法在下方
		pagination_data = self.pagination_data(paginator, page, is_paginated)

		# 将分页导航条的模板变量更新到context中，注意pagination_data方法返回的也是一个字典
		context.update(pagination_data)

		# 将更新后的context返回，以便ListView使用这个字典中的模板变量去渲染模板
		# 注意此时context字典中已有了显示分页导航条所需的数据
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			# 如果没有分页，则无需显示分页导航条，因此返回一个空字典
			return {}

		# 当前页左边连续的页码号，初始值为空
		left = []

		# 当前页右边连续的页码号，初始值为空
		right = []

		# 标识第一页页码后是否需要显示省略号
		left_has_more = False

		# 标识最后一页页码前是否需要显示省略号
		right_has_more = False

		# 标识是否需要显示第一页的页码号
		# 因为如果当前页左边的连续号码中已含有第一页的页码号，此时就无需再显示第一页
		# 其他情况下第一页页码始终显示
		# 初始值为False
		first = False

		# 标示是否需要显示最后一页页码号
		# 需要此指示变量的理由和上面相同
		last = False

		# 获得用户当前请求的页码号
		page_number = page.number

		# 获得分页后的总页数
		total_pages = paginator.num_pages

		# 获得整个分页页码列表，比如分四爷，则为[1,2,3,4]
		page_range = paginator.page_range

		if page_number == 1:
			# 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此left=[](已默认为空)
			# 此时只要获取当前页右边的连续页码号
			right = page_range[page_number:page_number + 2]

			# 如果最右边的页码号比最后一页的页码号减1还小,说明有其他页码，因此需要显示省略号，通过right_has_more来指示
			if right[-1] < total_pages - 1:
				right_has_more = True

			# 如果最右边的页码号比最后一页的页码号校，说明当前页右边的连续号中不包含最后一页的页码
			# 所以需要显示最后一页的页码号，通过last来指示
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			# 如果用户请求的是最后一页的数据，则right=[](默认为空)
			# 此时只要获取当前页左边的连续号码，比如分页页码列表为[1,2,3,4],则left=[2,3]
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			# 如果最左边的页码号比第二页页码号还大，说明最左边页码号和第一页中还有页码，因此需要显示省略号，通过left_has_more来指示
			if left[0] > 2:
				left_has_more = True

			# 如果最左边页码号比第一页大，说明需要显示第一页页码，通过first来指示
			if left[0] > 1:
				fitst = True

		else: 
			# 用户请求的既不是最后一页也不是第一页，则需要获得当前页左右两边的连续页号码，这里只获取了当前页码前后连续两个页码，也可以更改
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
			right = page_range[page_number: page_number + 2]

			# 是否需要显示最后一页和最后一页前的省略号
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			# 是否需要显示第一页和省略号
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}
		return data
'''
# Create your views here.
def index(request):
	# all方法返回一个QuerySet（可以理解为类似于列表的数据结构）；之后调用order_by方法对queryset进行排序，排序依据的字段是created_time；"-"表示逆序，不加则为正序
	post_list = Post.objects.all()
	return render(request, 'blog/index.html', context={
			'post_list':post_list
		})
'''

'''
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# 根据从URL捕获的文章id(即pk)获取数据库中文章id为该值的记录，然后传递给模板
	# get_object_or_404方法用于，当传入的pk对应的Post在数据库存在，则返回对应的post，否则会返回404错误
	
	# 阅读量函数调用
	post.increase_views()

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
	'''

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self, request, *args, **kwargs):
		# 覆写get方法的目的是因为每当文章被访问一次，就得将文章阅读量+1，get方法返回的是一个HttpResponse实例
		# 之所以需要先调用父类的get方法，是因为只有当get方法被调用后，才有self.object属性，其值为Post模型实例，即被访问的文章post
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		# 这里get_object、get_context_data最终在get方法中被调用，即父类的get方法中，最终传递给浏览器的http响应就是get方法返回的httpresponse对象

		# 将文章阅读量+1
		# 注意 self.object 的值就是被访问的文章post
		self.object.increase_views()

		# 视图必须返回一个HttpResponse对象
		return response

	def get_object(self, queryset=None):
		# 覆写get_object方法的目的是因为需要对post的body值进行markdown渲染
		post = super(PostDetailView, self).get_object(queryset=None)
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',	# 代码高亮拓展
			# 这里toc拓展不再是字符串xxx.toc，而是TocExtension实例，在实例化时其slugify参数可以接收一个函数作为参数，这个函数用于处理标题的锚点值
			# 由于markdown内置的处理方法不能处理中文标题，因此使用django.utils.text中的slugify方法处理中文
			TocExtension(slugify=slugify),
			# 美化前代码为'markdown.extensions.toc',	# 自动生成目录的拓展
		])
		post.body = md.convert(post.body)
		post.toc = md.toc
		return post

	def get_context_data(self, **kwargs):
		# 覆写get_context_data的目的是因为除了将post传递给模板外（DetailView自动完成）还要吧评论表单、post下的评论列表传递给模板
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list
			})
		return context

'''
def archives(request, year, month):
# 归档视图函数
	post_list = Post.objects.filter(created_time__year=year,	# Python中类实例调用属性的方法通常是created_time.year，但这里作为函数的参数列表
									created_time__month=month 	# 所以将点替换成两个下划线
									).order_by('-created_time')
	return render(request,'blog/index.html', context={'post_list':post_list})
	'''

# 由于models中没有Archives模型（即表格），所以不需要使用get_object_or_404方法
class ArchivesView(IndexView):
	def get_queryset(self):
		return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))

class TagsView(IndexView):
	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagsView, self).get_queryset().filter(tags=tag)
# 将category视图函数改写为类视图
# 由于这里CategoryView和IndexView类中属性值相同，因此可以直接继承IndexView类
'''
class CategoryView(IndexView):
	而不需要给属性值赋值
'''
class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	# 这里覆写父类ListView的get)queryset方法，原默认为获取指定模型的全部列表数据，这里为获取指定分类下的文章列表数据
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))	# 在类视图中，从URL捕获命名组参数值保存在实例的kwargs属性（一个字典）里，
																		# 非命名组参数保存在实例的args属性（一个列表）里
		return super(CategoryView, self).get_queryset().filter(category=cate)	# get_queryset()为父类的方法，用于获得全部文章列表，之后筛选该分类下的全部文章并返回

'''
def category(request, pk):
# 需要导入Category类
	cate = get_object_or_404(Category,pk=pk)
	# 首先根据pk值（即分类的id值）来从数据库中获取该分类并赋值给cate变量。
	post_list = Post.objects.filter(category=cate).order_by('-created_time')
	# 通过filter过滤出分类为所获取分类的全部文章并按创建时间倒序排列
	return render(request, 'blog/index.html', context={'post_list':post_list})
'''

def search(request):
	# 获取到用户提交的搜索关键词
	# 用户通过表单get方法提交的数据Django为我们保存在request.GET里，类似于Python字典的对象
	# 因此使用get方法从字典里驱逐键q对应的值，即搜索关键词
	# 之所以键叫q，是因为表单中搜索框input的name属性值是q，如果修改了name属性的值（即base.html中的input标签的name属性），键名也要改
	q = request.GET.get('q')
	error_msg = ''

	# 如果用户没有输入关键词而提交表单，则在模板中渲染一个错误提示信息
	if not q:
		error_msg = '请输入关键词'
		return render(request, 'blog/index.html', {'error_msg': error_msg})

	# 如果输入信息，则通过filter方法从数据库中过滤出符合条件的所有文章
	# 两个参数分别表示标题和正文中包含q的文章，i表示不区分大小写
	# icontains是查询表达式(Field lookups)，用法是在需要筛选的属性后面跟上两个下划线
	# 这里Q对象用于包装查询表达式，用于提供复杂的查询逻辑，|符号表示或逻辑
	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return render(request, 'blog/index.html', {'error_msg': error_msg,
												'post_list': post_list})