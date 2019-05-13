from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
# 数据库
from administrator.database import *
from administrator.models import *
# 表单
from administrator.forms import LoginForm, RegisterForm, NodeForm
# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
# 视图
from django.views import View
# 用户与权限
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
# json
import json

"""
 视图
"""


class LoginView(View):
    def get(self, request, *args, **kwargs):
        error_type = request.GET.get("error_type")
        error_info = ""
        if error_type == "1":
            error_info = "用户名或密码错误"
        else:
            error_info = ""
        return render(request, 'user/login.html', context={"error_info": error_info})

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
                error_type = 1
                return redirect(reverse('user:login') + '?error_type=' + str(error_type))
        else:
            print(form.errors)
            return redirect(reverse('user:login'))


def Logout(request):
    logout(request)
    return redirect(reverse('front:index'))


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        error_type = request.GET.get("error_type")
        error_info = ""
        if error_type == "1":
            error_info = "用户名已存在！"
        else:
            error_info = ""
        return render(request, 'user/register.html', context={"error_info": error_info})

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
            error_type = 1
            print(form.errors.get_json_data())
            return redirect(reverse('user:register') + '?error_type=' + str(error_type))


# 选择页面
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class SelectView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_select.html')


# 个人中心
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_profile.html')


# 个人中心
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class MessagesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_messages.html')


# 撤销
#@method_decorator(login_required(login_url='user:login'), name='dispatch')
def deny_node(request):
    id = request.POST.get('id')
    print(id)
    node = UserNode.objects.get(id=id)
    node.delete()
    return redirect(reverse('user:messages'))


# 学习推荐页面
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class StudyGuideView(View):
    def get(self, request, *args, **kwargs):
        level = kwargs['level']
        if level == 0:
            ids_list = get_nodes_by_layer(46, 2)
            results = []
            for id in ids_list:
                results.append(load_search_node(id[0]))
            return render(request, 'user/user_study_guide_base.html', context={'results': results})
        else:
            results = []
            results.append(load_search_node(46))
            results.append(load_search_node(47))
            results.append(load_search_node(48))
            return render(request, 'user/user_study_guide_up.html', context={'results': results})


labels = {'Style': '款式', 'Pattern': '制版', 'Technology': '工艺', 'Design': '服装设计', 'Example': '成衣实例'}
labels2 = {'Design': '概念', 'Example': '实例'}


# 用户添加节点页面
@method_decorator(login_required(login_url='user:login'), name='dispatch')
class AddObjectView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_add_object.html', context={'labels': labels2})

    def post(self, request, *args, **kwargs):
        form = NodeForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            name = form.cleaned_data.get('name')
            english = form.cleaned_data.get('english')
            label = form.cleaned_data.get('label')
            url = form.cleaned_data.get('url')

            user_id = request.user.id
            node = UserNode(name=name, description=description, english=english, label=label, url=url, user_id=user_id)
            node.save()
            return redirect(reverse('user:messages'))
        else:
            print(form.errors.get_json_data())
            print(form.get_errors())
            try:
                print(form.get_errors()['__all__'])
                name = form.get_errors()['__all__']
            except:
                name = ""

            return render(request, 'user/user_add_object.html', context={"labels": labels, "errors": form.get_errors(),
                                                                         "name": name})
