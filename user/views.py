from django.shortcuts import render,redirect,reverse

#数据库
from py2neo import Node

# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#视图
from django.views import View
#json
import json

"""
 视图
"""

#搜索页面
class AddObjectView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'user_add_object.html')
