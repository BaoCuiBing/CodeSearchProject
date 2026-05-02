import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录

MYSQL_DB_USER = "JhcwtwieiysHbE4p"  # 数据库用户名
MYSQL_DB_PASSWORD = "2JBBedBB4YRChhhC"  # 数据库密码
MYSQL_DB_NAME = "codesearchdb"  # 数据库名
MYSQL_DB_HOST = "127.0.0.1"  # 数据库主机
MYSQL_DB_PORT = "3306"  # 数据库端口
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB_NAME}"  # MySQL连接URI

SANIC_HOST = "0.0.0.0"  # Sanic主机
SANIC_PORT = 8848  # Sanic端口
MAX_UPLOAD_SIZE = 2  # 最大上传大小（单位：MB）