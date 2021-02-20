from django.urls import path
from web.views import account

# app_name = "web"

urlpatterns = [
    path("register/", account.register, name="register"),  # 反向解析得是：register
    path("send/sms/", account.send_sms, name="send_sms"),  # 反向解析得是：send_sms
]
