from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User
from models.db_init import get_db_session
from utils.password_analysis import generate_salt, hash_password, verify_password

admin_user_bp = Blueprint("admin_user", url_prefix="/api/admin/user")

@admin_user_bp.get("/list")
@openapi.summary("获取用户列表")
async def get_user_list(request, db):
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    status = request.args.get("status")
    query = db.query(User)
    if keyword:
        query = query.filter(User.username.contains(keyword) | User.usernumber.contains(keyword) | User.email.contains(keyword))
    if status and status != "all":
        query = query.filter(User.status == status)
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    user_list = [{"id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "avatar": u.avatar, "role": u.role, "status": u.status, "bio": u.bio, "created_at": str(u.created_at)} for u in users]
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": user_list, "total": total, "page": page, "page_size": page_size}})

@admin_user_bp.get("/<id>")
@openapi.summary("获取用户详情")
async def get_user_detail(request, db, id):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    return response.json({"code": 200, "msg": "获取成功", "data": {"id": user.id, "usernumber": user.usernumber, "username": user.username, "email": user.email, "avatar": user.avatar, "role": user.role, "status": user.status, "bio": user.bio, "created_at": str(user.created_at), "updated_at": str(user.updated_at)}})

@admin_user_bp.post("/<id>/ban")
@openapi.summary("封禁/解封用户")
async def toggle_user_ban(request, db, id):
    data = request.json
    action = data.get("action")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    if action == "ban":
        user.status = "banned"
        msg = "已封禁该用户"
    elif action == "unban":
        user.status = "active"
        msg = "已解封该用户"
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": msg})

@admin_user_bp.delete("/<id>")
@openapi.summary("删除用户")
async def delete_user(request, db, id):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    db.delete(user)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@admin_user_bp.put("/<id>")
@openapi.summary("编辑用户信息")
async def edit_user_info(request, db, id):
    data = request.json
    user = db.query(User).filter(User.id == id).first()
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
    db.commit()
    return response.json({"code": 200, "msg": "编辑成功"})

@admin_user_bp.post("/<id>/reset-password")
@openapi.summary("重置用户密码")
async def reset_user_password(request, db, id):
    data = request.json
    new_password = data.get("new_password")
    if not new_password or len(new_password) < 6:
        return response.json({"code": 400, "msg": "密码至少6位"})
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    salt = generate_salt()
    user.salt = salt
    user.password = hash_password(new_password, salt)
    db.commit()
    return response.json({"code": 200, "msg": "密码重置成功"})

@admin_user_bp.post("/batch-action")
@openapi.summary("批量操作用户")
async def batch_action_users(request, db):
    data = request.json
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择用户"})
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
async def export_users(request, db):
    users = db.query(User).all()
    user_list = [{"id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "role": u.role, "status": u.status, "created_at": str(u.created_at)} for u in users]
    return response.json({"code": 200, "msg": "导出成功", "data": {"list": user_list, "total": len(user_list)}})

@admin_user_bp.get("/stats/overview")
@openapi.summary("获取用户统计概览")
async def get_user_stats_overview(request, db):
    total_users = db.query(User).count()
    admin_count = db.query(User).filter(User.role == "admin").count()
    banned_count = db.query(User).filter(User.status == "banned").count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_users": total_users, "admin_count": admin_count, "banned_count": banned_count}})

@admin_user_bp.post("/<id>/notify")
@openapi.summary("发送系统消息给用户")
async def send_system_notification_to_user(request, db, id):
    data = request.json
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return response.json({"code": 400, "msg": "标题和内容不能为空"})
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    return response.json({"code": 200, "msg": "通知已发送"})
