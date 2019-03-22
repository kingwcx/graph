# 数据库neo4j
from py2neo import *
# NEOMODEL模型
from .models import *
import json

#neo4j链接
def get_graph():
	neo4j = Graph(
		host="127.0.0.1",  # neo4j 搭载服务器的ip地址
		http_port=7978,  # neo4j 服务器监听的端口号
		user="neo4j",  # 数据库user name
		password="123456"  # 密码
	)
	return neo4j

#OGM
class Design(GraphObject):
	name = Property()
	description = Property()
	view_times = Property(0)
	search_times = Property(0)

class Style(GraphObject):
	name = Property()
	description = Property()
	view_times = Property(0)
	search_times = Property(0)

class Pattern(GraphObject):
	name = Property()
	description = Property()
	view_times = Property(0)
	search_times = Property(0)

class Technology(GraphObject):
	name = Property()
	description = Property()
	view_times = Property(0)
	search_times = Property(0)

"""函数"""
#处理返回的节点和边的数据
def build_node(nodeRecord,node_str):
	data = { "id":str(nodeRecord['id('+node_str+')']),
	         "name": str(nodeRecord[node_str]['name']),
	         "label": next(iter(nodeRecord[node_str].labels))}

	return {"data": data}
#处理返回的节点和边的数据
def build_edge(relationRecord):
	data = {"source": str(relationRecord['id(m)']),
	        "target": str(relationRecord['id(n)']),
	        "relationship": relationRecord['Type(r)']}

	return {"data": data}
#处理返回的节点和边的数据
def build_nodes(nodes,node_str):
	result =[]
	for node in nodes:
		new = build_node(node,node_str)
		result.append(new)
	return result

#处理返回的节点和边的数据
def build_edges(edges):
	result =[]
	for edge in edges:
		new = build_edge(edge)
		result.append(new)
	return result

#加载全部节点和边
def load_graph():
	#print(request)
	neo_graph = get_graph()
	result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
	result_edges = neo_graph.run('MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)').data()
	nodes = build_nodes(result_nodes,'n')
	edges = build_edges(result_edges)
	return ({"nodes": nodes, "edges": edges})

#使用id查找单个节点信息
def load_search_node(id):
	neo_graph = get_graph()
	result = neo_graph.run("match (n) where id(n)= " + str(id) + " return n,id(n)").data()
	data = {"id": str(result[0]['id(n)']),
	        "property": result[0]['n'],
	        "label": next(iter(result[0]['n'].labels))}
	return data

#加载节点上级的边的节点
def load_up_node(id):
	neo_graph = get_graph()
	results = neo_graph.run("match (m)-[r]->(n) where id(n)= " + str(id) +" return m,id(m)").data()
	nodes = build_nodes(results, 'm')
	return nodes

#查找节点下级的边的节点
def load_down_node(id):
	neo_graph = get_graph()
	results = neo_graph.run("match (m)-[r]->(n) where id(m)= " + str(id) +" return n,id(n)").data()
	nodes = build_nodes(results, 'n')
	return nodes

#查找节点同级的节点
def load_peer_node(id):
	pass


#查找节点边以及周围的边
def load_search_graph(id):
	neo_graph = get_graph()
	results1 = neo_graph.run("match (m)-[r]->(n) where id(m)= " + str(id) +" return m,id(m),Type(r),id(r),n,id(n)").data()
	results2 = neo_graph.run("match (m)-[r]->(n) where id(n)= " + str(id) +" return m,id(m),Type(r),id(r),n,id(n)").data()
	edges = build_edges(results1)
	nodes = build_nodes(results1,'n')

	#error 改m，与n对其的关系
	edges2 = build_edges(results2)
	nodes2 = build_nodes(results2,'m')
	print(nodes2)
	print(edges2)
	for node in nodes2:
		nodes.append(node)
	for edge in edges2:
		edges.append(edge)

	result = load_search_node(id)
	data ={'id':result['id'],
	       'name':str(result['property']['name']),
	       'label':result['label']
	}
	node = {"data": data}
	nodes.append(node)

	return ({"nodes": nodes, "edges": edges})

#关键字搜索指定属性 返回ids
def search_property(search,property):
	neo_graph = get_graph()
	results = neo_graph.run("MATCH (n) WHERE n." + property + " =~ '.*" + search + ".*'RETURN *,id(n)").data()
	ids = []
	for result in results:
		ids.append(result['id(n)'])
	return results

#关键字搜索函数name与descroption 返回ids
def search(search):
	results = search_property(search,'name')
	results2 = search_property(search,'description')
	ids = []
	for result in results:
		ids.append(result['id(n)'])
	for result in results2:
		ids.append(result['id(n)'])
	return ids

#添加节点
def add_node(data,label):
	neo_graph = get_graph()
	tx = neo_graph.begin()
	a = Node(label, name=data['name'], view_times=0, search_times=0, description=data['description'])
	tx.create(a)
	tx.commit()
	return True

#修改节点单个属性
def edit_node(id,property,value):
	neo_graph = get_graph()
	matcher = NodeMatcher(neo_graph)
	result = matcher.get(int(id))
	result[property] = value
	neo_graph.push(result)



#查找节点关系/查找两节点之间关系
def find_relationship(idn,idm):
	neo_graph = get_graph()
	results = neo_graph.run("MATCH (n)-[r:Kind_of]->(m) WHERE id(n) = " +str(idn)+ " and id(m) = " +str(idm)+ "  RETURN r,type(r)").data()
	return results

#添加关系
def add_relationship(idn,idm,relationship):
	neo_graph = get_graph()
	results = find_relationship(idn,idm)
	if results != []:
		for result in results:
			if result['type(r)'] == relationship:
				return(relationship + "关系已存在")
	neo_graph.run("MATCH (n),(m) WHERE id(n) = " + str(idn) + " and id(m) = " + str(idm) + "  CREATE (n)-[r:Kind_of]->(m)")
	return True


#删除节点关系
def delete_relationship(idn,idm,relation):
	pass

#删除节点
def delete_node(id):
	pass


