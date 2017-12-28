# 表单是用来收集并向服务器提交用户输入的数据的
from django import forms
# 使用表单功能首先需要导入forms模块，django的表单类必须继承自forms.Form类或者forms.ModelForm类
from .models import Comment

class CommentForm(forms.ModelForm):		# 如果表单对应有一个数据库模型，则使用ModelForm类会简单很多
	class Meta:
		model = Comment 	# 表明这个表单对应的数据库模型是Comment类
		fields = ['name', 'email', 'url', 'text']	# 指定了表单需要显示的字段，如name, email, url, text