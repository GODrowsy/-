from django.shortcuts import render, get_object_or_404
import json
import random

import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def findall(request):
    if request.method == 'GET':
        result = WorkDate.objects.all()
        print(result[0].name)
        arr = []
        for i in result:
            content = ({"id": i.name_id, "name": i.name, "firsttime": i.firsttime,
                       "lasttime": i.lasttime, "date": i.date})
            print(type(content))
            arr.append(content)

        print(json.dumps(arr, cls=DateEncoder))
        # print(type(json.dumps(arr)))
        return HttpResponse(json.dumps(arr, cls=DateEncoder))


def find(request):
    if request.method == 'GET':
        id = request.GET['id']
        result = WorkDate.objects.filter(name_id=id)
        arr = []
        for i in result:
            content = ({"id": i.name_id, "name": i.name, "firsttime": i.firsttime,
                       "lasttime": i.lasttime, "date": i.date})
            print(type(content))
            arr.append(content)

        print(json.dumps(arr, cls=DateEncoder))
        # print(type(json.dumps(arr)))
        return HttpResponse(json.dumps(arr, cls=DateEncoder))





def wxAdSign(request):
    if request.method == 'GET':
        id = request.GET['id']
        password = request.GET['password']
        result = AdminDate.objects.filter(id=id)
        if len(result) != 0:
            if result[0].password == ' ' + password:
                return HttpResponse(json.dumps({'name': result[0].name, 'code': 'True'}))
            else:
                return HttpResponse(json.dumps({'name': '', 'code': 'False'}))
        else:
            return HttpResponse(json.dumps({'name': '', 'code': 'False'}))


def wxCaSign(request):
    if request.method == 'GET':
        id = request.GET['id']
        password = request.GET['password']
        result = CashierDate.objects.filter(id=id)
        if len(result) != 0:
            if result[0].password == ' ' + password:
                return HttpResponse(json.dumps({'name': result[0].name, 'code': 'True'}))
            else:
                return HttpResponse(json.dumps({'name': '', 'code': 'False'}))
        else:
            return HttpResponse(json.dumps({'name': '', 'code': 'False'}))


def post(request):
    if request.method == 'GET':
        return render(request, 'post.html')
    elif request.method == 'POST':
        id = request.POST.get('id', '')
        # 查询name = tom1的数据
        result = WorkDate.objects.filter(name_id=id)
        """
        result为<class 'django.db.models.query.QuerySet'>的对象
        需要进行数据处理
        """
        arr = []
        for i in result:
            content = {'工号': i.name_id, '姓名': i.name, '工作开始时间': i.firsttime,
                       '工作结束时间': i.lasttime, '日期': i.date}
            arr.append(content)
        print(arr)
        print(type(arr))
        return HttpResponse(arr)

