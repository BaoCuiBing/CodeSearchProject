import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, Message
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
admin_private_message_bp = Blueprint("admin_private_message", url_prefix="/api/admin/private_message")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_private_message_bp.get("/list")
@openapi.summary("获取私信列表")
async def get_private_message_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取私信列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    from_user_id = request.args.get("from_user_id")
    to_user_id = request.args.get("to_user_id")
    is_read = request.args.get("is_read")
    logger.info(f"管理员{admin_id}查询私信列表:page={page},page_size={page_size}")
    query = db.query(Message)
    if from_user_id:
        query = query.filter(Message.from_user_id == from_user_id)
    if to_user_id:
        query = query.filter(Message.to_user_id == to_user_id)
    if is_read is not None:
        query = query.filter(Message.is_read == int(is_read))
    total = query.count()
    messages = query.order_by(Message.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    msg_list = []
    for m in messages:
        from_user = db.query(User).filter(User.id == m.from_user_id).first()
        to_user = db.query(User).filter(User.id == m.to_user_id).first()
        msg_list.append({"message_id": m.id, "from_user": {"user_id": from_user.id, "username": from_user.username, "avatar": from_user.avatar} if from_user else None, "to_user": {"user_id": to_user.id, "username": to_user.username, "avatar": to_user.avatar} if to_user else None, "content": m.content, "is_read": m.is_read, "created_at": str(m.created_at)})
    logger.info(f"管理员{admin_id}查询私信列表成功:共{total}条,返回{len(msg_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": msg_list, "total": total, "page": page, "page_size": page_size}})

@admin_private_message_bp.get("/<message_id>/detail")
@openapi.summary("获取私信详情")
async def get_private_message_detail(request, message_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"获取私信详情失败:admin_id无效,message_id={message_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}获取私信详情:message_id={message_id}")
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        logger.warning(f"获取私信详情失败:私信不存在,message_id={message_id}")
        return response.json({"code": 404, "msg": "私信不存在"})
    from_user = db.query(User).filter(User.id == msg.from_user_id).first()
    to_user = db.query(User).filter(User.id == msg.to_user_id).first()
    msg_detail = {"message_id": msg.id, "from_user": {"user_id": from_user.id, "username": from_user.username, "avatar": from_user.avatar} if from_user else None, "to_user": {"user_id": to_user.id, "username": to_user.username, "avatar": to_user.avatar} if to_user else None, "content": msg.content, "is_read": msg.is_read, "created_at": str(msg.created_at)}
    logger.info(f"管理员{admin_id}获取私信详情成功:message_id={message_id}")
    return response.json({"code": 200, "msg": "获取成功", "data": msg_detail})

@admin_private_message_bp.delete("/<message_id>")
@openapi.summary("删除私信")
async def delete_private_message(request, message_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除私信失败:admin_id无效,message_id={message_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}删除私信:message_id={message_id}")
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        logger.warning(f"删除私信失败:私信不存在,message_id={message_id}")
        return response.json({"code": 404, "msg": "私信不存在"})
    db.delete(msg)
    db.commit()
    logger.info(f"管理员{admin_id}删除私信成功:message_id={message_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_private_message_bp.post("/batch-delete")
@openapi.summary("批量删除私信")
async def batch_delete_private_message(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除私信失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除私信失败:ids为空")
        return response.json({"code": 400, "msg": "ids不能为空"})
    logger.info(f"管理员{admin_id}批量删除私信:ids={ids}")
    deleted = db.query(Message).filter(Message.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除私信成功:deleted={deleted}")
    return response.json({"code": 200, "msg": f"成功删除{deleted}条私信"})
