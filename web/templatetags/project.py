#!/usr/bin/env python
# -*- coding:utf-8 -*-

from web import models
from django.template import Library
from django.urls import reverse

register = Library()


@register.inclusion_tag("inclusion/all_project_list.html")
def all_project_list(request):
    # 1、获取我创建的所有项目
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)
    # 2、我参与的所有项目
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {"my": my_project_list, "join": join_project_list, "request": request}


# 为了默认选中，把url写在了inclusion
@register.inclusion_tag("inclusion/manage_menu_list.html")
def manage_menu_list(request):
    data_list = [
        {
            "title": "概览",
            "url": reverse(
                "web:manage:dashboard", kwargs={"project_id": request.tracer.project.id}
            ),
        },
        {
            "title": "问题",
            "url": reverse(
                "web:manage:issues", kwargs={"project_id": request.tracer.project.id}
            ),
        },
        {
            "title": "统计",
            "url": reverse(
                "web:manage:statistics",
                kwargs={"project_id": request.tracer.project.id},
            ),
        },
        {
            "title": "wiki",
            "url": reverse(
                "web:manage:wiki", kwargs={"project_id": request.tracer.project.id}
            ),
        },
        {
            "title": "文件",
            "url": reverse(
                "web:manage:file", kwargs={"project_id": request.tracer.project.id}
            ),
        },
        {
            "title": "配置",
            "url": reverse(
                "web:manage:setting", kwargs={"project_id": request.tracer.project.id}
            ),
        },
    ]
    for item in data_list:
        # 当前用户访问的URL：request.path_info: /manage/1/file/xxx/ss/
        if request.path_info.startswith(item["url"]):
            item["class"] = "active"

    return {"data_list": data_list}
