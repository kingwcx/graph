from django import forms

from .models import User
from django.contrib.auth import get_user_model

#数据库
from py2neo import *

#连接数据库
def get_graph():
	neo4j = Graph(
		host="127.0.0.1",  # neo4j 搭载服务器的ip地址
		http_port=7978,  # neo4j 服务器监听的端口号
		user="neo4j",  # 数据库user name
		password="123456"  # 密码
	)
	return neo4j

class LoginForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	class Meta:
		model = get_user_model()
		fields = ['password']

class RegisterForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	re_password = forms.CharField(max_length=12)
	class Meta:
		model = get_user_model()
		fields = ['password']

	def clean_useranme(self):
		username = self.cleaned_data.get('username')
		exists = User.objects.filter(username=username).exists()
		if exists:
			raise forms.ValidationError("用户名已经存在！")
		return username

class NodeForm(forms.Form):
	name = forms.CharField(max_length=12)
	label = forms.CharField()
	introduction = forms.CharField()

	def clean(self):
		name = self.cleaned_data.get('name')
		label = self.cleaned_data.get('label')
		neo_graph = get_graph()
		matcher = NodeMatcher(neo_graph)
		exists = matcher.match(label, name=name).first()
		if exists != None:
			raise forms.ValidationError("节点:"+ name +"已经存在！")
