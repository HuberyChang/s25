from django.urls import path, re_path, include
from web.views import account, home, project, manage, wiki, file

app_name = "web"

urlpatterns = [
    path("register/", account.register, name="register"),  # 反向解析得是：register
    path("login/sms/", account.login_sms, name="login_sms"),  # 反向解析得是：login_sms
    path("login/", account.login, name="login"),  # 反向解析得是：login
    path("image/code/", account.image_code, name="image_code"),  # 反向解析得是：image_code
    path("index/", home.index, name="index"),
    path("send/sms/", account.send_sms, name="send_sms"),  # 反向解析得是：send_sms
    path("logout/", account.logout, name="logout"),
    # 项目列表
    path("project/list/", project.project_list, name="project_list"),
    re_path(
        "project/star/(?P<project_type>\\w+)/(?P<project_id>\\d+)/$",
        project.project_star,
        name="project_star",
    ),
    re_path(
        "project/unstar/(?P<project_type>\\w+)/(?P<project_id>\\d+)/$",
        project.project_unstar,
        name="project_unstar",
    ),
    # 项目管理
    re_path(
        "manage/(?P<project_id>\\d+)/",
        include(
            (
                [
                    path("dashboard/", manage.dashboard, name="dashboard"),
                    path("issue/", manage.issues, name="issues"),
                    path("statistics/", manage.statistics, name="statistics"),
                    path("wiki/", wiki.wiki, name="wiki"),
                    path("wiki/add/", wiki.wiki_add, name="wiki_add"),
                    path("wiki/catalog/", wiki.wiki_catalog, name="wiki_catalog"),
                    re_path(
                        "wiki/delete/(?P<wiki_id>\\d+)/",
                        wiki.wiki_delete,
                        name="wiki_delete",
                    ),
                    re_path(
                        "wiki/edit/(?P<wiki_id>\\d+)/",
                        wiki.wiki_edit,
                        name="wiki_edit",
                    ),
                    path("wiki/upload/", wiki.wiki_upload, name="wiki_upload"),
                    path("setting/", manage.setting, name="setting"),
                    path("file/", file.file, name="file"),
                    path("file/delete/", file.file_delete, name="file_delete"),
                ],
                "manage",
            ),
        ),
    ),
]
