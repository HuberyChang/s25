#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import redirect, render
from web.forms.file import FolderModelForm
from django.http import JsonResponse
from web import models
from django.forms import model_to_dict


# http://127.0.0.1:8000/manage/6/file/
# http://127.0.0.1:8000/manage/6/file/?folder=1
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

    # GET 查看页面
    if request.method == "GET":

        breadcrumb_list = []
        parent = parent_object
        while parent:
            # breadcrumb_list.insert(0, {"id": parent.id, "name": parent.name})
            breadcrumb_list.insert(0, model_to_dict(parent, ["id", "name"]))
            parent = parent.parent

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
            request,
            "file.html",
            {
                "form": form,
                "file_object_list": file_object_list,
                "breadcrumb_list": breadcrumb_list,
            },
        )

    # POST 添加文件夹

    fid = request.POST.get("fid", "")
    edit_object = None
    if fid.isdecimal():
        # 修改
        edit_object = models.FileRepository.objects.filter(
            id=int(fid), file_type=2, project=request.tracer.project
        ).first()
    if edit_object:
        form = FolderModelForm(
            request, parent_object, data=request.POST, instance=edit_object
        )
    else:
        form = FolderModelForm(request, parent_object, data=request.POST)

    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


# http://127.0.0.1:8000/manage/6/file/delete/?fid=1
def file_delete(request, project_id):
    """
    删除文件
    @param project_id:
    @param request:
    @return:
    """
    fid = request.GET.get("fid")

    # 只删除数据库的  文件&文件夹  （级联删除）
    delete_object = models.FileRepository.objects.filter(
        id=fid, project=request.tracer.project
    ).first()
    if delete_object.file_type == 1:
        pass  # 删除文件（数据库文件删除，cos文件删除、项目已使用空间容量还回去）
    else:
        pass  # 删除文件夹（找到文件夹下的所有文件->数据库文件删除，cos文件删除、项目已使用空间容量还回去）
    delete_object.delete()
    return JsonResponse({"status": True})
