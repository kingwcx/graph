from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from .database import *
# 表单验证
from .forms import NodeForm

# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#
import json


"""
 视图
"""
# 管理员主页面
class AdminIndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_home.html')


show = {'': '全部','People': '人物','Work': '作品','Style': '风格','Process': '设计过程'}


# 展示节点node
class AdminShowNodeView(View):
	def get(self, request, *args, **kwargs):
		element = json.dumps(load_graph())
		return render(request, 'admin_nodes.html', context={"labels": show,"element":element})

# 搜索节点node
class AdminSearchNodeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_search.html')


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


"""查找接口"""
#通过id返回节点和周围路径为1的点
class FindByIdInterface(View):
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		#print(id)
		elements = load_search_graph(id)
		current_data = load_search_node(id)
		data = {'current_data':current_data,'elements':elements}
		#print(data)
		return JsonResponse(data)


"""添加关系接口"""

"""修改节点接口"""

"""删除节点接口"""

"""删除关系接口"""
