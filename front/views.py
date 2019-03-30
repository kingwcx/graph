from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from administrator.database import *
#NEOMODEL模型

# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#视图
from django.views import View
# 用户与权限
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
#json
import json


"""
 视图
"""

#首页
class IndexView(View):
	#new = Basic(name="色彩").save()
	def get(self,request,*args,**kwargs):
		element = json.dumps(load_graph())
		return render(request, 'index.html',context={'element':element})

#搜索页面
class SearchView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'search.html')

#search操作
class SearchActionView(View):
	def post(self,request,*args,**kwargs):
		search_key = request.POST.get("search")
		if search_key != "":
			try:
				ids = search(search_key)
				data = {}
				if ids != []:
					ids = list(set(ids))
					for id in ids:
						result = load_search_node(id)
						data[id] = result['property']['name']
					return render(request, 'result.html',context={'ids':ids,'data':data})
				else:
					print("没有找到你要的内容!")
					return render(request, 'result_error.html',context={'error':"没有找到你要的内容!",'search':search})
			except:
				print("服务器错误！")
				return render(request, 'result_error.html')
		else:
			return redirect(reverse('front:search'))

#search结果
class SearchResultView(View):
	def get(self, request, *args, **kwargs):
		print(request.POST.get('id'))
		return render(request, 'result.html')

#search error结果
class SearchResultErrorView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'result_error.html')


class ExampleList(ListView):
	def get(self, request, *args, **kwargs):
		LIST = get_nodes_bylabels("Example")
		paginator = Paginator(LIST, 20 )
		pages = paginator.page_range  # 生成所有页码
		pages_num = paginator.num_pages  # 总也数

		page = request.GET.get('page')  # 当前页面
		contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页
		return render(request, 'example_list.html',
					  {'contacts': contacts, 'pages': pages, 'pagenums': pages_num})

#对象详情页面
class ObjectDetailView(View):
	def get(self,request,*args,**kwargs):
		try:
			id = kwargs['id']
			all_imgs = get_all_down_image(id)
			detail = load_search_node(id)
			up_nodes = load_up_node(id,'Kind_of')
			up_nodes2 = load_up_node(id, 'Attribute_of')
			down_nodes = load_down_node(id)
			peer_nodes = load_peer_node(id)
			#add_node_number(id,'search_times',1)
			other_nodes = {
				'up_nodes':up_nodes,
				'up_nodes2':up_nodes2,
				'down_nodes':down_nodes,
				'peer_nodes':peer_nodes,
			}
			#print(detail['property']['img_url'])
			return render(request, 'object_detail.html',
						  context={"object": detail,"labels":detail['label'],'other_nodes':other_nodes,'all_imgs':all_imgs})
		except:
			return HttpResponse("DetailView404")

	def post(self,request,*args,**kwargs):
		try:
			id = request.POST.get('id')
			return redirect(reverse('front:object_detail', kwargs = {"id": id}))
		except:
			return HttpResponse("DetailView404")