#!/usr/bin/env python
# -*- coding:utf-8 -*-

# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings


secret_id = settings.TENCENT_COS_ID  # 替换为用户的 secretId
secret_key = settings.TENCENT_COS_KEY  # 替换为用户的 secretKey
region = "ap-chengdu"  # 替换为用户的 Region

config = CosConfig(
    Region=region,
    SecretId=secret_id,
    SecretKey=secret_key,
)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket="demopy-1303250987",
    LocalFilePath="code.png",
    Key="code.png",
)
print(response["ETag"])
