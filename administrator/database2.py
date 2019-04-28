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


