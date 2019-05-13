"""project_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
	path('test/', views.TestView.as_view(), name='test'),

	path('', views.AdminIndexView.as_view(), name='index'),
	path('login/', views.AdminLoginView.as_view(), name='login'),
	path('logout/', views.AdminLogout, name='logout'),
	path('home/', views.AdminIndexView.as_view(), name='home'),

	path('knowledge_graph/', views.AdminShowNodeView.as_view(), name='knowledge_graph'),
	path('search/', views.AdminSearchNodeView.as_view(), name='search_node'),

	path('add_node_view/', views.AdminAddNodeView.as_view(), name='add_node_view'),
	path('add_node/', views.AdminAddNodeInterface.as_view(), name='add_node'),
	path('add_relationship_view/', views.AdminAddRelationshipView.as_view(), name='add_relationship_view'),
	path('add_relationship/', views.AdminAddRelationshipInterface.as_view(), name='add_relationship'),
	path('edit_node_view/', views.AdminEditNodeView.as_view(), name='edit_node_view_post'),
	path('edit_node_view/<int:id>/', views.AdminEditNodeView.as_view(), name='edit_node_view'),
	path('edit_node/', views.AdminEditNodeInterface .as_view(), name='edit_node'),
	path('upload_images/<int:id>/', views.AdminUploadImageInterface .as_view(), name='upload_images'),
	path('delete_images/', views.AdminDeleteImageInterface.as_view(), name='delete_images'),

	path('find/graph', views.FindGraphInterface.as_view(), name='find_graph'),
	path('find/node', views.FindByIdInterface.as_view(), name='find_node'),
	path('find/node/label', views.FindByLabelInterface.as_view(), name='find_label'),
	path('find/node/name', views.FindByNameInterface.as_view(), name='find_node_name'),

	path('user', views.AdminUserListView.as_view(), name='user_list'),
	path('get_info', views.AdminGetMessageInterface, name='get_info'),
	path('user/detail/<int:user_id>', views.AdminUserDetailView.as_view(), name='user_detail'),
	path('verify', views.AdminVerifyView.as_view(), name='verify'),
	path('verify/detail/<int:verify_id>', views.AdminVerifyDetailView.as_view(), name='verify_detail'),
	path('verify/confirm/', views.confirm_node, name='verify_confirm'),
	path('verify/deny/', views.deny_node, name='verify_deny'),

	#删除节点
	path('node/delete/', views.delete_node_interface, name='delete_node'),

	#异常处理
	path('500/', views.Admin500View, name='500'),

]
