#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import redirect, render
from web.forms.wiki import WikiModelForm
from django.urls import reverse
from web import models
from django.http import JsonResponse


def wiki(request, project_id):
    """
    wiki首页
    """
    return render(request, "wiki.html")


def wiki_add(request, project_id):
    """
    wiki添加文章
    """
    if request.method == "GET":
        form = WikiModelForm(request)
        return render(request, "wiki_add.html", {"form": form})
    form = WikiModelForm(request, request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.save()
        url = reverse("web:manage:wiki", kwargs={"project_id": project_id})
        return redirect(url)

    return render(request, "wiki_add.html", {"form": form})


def wiki_catalog(request, project_id):
    """
    wiki目录
    """
    # 获取当前项目的所有目录
    data = models.Wiki.objects.filter(project=request.tracer.project).values(
        "id", "title", "parent_id"
    )
    return JsonResponse({"status": True, "data": list(data)})
