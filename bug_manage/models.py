from django.db import models
import django.utils.timezone as timezone
class UserInfo(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    usr = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    email = models.EmailField(unique=True)#邮件设置
    sex = models.CharField(max_length=32,choices=gender,default='男')
    datatime = models.DateTimeField(u'保存日期',default=timezone.now)

class ShuJuCount(models.Model):
    typeid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10)
    type_data = models.CharField(max_length=10)

#英语提测版本管理
class PxVersion(models.Model):
    pvid = models.AutoField(u'版本数据ID',primary_key=True)
    pvname = models.CharField(u'交付版本名称',max_length=100)
    pvnumber = models.CharField(u'提测版本编号',max_length=100)
    datatime = models.DateTimeField(u'保存日期', default=timezone.now)
#组件模块管理
class PxModular(models.Model):
    pmid = models.AutoField(u'组件模块ID',primary_key=True,null=False)
    pmtype = models.BooleanField(u'组件类型',default=True)
    pmname = models.CharField(u'组件模块名称',max_length=30,null=False)
    datatime = models.DateTimeField(u'保存日期',default=timezone.now)
#BUG信息统计
class PxBugCount(models.Model):
    bugid = models.AutoField(u'BUGid',primary_key=True,null=False)
    bug_pvid = models.CharField(u'BUG大版本数据ID',max_length=100)
    bug_pmid = models.CharField(u'BUG提测版本编号',max_length=100)
    bug_zj = models.CharField(u'BUG组件模块ID',max_length=100)
    bug_wtms = models.CharField(u'BUG问题描述',max_length=255)
    bug_cdbh = models.CharField(u'BUG禅道编号',max_length=100)
    bug_sfxmk = models.CharField(u'BUG是否新模块',max_length=10)
    bug_wtdj = models.CharField(u'BUG问题等级',max_length=10)
    bug_xgyxj = models.CharField(u'BUG修改优先级',max_length=10)
    bug_sfyjj = models.CharField(u'BUG是否已解决',max_length=10)
    bug_sfyztg = models.CharField(u'BUG是否验证通过',max_length=10)
    bug_sfhg = models.CharField(u'BUG是否为回归',max_length=10)
    bug_cjr = models.CharField(u'BUG添加人',max_length=10)
    bug_tjsj = models.DateTimeField(u'BUG添加时间',default=timezone.now)
#存储图片数据库
class SaveImage(models.Model):
    img_url = models.ImageField(upload_to='image/')#指定图片上传的途径
    bug_id = models.CharField(u'对应PxBugCount的ID',max_length=100,null=True)