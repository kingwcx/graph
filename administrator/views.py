from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from py2neo import *
# NEOMODEL模型
from .models import *
# 表单验证
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


# 管理员主页面
class AdminIndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_home.html')


show = {'': '全部','People': '人物','Work': '作品','Style': '风格','Process': '设计过程'}


def build_node(nodeRecord):
	data = { "id":str(nodeRecord['id(n)']),
	         "name": str(nodeRecord['n']['name']),
	         "label": next(iter(nodeRecord['n'].labels))}

	return {"data": data}


def build_edge(relationRecord):
	data = {"source": str(relationRecord['id(m)']),
	        "target": str(relationRecord['id(n)']),
	        "relationship": relationRecord['Type(r)']}

	return {"data": data}

def build_nodes(nodes):
	result =[]
	for node in nodes:
		new = build_node(node)
		result.append(new)
	return result

def build_edges(edges):
	result =[]
	for edge in edges:
		new = build_edge(edge)
		result.append(new)
	return result

def load_graph(request):
	print(request)
	neo_graph = get_graph()
	result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
	result_edges = neo_graph.run('MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)').data()
	nodes = build_nodes(result_nodes)
	edges = build_edges(result_edges)
	print(nodes)
	return JsonResponse({"nodes": nodes, "edges": edges})

def load_search_graph(request):
	pass


# 展示节点node
class AdminShowNodeView(View):
	def get(self, request, *args, **kwargs):
		neo_graph = get_graph()
		result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
		result_edges = neo_graph.run('MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)').data()
		nodes = build_nodes(result_nodes)
		edges = build_edges(result_edges)
		element = json.dumps({"nodes": nodes, "edges": edges})
		return render(request, 'admin_nodes.html', context={"labels": show,"element":element})


# 标签清单
labels = {'People': '人物','Work': '作品','Style': '风格','Process': '设计过程'}
label_base = "Concept"
concepts = {'Style': '风格', 'Basic': '概念', 'tool': '工具'}
essemtial_labels = {'Color': '色彩', 'People': '人群', 'Mould': '造型', 'Type': '分类', 'Fabrictype': '面料类型'}
designer_labels = {'Brand': '设计品牌', 'Designer': '设计师'}


# ajax返回所需标签
def ajax_lable_list(request):
	return JsonResponse(basic)


# 添加节点页面node
class AdminAddNodeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_node.html', context={"labels": labels})


# 添加知识节点页面node
class AdminAddConceptView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_concept.html', context={"labels": concepts})


# 添加成衣节点页面node
class AdminAddExampleView(View):
	def get(self, request, *args, **kwargs):
		neo_graph = get_graph()
		# tx = neo_graph.begin()
		matcher = NodeMatcher(neo_graph)
		# style = matcher.match("style").where("_.name<>""")
		style = neo_graph.run("MATCH (a:Style) RETURN a.name AS name").data()
		type = neo_graph.run("MATCH (a:Type) RETURN a.name AS name").data()
		color = neo_graph.run("MATCH (a:Color) RETURN a.name AS name").data()
		people = neo_graph.run("MATCH (a:People) RETURN a.name AS name").data()
		mould = neo_graph.run("MATCH (a:Mould) RETURN a.name AS name").data()
		fabrictype = neo_graph.run("MATCH (a:Fabrictype) RETURN a.name AS name").data()
		brand = neo_graph.run("MATCH (a:Brand) RETURN a.name AS name").data()
		designer = neo_graph.run("MATCH (a:Designer) RETURN a.name AS name").data()
		select = {'style': style, 'color': color, 'people': people, 'mould': mould, 'fabrictype': fabrictype,
		          'brand': brand,
		          'designer': designer, 'type': type}
		return render(request, 'admin_add_example.html', context={'select': select})


# 添加成衣要素节点页面node
class AdminAddEssentialView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_essential.html', context={"labels": essemtial_labels})


# 添加设计对象节点页面node
class AdminAddDesignerView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_essential.html', context={"labels": designer_labels})


"""
接口
"""

"""添加节点接口"""


# 添加节点 （通用）
class AdminAddNode(View):
	def post(self, request, *args, **kwargs):
		form = NodeForm(request.POST)
		if form.is_valid():
			introduction = form.cleaned_data.get('introduction')
			name = form.cleaned_data.get('name')
			label = form.cleaned_data.get('label')
			# english_name = form.cleaned_data.get('english_name')
			neo_graph = get_graph()
			tx = neo_graph.begin()
			if label in concepts:
				a = Node(label_base, label, name=name, view_times=0, search_times=0, introduction=introduction)
			else:
				a = Node(label, name=name, view_times=0, search_times=0, introduction=introduction)
			tx.create(a)
			tx.commit()
			return redirect(reverse('admin:knowledge_graph'))
		else:
			print(form.errors.get_json_data())
			print(form.get_errors())
			try:
				print(form.get_errors()['__all__'])
				name = form.get_errors()['__all__']
			except:
				name = ""

			return render(request, 'admin_add_concept.html', context={"labels": concepts, "errors": form.get_errors(),
			                                                          "name": name})


# 添加服装知识：风格，工具，基础概念
class AdminAddConcept(View):
	def post(self, request, *args, **kwargs):
		# form = NodeForm(request.POST)
		# if form.is_valid():
		# 	introduction = form.cleaned_data.get('introduction')
		# 	name = form.cleaned_data.get('name')
		# 	label = form.cleaned_data.get('label')
		# 	neo_graph = get_graph()
		# 	tx = neo_graph.begin()
		# 	new = Sytle()
		# 	new.name = name
		# 	new.introduction = introduction
		# 	neo_graph.push(new)
		# 	#tx.commit()
		# 	return redirect(reverse('admin:knowledge_graph'))
		form = NodeForm(request.POST)
		if form.is_valid():
			introduction = form.cleaned_data.get('introduction')
			name = form.cleaned_data.get('name')
			label = form.cleaned_data.get('label')
			# english_name = form.cleaned_data.get('english_name')
			neo_graph = get_graph()
			tx = neo_graph.begin()
			a = Node(label_base, label, name=name, view_times=0, search_times=0, introduction=introduction)
			tx.create(a)
			tx.commit()
			return redirect(reverse('admin:knowledge_graph'))
		else:
			print(form.errors.get_json_data())
			print(form.get_errors())

			try:
				print(form.get_errors()['__all__'])
				name = form.get_errors()['__all__']
			except:
				name = ""

			return render(request, 'admin_add_concept.html', context={"labels": concepts, "errors": form.get_errors(),
			                                                          "name": name})


# 添加成衣示例
class AdminAddExample(View):
	def post(self, request, *args, **kwargs):
		# neo_graph = get_graph()
		# tx = neo_graph.begin()
		# matcher = NodeMatcher(neo_graph)
		# example = matcher.match("Example", name="黑色男装夹克").first()
		# type = matcher.match("Fabrictype", name="柔软型").first()
		# color = matcher.match("Color", name="黑色").first()
		#
		# et = Relationship(example, "use", type)
		# ec = Relationship(example, "mix", color)
		# tx.create(ec)
		# tx.create(et)
		# tx.commit()
		return redirect(reverse('admin:add_example_view'))


# 添加设计师
class AdminAddDesigner(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加品牌
class AdminAddBrand(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加造型
class AdminAddMould(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加造型
class AdminAddColor(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加类别
class AdminAddType(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加面料类型
class AdminAddFabrictype(View):
	def post(self, request, *args, **kwargs):
		pass


# 添加人群
class AdminAddPeople(View):
	def post(self, request, *args, **kwargs):
		pass


"""查找接口"""


class Find(View):
	def get(self, request, *args, **kwargs):
		neo_graph = get_graph()
		# tx = neo_graph.begin()
		# result = Style.match(neo_graph)
		matcher = NodeMatcher(neo_graph)
		# result = neo_graph.run("MATCH (a) RETURN a.name").data()
		result = matcher.match("Example")
		print(result)
		# tx.commit()
		return HttpResponse(200)


"""添加关系接口"""

"""修改节点接口"""

"""删除节点接口"""

"""删除关系接口"""
