from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from administrator.database import *
from administrator import database2
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
from ast import literal_eval
#近义词工具包
import synonyms


"""
 视图
"""

#首页
class IndexView(View):
	#new = Basic(name="色彩").save()
	def get(self,request,*args,**kwargs):
		element = json.dumps(load_graph())
		node = search_property("服装款式设计", 'name')
		results = load_down_node(node[0]['id(n)'], 'Instance_of')
		LIST = []
		for result in results:
			object = load_search_node(result['data']['id'])
			object['property']['images'] = literal_eval(object['property']['images'])
			LIST.append(object)
		return render(request, 'index/index.html', context={'element':element,'style_examples':LIST})

#导航
class GuideView(View):
	#new = Basic(name="色彩").save()
	def get(self,request,*args,**kwargs):
		element = json.dumps(load_graph())
		return render(request, 'index/guide.html', context={'element':element})



#概念图谱
class ConceptView(View):
	#new = Basic(name="色彩").save()
	def get(self,request,*args,**kwargs):
		element = json.dumps(load_graph())
		return render(request, 'index/shceme.html', context={'element':element})

#全部节点
class GraphView(View):
	#new = Basic(name="色彩").save()
	def get(self,request,*args,**kwargs):
		return render(request, 'index/graph.html')

#搜索页面
class SearchView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'index/search.html')

#search操作
class SearchActionView(View):
	def get(self,request,*args,**kwargs):
		search_key = request.GET.get("search")
		if search_key != "":
			try:
				ids = []
				data = {}
				all_keys_in = synonyms.seg(search_key)
				ids.extend(search(search_key))

				#print(all_keys)
				all_keys = []
				nearby_keys = []
				nearby_keys_in = [[],[]]
				i = 0
				for key_s in all_keys_in[1]:
					if 'n' in key_s:
						#print(all_keys[0][i])
						all_keys.append(all_keys_in[0][i])
						nearby = synonyms.nearby(all_keys_in[0][i])
						nearby_keys_in[0].extend(nearby[0])
						nearby_keys_in[1].extend(nearby[1])
						ids.extend(search(all_keys_in[0][i]))
					i+=1

				i = 0
				print(nearby_keys_in)
				for key_s in nearby_keys_in[1]:
					if key_s > 0.75 and key_s != 1.0:
						nearby_keys.append(nearby_keys_in[0][i])
						ids.extend(search(nearby_keys_in[0][i]))
						#print(nearby_keys_in[0][i])
					i += 1

				#加载详细信息
				if ids != []:
					for id in ids:
						result = load_search_node(id)
						data[id] = result['property']['name']

					#all_keys.append(search_key)
					return render(request, 'index/result.html',
								  context={'ids':ids, 'data':data, 'keys':all_keys,'nearby_keys':nearby_keys})
				else:
					print("没有找到你要的内容!")
					return render(request, 'index/result_error.html', context={'error': "没有找到你要的内容!", 'search':search})
			except Exception as e:
				print(e)
				print("服务器错误！")
				return render(request, 'index/result_error.html')
		else:
			return redirect(reverse('front:search'))

	def post(self,request,*args,**kwargs):
		search_key = request.POST.get("search")
		if search_key != "":
			try:
				ids = []
				data = {}
				all_keys_in = synonyms.seg(search_key)
				ids.extend(search(search_key))

				#print(all_keys)
				all_keys = []
				nearby_keys = []
				nearby_keys_in = [[],[]]
				i = 0
				for key_s in all_keys_in[1]:
					if 'n' in key_s:
						#print(all_keys[0][i])
						all_keys.append(all_keys_in[0][i])
						nearby = synonyms.nearby(all_keys_in[0][i])
						nearby_keys_in[0].extend(nearby[0])
						nearby_keys_in[1].extend(nearby[1])
						ids.extend(search(all_keys_in[0][i]))
					i+=1

				i = 0
				print(nearby_keys_in)
				for key_s in nearby_keys_in[1]:
					if key_s > 0.75 and key_s != 1.0:
						nearby_keys.append(nearby_keys_in[0][i])
						ids.extend(search(nearby_keys_in[0][i]))
						#print(nearby_keys_in[0][i])
					i += 1

				#加载详细信息
				if ids != []:
					for id in ids:
						result = load_search_node(id)
						data[id] = result['property']['name']

					if nearby_keys == []:
						nearby_keys = None

					#all_keys.append(search_key)
					return render(request, 'index/result.html',
								  context={'ids':ids, 'data':data, 'keys':all_keys,'nearby_keys':nearby_keys})
				else:
					print("没有找到你要的内容!")
					return render(request, 'index/result_error.html', context={'error': "没有找到你要的内容!", 'search':search})
			except Exception as e:
				print(e)
				print("服务器错误！")
				return render(request, 'index/result_error.html')
		else:
			return redirect(reverse('front:search'))

#search结果
class SearchResultView(View):
	def get(self, request, *args, **kwargs):
		print(request.POST.get('id'))
		return render(request, 'index/result.html')

#search error结果
class SearchResultErrorView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'index/result_error.html')


class ExampleList(ListView):
	def get(self, request, *args, **kwargs):
		example = "服装款式设计"
		node = search_property(example, 'name')
		results = load_down_node(node[0]['id(n)'], 'Instance_of')
		LIST =[]
		for result in results:
			object = load_search_node(result['data']['id'])
			print(object)
			object['property']['images'] = literal_eval(object['property']['images'])
			LIST.append(object)
		paginator = Paginator(LIST, 20 )
		pages = paginator.page_range  # 生成所有页码
		pages_num = paginator.num_pages  # 总也数

		page = request.GET.get('page')  # 当前页面
		contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页
		return render(request, 'index/example_list.html',
					  {'contacts': contacts, 'pages': pages, 'pagenums': pages_num})

#知识详情页面
class ObjectDetailView(View):
	def get(self,request,*args,**kwargs):
		#try:
			id = kwargs['id']

			all_imgs = get_all_down_image(id)
			detail = load_search_node(id)

			if 'Example' in detail['label']:
				return redirect(reverse('front:example_detail', kwargs={"id": id}))
			else:
				pass

			up_nodes_part = load_up_node(id,'Part_of')
			down_nodes_part = load_down_node(id, 'Part_of')
			up_nodes_kind = load_up_node(id, 'Kind_of')
			down_nodes_kind = load_down_node(id, 'Kind_of')
			up_nodes_instance = load_up_node(id, 'Instance_of')
			down_nodes_instance = load_down_node(id, 'Instance_of')

			#其他数据库节点
			down_nodes_out = []
			down_nodes_out.extend(load_down_node(id, 'DesignTrend'))
			down_nodes_out.extend(load_down_node(id, 'FabricDesign'))

			#同级节点
			peer_nodes = load_peer_node(id)

			other_nodes = {
				'up_nodes_part':up_nodes_part,
				'down_nodes_part':down_nodes_part,
				'up_nodes_kind':up_nodes_kind,
				'down_nodes_kind':down_nodes_kind,
				'up_nodes_instance':up_nodes_instance,
				'down_nodes_instance':down_nodes_instance,
				'peer_nodes':peer_nodes,
				'down_nodes_out':down_nodes_out,
			}
			#print(detail['property']['img_url'])
			return render(request, 'index/object_detail.html',
						  context={"object": detail,"labels":detail['label'],'other_nodes':other_nodes,'all_imgs':all_imgs})
		#except Exception as e:
			print(e)
			return HttpResponse("DetailView404")

	def post(self,request,*args,**kwargs):
		try:
			id = request.POST.get('id')
			detail = load_search_node(id)
			if 'Example' in detail['label']:
				return redirect(reverse('front:example_detail', kwargs = {"id": id}))
			else:
				return redirect(reverse('front:object_detail', kwargs={"id": id}))
		except:
			return HttpResponse("DetailView404")

#实例详情页面
class ExampleDetailView(View):
	def get(self,request,*args,**kwargs):
		try:
			id = kwargs['id']
			all_imgs = get_all_down_image(id)
			detail = load_search_node(id)

			up_nodes_part = load_up_node(id, 'Part_of')
			down_nodes_part = load_down_node(id, 'Part_of')
			up_nodes_kind = load_up_node(id, 'Kind_of')
			down_nodes_kind = load_down_node(id, 'Kind_of')
			up_nodes_instance = load_up_node(id, 'Instance_of')
			down_nodes_instance = load_down_node(id, 'Instance_of')


			up_nodes = load_up_node(id,'Kind_of')
			up_nodes2 = load_up_node(id, 'Attribute_of')
			down_nodes = load_down_node(id)
			peer_nodes = load_peer_node(id)
			#add_node_number(id,'search_times',1)
			other_nodes = {
				'up_nodes_part': up_nodes_part,
				'down_nodes_part': down_nodes_part,
				'up_nodes_kind': up_nodes_kind,
				'down_nodes_kind': down_nodes_kind,
				'up_nodes_instance': up_nodes_instance,
				'down_nodes_instance': down_nodes_instance,
				'up_nodes':up_nodes,
				'up_nodes2':up_nodes2,
				'down_nodes':down_nodes,
				'peer_nodes':peer_nodes,
			}
			#print(detail['property']['img_url'])
			return render(request, 'index/object_example.html',
                          context={"object": detail,"labels":detail['label'],'other_nodes':other_nodes,'all_imgs':all_imgs})
		except Exception as e:
			print(e)
			return HttpResponse("DetailView404")

	def post(self,request,*args,**kwargs):
		try:
			id = request.POST.get('id')
			return redirect(reverse('front:example_detail', kwargs = {"id": id}))
		except Exception as e:
			print(e)
			return HttpResponse("DetailView404")

