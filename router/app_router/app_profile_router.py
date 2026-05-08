import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Follow
from models.db_init import get_db_session
from utils.password_analysis import generate_salt, hash_password, verify_password

logger = logging.getLogger(__name__)
profile_bp = Blueprint("profile", url_prefix="/api/profile")

@profile_bp.get("/<user_id>")
@openapi.summary("获取用户个人主页统计数据")
async def get_user_profile(request, user_id):
    db = request.ctx.db
    current_user_id = request.args.get("current_user_id")
    logger.info(f"查询用户资料:user_id={user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"获取用户资料失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    article_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "article", Post.status == "published").count()
    question_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "question", Post.status == "published").count()
    follower_count = db.query(Follow).filter(Follow.following_id == user.id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
    like_count = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.like_count)).scalar() or 0
    view_count = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.view_count)).scalar() or 0
    is_followed = False
    if current_user_id:
        is_followed = db.query(Follow).filter(Follow.follower_id == current_user_id, Follow.following_id == user.id).first() is not None
    logger.info(f"获取用户资料成功:username={user.username}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"user_id": user.id, "username": user.username, "avatar": user.avatar, "bio": user.bio, "email": user.email, "phone": user.phone, "location": user.location, "website": user.website, "github": user.github, "stats": {"article_count": article_count, "question_count": question_count, "follower_count": follower_count, "following_count": following_count, "like_count": like_count, "view_count": view_count}, "created_at": str(user.created_at), "is_followed": is_followed}})

@profile_bp.put("/")
@openapi.summary("更新用户个人资料")
async def update_profile(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        logger.warning("更新资料失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"更新资料失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"更新用户资料:user_id={user_id}")
    if "username" in data:
        exist_user = db.query(User).filter(User.username == data["username"], User.id != user_id).first()
        if exist_user:
            logger.warning(f"更新资料失败:用户名已存在,username={data['username']}")
            return response.json({"code": 400, "msg": "用户名已存在"})
        user.username = data["username"]
    if "avatar" in data:
        user.avatar = data["avatar"]
    if "bio" in data:
        if len(data["bio"]) > 200:
            logger.warning("更新资料失败:个人简介超出限制")
            return response.json({"code": 400, "msg": "个人简介最多200字"})
        user.bio = data["bio"]
    if "email" in data:
        user.email = data["email"]
    if "location" in data:
        user.location = data["location"]
    if "website" in data:
        user.website = data["website"]
    if "github" in data:
        user.github = data["github"]
    if "phone" in data:
        user.phone = data["phone"]
    db.commit()
    logger.info(f"更新用户资料成功:user_id={user_id}")
    return response.json({"code": 200, "msg": "更新成功", "data": {"user_id": user.id, "username": user.username, "avatar": user.avatar, "bio": user.bio}})

@profile_bp.put("/password")
@openapi.summary("修改登录密码")
async def change_password(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not user_id:
        logger.warning("修改密码失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    if not old_password or not new_password:
        logger.warning("修改密码失败:密码为空")
        return response.json({"code": 400, "msg": "密码不能为空"})
    if len(new_password) < 6:
        logger.warning("修改密码失败:新密码长度不足")
        return response.json({"code": 400, "msg": "新密码不能少于6位"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"修改密码失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    if not verify_password(old_password, user.salt, user.password):
        logger.warning(f"修改密码失败:原密码错误,user_id={user_id}")
        return response.json({"code": 400, "msg": "原密码错误"})
    logger.info(f"修改密码:user_id={user_id}")
    salt = generate_salt()
    user.salt = salt
    user.password = hash_password(new_password, salt)
    db.commit()
    logger.info(f"修改密码成功:user_id={user_id}")
    return response.json({"code": 200, "msg": "密码修改成功"})