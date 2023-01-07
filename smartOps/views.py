from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

import json
from datetime import datetime

ADMIN_NAME='trade'
ADMIN_PASSWD=''

Copyright="Copyright CFFEX SmartOps V1.0"

def obj_to_dict(obj_list):
    result = []
    for obj in obj_list:
        result.append(model_to_dict(obj))
    return result


def log_info(msg: str = ""):
    print("--------------------------------------------------------------------")
    print(msg)
    print("--------------------------------------------------------------------")


def test(request):
    return render(request, 'test.html')

def add(request):
    return HttpResponse("add\n\n\tadd")


def chk_login(name, passwd) -> str:
    if name != ADMIN_NAME:
        return "用户名错误"
    elif passwd != ADMIN_PASSWD:
        return "密码错误"
    else:
        return None


def so_render(request: WSGIRequest, html: str = ""):
    '''前缀 so : SmartOps缩写'''
    render_dict = {}
    so_date_time= datetime.now()
    render_dict['Copyright']=Copyright
    render_dict['so_date_time']=so_date_time
    render_dict['req_ip']=request.META['REMOTE_ADDR']
    if html=="":
        log_info("ERROR")
    return render(request, html,render_dict)


def login(request: WSGIRequest):
    log_info(request)
    if request.method == 'GET':
        return so_render(request, "user/login.html")

    chk_rst = chk_login(request.POST['name'], request.POST['password'])
    if chk_rst != None:
        return render(request, 'user/login.html', {'errmsg': chk_rst})

    return index(request) 


def index(request):
    log_info(str(request))
    return so_render(request, 'index/index.html')

def welcome(request):
    log_info(str(request))
    return so_render(request, 'index/welcome.html')


# 知识点列表
def kp_list(request):
    pass


def product_list(request):
    l = [
        ["1", "2", '3', '4', '5', '6'],
        ["1", "2", '3', '4', '5', '6'],
        ["1", "2", '3', '4', '5', '6'],
        ["1", "2", '3', '4', '5', '6'],
    ]
    return render(request, 'product-list.html', {'l': l})