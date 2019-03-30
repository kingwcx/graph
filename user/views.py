from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from administrator.database import *
#表单
from administrator.forms import LoginForm,RegisterForm
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


"""
 视图
"""
class LoginView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'login.html')

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		next_href = request.GET.get('next', '')  # 之前登录页面
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user and user.is_active:
				login(request, user)
				# request.session.set_expriy(0)
				if next_href == "":
					return redirect(reverse('front:index'))
				else:
					return redirect(next_href)
			else:
				return redirect(reverse('user:login'))
		else:
			print(form.errors)
			return redirect(reverse('user:login'))

def Logout(request):
	logout(request)
	return redirect(reverse('front:index'))

class RegisterView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'register.html')

	def post(self, request, *args, **kwargs):
		form = RegisterForm(request.POST)
		# next_href = request.GET.get('next', '') #之前登录页面
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			re_password = form.cleaned_data.get('re_password')
			User.objects.create_user(username, ".@.", password)
			return redirect(reverse('user:login'))
		else:
			print(form.errors.get_json_data())
			return redirect(reverse('user:register'))

#选择页面
class SelectView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'user_select.html')

#个人中心
class ProfileView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'user_profile.html')

#个人中心
class MessagesView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'user_messages.html')

#学习推荐页面
class StudyGuideView(View):
	def get(self,request,*args,**kwargs):
		level = kwargs['level']
		if level == 0:
			ids_list = get_nodes_by_layer(0,2)
			results = []
			for id in ids_list:
				results.append(load_search_node(id[0]))
			return render(request, 'user_study_guide_base.html',context={'results':results})
		else:
			return HttpResponse(200)

#用户添加节点页面
class AddObjectView(View):
	def get(self,request,*args,**kwargs):
		return render(request, 'user_add_object.html')
