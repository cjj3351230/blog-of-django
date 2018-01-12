# 该文件用于告诉django，haystack使用那些数据建立索引以及如何存放索引
# 这里对blog应用下的数据进行全文检索，因此在blog应用下建立一个search_indexes.py文件
# 这是django haystack的规定，要想对某个app下的数据进行全文检索，就要在该app下创建一个search_indexes.py文件，然后创建一个XXIndex类
# XX为含有被检索数据的模型，如这里的Post，并需要继承SearchIndex和Indexable

from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
	# 每个索引里面必须有且只能有一个字段为document=True，这代表django haystack和搜索引擎将使用此字段内容作为索引进行检索
	# 如果使用一个字段设置了document=True，则一般约定此字段名为text，这是在SearchIndex类里面一惯的命名，防止后台混乱
	# haystack提供了use_template=True在text字段中，这样允许使用数据模板来建立搜索引擎索引的文件
	text = indexes.CharField(document=True, use_template=True)

	def get_model(self):
		return Post

	def index_queryset(self, using=None):
		return self.get_model().objects.all()