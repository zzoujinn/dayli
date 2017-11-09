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
            return red
        else:
            print ('---------------------------------->' )
            context = {'error_name': 0, 'error_passwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'error_name': 1, 'error_passwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def user_center_info(request):
    return render(request, 'df_user/user_center_info.html')



