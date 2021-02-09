from django.urls import path
from web.views import account

# app_name = "web"

urlpatterns = [
    path("register/", account.register, name="register"),  # 反向解析得是：register
]
