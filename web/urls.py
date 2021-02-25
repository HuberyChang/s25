from django.urls import path
from web.views import account, home

app_name = "web"

urlpatterns = [
    path("register/", account.register, name="register"),  # 反向解析得是：register
    path("login/sms/", account.login_sms, name="login_sms"),  # 反向解析得是：login_sms
    path("login/", account.login, name="login"),  # 反向解析得是：login
    path("image/code/", account.image_code, name="image_code"),  # 反向解析得是：image_code
    path("index/", home.index, name="index"),
    path("send/sms/", account.send_sms, name="send_sms"),  # 反向解析得是：send_sms
    path("logout/", account.logout, name="logout"),
]
