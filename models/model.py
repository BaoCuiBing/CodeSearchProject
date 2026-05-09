from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, SmallInteger, Integer, Text, Boolean, UniqueConstraint
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from sqlalchemy.sql import func
from models.db_base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    usernumber = Column(String(50), nullable=False)  # 账号
    username = Column(String(50), nullable=False)  # 用户名
    password = Column(String(255), nullable=False)  # 密码
    salt = Column(String(64), nullable=False)  # 密码盐
    email = Column(String(100), nullable=True)  # 邮箱
    phone = Column(String(20), nullable=True)  # 手机号
    role = Column(String(20), default="user", nullable=False)  # 角色：user/admin
    avatar = Column(String(500), nullable=True)  # 头像URL
    bio = Column(Text, nullable=True)  # 个人简介
    location = Column(String(100), nullable=True)  # 所在地
    website = Column(String(200), nullable=True)  # 个人网站
    github = Column(String(200), nullable=True)  # GitHub地址
    status = Column(String(20), default="active", nullable=False)  # 状态：active-正常,banned-封禁
    is_verified = Column(TINYINT, default=0, nullable=False)  # 是否认证：0-否,1-是
    ban_reason = Column(String(500), nullable=True)  # 封禁原因
    ban_expire_time = Column(DateTime, nullable=True)  # 封禁过期时间
    last_login_time = Column(DateTime, nullable=True)  # 最后登录时间
    login_ip = Column(String(50), nullable=True)  # 登录IP
    device_info = Column(String(200), nullable=True)  # 设备信息
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class File(Base):
    __tablename__ = "files"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)  # 用户ID外键，匿名上传为NULL
    filename = Column(String(255), nullable=False)  # 文件名
    file_path = Column(String(500), nullable=False)  # 文件路径
    file_size = Column(BigInteger, default=0, nullable=True)  # 文件大小
    file_type = Column(String(50), nullable=True)  # 文件类型
    file_url = Column(String(500), nullable=False)  # 文件访问链接
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class Report(Base):
    __tablename__ = "reports"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    reporter_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 举报者ID
    target_id = Column(BigInteger, nullable=False)  # 被举报目标ID
    target_type = Column(String(20), nullable=False)  # 目标类型：post-内容,comment-评论,user-用户
    reason = Column(String(500), nullable=False)  # 举报原因
    status = Column(String(20), default="pending", nullable=False)  # 状态：pending-待处理,handled-已处理,rejected-已驳回
    handler_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)  # 处理者ID
    handle_note = Column(String(500), nullable=True)  # 处理备注
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID
    keyword = Column(String(200), nullable=False)  # 搜索关键词
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    name = Column(String(100), nullable=False)  # 分类名称
    description = Column(String(500), nullable=True)  # 分类描述
    icon = Column(String(500), nullable=True)  # 分类图标URL
    sort = Column(Integer, default=0, nullable=True)  # 排序
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class Post(Base):
    __tablename__ = "posts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=True)  # 分类ID外键
    title = Column(String(500), nullable=False)  # 标题
    content = Column(LONGTEXT, nullable=False)  # 内容
    summary = Column(String(1000), nullable=True)  # 摘要
    cover_image = Column(Text, nullable=True)  # 封面图(JSON格式)
    type = Column(String(20), default="article", nullable=False)  # 类型：article-文章,question-问题
    status = Column(String(20), default="published", nullable=False)  # 状态：published-已发布,draft-草稿,hidden-已隐藏
    is_top = Column(SmallInteger, default=0, nullable=False)  # 是否置顶：0-否,1-是
    view_count = Column(BigInteger, default=0, nullable=True)  # 浏览次数
    like_count = Column(BigInteger, default=0, nullable=True)  # 点赞次数
    comment_count = Column(BigInteger, default=0, nullable=True)  # 评论次数
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class Tag(Base):
    __tablename__ = "tags"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    name = Column(String(100), nullable=False)  # 标签名称
    slug = Column(String(100), nullable=False)  # 标签别名
    description = Column(String(200), nullable=True)  # 标签描述
    icon = Column(String(500), nullable=True)  # 标签图标URL
    color = Column(String(20), nullable=True)  # 标签颜色
    post_count = Column(BigInteger, default=0, nullable=True)  # 关联内容数
    is_hot = Column(SmallInteger, default=0, nullable=False)  # 是否热门：0-否,1-是
    is_recommend = Column(SmallInteger, default=0, nullable=False)  # 是否推荐：0-否,1-是
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=True)  # 分类ID外键
    sort_order = Column(Integer, default=0, nullable=True)  # 排序
    status = Column(String(20), default="active", nullable=False)  # 状态：active-启用,disabled-禁用
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class PostTag(Base):
    __tablename__ = "post_tags"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)  # 内容ID外键
    tag_id = Column(BigInteger, ForeignKey("tags.id"), nullable=False)  # 标签ID外键
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class Comment(Base):
    __tablename__ = "comments"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)  # 内容ID外键
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    parent_id = Column(BigInteger, nullable=True)  # 父评论ID
    content = Column(Text, nullable=False)  # 评论内容
    status = Column(String(20), default="normal", nullable=False)  # 状态：normal-正常,hidden-隐藏
    like_count = Column(BigInteger, default=0, nullable=True)  # 点赞次数
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)  # 内容ID外键
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "target_id", "target_type"),)
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    target_id = Column(BigInteger, nullable=False)  # 目标ID
    target_type = Column(String(20), default="post", nullable=False)  # 类型：post-内容,comment-评论
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id"),)
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    follower_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 关注者ID外键
    following_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 被关注者ID外键
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class Message(Base):
    __tablename__ = "messages"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    from_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 发送者ID外键
    to_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 接收者ID外键
    content = Column(Text, nullable=False)  # 消息内容
    is_read = Column(SmallInteger, default=0, nullable=False)  # 是否已读：0-未读,1-已读
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class SystemMessage(Base):
    __tablename__ = "system_messages"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    sender_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 发送者ID外键
    title = Column(String(200), nullable=False)  # 消息标题
    content = Column(Text, nullable=False)  # 消息内容
    type = Column(String(20), default="system", nullable=False)  # 类型：system-系统,announcement-公告
    target_type = Column(String(20), default="all", nullable=False)  # 目标类型：all-全部,user_list-指定用户
    priority = Column(String(20), default="medium", nullable=False)  # 优先级：low/medium/high
    is_top = Column(SmallInteger, default=0, nullable=False)  # 是否置顶：0-否,1-是
    status = Column(String(20), default="draft", nullable=False)  # 状态：draft-草稿,sent-已发送
    send_time = Column(DateTime, nullable=True)  # 发送时间
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class SystemMessageTarget(Base):
    __tablename__ = "system_message_targets"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    message_id = Column(BigInteger, ForeignKey("system_messages.id"), nullable=False)  # 消息ID外键
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    is_read = Column(SmallInteger, default=0, nullable=False)  # 是否已读：0-未读,1-已读
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    key = Column(String(100), nullable=False)  # 设置键
    value = Column(Text, nullable=True)  # 设置值
    description = Column(String(200), nullable=True)  # 设置说明
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # 主键ID
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)  # 用户ID外键
    type = Column(String(20), default="system", nullable=False)  # 类型：system-系统,system_msg-系统消息,comment-评论,like-点赞,follow-关注
    content = Column(String(500), nullable=False)  # 通知内容
    related_id = Column(BigInteger, nullable=True)  # 关联ID
    is_read = Column(SmallInteger, default=0, nullable=False)  # 是否已读：0-未读,1-已读
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间
