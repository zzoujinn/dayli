# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render
from django.db import transaction
from df_goods.models import *
from df_cart.models import *
from df_user.models import *
import datetime
import uuid
# Create your views here.

# 获取当前时间的函数
def curtime():
    cur = datetime.datetime.now()
    return cur



'''
使用事务保证以下操作的完整性transaction
1.创建订单对象
# 2.判断商品的库存
3.创建详单对象
# 4.修改商品库存
5.删除购物车
'''


def order(request):
    cart_id = request.GET.getlist('cart_id')  #一键多值
    print cart_id
    goodlist=[]
    totalPrice = 0
    oid = uuid.uuid1()
    for id in cart_id:
        goodsinfo = GoodInfo.objects.filter(cartinfo__id=int(id)).values('gprice', 'cartinfo__count')
        price = goodsinfo[0]['gprice'] * goodsinfo[0]['cartinfo__count']
        totalPrice += price
    cur = curtime()
    orderinfo = OrderInfo()
    orderinfo.odate = cur
    orderinfo.oid = oid
    orderinfo.ototal = totalPrice
    orderinfo.user_id = request.session['user_id']
    userinfo = UserInfo.objects.get(id=request.session['user_id'])
    orderinfo.oaddress = userinfo.uaddress
    orderinfo.save()
    number = 1
    for id in cart_id:
        goodsinfo = GoodInfo.objects.filter(cartinfo__id=int(id)).values('id','gtitle','gpic','gprice','gunit','cartinfo__count','cartinfo__id','cartinfo__user_id')
        orderdetail = OrderDetailInfo()
        price = goodsinfo[0]['gprice'] * goodsinfo[0]['cartinfo__count']
        orderdetail.price = price
        orderdetail.count = goodsinfo[0]['cartinfo__count']
        orderdetail.goods_id = goodsinfo[0]['id']
        orderdetail.order_id = oid
        orderdetail.save()
        goodsinfo[0]['num'] = number
        a= goodsinfo[0]
        a['num']=number
        number+=1
        print ('goodinfo----------------------------------->',goodsinfo[0])
        goodlist.append(a)
        print goodlist
        # CartInfo.objects.filter(cartinfo__id=int(id)).delete()

    context={
        'title': '提交订单',
        'goodsinfo': goodlist,
        'uaddress': userinfo.uaddress,
        'uphone': userinfo.uphone,
        'ushou': userinfo.ushou,
    }
    return render(request, 'df_order/place_order.html', context)

