from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Comment, Follow, Favorite, Like, Notification
from models.db_init import get_db_session
from utils.password_analysis import generate_salt, hash_password, verify_password

admin_user_bp = Blueprint("admin_user", url_prefix="/api/admin/user")

@admin_user_bp.get("/list")
@openapi.summary("获取用户列表")
async def get_user_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    status = request.args.get("status", "all")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    register_start = request.args.get("register_start")
    register_end = request.args.get("register_end")
    query = db.query(User)
    if keyword:
        query = query.filter(User.username.contains(keyword) | User.usernumber.contains(keyword) | User.email.contains(keyword))
    if status != "all":
        query = query.filter(User.status == status)
    if register_start:
        query = query.filter(User.created_at >= register_start)
    if register_end:
        query = query.filter(User.created_at <= register_end)
    sort_map = {"created_time": User.created_at, "last_login": User.last_login_time}
    order_func = sort_map.get(sort, User.created_at).desc() if order == "desc" else sort_map.get(sort, User.created_at).asc()
    total = query.count()
    users = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    user_list = []
    for u in users:
        article_count = db.query(Post).filter(Post.user_id == u.id, Post.type == "article").count()
        question_count = db.query(Post).filter(Post.user_id == u.id, Post.type == "question").count()
        comment_count = db.query(Comment).filter(Comment.user_id == u.id).count()
        follower_count = db.query(Follow).filter(Follow.following_id == u.id).count()
        following_count = db.query(Follow).filter(Follow.follower_id == u.id).count()
        like_count = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.like_count)).scalar() or 0
        view_count = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.view_count)).scalar() or 0
        user_list.append({"user_id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "avatar": u.avatar, "status": u.status, "role": u.role, "article_count": article_count, "question_count": question_count, "comment_count": comment_count, "follower_count": follower_count, "following_count": following_count, "like_count": like_count, "view_count": view_count, "last_login_time": str(u.last_login_time) if u.last_login_time else None, "created_at": str(u.created_at)})
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": user_list, "total": total, "page": page, "page_size": page_size}})

@admin_user_bp.get("/<user_id>")
@openapi.summary("获取用户详情")
async def get_user_detail(request, user_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    article_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "article").count()
    question_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "question").count()
    comment_count = db.query(Comment).filter(Comment.user_id == user.id).count()
    favorite_count = db.query(Favorite).filter(Favorite.user_id == user.id).count()
    follower_count = db.query(Follow).filter(Follow.following_id == user.id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
    like_received = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.like_count)).scalar() or 0
    like_given = db.query(Like).filter(Like.user_id == user.id).count()
    view_count = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.view_count)).scalar() or 0
    return response.json({"code": 200, "msg": "获取成功", "data": {"user_id": user.id, "usernumber": user.usernumber, "username": user.username, "email": user.email, "phone": user.phone, "avatar": user.avatar, "bio": user.bio, "location": user.location, "website": user.website, "github": user.github, "status": user.status, "role": user.role, "stats": {"article_count": article_count, "question_count": question_count, "comment_count": comment_count, "favorite_count": favorite_count, "follower_count": follower_count, "following_count": following_count, "like_received": like_received, "like_given": like_given, "view_count": view_count}, "created_at": str(user.created_at), "last_login_time": str(user.last_login_time) if user.last_login_time else None, "login_ip": user.login_ip, "device_info": user.device_info, "is_verified": bool(user.is_verified), "ban_reason": user.ban_reason, "ban_expire_time": str(user.ban_expire_time) if user.ban_expire_time else None}})

@admin_user_bp.post("/ban")
@openapi.summary("封禁/解封用户")
async def toggle_user_ban(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    action = data.get("action")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    if action == "ban":
        reason = data.get("reason")
        if not reason:
            return response.json({"code": 400, "msg": "封禁原因不能为空"})
        duration = data.get("duration", 7)
        user.status = "banned"
        user.ban_reason = reason
        if duration > 0:
            user.ban_expire_time = datetime.now() + timedelta(days=duration)
        else:
            user.ban_expire_time = None
        msg = "已封禁该用户"
    elif action == "unban":
        user.status = "active"
        user.ban_reason = None
        user.ban_expire_time = None
        msg = "已解封该用户"
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": msg, "data": {"user_id": user.id, "status": user.status, "ban_reason": user.ban_reason, "ban_expire_time": str(user.ban_expire_time) if user.ban_expire_time else None}})

@admin_user_bp.delete("/<user_id>")
@openapi.summary("删除用户")
async def delete_user(request, user_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    db.delete(user)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@admin_user_bp.put("/")
@openapi.summary("编辑用户信息")
async def edit_user_info(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "role" in data:
        user.role = data["role"]
    if "bio" in data:
        user.bio = data["bio"]
    if "is_verified" in data:
        user.is_verified = 1 if data["is_verified"] else 0
    db.commit()
    return response.json({"code": 200, "msg": "编辑成功"})

@admin_user_bp.post("/reset-password")
@openapi.summary("重置用户密码")
async def reset_user_password(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    new_password = data.get("new_password")
    if not new_password or len(new_password) < 6:
        return response.json({"code": 400, "msg": "新密码不能少于6位"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    salt = generate_salt()
    user.salt = salt
    user.password = hash_password(new_password, salt)
    db.commit()
    return response.json({"code": 200, "msg": "密码重置成功"})

@admin_user_bp.post("/batch-action")
@openapi.summary("批量操作用户")
async def batch_action_users(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择要操作的用户"})
    users = db.query(User).filter(User.id.in_(ids)).all()
    if action == "ban":
        for u in users:
            u.status = "banned"
    elif action == "unban":
        for u in users:
            u.status = "active"
    elif action == "delete":
        for u in users:
            db.delete(u)
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "批量操作成功"})

@admin_user_bp.post("/export")
@openapi.summary("导出用户数据")
async def export_users(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    users = db.query(User).all()
    user_list = [{"user_id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "role": u.role, "status": u.status, "created_at": str(u.created_at)} for u in users]
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "users.xlsx", "file_url": "/static/exports/users.xlsx"}})

@admin_user_bp.get("/stats/overview")
@openapi.summary("获取用户统计概览")
async def get_user_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        return response.json({"code": 403, "msg": "权限不足"})
    period = request.args.get("period", "month")
    total_users = db.query(User).count()
    new_users_today = db.query(User).filter(func.date(User.created_at) == datetime.now().date()).count()
    new_users_week = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=7)).count()
    new_users_month = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=30)).count()
    active_users = db.query(User).filter(User.status == "active").count()
    banned_users = db.query(User).filter(User.status == "banned").count()
    verified_users = db.query(User).filter(User.is_verified == 1).count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_users": total_users, "new_users_today": new_users_today, "new_users_week": new_users_week, "new_users_month": new_users_month, "active_users": active_users, "banned_users": banned_users, "verified_users": verified_users, "growth_rate": round((new_users_month / total_users * 100) if total_users > 0 else 0, 2), "trend_data": []}})

@admin_user_bp.post("/<user_id>/notify")
@openapi.summary("发送系统消息给用户")
async def send_system_notification_to_user(request, user_id):
    db = request.ctx.db
    data = request.json
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return response.json({"code": 400, "msg": "标题和内容不能为空"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    return response.json({"code": 200, "msg": "通知已发送"})
