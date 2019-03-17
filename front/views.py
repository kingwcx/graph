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
		neo_graph = get_graph()
		result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
		result_edges = neo_graph.run('MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)').data()
		nodes = build_nodes(result_nodes)
		edges = build_edges(result_edges)
		element = json.dumps({"nodes": nodes, "edges": edges})
		print(element)
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
				# tx = neo_graph.begin()
				result = neo_graph.run("MATCH (n) WHERE n.name = '"+ search + "'RETURN *,id(n)").data()
				print(result)
				matcher = NodeMatcher(neo_graph)
				result_edit = matcher.match(name=search).first()
				result_edit["search_times"] += 1
				neo_graph.push(result_edit)
				# tx.commit()
				return redirect(reverse('front:search_result')+ "?name=" + result["n.name"])
			except:
				print("没有找到你要的内容!")
				return redirect(reverse('front:search'))
		else:
			return redirect(reverse('front:search'))

#search结果
class SearchResultView(View):
	def post(self, request, *args, **kwargs):
		print(request.POST.get('id'))
		return render(request, 'result.html')

#search error结果
class SearchResultErrorView(View):
	def post(self, request, *args, **kwargs):
		print(request.POST.get('id'))
		return render(request, 'result.html')

#对象详情页面
class ObjectDetailView(View):
	def get(self,request,*args,**kwargs):
		neo_graph = get_graph()
		#tx = neo_graph.begin()
		matcher = NodeMatcher(neo_graph)
		object=matcher.match( name=request.GET.get("name")).first()
		object["view_times"] +=1
		neo_graph.push(object)
		#tx.commit()
		return render(request, 'object_detail.html', context={"object": object,"labels":object.labels})