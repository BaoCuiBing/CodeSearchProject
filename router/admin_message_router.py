from datetime import datetime
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, SystemMessage, SystemMessageTarget, Notification
from models.db_init import get_db_session

admin_message_bp = Blueprint("admin_system_message", url_prefix="/api/admin/system_messages")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_message_bp.get("/list")
@openapi.summary("获取系统消息列表")
async def get_system_messages_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    type_filter = request.args.get("type", "all")
    status = request.args.get("status", "all")
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    query = db.query(SystemMessage)
    if type_filter != "all":
        query = query.filter(SystemMessage.type == type_filter)
    if status != "all":
        query = query.filter(SystemMessage.status == status)
    if keyword:
        query = query.filter(SystemMessage.title.contains(keyword) | SystemMessage.content.contains(keyword))
    sort_map = {"created_time": SystemMessage.created_at, "send_time": SystemMessage.send_time}
    order_func = sort_map.get(sort, SystemMessage.created_at).desc() if order == "desc" else sort_map.get(sort, SystemMessage.created_at).asc()
    total = query.count()
    messages = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    message_list = []
    for m in messages:
        sender = db.query(User).filter(User.id == m.sender_id).first()
        target_count = db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == m.id).count()
        read_count = db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == m.id, SystemMessageTarget.is_read == 1).count()
        message_list.append({"system_message_id": m.id, "type": m.type, "title": m.title, "content": m.content, "target_type": m.target_type, "target_count": target_count, "read_count": read_count, "status": m.status, "is_top": bool(m.is_top), "priority": m.priority, "sender": {"user_id": sender.id, "username": sender.username} if sender else None, "send_time": str(m.send_time) if m.send_time else None, "created_at": str(m.created_at), "updated_at": str(m.updated_at)})
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": message_list, "total": total, "page": page, "page_size": page_size}})

@admin_message_bp.post("/")
@openapi.summary("创建系统消息")
async def create_system_message(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    title = data.get("title")
    content = data.get("content")
    type_filter = data.get("type")
    target_type = data.get("target_type")
    if not title or not content or not type_filter or not target_type:
        return response.json({"code": 400, "msg": "必填字段不能为空"})
    message = SystemMessage(sender_id=admin_id, title=title, content=content, type=type_filter, target_type=target_type, priority=data.get("priority", "medium"), is_top=1 if data.get("is_top") else 0, status="draft")
    db.add(message)
    db.commit()
    if target_type == "user_list":
        target_ids = data.get("target_ids", [])
        for uid in target_ids:
            target = SystemMessageTarget(message_id=message.id, user_id=uid)
            db.add(target)
        db.commit()
    return response.json({"code": 200, "msg": "创建成功", "data": {"system_message_id": message.id, "type": message.type, "title": message.title, "status": message.status, "created_at": str(message.created_at)}})

@admin_message_bp.put("/")
@openapi.summary("编辑系统消息")
async def edit_system_message(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    message_id = data.get("system_message_id")
    message = db.query(SystemMessage).filter(SystemMessage.id == message_id).first()
    if not message:
        return response.json({"code": 404, "msg": "消息不存在"})
    if "title" in data:
        message.title = data["title"]
    if "content" in data:
        message.content = data["content"]
    if "type" in data:
        message.type = data["type"]
    if "priority" in data:
        message.priority = data["priority"]
    if "is_top" in data:
        message.is_top = 1 if data["is_top"] else 0
    db.commit()
    return response.json({"code": 200, "msg": "更新成功", "data": {"system_message_id": message.id, "type": message.type, "title": message.title, "updated_at": str(message.updated_at)}})

@admin_message_bp.delete("/<system_message_id>")
@openapi.summary("删除系统消息")
async def delete_system_message(request, system_message_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    message = db.query(SystemMessage).filter(SystemMessage.id == system_message_id).first()
    if not message:
        return response.json({"code": 404, "msg": "消息不存在"})
    db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == system_message_id).delete()
    db.delete(message)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@admin_message_bp.post("/send")
@openapi.summary("发送消息")
async def send_system_message(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    message_id = data.get("system_message_id")
    message = db.query(SystemMessage).filter(SystemMessage.id == message_id).first()
    if not message:
        return response.json({"code": 404, "msg": "消息不存在"})
    if message.status == "sent":
        return response.json({"code": 400, "msg": "该消息已发送，不能重复发送"})
    message.status = "sent"
    message.send_time = datetime.now()
    if message.target_type == "all":
        users = db.query(User).all()
        for u in users:
            target = SystemMessageTarget(message_id=message.id, user_id=u.id)
            db.add(target)
    db.commit()
    return response.json({"code": 200, "msg": "发送成功", "data": {"system_message_id": message.id, "status": message.status, "send_time": str(message.send_time)}})

@admin_message_bp.post("/batch-delete")
@openapi.summary("批量删除消息")
async def batch_delete_messages(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        return response.json({"code": 400, "msg": "请选择要删除的消息"})
    for mid in ids:
        message = db.query(SystemMessage).filter(SystemMessage.id == mid).first()
        if message:
            db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == mid).delete()
            db.delete(message)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功", "data": {"deleted_count": len(ids)}})

@admin_message_bp.get("/stats/overview")
@openapi.summary("获取消息统计概览")
async def get_message_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    total_messages = db.query(SystemMessage).count()
    sent_today = db.query(SystemMessage).filter(func.date(SystemMessage.send_time) == datetime.now().date()).count()
    sent_week = db.query(SystemMessage).filter(SystemMessage.send_time >= datetime.now() - timedelta(days=7)).count()
    draft_count = db.query(SystemMessage).filter(SystemMessage.status == "draft").count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_messages": total_messages, "sent_today": sent_today, "sent_week": sent_week, "draft_count": draft_count, "total_read_count": 0, "avg_read_rate": 0, "by_type": {"system": 0, "announcement": 0}, "trend_data": []}})

@admin_message_bp.get("/<system_message_id>/detail")
@openapi.summary("获取消息详情")
async def get_system_message_detail(request, system_message_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    message = db.query(SystemMessage).filter(SystemMessage.id == system_message_id).first()
    if not message:
        return response.json({"code": 404, "msg": "消息不存在"})
    target_count = db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == message.id).count()
    read_count = db.query(SystemMessageTarget).filter(SystemMessageTarget.message_id == message.id, SystemMessageTarget.is_read == 1).count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"system_message_id": message.id, "type": message.type, "title": message.title, "content": message.content, "status": message.status, "stats": {"target_count": target_count, "read_count": read_count, "unread_count": target_count - read_count, "read_rate": round(read_count / target_count * 100, 2) if target_count > 0 else 0}, "read_users": [], "unread_users": [], "created_at": str(message.created_at), "send_time": str(message.send_time) if message.send_time else None}})

@admin_message_bp.post("/send-to-user")
@openapi.summary("发送消息给指定用户")
async def send_system_notification_to_user(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    if not user_id or not title or not content:
        return response.json({"code": 400, "msg": "必填字段不能为空"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return response.json({"code": 404, "msg": "用户不存在"})
    notification = Notification(user_id=user_id, type="system_msg", content=f"{title}: {content}")
    db.add(notification)
    db.commit()
    return response.json({"code": 200, "msg": "发送成功", "data": {"notification_id": notification.id, "user_id": user_id, "created_at": str(notification.created_at)}})
