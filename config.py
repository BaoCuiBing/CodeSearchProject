import os
import logging

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录

MYSQL_DB_USER = "JhcwtwieiysHbE4p"  # 数据库用户名
MYSQL_DB_PASSWORD = "2JBBedBB4YRChhhC"  # 数据库密码
MYSQL_DB_NAME = "codesearchdb"  # 数据库名
MYSQL_DB_HOST = "127.0.0.1"  # 数据库主机
MYSQL_DB_PORT = "3306"  # 数据库端口
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB_NAME}"  # MySQL连接URI

SANIC_HOST = "0.0.0.0"  # Sanic主机
SANIC_PORT = 8848  # Sanic端口
SANIC_THRESHOLD = 3000  # worker ack超时(单位0.1s,即300秒)
MAX_UPLOAD_SIZE = 2  # 最大上传大小（单位：MB）

LOG_DIR = os.path.join(PROJECT_DIR, "static", "logs")  # 日志目录
LOG_FILE = os.path.join(LOG_DIR, "sanic.log")  # 日志文件
LOG_LEVEL = logging.INFO  # 日志级别（及以上级别会被记录）
WEB_LOG_FILE = os.path.join(LOG_DIR, "web_log.log")  # 前端日志文件

OSS_BUCKET_NAME = "code-search-app"  # OSS桶名
OSS_REGION = "cn-beijing"  # OSS区域
OSS_ACCESS_KEY_ID = ""
OSS_ACCESS_KEY_SECRET = ""

UPLOAD_DIR = os.path.join(PROJECT_DIR, "static", "uploads")  # 上传目录（本地存储）
USE_OSS = True  # 是否使用OSS存储文件
