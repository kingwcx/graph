from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse,HttpResponse
#数据库
from py2neo import Node,Relationship,Graph
#NEOMODEL模型
#表单验证
from .forms import NodeForm

# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#
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
#管理员主页面
class AdminIndexView(View):
	def get(self, request, *args, **kwargs):

		return render(request, 'admin_home.html')

#展示节点node
class AdminShowNodeView(View):
	def get(self, request, *args, **kwargs):
		return render( request, 'admin_nodes.html')

#标签清单
labels = { 'Sytle':'风格','Basic':'概念','tool':'工具','ColorMatch':'配色方案','Dresser':'穿衣者','Designer':'设计者'}
basic = {'basic':'一般概念','element':'造型要素','paint':'绘画技巧'}
#ajax返回所需标签
def ajax_lable_list(request):
	return JsonResponse(basic)

#添加节点页面node
class AdminAddNodeView(View):
	def get(self, request, *args, **kwargs):
		return render( request, 'admin_add_node.html',context={"labels": labels})

"""
接口"""

class AdminAddNode(View):
	def post(self, request, *args, **kwargs):
		form = NodeForm(request.POST)
		if form.is_valid():
			introduction = form.cleaned_data.get('introduction')
			name = form.cleaned_data.get('name')
			label = form.cleaned_data.get('label')
			#english_name = form.cleaned_data.get('english_name')
			neo_graph = get_graph()
			tx = neo_graph.begin()
			a = Node(label, name=name,view_times=0,search_times=0,introduction=introduction)
			tx.create(a)
			tx.commit()
			return redirect(reverse('admin:knowledge_graph'))
		else:
			print(form.errors)
			html = form.errors
			print(html)
			return HttpResponse(html)