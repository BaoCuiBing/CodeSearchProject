from models.db_base import Database
from models.model import User, File

def init_database():
    """初始化数据库,创建表结构"""
    db = Database()
    db.create_tables()
    session = db.get_session()
    try:
        admin = session.query(User).filter(User.usernumber == "admin").first()
        if not admin:
            admin_user = User(usernumber="admin", username="管理员", password="admin123", email="admin@example.com")
            session.add(admin_user)
            session.commit()
    finally:
        session.close()
    return db

def get_db_session(db: Database):
    """获取数据库会话生成器,用于依赖注入"""
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()
