import ast
import datetime
import os
import re
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from bysjapp import news
import json
import io
from .models import *
from .import check_code as CheckCode
from . import dbforshopcar as dsc
from django.conf import settings
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import *
# Create your views here.
# Create your views here.
def about(request):
    ison = request.session['ison']
    user=Users.objects.get(username=request.session['username'])
    return  render(request,'about.html',locals())
def index(request):
    petlist0 = Pets.objects.filter(pett="未出售").order_by('-vnum')
    request.session.setdefault('username', '')
    if not request.session['username']=='':
        user = Users.objects.get(username=request.session['username'])
    petlist = []
    for i in range(0, 4):
        petlist.append(petlist0[i])
    base_url = 'https://petssky.com/topics/news/world/'
    q = news.chongwu(base_url)
    filename = 'news.json'
    with open(filename, 'w', encoding='utf-8') as fp:
        # json.dump把python内置数据类型写入json文件
        # dump（内置类型的名称，文件流）
        json.dump(q.info_list, fp)
    info = []
    with open(filename, 'r', encoding='utf-8') as fp:
        # json.load从json'文件中读出json数据，得到一个list（python内置类型）
        info = json.load(fp)
    print(info)
    request.session.setdefault('ison', False)
    ison = request.session['ison']
    print(ison)
    return render(request, 'index.html', locals())

# 登录页面
def logIn(request):
    if request.method == 'GET':
        ison = request.session['ison']
        inl = 'http://'
        list = request.META.get('HTTP_REFERER')[7:].split('/')
        request.session['index'] = inl + list[0] + '/index/'
        return render(request, 'login.html',locals())

    elif request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        if username != '' and password != '':
            try:
                user = Users.objects.get(username=username)
            except Exception as e:
                print(e)
                errormsg = '用户名不存在！'
                return render(request, 'login.html', locals())
            else:
                print('1')
                if user.password !=password:
                    errormsg = '用户名或密码错误！'
                    return render(request, 'login.html', locals())
                else:
                    request.session['username'] = username
                    request.session['ison'] = True
                    return redirect(request.session['index'] ,'/')
# 注册页面
def register(request):
    if request.method == 'GET':
        ison = request.session['ison']
        inl = 'http://'
        list = request.META.get('HTTP_REFERER')[7:].split('/')
        request.session['index'] = inl + list[0] + '/index/'
        return render(request,'register.html',locals())
    elif request.method == 'POST':
        username=request.POST.get("username", '')
        password1=request.POST.get("password1", '')
        password2=request.POST.get("password2", '')
        birth=request.POST.get("birth","")
        sex=request.POST.get("sex","")
        checkcode=request.POST.get("checkcode", '')
        if checkcode == request.session['CheckCode'].lower():
            if password1==password2:
                if Users.objects.filter(username=username).exists() == False:

                    user = Users.objects.create(username=username, password=password1,birth=birth,sex=sex)
                    user.save()
                    user0 = Users.objects.get(username=username)
                    car=WhosCar.objects.create(user=user0,carname="user"+str(user0.userid),useradress="",phone="")
                    car.save()
                    dsc.createtable("user"+str(user0.userid))
                    request.session['username'] = username
                    request.session['ison']=True
                    # 重定向跳转
                    return redirect(request.session['index'])
                else:
                    emsg="用户名已存在"
                    return render(request, 'register.html',locals())
            else:
                emsg = "两次密码不一致"
                return render(request, 'register.html', locals())
        else:
            emsg = "验证码不正确"
            return render(request, 'register.html', locals())

def logOut(request):
    request.session['ison']=False
    ison = request.session['ison']
    return redirect(request.META['HTTP_REFERER'])
def check_code(request):
    stream = io.BytesIO()
    # img图片对象,code在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())
def pet(request,speci):
    petlist=[]
    user = Users.objects.get(username=request.session['username'])
    if speci=='all':
        petlist=Pets.objects.filter(pett='未出售')
    else:
        petlist=Pets.objects.filter(speci=speci,pett='未出售')
    page_list=getPage(request,petlist)
    ison = request.session['ison']
    return render(request,'pets.html',locals())

def informationcheck(request):
    if request.method=='GET':
        username = request.session['username']
        user = Users.objects.get(username=username)
        return  render(request,'information.html',locals())
    elif request.method == 'POST':
        username = request.session['username']
        user = Users.objects.get(username=username)
        user.username=request.POST.get('username')
        user.sex=request.POST.get('sex')
        if not request.POST.get('birth')=='':
            user.birth=request.POST.get('birth')
        if not request.POST.get('pwb')=='':
            if request.POST.get('pwb')==user.password:
                user.password=request.POST.get('pwn')
            else:
                emsg="与原密码不一致"
                return render(request, 'information.html', locals())
        img = request.FILES.get('head')


        if img:
            if img.name[-4:]=='.png':
                hedn = str(user.userid) + datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '.png'
                print(hedn)
                img_path=os.path.join(os.path.join(settings.UPLOADFILES_DIRS,hedn))
                print(img_path)
                f = open(img_path, 'wb')
                for i in img.chunks():
                    f.write(i)
                    f.close()
                user.head=hedn
            else:
                emsg="请上传png格式图片"
                return render(request, 'information.html', locals())
        user.save()
        return redirect(request.META['HTTP_REFERER'])
def personp(request,type):
    if type=="dem":
        username = request.session['username']
        user = Users.objects.get(username=username)
        try:
            demlist=Developments.objects.filter(user=user).order_by('-create_date')
            demn=len(demlist)
            page_list=getPage(request,demlist)
        except Exception as e:
            print(e)

    elif type=="sc":
        username = request.session['username']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        adres = car.useradress
        phone = car.phone
        goodslist = dsc.showall(car.carname)
        print(goodslist)
        goodlist = []
        ap = 0.0
        gd = {}
        for good in goodslist:
            gdd = Goods.objects.get(goodsid=good[0])
            gd.update(gid=gdd.goodsid, gn=gdd.goodname, gp=gdd.goodprice)
            ap = ap + good[1] * gdd.goodprice
            print(gd)
            gd.update(gnum=good[1])
            print(gd)
            goodlist.append(gd)
            gd = {}
    elif type=="list":
        username = request.session['username']
        user = Users.objects.get(username=username)
        list0=Orders.objects.filter(userid=user)
        list1=[]
        gd={}
        bigdic={}
        alllist=[]
        for li in list0:
            if li.type=='商品':
                list2=ast.literal_eval(li.oderitem)
                i=0
                for l in list2:
                    dic=ast.literal_eval(str(l))
                    i=i+1
                    gdd=Goods.objects.get(goodsid=dic['gid'])
                    gd.update(gname=gdd.goodname,gnum=dic['gnum'],gp=dic['gp'],bk=i%2)
                    list1.append(gd)
                    gd={}
                bigdic.update(oderid=li.oderid,time=li.time,oderitem=list1,type=li.type,price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)

            elif li.type=='宠物':
                pt={}
                pet=Pets.objects.get(petid=li.oderitem)
                pt.update(ptn=pet.petname,pts=pet.petsex,ptid=pet.petid,sp=pet.speci)
                bigdic.update(oderid=li.oderid, time=li.time, oderitem=pt, type=li.type,price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)
                pt={}
            alllist.append(bigdic)
            bigdic = {}
        print(alllist)
    return render(request,'personspace.html',locals())
def shop(request,goodtype):
    if request.method=='GET':
        goodlist=[]
        if goodtype=='all':
            goodlist=Goods.objects.all()
        elif goodtype=='serch':
            try:
                serc=request.session['serch']
                goodlist = Goods.objects.filter(goodname__contains=serc)
            except Exception as e:
                print(e)
        else:
            goodlist=Goods.objects.filter(goodtype=goodtype)
        page_list = getPage(request, goodlist)
        ison = request.session['ison']
        user=Users.objects.get(username=request.session['username'])
        return render(request,'shop.html',locals())
    elif request.method=='POST':
        serc=request.POST.get("serch",'')
        print(serc)
        request.session['serch']=serc
        try:
            serc = request.session['serch']
            goodlist = Goods.objects.filter(goodname__contains=serc)
        except Exception as e:
            print(e)
        user = Users.objects.get(username=request.session['username'])
        ison = request.session['ison']
        return render(request,'shop.html',locals())
def singlepet(request,pid):
    if request.method=='GET':
        ison = request.session['ison']
        pet = Pets.objects.get(petid=pid)
        pet.vnum=pet.vnum+1
        pet.save()
        user = Users.objects.get(username=request.session['username'])
        return render(request, 'singlepet.html', locals())
    elif request.method=='POST':
        adres=request.POST.get('adres')
        phone=request.POST.get('phone')
        id=request.POST.get('id')
        pet=Pets.objects.get(petid=id)
        username = request.session['username']
        user = Users.objects.get(username=username)
        now = datetime.datetime.now()
        ode = Orders.objects.create(oderid="%d%d%d%d%d%d%d%s" % (
        now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond, user.userid), userid=user,
                                    totalprice=pet.petprice, oderitem=pet.petid, useradress=adres, phone=phone, type='宠物')
        ode.save()
        pet.pett='已出售'
        pet.save()
        return render(request, 'zhongzhuan.html', locals())
def singlep(request,username):
    user1 = Users.objects.get(username=username)
    user = Users.objects.get(username=request.session['username'])
    username0 = request.session['username']
    user0 = Users.objects.get(username=username0)
    if Follow.objects.filter(usertof=user1, usergetfid=user0.userid).count() == 0:
        if Follow.objects.filter(usertof=user0, usergetfid=user1.userid).count() == 0:
            ftxt="关注"
            ficon="wf"
        else:
            ftxt="已关注"
            ficon="yf"
    else:

        if Follow.objects.filter(usertof=user0, usergetfid=user1.userid).count() == 0:
            ftxt="关注"
            ficon="bf"
        else:
            ftxt="互相关注"
            ficon="hxf"
    ison=request.session['ison']
    demlist0 = Developments.objects.filter(user=user1.userid).order_by('-create_date')
    demlist = []
    dem = {}
    for dm in demlist0:
        dem.update(username=dm.username, create_time=dm.create_time, dmenttext=dm.dmenttext, dmentid=dm.dmentid,
                   likeed=False, likenum=dm.likenum)
        if Likes.objects.filter(userid=user0, dmentid=dm).count() == 1:
            dem.update(likeed=True)
        demlist.append(dem)
        dem = {}
    page_list = getPage(request, demlist)
    return render(request, 'singleuser.html', locals())
def singleg(request,gid):
    if request.method=='GET':
        user = Users.objects.get(username=request.session['username'])
        ison = request.session['ison']
        good=Goods.objects.get(goodsid=gid)
        txtlist=good.goodtext.split('\n')
        return render(request, 'singlegoods.html', locals())
    elif request.method=='POST':
        gnum=request.POST.get("gnum")
        username = request.session['username']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        dsc.insertg(car.carname, gid, gnum, "2")
        return redirect(request.META['HTTP_REFERER'])
def demp(request):
    demlist=[]
    ison = request.session['ison']
    if ison:
        username= request.session['username']
        user = Users.objects.get(username=username)
        fn=len(Follow.objects.filter(usertof=user))
        fsn=len(Follow.objects.filter(usergetfid=user.userid))

        demlist0 = Developments.objects.all().order_by('-create_date')
        demlist = []
        dem = {}
        for dm in demlist0:
            dem.update(username=dm.username,create_time=dm.create_time,dmenttext=dm.dmenttext,dmentid=dm.dmentid,likeed=False,likenum=dm.likenum)
            if Likes.objects.filter(userid=user, dmentid=dm).count() == 1:
                dem.update(likeed=True)
            demlist.append(dem)
            dem={}
        if request.method == 'POST':
            if ison:
                user = Users.objects.get(username=username)
                dst = request.POST.get("dst", '')
                dem = Developments.objects.create(user=user, dmenttext=dst,username=username)
                dem.save()
                return redirect(request.META['HTTP_REFERER'])
    else:
        demlist0=Developments.objects.all().order_by('-create_date')
        demlist=[]
        dem={}
        for dm in demlist0:
            dem.update(username=dm.username,create_time=dm.create_time,dmenttext=dm.dmenttext,dmentid=dm.dmentid,likeed=False,likenum=dm.likenum)
            demlist.append(dem)
            dem = {}
    demlist1=[]
    comlist=[]
    for dem in demlist:
        print(dem)
        comlist=Comment.objects.filter(dment=dem["dmentid"]).order_by('-create_time')
        print(comlist)
        dem.update(comlist=comlist)
        comlist=[]
        demlist1.append(dem)
    page_list = getPage(request, demlist1)
    return render(request, 'demp.html', locals())
def like(request):

    if request.method == 'POST':

        did = request.POST.get("did")
        username = request.session['username']
        user=Users.objects.get(username=username)
        dm = Developments.objects.get(dmentid=did)
        print(did)
        try:
            if Likes.objects.filter(userid=user,dmentid=dm).count()==0:

                like=Likes.objects.create(userid=user,dmentid=dm,)
                like.save()
                dm.likenum=dm.likenum+1
                dm.save()
                if not dm.user == user:
                    dm.user.mnum = dm.user.mnum + 1
                    js=ast.literal_eval(dm.user.newmessage)
                    js["like"].append({"useid":like.userid.userid,"dmentid":like.dmentid.dmentid})
                    dm.user.newmessage=js
                    dm.user.save()
                # InfoKeep.save()
                return JsonResponse({"success":True,"type":"1","likenum":dm.likenum})
            else:
                Likes.objects.filter(userid=user, dmentid=dm).delete()
                dm.likenum=dm.likenum-1
                dm.save()

                return JsonResponse({"success": True,"type":"2","likenum":dm.likenum})
        except Exception as e:
            print(e)
            return JsonResponse({"success":False})
    else:
        return JsonResponse({"success":False})
def deletd(request):
    if request.method=='POST':
        did=request.POST.get("did")
        dem=Developments.objects.get(dmentid=did)
        dem.delete()
        return JsonResponse({"success": True})
def deletc(request):
    if request.method=='POST':
        did=request.POST.get("did")
        com=Comment.objects.get(cid=did)
        com.delete()
        return JsonResponse({"success": True})
def addg(request):
    if request.method == 'POST':
        gid=request.POST.get("gid")
        username = request.session['username']
        user = Users.objects.get(username=username)
        car=WhosCar.objects.get(user=user.userid)
        dsc.insertg(car.carname,gid,1,"2")
        return JsonResponse({"success": True})
def deletg(request):
    if request.method=='POST':
        gid=request.POST.get("gid")
        username = request.session['username']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        dsc.delet(car.carname,gid)
        return JsonResponse({"success": True})
def shopcar(request):
    if request.method=='GET':
        username = request.session['username']
        ison=request.session['ison']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        adres=car.useradress
        phone=car.phone
        goodslist= dsc.showall(car.carname)
        print(goodslist)
        goodlist=[]
        ap=0.0
        gd={}
        for good in goodslist:
            gdd=Goods.objects.get(goodsid=good[0])
            gd.update(gid=gdd.goodsid,gn=gdd.goodname,gp=gdd.goodprice)
            ap=ap+good[1]*gdd.goodprice
            print(gd)
            gd.update(gnum=good[1])
            print(gd)
            goodlist.append(gd)
            gd={}
        print(goodlist)
        print(ap)
        return render(request, 'shopcar.html', locals())
    elif request.method=='POST':
        fom=[]
        emp={}
        gum=request.POST.getlist("goodnum")
        gid=request.POST.getlist("gid")
        ap = request.POST.get("ap")
        print(ap)
        for i in range(0,len(gid)):
            print(i)
            if int(gum[i])<0:
                gum[i]=0
            emp.update(gid=int(gid[i]),gnum=int(gum[i]))
            fom.append(emp)
            emp={}
        print(fom)
        username = request.session['username']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        car.useradress= request.POST.get("adres")
        car.phone= request.POST.get("phone")
        car.save()
        for i in range(0,len(fom)):
            dsc.insertg(car.carname,fom[i]['gid'],fom[i]['gnum'],'1')
        return redirect(request.META['HTTP_REFERER'])
def oder(request):
    if request.method=='POST':
        fom = []
        emp = {}
        gum = request.POST.getlist("goodnum")
        gid = request.POST.getlist("gid")
        ap=request.POST.get("ap")
        useradress = request.POST.get("adres")
        phone = request.POST.get("phone")
        print(ap)
        for i in range(0, len(gid)):
            gd=Goods.objects.get(goodsid=gid[i])
            if gd.goodnum>=int(gum[i]):
                gd.goodnum=gd.goodnum-int(gum[i])
            else:
                gum[i]=gd.goodnum
                gd.goodnum=0
            gd.save()
            emp.update(gid=int(gid[i]), gnum=int(gum[i]),gp=gd.goodprice)
            fom.append(emp)
            emp = {}
        print(fom)
        username = request.session['username']
        user = Users.objects.get(username=username)
        car = WhosCar.objects.get(user=user.userid)
        car.useradress = request.POST.get("adres")
        car.phone = request.POST.get("phone")
        car.save()
        dsc.clean(car.carname)
        now = datetime.datetime.now()
        ode=Orders.objects.create(oderid="%d%d%d%d%d%d%d%s"%(now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond,user.userid),userid=user,totalprice=ap,oderitem=fom,useradress=useradress,phone=phone,type='商品')
        ode.save()
        return render(request, 'zhongzhuan.html', locals())
def getPage(request, list):
    paginator = Paginator(list, 8)
    try:
        page = int(request.GET.get('page', 1))
        list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        list = paginator.page(1)

    return list
def upload_lg(request):
    if request.method=='GET':
        request.session.setdefault('sp_ison', False)
        request.session.setdefault('sp_username', '未知')
        sp_ison=request.session['sp_ison']
        username = request.session['sp_username']
        whc = 'good'
        opty = 'add'
        return render(request, 'upload.html', locals())
    elif request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username != '' and password != '':
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request,user)
                    print("登录成功！")
                    request.session['sp_ison']=True
                    request.session['sp_username'] = user.username
                    sp_ison=True
                    whc='good'
                    opty='add'
                    return render(request,'upload.html',locals())
                else:
                    print(username,password,user)
                    errormsg = '用户名或密码错误！'
                    return render(request,'upload.html',locals())
        else:
            errormsg = '用户名或密码未填写！'
            return render(request, 'upload.html', locals())
def upload(request,whc,optype):
    if request.method=='POST':
        if whc=='pet' and optype=='add':
            pn=request.POST.get('pname','')
            psex=request.POST.get('psex')
            pbir=request.POST.get('pbirth')
            spe=request.POST.get('speci')
            pprice=request.POST.get('pprice')
            img = request.FILES.get('pimg')
            print(pn,psex,pbir,spe,img)
            if img:
                if img.name[-4:] == '.png':
                    pet=Pets.objects.create(petname=pn,petsex=psex,petbirth=pbir,speci=spe,petprice=pprice)
                    pet.save()
                    imgn = pn+ str(pet.petid)+ '.png'

                    img_path = os.path.join(os.path.join(settings.UPLOADFILES_PET, imgn))
                    print(img_path)
                    f = open(img_path, 'wb')
                    for i in img.chunks():
                        f.write(i)
                        f.close()
                    sp_ison = request.session['sp_ison']
                    username = request.session['sp_username']
                    opty = optype
                    emsg="上架成功"
                    return render(request, 'upload.html', locals())
                else:
                    emsg = "请上传png格式图片"
                    sp_ison=request.session['sp_ison']
                    username = request.session['sp_username']
                    opty=optype
                    return render(request, 'upload.html', locals())
            else:
                emsg="尚未选择图片"
                sp_ison = request.session['sp_ison']
                username = request.session['sp_username']
                opty = optype
                return render(request, 'upload.html', locals())
        elif whc=='pet' and optype=='change':
            pidl=request.POST.getlist('pid')
            pet={}
            petlist={}
            f=False
            for pid in pidl:
                pt=Pets.objects.get(petid=pid)
                try:

                    if not pt.petname==request.POST.get('pname'+pid):
                        print(pt.petname,request.POST.get('pname'+pid))
                        ptrn=pt.petname
                        f=True
                    else:
                        f=False
                    pt.petname=request.POST.get('pname'+pid)
                    pt.petsex=request.POST.get('psex'+pid)
                    pt.pett=request.POST.get('ppt'+pid)
                    pt.petprice=request.POST.get('pprc'+pid)
                    pt.petbirth=request.POST.get('pbir'+pid)
                    pt.speci=request.POST.get('speci'+pid)
                    pt.save()
                except Exception as e:
                    print(e)
                if f:
                    os.rename(
                        os.path.join(os.path.join(settings.UPLOADFILES_PET, ptrn + str(pid) + '.png')),
                        os.path.join(os.path.join(settings.UPLOADFILES_PET,
                                                  request.POST.get('pname' + pid) + str(pid) + '.png')))
                    print('chan')
                if request.FILES.get('img'+pid):

                    if request.FILES.get('img'+pid).name[-4:] == '.png':

                        imgn = pt.petname + str(pid) + '.png'

                        img_path = os.path.join(os.path.join(settings.UPLOADFILES_PET, imgn))
                        print(img_path)
                        f = open(img_path, 'wb')
                        for i in request.FILES.get('img'+pid).chunks():
                            f.write(i)
                            f.close()

                    else:
                        emsg = "请上传png格式图片"
                        sp_ison = request.session['sp_ison']
                        username = request.session['sp_username']
                        opty = optype
                        return render(request, 'upload.html', locals())
                pet["pne"]=request.POST.get('pname'+pid)
                pet["psx"]=request.POST.get('psex'+pid)
                pet["pbir"]=request.POST.get('pbir'+pid)
                pet["spc"]=request.POST.get('speci'+pid)
                pet["img"]=request.FILES.get('img'+pid)
                petlist[pid]=pet
                pet={}
            print(petlist,datetime.datetime.now())
            f=open("oprecord.txt",'a',encoding='gbk')
            f.write(str(petlist)+str(datetime.datetime.now()))
            sp_ison = request.session['sp_ison']
            username = request.session['sp_username']
            opty = optype
            emsg = "修改成功"
            return render(request, 'upload.html', locals())
        elif whc=='good' and optype=='add':
            gn=request.POST.get('gname','')
            gnum=request.POST.get('gnum','')
            gprice=request.POST.get('gprice','')


            gty=request.POST.get('gtype')
            gimg = request.FILES.get('gimg')
            gtext=request.POST.get('gtext','')
            print(gn,gnum,gprice,gtext,gty,gimg)
            if gimg:

                if gimg.name[-4:] == '.png':
                    good=Goods.objects.create(goodname=gn,goodnum=gnum,goodprice=gprice,goodtype=gty,goodtext=gtext)
                    good.save()
                    imgn = 'good'+ str(good.goodsid)+ '.png'

                    img_path = os.path.join(os.path.join(settings.UPLOADFILES_GOOD, imgn))
                    print(img_path)
                    f = open(img_path, 'wb')
                    for i in gimg.chunks():
                        f.write(i)
                        f.close()
                    sp_ison = request.session['sp_ison']
                    username = request.session['sp_username']
                    opty = optype
                    emsg="上架成功"
                    return render(request, 'upload.html', locals())
                else:
                    emsg = "请上传png格式图片"
                    sp_ison=request.session['sp_ison']
                    username = request.session['sp_username']
                    opty=optype

                    return render(request, 'upload.html', locals())
            else:
                emsg="尚未选择图片"
                sp_ison = request.session['sp_ison']
                username = request.session['sp_username']
                opty = optype
                return render(request, 'upload.html', locals())
        elif whc=='good' and optype=='change':
            gidl=request.POST.getlist('gid')
            good={}
            goodlist={}
            for gid in gidl:
                gd=Goods.objects.get(goodsid=gid)
                try:
                    gd.goodname=request.POST.get('gname'+gid)
                    gd.goodnum=request.POST.get('gnum'+gid)
                    gd.goodprice=request.POST.get('gprc'+gid)
                    gd.goodtype=request.POST.get('gty'+gid)
                    gd.goodtext=request.POST.get('gtxt'+gid)
                    print(gd.goodtext)
                    gd.save()
                except Exception as e:
                    print(e)

                if request.FILES.get('img'+gid):

                    if request.FILES.get('img'+gid).name[-4:] == '.png':

                        imgn = 'good' + str(gid) + '.png'

                        img_path = os.path.join(os.path.join(settings.UPLOADFILES_GOOD, imgn))
                        print(img_path)
                        fo = open(img_path, 'wb')
                        for i in request.FILES.get('img'+gid).chunks():
                            fo.write(i)
                            fo.close()

                    else:
                        emsg = "请上传png格式图片"
                        sp_ison = request.session['sp_ison']
                        username = request.session['sp_username']
                        opty = optype
                        return render(request, 'upload.html', locals())
                good["gne"]=request.POST.get('gname'+gid)
                good["gnum"]=request.POST.get('gnum'+gid)
                good["gprc"]=request.POST.get('gprc'+gid)
                good["gty"]=request.POST.get('gty'+gid)
                good["gtxt"]=request.POST.get('gtxt'+gid)
                good["img"]=request.FILES.get('img'+gid)
                goodlist[gid]=good
                good={}
            print(goodlist,datetime.datetime.now())
            f=open("oprecord.txt",'a',encoding='gbk')
            f.write(str(goodlist)+str(datetime.datetime.now()))
            sp_ison = request.session['sp_ison']
            username = request.session['sp_username']
            opty = optype
            emsg = "修改成功"
            return render(request, 'upload.html', locals())
def upload_sel(request):
    if request.method=='POST':
        sp_ison=request.session['sp_ison']
        username = request.session['sp_username']
        if sp_ison:
            opty=request.POST.get('optype','')
            whc=request.POST.get('whc','')
            print(opty)
            print(whc)
            if opty=='change':
                if whc=='good':
                    goodlist=Goods.objects.all()
                    page_list = getPage(request, goodlist)
                elif whc=='pet':
                    petlist=Pets.objects.all()
                    pattern = re.compile(r'\d+')
                    for pet in petlist:
                        m=pattern.findall(str(pet.petbirth))
                        pet.petbirth=m[0]+'-'+m[1]+'-'+m[2]
                    page_list = getPage(request, petlist)
            if whc=='oder':
                if opty=='add':
                    list0 = Orders.objects.all()
                    list1 = []
                    gd = {}
                    bigdic = {}
                    alllist = []
                    for li in list0:
                        if li.type == '商品':
                            list2 = ast.literal_eval(li.oderitem)
                            for l in list2:
                                dic = ast.literal_eval(str(l))

                                gdd = Goods.objects.get(goodsid=dic['gid'])
                                gd.update(gname=gdd.goodname, gnum=dic['gnum'], gp=dic['gp'])
                                list1.append(gd)
                                gd = {}
                            bigdic.update(oderid=li.oderid, time=li.time, oderitem=list1, type=li.type,
                                          price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)

                        elif li.type == '宠物':
                            pt = {}
                            pet = Pets.objects.get(petid=li.oderitem)
                            pt.update(ptn=pet.petname, pts=pet.petsex, ptid=pet.petid, sp=pet.speci)
                            bigdic.update(oderid=li.oderid, time=li.time, oderitem=pt, type=li.type,
                                          price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)
                            pt = {}
                        alllist.append(bigdic)
                        bigdic = {}
                    page_list=getPage(request,alllist)
                elif opty=='change':
                    list0=Orders.objects.filter(oders='未发货')
                    list1 = []
                    gd = {}
                    bigdic = {}
                    alllist = []
                    for li in list0:
                        if li.type == '商品':
                            list2 = ast.literal_eval(li.oderitem)
                            for l in list2:
                                dic = ast.literal_eval(str(l))

                                gdd = Goods.objects.get(goodsid=dic['gid'])
                                gd.update(gname=gdd.goodname, gnum=dic['gnum'], gp=dic['gp'])
                                list1.append(gd)
                                gd = {}
                            bigdic.update(oderid=li.oderid, time=li.time, oderitem=list1, type=li.type,
                                          price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)

                        elif li.type == '宠物':
                            pt = {}
                            pet = Pets.objects.get(petid=li.oderitem)
                            pt.update(ptn=pet.petname, pts=pet.petsex, ptid=pet.petid, sp=pet.speci)
                            bigdic.update(oderid=li.oderid, time=li.time, oderitem=pt, type=li.type,
                                          price=li.totalprice,useradress=li.useradress,phone=li.phone,oders=li.oders)
                            pt = {}
                        alllist.append(bigdic)
                        bigdic = {}
                    page_list = getPage(request, alllist)
            return render(request,'upload.html',locals())
        else:
            return JsonResponse({"e": "非法请求"})
def sp_logOut(request):
    request.session['sp_ison']=False
    sp_ison = request.session['sp_ison']
    inl = 'http://'
    list = request.META.get('HTTP_REFERER')[7:].split('/')
    return redirect(inl + list[0] + '/admin/upload/',locals())
def oder_up(request,oid):
    ode=Orders.objects.get(oderid=oid)
    sp_ison = request.session['sp_ison']
    username = request.session['sp_username']
    ode.useradress=request.POST.get("adres")
    ode.phone=request.POST.get("phone")
    ode.oders=request.POST.get("odes")
    ode.save()
    opty = "add"
    whc="oder"
    emsg = "修改成功"
    return render(request, 'upload.html', locals())
def singnew(request,ns):
    ison = request.session['ison']
    new=news.news(str(ns))
    title=new.title
    body=new.info
    return render(request, 'single.html', locals())
def follow(request):
    if request.method == 'POST':
        uid = request.POST.get("uid")
        username = request.session['username']
        user=Users.objects.get(username=username)
        user0=Users.objects.get(userid=uid)
        if request.session['ison']:
            try:
                if Follow.objects.filter(usertof=user,usergetfid=user0.userid).count()==0:
                    Follow.objects.create(usertof=user, usergetfid=user0.userid)
                    if Follow.objects.filter(usertof=user0,usergetfid=user.userid).count()==0:
                        user0.mnum=user0.mnum+1
                        js=ast.literal_eval(user0.newmessage)
                        js["follow"].append(user.userid)
                        user0.newmessage=js
                        user0.save()
                        return JsonResponse({"success":True,"op":"add","txt":"已关注","type":"1"})
                    else:
                        user0.mnum = user0.mnum + 1
                        js = ast.literal_eval(user0.newmessage)
                        js["follow"].append(user.userid)
                        user0.newmessage = js
                        user0.save()
                        return JsonResponse({"success": True, "op": "add", "txt": "互相关注","type":"2"})
                else:
                    Follow.objects.filter(usertof=user,usergetfid=user0.userid).delete()
                    if Follow.objects.filter(usertof=user0, usergetfid=user.userid).count() == 0:
                        return JsonResponse({"success": True,"op":"del","txt":"关注","type":"3"})
                    else:
                        return JsonResponse({"success": True, "op": "del", "txt": "关注","type":"4"})
            except Exception as e:
                print(e)
                return JsonResponse({"success":False})
        else:
            return JsonResponse({"success": True, "type": "5"})
    else:
        return JsonResponse({"success":False})
def serv(request):
    ison = request.session['ison']
    return render(request, 'service.html', locals())
def map(request):
    return render(request, 'map.html')
def addcom(request,did):
    username=request.session['username']
    user = Users.objects.get(username=username)

    dment=Developments.objects.get(dmentid=did)

    dst = request.POST.get("dst", '')
    com=Comment.objects.create(user=user,ctext=dst,dment=dment)
    com.save()
    if not dment.user==user:
        dment.user.mnum=dment.user.mnum+1
        print(dment.user.newmessage)
        js = ast.literal_eval(dment.user.newmessage)
        js["comment"].append(com.cid)
        dment.user.newmessage=js
        dment.user.save()
    return redirect(request.META['HTTP_REFERER'])
def message(request):
    ison = request.session['ison']
    username = request.session['username']
    user = Users.objects.get(username=username)
    print(user.newmessage)
    js = ast.literal_eval(user.newmessage)
    list_like=[]
    list_comment=[]
    list_follow=[]
    for like in js["like"]:
        l=Likes.objects.get(userid=Users.objects.get(userid=like["useid"]),dmentid=Developments.objects.get(dmentid=like["dmentid"]))
        list_like.append(l)
    for com in js["comment"]:
        c=Comment.objects.get(cid=com)
        list_comment.append(c)
    for fol in js["follow"]:
        f=Users.objects.get(userid=fol)
        list_follow.append(f)
    lenl=len(list_like)
    lenc = len(list_comment)
    lenf = len(list_follow)
    user.mnum=0
    user.newmessage={"like":[],"comment":[],"follow":[]}
    user.save()
    return render(request, 'message.html', locals())
def analysis(request):
    femalenum=len(Users.objects.filter(sex="女"))
    malenum=len(Users.objects.filter(sex="男"))
    usernum=femalenum+malenum
    Pie().add("", [["男",malenum ],["女",femalenum]]).set_colors(["blue", "pink"]).set_global_opts(title_opts=opts.TitleOpts(title="用户男女比例")).render(os.path.join(settings.UPLOADFILES_TABLE, "user_sex_pietable.html"))
    list0 = Orders.objects.all().order_by('time')
    list_gt=['宠物食品','宠物玩具','清洁用品','药品','宠物衣物']
    list_num=[0,0,0,0,0]
    list_time=[]
    list_sell=[]
    for li in list0:
        if li.type == '商品':
            list2 = ast.literal_eval(li.oderitem)
            for l in list2:
                dic = ast.literal_eval(str(l))
                gdd = Goods.objects.get(goodsid=dic['gid'])
                list_num[list_gt.index(gdd.goodtype)]=list_num[list_gt.index(gdd.goodtype)]+dic['gnum']
        if not str(li.time)[:10] in list_time:
            list_time.append(str(li.time)[:10])
        if len(list_time)>len(list_sell):
            list_sell.append(li.totalprice)
        else:
            list_sell[list_time.index(str(li.time)[:10])]=list_sell[list_time.index(str(li.time)[:10])]+li.totalprice
    print(list_sell)
    for i in range(1,len(list_sell)):
        list_sell[i]=list_sell[i]+list_sell[i-1]
    Bar().add_xaxis(list_gt).add_yaxis("销售量",list_num).set_global_opts(title_opts=opts.TitleOpts(title="各商品销售量", subtitle="")).render(os.path.join(settings.UPLOADFILES_TABLE, "sell_bartable.html"))
    Line().add_xaxis(list_time).add_yaxis("销售总额", list_sell, areastyle_opts=opts.AreaStyleOpts(opacity=0.5)).set_global_opts(title_opts=opts.TitleOpts(title="销售总额面积图")).render(os.path.join(settings.UPLOADFILES_TABLE, "sell_linetable.html"))
    sp_ison = request.session['sp_ison']
    username = request.session['sp_username']
    return render(request, 'Analysis.html', locals())

def user_sex_pietable(request):
    return render(request, 'user_sex_pietable.html', locals())


def sell_bartable(request):
    return render(request, 'sell_bartable.html', locals())


def sell_linetable(request):
    return render(request, 'sell_linetable.html', locals())
#python manage.py makemigrations
#python manage.py migrate