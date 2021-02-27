#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings
from django.shortcuts import redirect
import datetime


class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        """
        如果用户已登录，则request中赋值
        """
        # tracer_object = Tracer()
        request.tracer = Tracer()
        user_id = request.session.get("user_id", 0)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        # tracer_object.user = user_obj
        # request.tracer = tracer_object
        request.tracer.user = user_obj

        """
        1、获取当前用户访问的URL
        2、检测URL是否在白名单，如果在则继续访问，如果不在则判断是否已登录
        """
        # settings.WHITE_REGEX_URL_LIST
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            return redirect("web:login")

        # 登录成功之后，访问后台管理时，获取当前用户所拥有的的额度
        # 方式一：免费额度在交易记录中存储
        # 获取当前用户ID值最大（最近交易记录）
        _object = (
            models.Transation.objects.filter(user=user_obj, status=2)
            .order_by("-id")
            .first()
        )
        # 判断是否过期，免费额度没有过期时间
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transation.objects.filter(
                user=user_obj, status=2, price_policy__category=1
            )
        # tracer_object.price_policy = _object.price_policy
        # request.tracer = tracer_object
        request.tracer.price_policy = _object.price_policy

        # 方拾二：免费的额度存储在配置文件
        # # 获取当前用户ID值最大（最近交易记录）
        # _object = (
        #     models.Transation.objects.filter(user=user_obj, status=2)
        #     .order_by("-id")
        #     .first()
        # )
        # if not _object:
        #     # 没有购买
        #     request.price_policy = models.PricePolicy.objects.filter(
        #         category=1, title="个人免费版"
        #     ).first()
        # else:
        #     # 付费版
        #     current_datetime = datetime.datetime.now()
        #     if _object.end_datetime and _object.end_datetime < current_datetime:
        #         # 过期
        #         request.price_policy = models.PricePolicy.objects.filter(
        #             category=1, title="个人免费版"
        #         ).first()
        #     else:
        #         request.price_policy = _object.price_policy
