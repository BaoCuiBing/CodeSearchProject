import os
import logging
import alibabacloud_oss_v2 as oss
from config import OSS_BUCKET_NAME, OSS_REGION, OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET

logger = logging.getLogger(__name__)

class OSSClient:
    """阿里云OSS客户端封装类"""
    def __init__(self):
        """初始化OSS客户端配置"""
        credentials_provider = oss.credentials.StaticCredentialsProvider(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = OSS_REGION
        self.client = oss.Client(cfg)
        self.bucket = OSS_BUCKET_NAME
        logger.info(f"OSS客户端初始化成功:bucket={self.bucket},region={OSS_REGION}")

    def upload_file(self, object_key, local_file_path):
        """上传本地文件到OSS"""
        logger.info(f"上传文件:object_key={object_key},local_file={local_file_path}")
        if not os.path.exists(local_file_path):
            logger.warning(f"上传文件失败:本地文件不存在,local_file={local_file_path}")
            raise FileNotFoundError(f"文件不存在: {local_file_path}")
        with open(local_file_path, 'rb') as f:
            result = self.client.put_object(oss.PutObjectRequest(bucket=self.bucket, key=object_key, body=f))
        logger.info(f"上传文件成功:object_key={object_key},etag={result.etag}")
        return result

    def download_file(self, object_key, local_file_path):
        """从OSS下载文件到本地"""
        logger.info(f"下载文件:object_key={object_key},local_file={local_file_path}")
        result = self.client.get_object(oss.GetObjectRequest(bucket=self.bucket, key=object_key))
        with open(local_file_path, 'wb') as f:
            for chunk in result.content:
                f.write(chunk)
        logger.info(f"下载文件成功:object_key={object_key},local_file={local_file_path}")
        return result

    def delete_file(self, object_key):
        """删除OSS上的文件"""
        logger.info(f"删除文件:object_key={object_key}")
        result = self.client.delete_object(oss.DeleteObjectRequest(bucket=self.bucket, key=object_key))
        logger.info(f"删除文件成功:object_key={object_key}")
        return result

    def list_files(self, prefix='', max_keys=100):
        """列出OSS上的文件"""
        logger.info(f"列出文件:prefix={prefix},max_keys={max_keys}")
        paginator = self.client.list_objects_v2_paginator()
        files = []
        for page in paginator.iter_page(oss.ListObjectsV2Request(bucket=self.bucket, prefix=prefix, max_keys=max_keys)):
            for obj in page.contents:
                files.append({'key': obj.key, 'size': obj.size, 'last_modified': obj.last_modified})
        logger.info(f"列出文件成功:共{len(files)}个文件")
        return files

    def get_file_url(self, object_key, expires=3600):
        """获取文件临时访问URL"""
        logger.info(f"获取文件URL:object_key={object_key},expires={expires}s")
        result = self.client.presign(oss.GetObjectRequest(bucket=self.bucket, key=object_key), expires=expires)
        logger.info(f"获取文件URL成功:object_key={object_key}")
        return result.url

oss_client = OSSClient()
