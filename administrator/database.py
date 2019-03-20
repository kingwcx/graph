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
	print(result)
	data = {"id": str(result[0]['id(n)']),
	        "property": result[0]['n'],
	        "label": next(iter(result[0]['n'].labels))}
	return data

#加载节点边以及周围的边
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

