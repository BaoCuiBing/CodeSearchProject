import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import User, Notification, Message, SystemMessage, SystemMessageTarget

logger = logging.getLogger(__name__)
message_bp = Blueprint("message", url_prefix="/api/message")

@message_bp.get("/notifications")
@openapi.summary("获取系统通知列表")
async def get_notifications(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取通知失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    notif_type = request.args.get("type", "all")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询通知列表:user_id={user_id}")
    notif_list = []
    if notif_type in ["all", "system"]:
        sys_targets = db.query(SystemMessageTarget).filter(SystemMessageTarget.user_id == user_id).all()
        for st in sys_targets:
            sm = db.query(SystemMessage).filter(SystemMessage.id == st.message_id, SystemMessage.status == "sent").first()
            if sm:
                notif_list.append({"notification_id": sm.id, "type": "system", "content": sm.content, "title": sm.title, "is_read": bool(st.is_read), "created_at": str(sm.send_time or sm.created_at), "related_id": sm.id, "actor": None})
    if notif_type in ["all", "comment", "like", "follow"]:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if notif_type != "all":
            query = query.filter(Notification.type == notif_type)
        notifs = query.order_by(Notification.created_at.desc()).all()
        for n in notifs:
            actor = None
            if n.type in ["comment", "like", "follow"]:
                actor = db.query(User).filter(User.id == n.related_id).first()
            notif_list.append({"notification_id": n.id, "type": n.type, "content": n.content, "is_read": bool(n.is_read), "created_at": str(n.created_at), "related_id": n.related_id, "actor": {"user_id": actor.id, "username": actor.username, "avatar": actor.avatar} if actor else None})
    notif_list.sort(key=lambda x: x["created_at"], reverse=True)
    total = len(notif_list)
    unread_count = sum(1 for n in notif_list if not n["is_read"])
    paged = notif_list[(page - 1) * page_size:page * page_size]
    logger.info(f"获取通知列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": paged, "total": total, "unread_count": unread_count, "page": page, "page_size": page_size}})

@message_bp.put("/notification/read")
@openapi.summary("标记通知为已读")
async def mark_notification_read(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    notification_id = data.get("notification_id")
    if not user_id or not notification_id:
        logger.warning("标记已读失败:参数为空")
        return response.json({"code": 400, "msg": "参数错误"})
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if not notif:
        logger.warning(f"标记已读失败:通知不存在,notification_id={notification_id}")
        return response.json({"code": 404, "msg": "通知不存在"})
    notif.is_read = 1
    db.commit()
    return response.json({"code": 200, "msg": "标记成功"})

@message_bp.put("/notifications/read-all")
@openapi.summary("标记所有通知为已读")
async def mark_all_notifications_read(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        logger.warning("标记全部已读失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == 0).update({"is_read": 1})
    db.commit()
    return response.json({"code": 200, "msg": "标记成功"})

@message_bp.delete("/notification/<notification_id>")
@openapi.summary("删除通知")
async def delete_notification(request, notification_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("删除通知失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if not notif:
        logger.warning(f"删除通知失败:通知不存在,notification_id={notification_id}")
        return response.json({"code": 404, "msg": "通知不存在"})
    db.delete(notif)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@message_bp.get("/notification/unread-count")
@openapi.summary("获取未读通知数量")
async def get_unread_notification_count(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取未读数失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    total = db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == 0).count()
    comment = db.query(Notification).filter(Notification.user_id == user_id, Notification.type == "comment", Notification.is_read == 0).count()
    like = db.query(Notification).filter(Notification.user_id == user_id, Notification.type == "like", Notification.is_read == 0).count()
    follow = db.query(Notification).filter(Notification.user_id == user_id, Notification.type == "follow", Notification.is_read == 0).count()
    system = db.query(Notification).filter(Notification.user_id == user_id, Notification.type == "system", Notification.is_read == 0).count()
    system_msg = db.query(SystemMessageTarget).filter(SystemMessageTarget.user_id == user_id, SystemMessageTarget.is_read == 0).count()
    total += system_msg
    return response.json({"code": 200, "msg": "获取成功", "data": {"total": total, "comment": comment, "like": like, "follow": follow, "system": system, "system_msg": system_msg}})

@message_bp.get("/conversations")
@openapi.summary("获取私信会话列表")
async def get_conversations(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取会话列表失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    user_id = int(user_id)
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询会话列表:user_id={user_id}")
    msgs = db.query(Message).filter((Message.from_user_id == user_id) | (Message.to_user_id == user_id)).order_by(Message.created_at.desc()).all()
    conv_dict = {}
    for m in msgs:
        other_id = m.to_user_id if m.from_user_id == user_id else m.from_user_id
        if other_id not in conv_dict:
            conv_dict[other_id] = {"last_message": m, "unread": 0}
        if m.to_user_id == user_id and m.is_read == 0:
            conv_dict[other_id]["unread"] += 1
    total = len(conv_dict)
    conv_list = []
    for other_id, info in list(conv_dict.items())[(page-1)*page_size:page*page_size]:
        user = db.query(User).filter(User.id == other_id).first()
        conv_list.append({"user": {"user_id": user.id, "username": user.username, "avatar": user.avatar} if user else None, "last_message": info["last_message"].content, "last_time": str(info["last_message"].created_at), "unread_count": info["unread"]})
    logger.info(f"获取会话列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": conv_list, "total": total, "page": page, "page_size": page_size}})

@message_bp.get("/conversation/user/<to_user_id>")
@openapi.summary("获取会话消息详情")
async def get_conversation_messages(request, to_user_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取消息失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询会话消息:user_id={user_id},to_user_id={to_user_id}")
    user = db.query(User).filter(User.id == to_user_id).first()
    if not user:
        logger.warning(f"获取消息失败:用户不存在,to_user_id={to_user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    query = db.query(Message).filter(((Message.from_user_id == user_id) & (Message.to_user_id == to_user_id)) | ((Message.from_user_id == to_user_id) & (Message.to_user_id == user_id)))
    total = query.count()
    msgs = query.order_by(Message.created_at.asc()).offset((page - 1) * page_size).limit(page_size).all()
    msg_list = [{"message_id": m.id, "from_user_id": m.from_user_id, "to_user_id": m.to_user_id, "content": m.content, "is_read": bool(m.is_read), "created_at": str(m.created_at)} for m in msgs]
    logger.info(f"获取会话消息成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": msg_list, "total": total, "page": page, "page_size": page_size}})

@message_bp.post("/send")
@openapi.summary("发送私信")
async def send_private_message(request):
    db = request.ctx.db
    data = request.json
    from_user_id = data.get("from_user_id")
    to_user_id = data.get("to_user_id")
    content = data.get("content")
    if not from_user_id or not to_user_id or not content:
        logger.warning("发送私信失败:参数为空")
        return response.json({"code": 400, "msg": "参数错误"})
    if len(content) > 500:
        logger.warning("发送私信失败:内容超出限制")
        return response.json({"code": 400, "msg": "消息内容最多500字"})
    to_user = db.query(User).filter(User.id == to_user_id).first()
    if not to_user:
        logger.warning(f"发送私信失败:用户不存在,to_user_id={to_user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"发送私信:from={from_user_id},to={to_user_id}")
    new_msg = Message(from_user_id=from_user_id, to_user_id=to_user_id, content=content)
    db.add(new_msg)
    db.commit()
    logger.info(f"发送私信成功:message_id={new_msg.id}")
    return response.json({"code": 200, "msg": "发送成功", "data": {"message_id": new_msg.id}})

@message_bp.delete("/conversation/user/<to_user_id>")
@openapi.summary("删除会话")
async def delete_conversation(request, to_user_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("删除会话失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    user_id = int(user_id)
    to_user_id = int(to_user_id)
    user = db.query(User).filter(User.id == to_user_id).first()
    if not user:
        logger.warning(f"删除会话失败:用户不存在,to_user_id={to_user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    db.query(Message).filter(((Message.from_user_id == user_id) & (Message.to_user_id == to_user_id)) | ((Message.from_user_id == to_user_id) & (Message.to_user_id == user_id))).delete()
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})