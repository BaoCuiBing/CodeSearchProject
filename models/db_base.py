from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import config

Base = declarative_base()

class Database:
    """数据库操作类,提供引擎和会话管理"""
    def __init__(self):
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """获取数据库会话"""
        return self.SessionLocal()

    def create_tables(self):
        """创建所有表结构"""
        Base.metadata.create_all(bind=self.engine)
