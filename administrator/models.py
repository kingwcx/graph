from django.db import models

#django model
# django 自带用户表
from django.contrib.auth.models import User

#neo4j model
from py2neo.ogm import *

# 用户扩展表
class UserExtension(models.Model):
	telephone = models.CharField('Telephone', max_length=50, blank=True)
	sex = models.IntegerField(null=True, blank=True)
	age = models.IntegerField(null=True, blank=True)
	# 一对一外键（User）
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
	# 一对多外键
	studies = models.ForeignKey("UserStudy", on_delete=models.CASCADE)

	class Meta:
		db_table = 'user_extension'

#用户已学习中间件 表
class UserStudy(models.Model):
	id = models.AutoField(primary_key=True)
	study_time = models.DateTimeField(null=True, blank=True)
	#一对一外键
	study_id = models.IntegerField()

	class Meta:
		db_table = 'study_mid'

#用户添加节点中间储存
class UserNode(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(null=True, blank=True,max_length=20)
	english = models.CharField(null=True, blank=True,max_length=30)
	description = models.CharField(null=True, blank=True,max_length=300)
	label = models.CharField(null=True, blank=True,max_length=10)
	url = models.CharField(null=True, blank=True,max_length=100)

	# 多对一外键
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		db_table = 'user_node'


# 用户添加节点中间储存
class UserRelation(models.Model):
	id = models.AutoField(primary_key=True)
	sou_id = models.IntegerField(null=True, blank=True)
	dst_id = models.IntegerField(null=True, blank=True)

	class Meta:
		db_table = 'user_relation'




