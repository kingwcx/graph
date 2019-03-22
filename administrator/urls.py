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
	path('', views.AdminIndexView.as_view(), name='index'),
	path('home/', views.AdminIndexView.as_view(), name='home'),

	path('knowledge_graph/', views.AdminShowNodeView.as_view(), name='knowledge_graph'),
	path('search/', views.AdminSearchNodeView.as_view(), name='search_node'),

	path('add_node_view/', views.AdminAddNodeView.as_view(), name='add_node_view'),
	path('add_node/', views.AdminAddNodeInterface.as_view(), name='add_node'),
	path('add_relationship_view/', views.AdminAddRelationshipView.as_view(), name='add_relationship_view'),
	path('add_relationship/', views.AdminAddRelationshipInterface.as_view(), name='add_relationship'),
	path('edit_node_view/', views.AdminEditNodeView.as_view(), name='edit_node_view'),
	path('edit_node/', views.AdminEditNodeInterface .as_view(), name='edit_node'),


	path('add_example_view/', views.AdminAddExampleView.as_view(), name='add_example_view'),


	path('add_concept_view/', views.AdminAddConceptView.as_view(), name='add_concept_view'),

	path('find/node', views.FindByIdInterface.as_view(), name='find_node'),
	path('find/node/name', views.FindByNameInterface.as_view(), name='find_node_name'),



]
