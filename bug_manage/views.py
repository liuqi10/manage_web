from django.shortcuts import render,HttpResponse
from bug_manage import models
from django.forms.models import model_to_dict
from django.db.models import Count, Min, Sum, Avg
import json,os
from django.core import serializers
from datetime import datetime,date

class ComplexEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
      return obj.strftime('%Y-%m-%d')
    else:
      return json.JSONEncoder.default(self, obj)
def looplist(listname):
    newlist = []
    for i in range(len(listname)):
        newlist.append(listname[i])
    return newlist
#注册函数
def register(request):
    pass
    return render(request,'register.html')
def login(request):
    if request.method =="POST":
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        print(usr,pwd)
        models.UserInfo.objects.create(usr=usr,pwd=pwd)
    user_list = models.UserInfo.objects.all()
    print('123',user_list)
    return render(request, 'login.html', {'user_list':user_list})
#主查询页面
def index(request):
    if request.is_ajax():
        #查询大版本号和提测版本编号
        pv_list1 = models.PxVersion.objects.all().values('pvname').distinct()
        pv_list2 = models.PxVersion.objects.all().values('pvnumber').distinct()
        pvnames = looplist(pv_list1)
        pvnumbers = looplist(pv_list2)
        #根据条件进行查询
        dbbh = request.GET.get('dbbh')
        tcbbh = request.GET.get('tcbbh')
        sfhg = request.GET.get('sfhg')
        print(dbbh,tcbbh,sfhg)
        if tcbbh =="全部" and sfhg != "全部":
            bug_lists = models.PxBugCount.objects.filter(bug_pvid=dbbh,bug_sfhg=sfhg).values('bug_pvid','bug_pmid','bug_zj','bug_cdbh','bug_wtdj','bug_wtms','bug_sfyjj','bug_sfyztg','bug_sfhg').distinct().order_by('-bug_pmid','-bug_wtdj')
        elif tcbbh !="全部" and sfhg == "全部":
            bug_lists = models.PxBugCount.objects.filter(bug_pvid=dbbh,bug_pmid=tcbbh).values('bug_pvid', 'bug_pmid','bug_zj', 'bug_cdbh','bug_wtdj','bug_wtms','bug_sfyjj','bug_sfyztg','bug_sfhg').distinct().order_by('-bug_pmid','-bug_wtdj')
        elif tcbbh=="全部" and sfhg == "全部":
            bug_lists = models.PxBugCount.objects.filter(bug_pvid=dbbh).values('bug_pvid', 'bug_pmid','bug_zj', 'bug_cdbh','bug_wtdj','bug_wtms','bug_sfyjj','bug_sfyztg','bug_sfhg').distinct().order_by('-bug_pmid','-bug_wtdj')
        else:
            bug_lists = models.PxBugCount.objects.filter(bug_pvid=dbbh, bug_pmid=tcbbh, bug_sfhg=sfhg).values('bug_pvid', 'bug_pmid', 'bug_zj', 'bug_cdbh', 'bug_wtdj','bug_wtms','bug_sfyjj','bug_sfyztg','bug_sfhg').distinct().order_by('-bug_pmid','-bug_wtdj')
        bug_datas = []
        for i in range(len(bug_lists)):
            bug_datas.append(bug_lists[i])
        datas ={
            "code":200,
            "msg":"获取数据成功",
            "result":{
                "pvnames":pvnames,
                "pvnumbers":pvnumbers,
                "bug_datas":bug_datas
            }
        }
        return HttpResponse(json.dumps(datas,cls=ComplexEncoder))
    else:
        if request.method == "POST":
            return render(request,'index.html')
        else:
            return render(request,'index.html')

#配置提测版本
def configversion(request):
    if request.is_ajax():
        pv_list = models.PxVersion.objects.all().values_list('pvname','pvnumber')
        print(list(pv_list))
        return HttpResponse(json.dumps(list(pv_list)),content_type="application/json")
    else:
        if request.method =="POST":
            dbbbh = request.POST.get('dbbbh')
            tcbbbh = request.POST.get('tcbbbh')
            code = "success"
            models.PxVersion.objects.create(pvname=dbbbh,pvnumber=tcbbbh)
            return render(request,'configversion.html',context={"code":code})
        else:
            return render(request,'configversion.html',context={"code":"无更新信息或者提交信息不正确"})
#模块管理
def configmodular(request):
    if request.is_ajax():
        pv_list = models.PxModular.objects.all().values_list('pmtype','pmname')
        print(list(pv_list))
        return HttpResponse(json.dumps(list(pv_list)),content_type="application/json")
    else:
        if request.method =="POST":
            sfxzj = request.POST.get('sfxzj')
            zjmkmc = request.POST.get('zjmkmc')
            code = "success"
            models.PxModular.objects.create(pmtype=sfxzj,pmname=zjmkmc)
            return render(request,'modular.html',context={"code":code})
        else:
            return render(request,'modular.html',context={"code":"无更新信息或者提交信息不正确"})
#提交BUG配置
def sub_bug(request):
    if request.is_ajax():
        pv_list = models.PxModular.objects.all().values('pmname')
        userinfo = models.UserInfo.objects.all().values('usr')
        pn_list1 = models.PxVersion.objects.all().values('pvname').distinct()
        pn_list2 = models.PxVersion.objects.all().values('pvnumber')
        bbmc_list = []
        ryxx_list = []
        bbgl_list = []
        type_list = []
        for i in range(len(userinfo)):
            ryxx_list.append(userinfo[i]['usr'])
        for j in range(len(pv_list)):
            bbmc_list.append(pv_list[j]['pmname'])
        for m in range(len(pn_list1)):
            type_list.append(pn_list1[m]['pvname'])
        for n in range(len(pn_list2)):
            bbgl_list.append(pn_list2[n]['pvnumber'])
        data_list ={
            "code":200,
            "msg":"成功",
            "result":{
                "bbmc":bbmc_list,
                "ryxx":ryxx_list,
                "bbgl":bbgl_list,
                "bug":type_list
            }
        }
        # print(data_list)
        return HttpResponse(json.dumps(data_list,ensure_ascii=False),content_type="application/json,charset=utf-8")
    else:
        if request.method == "POST":
            dbbh = request.POST.get('dbbh')
            tcbbbh = request.POST.get('tcbbbh')
            zjmk = request.POST.get('zjmk')
            postion = request.POST.get('postion')
            bug_bh = request.POST.get('bug_bh')
            nmk = request.POST.get('nmk')
            wtdj = request.POST.get('wtdj')
            xgyxj = request.POST.get('xgyxj')
            bug_jj = request.POST.get('bug_jj')
            bug_clo = request.POST.get('bug_clo')
            bug_hg = request.POST.get('bug_hg')
            cjr = request.POST.get('cjr')
            img_url = request.FILES.get('fjsc')
            print(dbbh,tcbbbh,zjmk,postion,bug_bh,nmk,wtdj,xgyxj,bug_jj,bug_clo,bug_hg,cjr)
            #写入添加的BUG内容
            bug_insert = models.PxBugCount.objects.create(bug_pvid=dbbh,bug_pmid=tcbbbh,bug_zj=zjmk,bug_wtms=postion,bug_cdbh=bug_bh,bug_sfxmk=nmk,bug_wtdj=wtdj,
                                             bug_xgyxj=xgyxj,bug_sfyjj=bug_jj,bug_sfyztg=bug_clo,bug_sfhg=bug_hg,bug_cjr=cjr)
            #查询写入当前BUG的ID
            bug_insert_id = models.PxBugCount.objects.filter(bug_pvid=dbbh,bug_pmid=tcbbbh,bug_cdbh=bug_bh).values()
            print("对应的BUGID",bug_insert_id[0]['bugid'])
            #上传的图片写入到数据库
            if bug_insert_id[0]['bugid'] != '':
                img = models.SaveImage(img_url=img_url,bug_id=bug_insert_id[0]['bugid'])
                img.save()
            else:
                print("BUG内容没有添加成功！！！")
            if bug_insert and img:
                return render(request,'subbug.html',context={"code":200,"msg":"提交BUG成功！！！"})
            else:
                return render(request,'subbug.html',context={"code":100,"msg": "提交BUG失败！！！"})
        else:
            return render(request,'subbug.html')
#更新bug模块
def update_bug(request):
    if request.is_ajax():
        #默认加载查询数据
        bbgl_list = []
        type_list = []
        pm_list = []
        user_list = []
        pn_list1 = models.PxVersion.objects.all().distinct().values('pvname')
        for m in range(len(pn_list1)):
            bbgl_list.append(pn_list1[m]['pvname'])

        pn_list2 = models.PxVersion.objects.all().distinct().values('pvnumber')
        for m in range(len(pn_list2)):
            type_list.append(pn_list2[m]['pvnumber'])

        pm_list3 = models.PxModular.objects.all().distinct().values('pmname')
        for m in range(len(pm_list3)):
            pm_list.append(pm_list3[m]['pmname'])

        userinfo = models.UserInfo.objects.all().distinct().values('usr')
        for m in range(len(userinfo)):
            user_list.append(userinfo[m]['usr'])

        print("aaaa",bbgl_list,type_list,pm_list,user_list)
        #通过禅道BUG编号，查询具体数据
        bugbh = request.GET.get('bug_cdbh')
        print(bugbh)
        bug_list = models.PxBugCount.objects.filter(bug_cdbh = bugbh).values()
        bug_data = ''
        for i in range(len(bug_list)):
            bug_data = bug_list[i]
        print('c',bug_data)
        #查询BUG上传的图片
        if bug_data == '':
            print("空内容")
            bug_img = ''
        else:
            print(bug_data['bugid'])
            bug_image = models.SaveImage.objects.filter(bug_id=bug_data['bugid']).values()
            for n in range(len(bug_image)):
                print(bug_image[n])
            bug_img = bug_image[n]['img_url']
            print(bug_img)
        img_url = os.path.join(r'media/',bug_img)
        # img_url = bug_img
        print(img_url)
        #返回数据
        result = {
            "code":200,
            "results":{
                "bug_data":bug_data,
                "bug_img":img_url,
                "bbgl":bbgl_list,
                "type_list":type_list,
                "pmname":pm_list,
                "userinfo":user_list
            }
        }
        # return HttpResponse(json.dumps(bug_list,cls=ComplexEncoder), content_type="application/json,charset=utf-8")
        # return HttpResponse(json.dumps(bug_data,cls=ComplexEncoder))
        return HttpResponse(json.dumps(result,cls=ComplexEncoder))
    else:
        if request.method == "POST":
            bugid = request.POST.get('bugid')
            dbbh = request.POST.get('dbbh')
            tcbbbh = request.POST.get('tcbbbh')
            zjmk = request.POST.get('zjmk')
            postion = request.POST.get('postion')
            bug_bh = request.POST.get('bug_bh')
            nmk = request.POST.get('nmk')
            wtdj = request.POST.get('wtdj')
            xgyxj = request.POST.get('xgyxj')
            bug_jj = request.POST.get('bug_jj')
            bug_clo = request.POST.get('bug_clo')
            bug_hg = request.POST.get('bug_hg')
            cjr = request.POST.get('cjr')
            print(bugid,dbbh, tcbbbh, zjmk, postion, bug_bh, nmk, wtdj, xgyxj, bug_jj, bug_clo, bug_hg, cjr)
            models.PxBugCount.objects.filter(bugid=bugid).update(
                bug_pvid=dbbh, bug_pmid=tcbbbh, bug_zj=zjmk, bug_wtms=postion, bug_cdbh=bug_bh, bug_sfxmk=nmk,
                bug_wtdj=wtdj,bug_xgyxj=xgyxj, bug_sfyjj=bug_jj, bug_sfyztg=bug_clo, bug_sfhg=bug_hg, bug_cjr=cjr
            )
            return render(request, 'updatebug.html', context={"msg": "更改成功！"})
        else:
             return render(request, 'updatebug.html')
def count_bug(request):
    if request.is_ajax():
        #默认大版本查询下拉框数据
        bbgl_list = []
        pn_list1 = models.PxVersion.objects.all().distinct().values('pvname')
        for m in range(len(pn_list1)):
            bbgl_list.append(pn_list1[m]['pvname'])
        #js获取的参数值
        dbbh = request.GET.get('dbbh')
        print(dbbh)

        bug_list = models.PxBugCount.objects.values("bug_pmid").filter(bug_pvid=dbbh).annotate(total_bug=Count('bug_cdbh')).all()
        print(bug_list)
        bug_total = []
        for i in range(len(bug_list)):
            bug_total.append(bug_list[i])
        print(bug_total)
        if(bbgl_list):
            result = {
                "code": 200,
                "results": {
                    "bbgl": bbgl_list,
                    "dbbh": dbbh,
                    "bug_total":bug_total
                }
            }
        else:
            result = {
                "code": 100,
                "results": {
                    "bbgl": bbgl_list
                }
            }
        return HttpResponse(json.dumps(result,cls=ComplexEncoder))
    else:
        if request.method == 'POST':
            pass
        else:
            return render(request,'bugcount.html')

def showimage(request):
    bug_image = models.SaveImage.objects.all()
    context = {
        'imgs':bug_image
    }
    return render(request,'showimage.html',context)
