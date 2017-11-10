# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render,redirect
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
# Create your views here.


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != ucpwd:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def login(request):
    return render(request, 'df_user/login.html')


def login_handle(request):
    context={'error_name': 0, 'error_passwd': 0, 'uname':'', 'upwd':'' }
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 查询用户信息
    userinfo = UserInfo.objects.filter(uname=uname)
    if len(userinfo)==1:#用户名是否存在
        s1 = sha1()
        s1.update(upwd)
        upwdsha = s1.hexdigest()
        realpass = userinfo[0].upwd
        red = HttpResponseRedirect('/user/info')
        if upwdsha == realpass:#密码验证
            request.session['user_id']=userinfo[0].id
            request.session['user_name'] = userinfo[0].uname
            return red
        else:
            context = {'error_name': 0, 'error_passwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'error_name': 1, 'error_passwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def user_center_info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    context={'title': '用户中心',
             'user_email': user_email,
             'user_name': request.session['user_name']}
    return render(request, 'df_user/user_center_info.html',context)


def user_center_order(request):
    return render(request,'df_user/user_center_order.html')


def user_center_site(request):
    # 收货地址的默认显示效果
    user_info=UserInfo.objects.get(id=request.session['user_id'])
    ushou=user_info.ushou
    uaddress=user_info.uaddress
    uyoubian=user_info.uyoubian
    uphone=user_info.uphone
    context={'ushou': ushou, 'uaddress': uaddress, 'uyoubian':uyoubian, 'uphone':uphone ,'uname': request.session['user_name']}
    print ('----->',context)
    return render(request,'df_user/user_center_site.html',context)


def user_center_site_handle(request):
    # 用户修改收货地址
    post = request.POST
    ushou = post.get('ushou')
    uphone = post.get('uphone')
    uyoubian = post.get('uyoubian')
    uaddress = post.get('uaddress')
    user = UserInfo.objects.get(id=request.session['user_id'])
    user.ushou = ushou
    user.uphone = uphone
    user.uyoubian = uyoubian
    user.uaddress = uaddress
    user.save()
    return redirect('/user/site/')





