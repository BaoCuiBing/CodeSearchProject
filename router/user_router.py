from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User
from models.db_init import get_db_session

user_bp = Blueprint("user", url_prefix="/api/user")

@user_bp.post("/register")
@openapi.summary("用户注册")
@openapi.body({"application/json": User})
async def register(request, db):
    data = request.json
    new_user = User(usernumber=data["usernumber"], username=data["username"], password=data["password"], email=data.get("email"))
    db.add(new_user)
    db.commit()
    return response.json({"code": 200, "msg": "注册成功"})

@user_bp.post("/login")
@openapi.summary("用户登录")
async def login(request, db):
    data = request.json
    user = db.query(User).filter(User.usernumber == data["usernumber"], User.password == data["password"]).first()
    if user:
        return response.json({"code": 200, "msg": "登录成功", "data": {"id": user.id, "username": user.username}})
    return response.json({"code": 401, "msg": "账号或密码错误"})
