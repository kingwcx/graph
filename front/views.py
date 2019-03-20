from django.shortcuts import render,redirect,reverse

#数据库
from py2neo import *
#NEOMODEL模型

# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#视图
from django.views import View
#json
import json
#其他视图函数
from administrator.views import *


def get_graph():
	neo4j = Graph(
		host="127.0.0.1",  # neo4j 搭载服务器的ip地址
		http_port=7978,  # neo4j 服务器监听的端口号
		user="neo4j",  # 数据库user name
		password="123456"  # 密码
	)
	return neo4j

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
		search = request.POST.get("search")
		if search != "":
			try:
				neo_graph = get_graph()
				results = neo_graph.run("MATCH (n) WHERE n.name =~ '.*"+ search + ".*'RETURN *,id(n)").data()
				results2 = neo_graph.run("MATCH (n) WHERE n.description =~ '.*"+ search + ".*'RETURN *,id(n)").data()
				ids = []
				for result in results:
					ids.append(result['id(n)'])
				for result in results2:
					ids.append(result['id(n)'])
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
			print(detail)
			return render(request, 'object_detail.html', context={"object": detail,"labels":detail['label']})
		except:
			return HttpResponse("DetailView404")

	def post(self,request,*args,**kwargs):
		try:
			id = request.POST.get('id')
			return redirect(reverse('front:object_detail', kwargs = {"id": id}))
		except:
			return HttpResponse("DetailView404")