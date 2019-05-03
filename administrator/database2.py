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
import synonyms

#语义网络相关数据库
# neo4j链接
def get_graph():
    neo4j = Graph(
        host="127.0.0.1",  # neo4j 搭载服务器的ip地址
        http_port=7978,  # neo4j 服务器监听的端口号
        user="neo4j",  # 数据库user name
        password="123456"  # 密码
    )
    return neo4j

# 添加节点
def add_node(label,name,vector):
    neo_graph = get_graph()
    tx = neo_graph.begin()
    print(type(vector))
    a = Node(label, name=name, vector=vector.tolist())
    tx.create(a)
    tx.commit()

# 添加边
def add_link(type,label1,label2,name1,name2,value):
    neo_graph = get_graph()
    matcher = NodeMatcher(neo_graph)
    tx = neo_graph.begin()
    node1 = matcher.match(label1, name=name1).first()
    node2 = matcher.match(label2, name=name2).first()
    link = Relationship(node1, type, node2, value = value.tolist())
    tx.create(link)
    tx.commit()

#判断节点是否存在
def node_exist(label,name):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    result = matcher.match(label, name=name)
    if result.first() == None:
        print("不存在")
        return False
    else:
        print(result.first())
        return True

#判断变是否存在
def link_exist(type,label1,label2,name1,name2):
    graph = get_graph()
    matcher = NodeMatcher(graph)
    matcher2 = RelationshipMatcher(graph)
    node1 = matcher.match(label1, name=name1).first()
    node2 = matcher.match(label2, name=name2).first()
    links = matcher2.match(nodes=[node1,node2],r_type=type)
    if links.first() == None:
        print("不存在")
        return False
    else:
        print(links.first())
        return True



label = "Concept"
relation_type = "Concept_nearby_of"

def add_words(start_word):
    if node_exist(label, start_word):
        pass
    else:
        add_node(label, start_word, synonyms.v(start_word))

    words = synonyms.nearby(start_word)
    print(words)
    i = 0
    for word in words[0]:
        if words[1][i] == 1.0:
            pass
        else:
            #判断词语在不在图谱中
            if node_exist(label, word):
                pass
            else:
                add_node(label, word, synonyms.v(start_word))

            #判断两点之间是否有连线
            if link_exist(relation_type, label, label, start_word, word) :
                pass
            else:
                add_link(relation_type, label, label, start_word, word,words[1][i])
                add_link(relation_type, label, label, word, start_word, words[1][i])
        i+=1


