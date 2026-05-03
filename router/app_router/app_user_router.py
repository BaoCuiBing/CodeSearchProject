import re
import logging
from datetime import datetime
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User
from models.db_init import get_db_session
from utils.password_analysis import generate_salt, hash_password, verify_password

logger = logging.getLogger(__name__)

user_bp = Blueprint("user", url_prefix="/api/user")

@user_bp.post("/register")
@openapi.summary("用户注册")
async def register(request):
    db = request.ctx.db
    data = request.json
    usernumber = data.get("usernumber")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")
    if not usernumber or not username or not password:
        logger.warning("用户注册失败:必填字段为空")
        return response.json({"code": 400, "msg": "账号、用户名、密码不能为空"})
    if not re.match(r'^[a-zA-Z0-9_]{6,20}$', usernumber):
        logger.warning(f"用户注册失败:账号格式不正确,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号格式不正确(字母、数字、下划线,6-20位)"})
    if len(password) < 6:
        logger.warning("用户注册失败:密码长度不足")
        return response.json({"code": 400, "msg": "密码不能少于6位"})
    exist_user = db.query(User).filter(User.usernumber == usernumber).first()
    if exist_user:
        logger.warning(f"用户注册失败:账号已存在,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号已存在"})
    logger.info(f"用户注册:usernumber={usernumber},username={username}")
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    new_user = User(usernumber=usernumber, username=username, password=hashed_password, salt=salt, email=email)
    db.add(new_user)
    db.commit()
    logger.info(f"用户注册成功:user_id={new_user.id},username={username}")
    return response.json({"code": 200, "msg": "注册成功", "data": {"user_id": new_user.id, "username": new_user.username, "role": new_user.role}})

@user_bp.post("/login")
@openapi.summary("用户登录")
async def login(request):
    db = request.ctx.db
    data = request.json
    usernumber = data.get("usernumber")
    password = data.get("password")
    if not usernumber or not password:
        logger.warning("用户登录失败:账号或密码为空")
        return response.json({"code": 400, "msg": "账号或密码不能为空"})
    user = db.query(User).filter(User.usernumber == usernumber).first()
    if not user:
        logger.warning(f"用户登录失败:用户不存在,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号或密码错误"})
    if not verify_password(password, user.salt, user.password):
        logger.warning(f"用户登录失败:密码错误,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号或密码错误"})
    if user.status == "banned":
        ban_info = {"ban_reason": user.ban_reason, "ban_expire_time": str(user.ban_expire_time) if user.ban_expire_time else None}
        logger.warning(f"用户登录失败:账号被封禁,usernumber={usernumber}")
        return response.json({"code": 403, "msg": "账号被封禁", "data": ban_info})
    user.last_login_time = datetime.now()
    db.commit()
    logger.info(f"用户登录成功:user_id={user.id},username={user.username}")
    return response.json({"code": 200, "msg": "登录成功", "data": {"user_id": user.id, "username": user.username, "role": user.role}})