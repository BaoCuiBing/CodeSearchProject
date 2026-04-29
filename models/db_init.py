from models.db_base import Database
from models.model import User, File

def init_database():
    """初始化数据库,创建表结构"""
    db = Database()
    db.create_tables()
    return db

def get_db_session(db: Database):
    """获取数据库会话生成器,用于依赖注入"""
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()
