from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# 数据库neo4j
from py2neo import *
# NEOMODEL模型
from .models import *
import json
import os
from ast import literal_eval


# neo4j链接
def get_graph():
    neo4j = Graph(
        host="127.0.0.1",  # neo4j 搭载服务器的ip地址
        http_port=7978,  # neo4j 服务器监听的端口号
        user="neo4j",  # 数据库user name
        password="123456"  # 密码
    )
    return neo4j


# OGM
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
#D3使用
def build_node_d3(nodeRecord):
    data = {"id": int(nodeRecord['id']),
            "name": str(nodeRecord['property']['name']),
            "property": (nodeRecord['property']),
            "label": nodeRecord['label']}

    return data

# 处理返回的节点和边的数据
def build_nodes_d3(nodes):
    result = []
    for node in nodes:
        new = build_node_d3(node)
        result.append(new)
    return result

# 处理返回的节点和边的数据
def build_edge_d3(relationRecord):
    data = {"source": int(relationRecord['id(m)']),
            "target": int(relationRecord['id(n)']),
            "type": relationRecord['Type(r)']}

    return data

# 处理返回的节点和边的数据
def build_edges_d3(edges):
    result = []
    for edge in edges:
        new = build_edge_d3(edge)
        result.append(new)
    return result

# 加载全部节点和边
def load_graph_d3():
    # print(request)
    neo_graph = get_graph()
    result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
    result_links = neo_graph.run("MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)").data()
    nodes = []
    links = []
    for result in result_nodes:
        nodes.append(load_search_node(result['id(n)']))

    for result in result_links:
        links.append(result)


    print("load_graph_d3" )
    print(nodes)
    nodes2 = build_nodes_d3(nodes)
    links2 = build_edges_d3(links)
    return ({"nodes": nodes2, "links": links2})

# 查找节点边以及周围的边
def load_search_graph_d3(id):
    neo_graph = get_graph()
    results1 = neo_graph.run(
        "match (m)-[r]->(n) where id(m)= " + str(id) + " return m,id(m),Type(r),id(r),n,id(n)").data()
    results2 = neo_graph.run(
        "match (m)-[r]->(n) where id(n)= " + str(id) + " return m,id(m),Type(r),id(r),n,id(n)").data()

    nodes = []
    links = []
    for result in results1:
        nodes.append(load_search_node(result['id(n)']))
        links.append(result)
    for result in results2:
        nodes.append(load_search_node(result['id(m)']))
        links.append(result)
    nodes.append(load_search_node(id))

    nodes2 = build_nodes_d3(nodes)
    links2 = build_edges_d3(links)

    return ({"nodes": nodes2, "links": links2})


# 处理返回的节点和边的数据
def build_node(nodeRecord, node_str):
    data = {"id": str(nodeRecord['id(' + node_str + ')']),
            "name": str(nodeRecord[node_str]['name']),
            "label": next(iter(nodeRecord[node_str].labels))}

    return {"data": data}


# 处理返回的节点和边的数据
def build_edge(relationRecord):
    data = {"source": str(relationRecord['id(m)']),
            "target": str(relationRecord['id(n)']),
            "relationship": relationRecord['Type(r)']}

    return {"data": data}


# 处理返回的节点和边的数据
def build_nodes(nodes, node_str):
    result = []
    for node in nodes:
        new = build_node(node, node_str)
        result.append(new)
    return result


# 处理返回的节点和边的数据
def build_edges(edges):
    result = []
    for edge in edges:
        new = build_edge(edge)
        result.append(new)
    return result


# 加载全部节点和边
def load_graph():
    # print(request)
    neo_graph = get_graph()
    result_nodes = neo_graph.run("MATCH (n) RETURN *,id(n)").data()
    result_edges = neo_graph.run("MATCH (m)-[r]->(n) RETURN id(m), id(n), Type(r)").data()
    nodes = build_nodes(result_nodes, 'n')
    edges = build_edges(result_edges)
    return ({"nodes": nodes, "edges": edges})


# 使用id查找单个节点信息
def load_search_node(id):
    neo_graph = get_graph()
    result = neo_graph.run("match (n) where id(n)= " + str(id) + " return n,id(n)").data()
    data = {"id": str(result[0]['id(n)']),
            "property": result[0]['n'],
            "label": next(iter(result[0]['n'].labels))}
    return data


# 加载节点上级的边的节点
def load_up_node(id, relationship=""):
    neo_graph = get_graph()
    if relationship == "":
        pass
    else:
        relationship = ':' + relationship
    results = neo_graph.run("match (m)-[r" + relationship + "]->(n) where id(n)= " +
                            str(id) + " return m,id(m) ORDER BY m.search_times DESC").data()
    nodes = build_nodes(results, 'm')
    return nodes


# 查找节点下级的边的节点
def load_down_node(id, relationship=""):
    neo_graph = get_graph()
    if relationship == "":
        pass
    else:
        relationship = ':' + relationship
    results = neo_graph.run("match (m)-[r" + relationship + "]->(n) where id(m)= " + str(
        id) + " return n,id(n) ORDER BY m.search_times DESC").data()
    nodes = build_nodes(results, 'n')
    # node['data']['id']
    return nodes


# 查找节点同级的节点
def load_peer_node(id):
    nodes = load_up_node(id, 'Part_of')
    results = []
    for node in nodes:
        mids = load_down_node(node['data']['id'])
        for mid in mids:
            if mid['data']['id'] != str(id):
                results.append(mid)
    return results


# 查找节点边以及周围的边
def load_search_graph(id):
    neo_graph = get_graph()
    results1 = neo_graph.run(
        "match (m)-[r]->(n) where id(m)= " + str(id) + " return m,id(m),Type(r),id(r),n,id(n)").data()
    results2 = neo_graph.run(
        "match (m)-[r]->(n) where id(n)= " + str(id) + " return m,id(m),Type(r),id(r),n,id(n)").data()
    edges = build_edges(results1)
    nodes = build_nodes(results1, 'n')

    # error 改m，与n对其的关系
    edges2 = build_edges(results2)
    nodes2 = build_nodes(results2, 'm')
    for node in nodes2:
        nodes.append(node)
    for edge in edges2:
        edges.append(edge)

    result = load_search_node(id)
    data = {'id': result['id'],
            'name': str(result['property']['name']),
            'label': result['label']
            }
    node = {"data": data}
    nodes.append(node)

    return ({"nodes": nodes, "edges": edges})

str_lim = "where not (n:Concept)"
# 关键字搜索指定属性 返回ids
def search_property(search, property):
    neo_graph = get_graph()
    results = neo_graph.run("MATCH (n) WHERE n." + property + " =~ '.*" + search + ".*' and not (n:Concept) RETURN *,id(n) ORDER BY n.id").data()
    ids = []
    for result in results:
        ids.append(result['id(n)'])
    return results


# 关键字搜索函数name与descroption 返回ids
def search(search):
    results = search_property(search, 'name')
    results2 = search_property(search, 'description')
    ids = []
    for result in results:
        ids.append(result['id(n)'])
    for result in results2:
        ids.append(result['id(n)'])


    ids_new = set(ids)
    ids_new = list(set(ids))
    ids_new.sort(key=ids.index)
    return ids_new


# 添加节点
def add_node(data, label):
    neo_graph = get_graph()
    tx = neo_graph.begin()
    a = Node(label, name=data['name'], english=data['english'], view_times=0, search_times=0,
             description=data['description'])
    tx.create(a)
    tx.commit()
    return True


# 修改节点单个数字属性
def add_node_number(id, property, value):
    neo_graph = get_graph()
    matcher = NodeMatcher(neo_graph)
    result = matcher.get(int(id))
    result[property] = result[property] + value
    neo_graph.push(result)


# 修改节点单个属性
def edit_node(id, property, value):
    neo_graph = get_graph()
    matcher = NodeMatcher(neo_graph)
    result = matcher.get(int(id))
    result[property] = value
    neo_graph.push(result)


# 查找字符
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


# 上传图片
import threading
from threading import Thread
from threading import Lock
import time

mutex = Lock()


def upload_img(id, img):
    saveDir = settings.MEDIA_ROOT + "\\node\\" + str(id)  # 保存路径
    # 获取保存路径并查看是否存在，不存在则新建
    getSaveDir = os.path.join(os.getcwd(), saveDir)
    if not os.path.exists(getSaveDir):
        os.makedirs(getSaveDir, 493)

    ImgPath = os.path.join(getSaveDir, img.name)  # filename是f的固有属性
    # print(ImgPath) #D:\works\毕业设计\代码\project\media\node\79\20151215000118_rRPfm.jpeg
    path = default_storage.save(ImgPath, ContentFile(img.read()))
    # print(path) #D:/works/毕业设计/代码/project/media/node/79/20151215000118_rRPfm_5D5LF0h.jpeg
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    # print(tmp_file) #D:/works/毕业设计/代码/project/media/node/79/20151215000118_rRPfm_5D5LF0h.jpeg
    index = find_last(tmp_file, '/')
    img_url = "{}node/{}/{}".format(settings.MEDIA_URL, id, tmp_file[index + 1:])

    global mutex
    mutex.acquire()
    neo_graph = get_graph()
    matcher = NodeMatcher(neo_graph)
    result = matcher.get(int(id))
    if result['img_url'] == None:
        result['img_url'] = []
    else:
        pass
    result['img_url'].append(img_url)
    neo_graph.push(result)
    mutex.release()
    return img_url


def delete_img(id, url):
    neo_graph = get_graph()
    matcher = NodeMatcher(neo_graph)
    result = matcher.get(int(id))
    result['img_url'].remove(url)
    neo_graph.push(result)


# 查找节点关系/查找两节点之间关系
def find_relationship(idn, idm):
    neo_graph = get_graph()
    results = neo_graph.run("MATCH (n)-[r:Kind_of]->(m) WHERE id(n) = " + str(idn) + " and id(m) = " + str(
        idm) + "  RETURN r,type(r)").data()
    return results


# 添加关系
def add_relationship(idn, idm, relationship):
    neo_graph = get_graph()
    results = find_relationship(idn, idm)
    if results != []:
        for result in results:
            if result['type(r)'] == relationship:
                return (relationship + "关系已存在")
    neo_graph.run("MATCH (n),(m) WHERE id(n) = " + str(idn) + " and id(m) = " + str(
        idm) + "  CREATE (n)-[r:" + relationship + "]->(m)")
    return True


# 删除节点关系  修改ing
def delete_relationship(idn, idm, relation):
    neo_graph = get_graph()
    neo_graph.run("MATCH (n)-[r]->(m) WHERE id(n) = " + str(idn) + " and id(m) = " + str(
        idm) + " and type(r) = " + relation + "  DELETE r")


# 删除节点  删之前删除关系
def delete_node(id):
    neo_graph = get_graph()
    neo_graph.run("MATCH (n) WHERE id(n) = " + str(id) + "  DELETE n")


# 获得底层所有图片
def get_img(id):
    imgs = []
    mids = load_down_node(id)
    if mids == []:
        return []
    for mid in mids:
        node = load_search_node(mid['data']['id'])
        if node['property']['img_url'] == None:
            imgs.extend([])
        else:
            imgs.extend(node['property']['img_url'])
        if node['property']['images'] == None:
            imgs.extend([])
        else:
            nodeimages = literal_eval(node['property']['images'])
            for img in nodeimages:
                imgs.append(img['src'])
        imgs.extend(get_img(node['id']))

    return imgs


def get_all_down_image(id):
    all_imgs = []
    node = load_search_node(id)
    if node['property']['img_url'] == None:
        all_imgs.extend([])
    else:
        all_imgs.extend(node['property']['img_url'])

    if node['property']['images'] == None:
        all_imgs.extend([])
    else:
        nodeimages = literal_eval(node['property']['images'])
        for img in nodeimages:
            all_imgs.append(img['src'])
    all_imgs.extend(get_img(id))
    return all_imgs

#查找指定标签的所有节点
def get_nodes_by_labels(label):
    neo_graph = get_graph()
    results = neo_graph.run("MATCH (n:" + label + ") RETURN n,id(n)").data()
    data = []
    for result in results:
        data.append(load_search_node(result['id(n)']))
    return  data

#查找指定标签的所有节点链接
def get_links_by_labels(label):
    neo_graph = get_graph()
    results = neo_graph.run("MATCH (n:" + label + ")-[r]-(m:" + label + ") RETURN Type(r),id(n),id(m)").data()
    data = []
    return  results


#查找指定指定层数的节点 返回所有节点层数和id BFS算法
def get_nodes_by_layer(id,layer):
    list = []
    list.append([id,0])
    for node in list:
        if node[1] == layer:
            break
        else:
            results = load_down_node(node[0],"Part_of")
            for result in results:
                list.append([int(result['data']['id']),node[1]+1])

    #指定层数id
    # ids = []
    # for node in list:
    #     if node[1] == layer:
    #         ids.append(node[0])

    return list