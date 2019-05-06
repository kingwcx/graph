from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.core.files import  *
# 数据库
from .database import *
from .models import *
# 表单验证
from .forms import LoginForm,RegisterForm,NodeForm,RelationshipForm
# 用户与权限
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
#
import json

#测试页面
class TestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'test.html')
"""
 视图
"""
#管理员登陆页面
class AdminLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        next_href = request.GET.get('next', '') #之前登录页面
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                # request.session.set_expriy(0)
                if next_href == "":
                    return redirect(reverse('admin:home'))
                else:
                    return redirect(next_href)
        else:
            print(form.errors)
            return redirect(reverse('admin:login'))

def AdminLogout(request):
    logout(request)
    return redirect(reverse('admin:login'))

# 管理员主页面
@method_decorator(login_required(login_url='admin:login'),name='dispatch')
class AdminIndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_home.html')

class AdminUserListView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()

        paginator = Paginator(users, 10)
        pages = paginator.page_range  # 生成所有页码
        pages_num = paginator.num_pages  # 总页数

        page = request.GET.get('page')  # 当前页面
        contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页
        return render(request, 'admin/admin_user_list.html', context={'contacts': contacts, 'pages': pages, 'pagenums': pages_num})

class AdminUserDetailView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        return render(request, 'admin/admin_user_detail.html', context={"user": user})

class AdminVerifyView(View):
    def get(self, request, *args, **kwargs):
        nodes = UserNode.objects.all()

        paginator = Paginator(nodes, 10)
        pages = paginator.page_range  # 生成所有页码
        pages_num = paginator.num_pages  # 总也数

        page = request.GET.get('page')  # 当前页面;[
        contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页
        return render(request, 'admin/admin_verify.html', context={'contacts': contacts, 'pages': pages, 'pagenums': pages_num})

class AdminVerifyDetailView(View):
    def get(self, request, *args, **kwargs):
        node = UserNode.objects.get(id=kwargs['verify_id'])
        return render(request, 'admin/admin_verify_detail.html', context={"node": node})


show = {'': '全部','People': '人物','Work': '作品','Style': '风格','Process': '设计过程'}


# 展示节点node
class AdminShowNodeView(View):
    def get(self, request, *args, **kwargs):
        element = json.dumps(load_graph())
        return render(request, 'admin/admin_nodes.html', context={"labels": show, "element":element})

# 搜索节点node
class AdminSearchNodeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_search.html')
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
                    return render(request, 'admin/admin_search.html', context={'search': search_key, 'ids':ids, 'data':data})
                else:
                    print("没有找到你要的内容!")
                    return redirect(reverse('admin:search_node'))
            except Exception as e:
                print(e)
                print("服务器错误！")
                return redirect(reverse('admin:search_node'))
        else:
            return redirect(reverse('admin:search_node'))


# 标签清单
labels = {'Style': '款式','Pattern': '制版','Technology': '工艺','Design':'服装设计','Example':'成衣实例'}
show_labels = {'Design': '服装设计','Style': '款式','Patternmaking': '制版','Technology': '工艺'}

relationships = {'Kind_of': 'Kind_of','Part_of': 'Part_of','Instance_of': 'Instance_of','Attribute_of': 'Attribute_of',
                 'Join_of':'Join_of', 'Collocation_of':'Collocation_of'}


# ajax返回所需标签
def ajax_lable_list(request):
    return JsonResponse(basic)


# 添加节点页面node
class AdminAddNodeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_add_node.html', context={"labels": labels})

# 添加关系页面relation
class AdminAddRelationshipView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_add_relationship.html', context={"relationships": relationships})

# 修改节点页面node
class AdminEditNodeView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        data = load_search_node(id)
        return render(request, 'admin/admin_edit_node.html', context={'data':data})
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        data = load_search_node(id)
        return render(request, 'admin/admin_edit_node.html', context={'data':data})

# 修改关系页面relationship
class AdminEditRelationshipView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_add_relationship.html', context={"relationships": relationships})



"""
接口
"""
"""获取消息接口"""
def AdminGetMessageInterface(request):
    results = UserNode.objects.all().values()
    nodes = []
    for result in results:
        nodes.append(result)

    data={'nodes':nodes}
    return JsonResponse(data)

"""
neo4j接口
"""

"""添加节点接口"""

# 添加节点 （通用）
class AdminAddNodeInterface(View):
    def post(self, request, *args, **kwargs):
        form = NodeForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            name = form.cleaned_data.get('name')
            english = form.cleaned_data.get('english')
            label = form.cleaned_data.get('label')
            data = {'name':name,'english':english,'description':description}
            add_node(data,label)
            return redirect(reverse('admin:knowledge_graph'))
        else:
            print(form.errors.get_json_data())
            print(form.get_errors())
            try:
                print(form.get_errors()['__all__'])
                name = form.get_errors()['__all__']
            except Exception as e:
                print(e)
                name = ""

            return render(request, 'admin/admin_add_node.html', context={"labels": labels, "errors": form.get_errors(),
                                                                      "name": name})


"""查找接口"""
#返回整张图
class FindGraphInterface(View):
    def get(self, request, *args, **kwargs):
        data = load_graph_d3()
        print(data)
        return JsonResponse(data)

#通过标签返回节点和图
class FindByLabelInterface(View):
    def get(self, request, *args, **kwargs):
        nodes = get_nodes_by_labels('Design')
        links = get_links_by_labels('Design')
        nodes2 = build_nodes_d3(nodes)
        links2 = build_edges_d3(links)
        data = {"nodes":nodes2,
                "links":links2}
        print(data)
        return JsonResponse(data)


#通过id返回节点和周围路径为1的点
class FindByIdInterface(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        #print(id)
        elements = load_search_graph_d3(id)
        #print(elements)
        current_data = load_search_node(id)
        data = {'current_data':current_data,'elements':elements}

        return JsonResponse(data)
    def get(self, request, *args, **kwargs):
        results = load_search_graph_d3(1)
        print(results)
        return JsonResponse(results)

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
        nodes = load_up_node(id,'Kind_of')
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
        try:
            form = RelationshipForm(request.POST)
            if form.is_valid():
                souname = form.cleaned_data.get('souname')
                dstname = form.cleaned_data.get('dstname')
                souid = form.cleaned_data.get('souid')
                dstid = form.cleaned_data.get('dstid')
                relationship = form.cleaned_data.get('relationship')
                add_relationship(souid,dstid,relationship)
                return redirect(reverse('admin:knowledge_graph'))
            else:
                print(form.errors.get_json_data())
                print(form.get_errors())
                return HttpResponse(404)
        except:
            return HttpResponse("提交了一个错误的参数")

"""上传图片"""
class AdminUploadImageInterface(View):
    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        img = request.FILES.get('image')
        url = upload_img(id,img)
        return JsonResponse({'url':url})

"""删除节点图片"""
class AdminDeleteImageInterface(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        url = request.POST.get('url')
        delete_img(id,url)
        return redirect(reverse('admin:edit_node_view',kwargs={'id':id}))

"""修改节点接口"""
class AdminEditNodeInterface(View):
    def post(self, request, *args, **kwargs):
        data = {}
        id = request.POST.get('id')
        name = request.POST.get('name')
        english = request.POST.get('english')
        description = request.POST.get('description')
        url = request.POST.get('url')
        if name!='':
            edit_node(id,"name",name)
        else:
            print("不修改name")
        if english != '':
            edit_node(id, "english", english)
        else:
            print("不修改english")
        if description != '':
            edit_node(id, "description", description)
        else:
            print("不修改description")
        if url!='None' and url !=' ':
            if "https://" not in url:
                url = "https://" + url
            edit_node(id, "url", url)
        else:
            print("不修改url")

        return redirect(reverse('front:object_detail',kwargs={'id':id}))

"""删除节点接口"""

"""删除关系接口"""
