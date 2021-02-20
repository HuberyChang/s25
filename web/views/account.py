from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm
from django.http import JsonResponse
from web import models


def register(request):
    """
    注册
    """
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库，密码得是密文
        form.save()
        return JsonResponse({"status": True, "data": "/login/"})

    return JsonResponse({"status": False, "error": form.errors})


def send_sms(request):
    """
    发送短信
    """
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号，不能为空，格式是否正确
    if form.is_valid():
        # 发短信
        # 写redis
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})
