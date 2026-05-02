from models.db_base import Database
from models.model import User, File, Report, SearchHistory, Category, Post, Tag, PostTag, Comment, Favorite, Like, Follow, Message, Notification
from utils.password_analysis import generate_salt, hash_password

def init_database():
    """初始化数据库,创建表结构"""
    db = Database()
    db.create_tables()
    session = db.get_session()
    try:
        admin = session.query(User).filter(User.usernumber == "admin").first()
        if not admin:
            salt = generate_salt()
            hashed_password = hash_password("admin123", salt)
            admin_user = User(usernumber="admin", username="管理员", password=hashed_password, salt=salt, email="admin@example.com", role="admin")
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
