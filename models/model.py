from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from models.db_base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    username = Column(String(50), nullable=False)  # 用户名
    password = Column(String(255), nullable=False)  # 密码
    email = Column(String(100), nullable=True)  # 邮箱
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class File(Base):
    __tablename__ = "files"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    filename = Column(String(255), nullable=False)  # 文件名
    file_path = Column(String(500), nullable=False)  # 文件路径
    file_size = Column(BigInteger, default=0, nullable=True)  # 文件大小
    file_type = Column(String(50), nullable=True)  # 文件类型
    file_url = Column(String(500), nullable=False)  # 文件访问链接
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
