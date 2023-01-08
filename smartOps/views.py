from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

import json
from datetime import datetime
import os
import uuid
#
from .models import File
from .forms import FileUploadForm, FileUploadModelForm
from  .file_handle.file_download import file_response_download

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


def so_render(request: WSGIRequest, html: str = "", rsq_dict: dict = {}):
    '''前缀 so : SmartOps缩写'''
    render_dict = {}
    so_date_time= datetime.now()
    render_dict['Copyright']=Copyright
    render_dict['so_date_time']=so_date_time
    render_dict['req_ip']=request.META['REMOTE_ADDR']
    for k,v in rsq_dict.items():
        render_dict[k] = v
    if html=="":
        log_info("ERROR")
    return render(request, html,render_dict)


def login(request: WSGIRequest):
    log_info(request)
    if request.method == 'GET':
        return so_render(request, "user/login.html")

    chk_rst = chk_login(request.POST['name'], request.POST['password'])
    if chk_rst != None:
        return so_render(request, 'user/login.html', {'errmsg': chk_rst})

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


def knowledge_list(request: WSGIRequest):
    return so_render(request, 'knowledge/knowledge_list.html')

def knowledge_category(request: WSGIRequest):
    return so_render(request, 'knowledge/knowledge_category.html')

def knowledge_category_add(request: WSGIRequest):
    return so_render(request, 'knowledge/knowledge_category_add.html')

def knowledge_upload(request: WSGIRequest):
    return so_render(request, 'knowledge/knowledge_upload.html')



# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_upload/file_list.html', {'files': files})

# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            # new_file.upload_method = upload_method
            # new_file.save()
        # return so_render(request, 'knowledge/knowledge_list.html')
        return HttpResponse("上传成功，请返回查看!")
    else:
        form = FileUploadForm()

    return render(request, 'file_handle/upload_form.html', 
                  {'form': form, 'heading': '上传交易知识点excel文件'}
                 )

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


# Upload File with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_handle/upload_form.html', 
                  {'form': form,'heading': '上传交易知识点excel文件'}
                 )


def file_download(request, file_path=""):
    log_info(file_path)
    return file_response_download(request)
