from django import forms

from .models import User
from django.contrib.auth import get_user_model

#数据库
from .database import *


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
	name = forms.CharField(max_length=12,error_messages={'required':u'名字不能为空'})
	label = forms.CharField()
	description = forms.CharField(error_messages={'required':u'简介不能为空'})

	def clean(self):
		name = self.cleaned_data.get('name')
		label = self.cleaned_data.get('label')
		neo_graph = get_graph()
		matcher = NodeMatcher(neo_graph)
		exists = matcher.match( label,name=name).first()
		if exists != None:
			raise forms.ValidationError("节点:"+ name +"已经存在！")

	def get_errors(self):
		errors = self.errors.get_json_data()
		new_errors = {}
		for key, message_dicts in errors.items():
			messages = []
			for message in message_dicts:
				messages.append(message['message'])
			new_errors[key] = messages
		return new_errors

class RelationshipForm(forms.Form):
	souid = forms.IntegerField(error_messages={'required':u'名字不能为空'})
	dstid = forms.IntegerField(error_messages={'required':u'名字不能为空'})
	souname = forms.CharField(max_length=12,error_messages={'required':u'名字不能为空'})
	dstname = forms.CharField(max_length=12,error_messages={'required':u'名字不能为空'})
	relationship = forms.CharField(error_messages={'required':u'关系不能为空'})

	def clean(self):
		souid = self.cleaned_data.get('souid')
		dstid = self.cleaned_data.get('dstid')
		relationship = self.cleaned_data.get('relationship')
		if(souid == dstid):
			raise forms.ValidationError(souid+"  "+dstid+"源节点和目的节点不能是同一节点")
		results = find_relationship(souid,dstid)
		if results != []:
			for result in results:
				if result['type(r)'] == relationship:
					raise forms.ValidationError(relationship + "关系已存在")



	def get_errors(self):
		errors = self.errors.get_json_data()
		new_errors = {}
		for key, message_dicts in errors.items():
			messages = []
			for message in message_dicts:
				messages.append(message['message'])
			new_errors[key] = messages
		return new_errors
