from django.contrib import admin
from django.urls import path
from app01 import views

app_name = "app01"

urlpatterns = [
    path("send/sms/", views.send_sms),
    path("register/", views.register),  # 反向解析得是：app01:register
]
