#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from web import models
from web.forms.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ["project", "depth"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 找到想要的字段，把他绑定显示的数据重置
        # 数据=数据库中取， 当前项目所有的wiki标题

        total_data_list = [("", "请选择")]
        data_list = models.Wiki.objects.filter(
            project=request.tracer.project
        ).values_list("id", "title")
        total_data_list.extend(data_list)

        # modelform中的数据显示的不是自己想要的，就在init中找到相应字段，修改它的choices
        self.fields["parent"].choices = total_data_list
