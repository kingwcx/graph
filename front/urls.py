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

app_name = 'front'

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('search/', views.SearchView.as_view(), name='search'),
	path('search/action/', views.SearchActionView.as_view(), name='search_action'),
	path('result/', views.SearchResultView.as_view(), name='search_result'),
	path('result/error/', views.SearchResultErrorView.as_view(), name='search_result_error'),
	path('object/', views.ObjectDetailView.as_view(), name='object_detail'),
	path('object/<int:id>/', views.ObjectDetailView.as_view(), name='object_detail'),
	path('example_list/', views.ExampleList.as_view(), name='example_list'),
]
