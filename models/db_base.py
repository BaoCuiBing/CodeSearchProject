from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import config

Base = declarative_base()

class Database:
    """数据库操作类,提供引擎和共享会话管理"""
    def __init__(self):
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=2, max_overflow=5)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = None  # 共享会话,启动时初始化一次

    def init_session(self):
        """初始化共享数据库会话(仅在启动时调用一次)"""
        self.session = self.SessionLocal()
        return self.session

    def get_session(self):
        """获取共享数据库会话"""
        return self.session

    def create_tables(self):
        """创建所有表结构"""
        Base.metadata.create_all(bind=self.engine)
