# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render,redirect
from django.core.paginator import Paginator

def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodinfo_set.order_by('-gclick')[0:4]
    context = {'title': '商品首页',
               'type0': type0, 'type01':type01,
               'type1': type1, 'type11':type11,
               'type2': type2, 'type21':type21,
               'type3': type3, 'type31':type31,
               'type4': type4, 'type41':type41,
               'type5': type5, 'type51':type51,
               }
    print context
    return render(request, 'df_goods/index.html',context)


def detail(request,id):
    print id
    goods = GoodInfo.objects.get(id=int(id))
    goods.gclick = goods.gclick+1
    goods.save()
    news = goods.gtype.goodinfo_set.order_by('-id')[0:2]
    context = {"id":id, "goods":goods, "title":"商品详情", "news":news}
    print goods.id
    return render(request, 'df_goods/detail.html',context)


def list(request, tid, pindex, sort):  # typeid,当前第几页,排序依据
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodinfo_set.order_by('-id')[0:2]
    if sort == '1': #默认id排序,显示最新
        good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2': #按价格排序
        good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3': #按照点击量排序
        good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    paginator = Paginator(good_list,15)
    page = paginator.page(int(pindex))
    context = {
        'title':typeinfo.ttitle,
        'page':page,
        'paginator':paginator,
        'typeinfo':typeinfo,
        'sort':sort,
        'news':news
    }
    return render(request, 'df_goods/list.html',context)


