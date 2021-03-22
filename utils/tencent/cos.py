#!/usr/bin/env python
# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings


def create_bucket(bucket, region="ap-chengdu"):
    """
    创建桶
    @param bucket:
    @param region:
    @return:
    """
    # appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
    # 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
    secret_id = settings.TENCENT_COS_ID
    secret_key = settings.TENCENT_COS_KEY

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
    )
    # 2. 获取客户端对象
    client = CosS3Client(config)

    client.create_bucket(Bucket=bucket, ACL="public-read")


def upload_file(bucket, region, file_object, key):
    secret_id = settings.TENCENT_COS_ID  # 替换为用户的 secretId
    secret_key = settings.TENCENT_COS_KEY  # 替换为用户的 secretKey

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
    )
    # 2. 获取客户端对象
    client = CosS3Client(config)

    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    # response = client.upload_file(
    #     Bucket=request.tracer.project.bucket,
    #     LocalFilePath="code.png",
    #     Key="code.png",
    # )
    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,  # 文件对象
        Key=key,  # 上传到桶之后的文件名
    )
    # print(response["ETag"])
    # https://demopy-1303250987.cos.ap-chengdu.myqcloud.com/code.png
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)


def delete_file(bucket, region, key):
    secret_id = settings.TENCENT_COS_ID  # 替换为用户的 secretId
    secret_key = settings.TENCENT_COS_KEY  # 替换为用户的 secretKey

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
    )
    # 2. 获取客户端对象
    client = CosS3Client(config)

    client.delete_object(
        Bucket=bucket,
        Key=key,  # 上传到桶之后的文件名
    )


def delete_file_list(bucket, region, key_list):
    secret_id = settings.TENCENT_COS_ID  # 替换为用户的 secretId
    secret_key = settings.TENCENT_COS_KEY  # 替换为用户的 secretKey

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
    )
    # 2. 获取客户端对象
    client = CosS3Client(config)

    objects = {"Quiet": "true", "Object": key_list}

    client.delete_objects(
        Bucket=bucket,
        Delete=objects,  # 上传到桶之后的文件名
    )
