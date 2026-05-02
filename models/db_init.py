from models.db_base import Database, Base
from models.model import User, File, Report, SearchHistory, Category, Post, Tag, PostTag, Comment, Favorite, Like, Follow, Message, Notification, SystemMessage, SystemMessageTarget, SystemSetting
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

def reset_database():
    """重置数据库,删除所有表后重新创建"""
    db = Database()
    session = db.get_session()
    try:
        print("正在删除所有数据表...")
        Base.metadata.drop_all(bind=db.engine)
        print("数据表删除完成")
        print("正在创建数据表...")
        Base.metadata.create_all(bind=db.engine)
        print("数据表创建完成")
        salt = generate_salt()
        hashed_password = hash_password("admin123", salt)
        admin_user = User(usernumber="admin", username="管理员", password=hashed_password, salt=salt, email="admin@example.com", role="admin")
        session.add(admin_user)
        session.commit()
        print("管理员账号创建完成: usernumber=admin, password=admin123")
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

if __name__ == "__main__":
    reset_database()