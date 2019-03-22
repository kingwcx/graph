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

#对象详情页面
class ObjectDetailView(View):
	def get(self,request,*args,**kwargs):
		try:
			id = kwargs['id']
			detail = load_search_node(id)
			up_nodes = load_up_node(id)
			down_nodes = load_down_node(id)
			peer_nodes = load_peer_node(id)
			other_nodes = {
				'up_nodes':up_nodes,
				'down_nodes':down_nodes,
				'peer_nodes':peer_nodes,
			}
			print(other_nodes)
			return render(request, 'object_detail.html', context={"object": detail,"labels":detail['label'],'other_nodes':other_nodes})
		except:
			return HttpResponse("DetailView404")

	def post(self,request,*args,**kwargs):
		try:
			id = request.POST.get('id')
			return redirect(reverse('front:object_detail', kwargs = {"id": id}))
		except:
			return HttpResponse("DetailView404")