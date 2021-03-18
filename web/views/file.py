#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import redirect, render
from web.forms.file import FolderModelForm
from django.http import JsonResponse
from web import models


def file(request, project_id):
    """
    文件列表 & 添加文件夹
    @param request:
    @param project_id:
    @return:
    """

    parent_object = None
    folder_id = request.GET.get("folder", "")
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(
            id=int(folder_id), file_type=2, project=request.tracer.project
        ).first()

    if request.method == "GET":
        queryset = models.FileRepository.objects.filter(project=request.tracer.project)
        if parent_object:
            file_object_list = queryset.filter(parent=parent_object).order_by(
                "-file_type"
            )
        else:
            file_object_list = queryset.filter(parent__isnull=True).order_by(
                "-file_type"
            )
        form = FolderModelForm(request, parent_object)
        return render(
            request, "file.html", {"form": form, "file_object_list": file_object_list}
        )

    # 添加文件夹
    form = FolderModelForm(request, parent_object, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})