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
		return render(request, 'index.html')

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
				matcher = NodeMatcher(neo_graph)
				result = matcher.match("Concept", name=search).first()
				print(result)
				result["search_times"] += 1
				neo_graph.push(result)
				# tx.commit()
				return redirect(reverse('front:object_detail')+ "?name=" + result["name"])
			except:
				print("没有找到你要的内容!")
				return redirect(reverse('front:search'))
		else:
			return redirect(reverse('front:search'))

#对象详情页面
class ObjectDetailView(View):
	def get(self,request,*args,**kwargs):
		neo_graph = get_graph()
		#tx = neo_graph.begin()
		matcher = NodeMatcher(neo_graph)
		object=matcher.match("Concept", name=request.GET.get("name")).first()
		object["view_times"] +=1
		neo_graph.push(object)
		#tx.commit()
		return render(request, 'object_detail.html', context={"object": object,"custom":json.loads(object["custom"]),"labels":object.labels})