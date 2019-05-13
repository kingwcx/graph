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

app_name = 'user'

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.Logout, name='logout'),
	path('register/', views.RegisterView.as_view(), name='register'),
	path('select/', views.SelectView.as_view(), name='select'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('messages/', views.MessagesView.as_view(), name='messages'),
	path('node/deny/', views.deny_node, name='node_deny'),
	path('study/<int:level>/', views.StudyGuideView.as_view(), name='study'),
	path('add_object/', views.AddObjectView.as_view(), name='add_object'),
]
