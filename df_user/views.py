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
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    s1 = sha1()
    s1.update(upwd)
    upwdsha = s1.hexdigest()
    userinfo = UserInfo.objects.filter(uname=uname)
    realpass = userinfo[0].upwd
    if upwdsha == realpass:
        return HttpResponseRedirect('/user/info')


def user_center_info(request):
    return render(request, 'df_user/user_center_info.html')



