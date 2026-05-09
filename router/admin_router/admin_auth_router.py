from datetime import datetime
import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from models.model import User
from utils.password_analysis import generate_salt, hash_password, verify_password

logger = logging.getLogger(__name__)
admin_auth_bp = Blueprint("admin_auth", url_prefix="/api/admin/auth")

@admin_auth_bp.post("/login")
@openapi.summary("管理员登录")
async def admin_login(request):
    db = request.ctx.db
    data = request.json
    usernumber = data.get("usernumber")
    password = data.get("password")
    if not usernumber or not password:
        logger.warning("管理员登录失败:账号或密码为空")
        return response.json({"code": 400, "msg": "账号或密码错误"})
    logger.info(f"管理员登录尝试:usernumber={usernumber},IP={request.ip}")
    user = db.query(User).filter(User.usernumber == usernumber).first()
    if not user:
        logger.warning(f"管理员登录失败:账号不存在,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号或密码错误"})
    if user.role != "admin":
        logger.warning(f"管理员登录失败:权限不足,usernumber={usernumber},role={user.role}")
        return response.json({"code": 403, "msg": "权限不足"})
    if user.status == "banned":
        logger.warning(f"管理员登录失败:账号被封禁,usernumber={usernumber}")
        return response.json({"code": 403, "msg": "权限不足"})
    if not verify_password(password, user.salt, user.password):
        logger.warning(f"管理员登录失败:密码错误,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号或密码错误"})
    user.last_login_time = datetime.now()
    user.login_ip = request.ip
    db.commit()
    logger.info(f"管理员{user.username}登录成功,IP:{request.ip}")
    return response.json({"code": 200, "msg": "登录成功", "data": {"admin_id": user.id, "username": user.username, "role": user.role, "avatar": user.avatar}})

@admin_auth_bp.get("/me")
@openapi.summary("获取当前管理员信息")
async def get_current_admin(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        logger.warning("获取管理员信息失败:admin_id为空")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"获取管理员信息:admin_id={admin_id}")
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning(f"获取管理员信息失败:admin_id={admin_id}不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    logger.info(f"获取管理员信息成功:username={admin.username}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"admin_id": admin.id, "username": admin.username, "role": admin.role, "avatar": admin.avatar, "last_login_time": str(admin.last_login_time) if admin.last_login_time else None}})

@admin_auth_bp.put("/change-password")
@openapi.summary("修改管理员密码")
async def change_admin_password(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")
    if not admin_id:
        logger.warning("修改密码失败:admin_id为空")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning(f"修改密码失败:admin_id={admin_id}不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    if not new_password or len(new_password) < 8:
        logger.warning(f"修改密码失败:新密码长度不足,admin_id={admin_id}")
        return response.json({"code": 400, "msg": "新密码至少8位"})
    if new_password != confirm_password:
        logger.warning(f"修改密码失败:两次密码不一致,admin_id={admin_id}")
        return response.json({"code": 400, "msg": "两次密码输入不一致"})
    logger.info(f"管理员{admin_id}修改密码")
    salt = generate_salt()
    admin.salt = salt
    admin.password = hash_password(new_password, salt)
    db.commit()
    logger.info(f"管理员{admin_id}修改密码成功")
    return response.json({"code": 200, "msg": "密码修改成功"})
