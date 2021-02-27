#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect


def project_list(request):
    """
    项目列表
    """
    request.tracer.user
    request.tracer.price_policy
    return render(request, "project_list.html")
