# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import JsonResponse
from df_user import user_decoration
from models import *
from df_goods.models import *

# Create your views here.
@user_decoration.login
def cart(request):
    uid = request.session['user_id']
    # 链表查询
    goods = GoodInfo.objects.filter(cartinfo__user_id=uid).values('id','gtitle','gpic','gprice','gunit','cartinfo__count','cartinfo__id')
    context={'goods': goods}
    return render(request,'df_cart/cart.html',context)

@user_decoration.login
def add(request,gid,count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    #查询是否有此商品,有则数量增加,没有就新增
    carts = CartInfo.objects.filter(user_id = uid, goods_id = gid)
    if len(carts)>=1:
        cart=carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/cart')


@user_decoration.login
def edit(request, cart_id, count):
    try:
        carts = CartInfo.objects.get(id=int(cart_id))
        carts.count=count
        carts.save()
        data={'ok':0}
    except Exception as e:
        data = {'ok': 1}
    return JsonResponse(data)


@user_decoration.login
def delete(request, cart_id):
    try:
        CartInfo.objects.filter(id=int(cart_id)).delete()
        data={'ok':0}
    except Exception as e:
        data = {'ok': 1}
    return JsonResponse(data)