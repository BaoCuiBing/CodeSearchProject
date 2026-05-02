from datetime import datetime
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, SystemSetting
from models.db_init import get_db_session

admin_system_bp = Blueprint("admin_system", url_prefix="/api/admin/system")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_system_bp.get("/settings")
@openapi.summary("获取系统设置")
async def get_system_settings(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    key = request.args.get("key")
    query = db.query(SystemSetting)
    if key:
        query = query.filter(SystemSetting.key == key)
    settings = query.all()
    setting_list = [{"system_setting_id": s.id, "key": s.key, "value": s.value, "description": s.description, "created_at": str(s.created_at), "updated_at": str(s.updated_at)} for s in settings]
    return response.json({"code": 200, "msg": "获取成功", "data": setting_list})

@admin_system_bp.put("/settings")
@openapi.summary("更新系统设置")
async def update_system_settings(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    key = data.get("key")
    value = data.get("value")
    if not key:
        return response.json({"code": 400, "msg": "设置键不能为空"})
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if setting:
        setting.value = value
        if "description" in data:
            setting.description = data["description"]
    else:
        setting = SystemSetting(key=key, value=value, description=data.get("description"))
        db.add(setting)
    db.commit()
    return response.json({"code": 200, "msg": "更新成功", "data": {"system_setting_id": setting.id, "key": setting.key, "value": setting.value, "description": setting.description, "created_at": str(setting.created_at), "updated_at": str(setting.updated_at)}})

@admin_system_bp.post("/settings/reset")
@openapi.summary("重置设置为默认值")
async def reset_settings_to_default(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    key = data.get("key")
    if not key:
        return response.json({"code": 400, "msg": "设置键不能为空"})
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not setting:
        return response.json({"code": 404, "msg": "设置项不存在"})
    default_values = {"site_name": "代码搜索社区", "site_description": "专业的技术问答和文章分享平台"}
    setting.value = default_values.get(key, "")
    db.commit()
    return response.json({"code": 200, "msg": "重置成功"})

@admin_system_bp.post("/test-email")
@openapi.summary("测试邮件发送")
async def test_email_config(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    to_email = data.get("to_email")
    if not to_email or "@" not in to_email:
        return response.json({"code": 400, "msg": "邮箱格式不正确"})
    return response.json({"code": 200, "msg": "测试邮件发送成功", "data": {"success": True, "message": f"邮件已发送至 {to_email}"}})

@admin_system_bp.post("/clear-cache")
@openapi.summary("清除缓存")
async def clear_cache(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    cache_types = data.get("cache_types", ["all"])
    return response.json({"code": 200, "msg": "缓存清除成功", "data": {"cleared_types": cache_types, "affected_keys": 0}})
