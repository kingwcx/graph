from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.core.files import  *
# 数据库
from .database import *
# 表单验证
from .forms import NodeForm,RelationshipForm

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
	def post(self, request, *args, **kwargs):
		search_key = request.POST.get('search')
		if search_key != "":
			try:
				ids = search(search_key)
				data = {}
				if ids != []:
					ids = list(set(ids))
					for id in ids:
						result = load_search_node(id)
						data[id] = result['property']['name']
					return render(request, 'admin_search.html', context={'search': search_key,'ids':ids,'data':data})
				else:
					print("没有找到你要的内容!")
					return redirect(reverse('admin:search_node'))
			except:
				print("服务器错误！")
				return redirect(reverse('admin:search_node'))
		else:
			return redirect(reverse('admin:search_node'))


# 标签清单
labels = {'Style': '款式','Pattern': '制版','Technology': '工艺','Design':'服装设计'}
show_labels = {'Design': '服装设计','Style': '款式','Patternmaking': '制版','Technology': '工艺'}

relationships = {'Kind_of': 'Kind_of'}


# ajax返回所需标签
def ajax_lable_list(request):
	return JsonResponse(basic)


# 添加节点页面node
class AdminAddNodeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_node.html', context={"labels": labels})

# 添加关系页面relation
class AdminAddRelationshipView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_relationship.html', context={"relationships": relationships})

# 修改节点页面node
class AdminEditNodeView(View):
	def get(self, request, *args, **kwargs):
		id = request.GET.get('id')
		data = load_search_node(id)
		print(data['property'])
		return render(request, 'admin_edit_node.html',context={'data':data})

# 修改关系页面relationship
class AdminEditRelationshipView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_relationship.html', context={"relationships": relationships})


# 添加知识节点页面node
class AdminAddConceptView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_concept.html', context={"labels": labels})


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
		return render(request, 'admin_add_essential.html', context={"labels": labels})


# 添加设计对象节点页面node
class AdminAddDesignerView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_add_essential.html', context={"labels": labels})


"""
接口
"""

"""添加节点接口"""

# 添加节点 （通用）
class AdminAddNodeInterface(View):
	def post(self, request, *args, **kwargs):
		form = NodeForm(request.POST)
		if form.is_valid():
			description = form.cleaned_data.get('description')
			name = form.cleaned_data.get('name')
			label = form.cleaned_data.get('label')
			data = {'name':name,'description':description}
			add_node(data,label)
			return redirect(reverse('admin:knowledge_graph'))
		else:
			print(form.errors.get_json_data())
			print(form.get_errors())
			try:
				print(form.get_errors()['__all__'])
				name = form.get_errors()['__all__']
			except:
				name = ""

			return render(request, 'admin_add_node.html', context={"labels": labels, "errors": form.get_errors(),
			                                                          "name": name})


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

#通过name返回节点集
class FindByNameInterface(View):
	def post(self, request, *args, **kwargs):
		name = request.POST.get('name')
		nodes = []
		if(name != ""):
			try:
				results = search_property(name,"name")
				for result in results:
					id = result['id(n)']
					name = result['n']['name']
					nodes.append({'id': id, 'name': name})
			except:
				results = {}
				print("非法输入")
		else:
			pass
		data = {'nodes':nodes}
		return JsonResponse(data)

#通过id返回上级节点
class FindUpByIdInterface(View):
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		nodes = load_up_node(id)
		return JsonResponse(nodes)

#通过id返回下级节点
class FindDownByIdInterface(View):
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		nodes = load_down_node(id)
		return JsonResponse(nodes)

#通过id返回同级节点
class FindPeerByIdInterface(View):
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		nodes = load_peer_node(id)
		return JsonResponse(nodes)


"""添加关系接口"""
# 添加关系（通用）
class AdminAddRelationshipInterface(View):
	def post(self, request, *args, **kwargs):
		form = RelationshipForm(request.POST)
		if form.is_valid():
			souname = form.cleaned_data.get('souname')
			dstname = form.cleaned_data.get('dstname')
			souid = form.cleaned_data.get('souid')
			dstid = form.cleaned_data.get('dstid')
			relationship = form.cleaned_data.get('relationship')
			add_relationship(souid,dstid,relationship)
			return HttpResponse(200)
		else:
			print(form.errors.get_json_data())
			print(form.get_errors())
			return HttpResponse(404)

"""上传图片"""
class AdminUploadImageInterface(View):
	def post(self, request, *args, **kwargs):
		id = kwargs['id']
		img = request.FILES.get('image')
		url = upload_img(id,img)
		return JsonResponse({'url':url})

"""修改节点接口"""
class AdminEditNodeInterface(View):
	def post(self, request, *args, **kwargs):
		data = {}
		id = request.POST.get('id')
		name = request.POST.get('name')
		description = request.POST.get('description')
		if(name!=''):
			edit_node(id,"name",name)
		else:
			print("不修改name")
		if (description != ''):
			edit_node(id, "description", description)
		else:
			print("不修改description")

		return JsonResponse({})

"""删除节点接口"""

"""删除关系接口"""
