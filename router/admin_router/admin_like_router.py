import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, Like, Post, Comment
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

admin_like_bp = Blueprint("admin_like", url_prefix="/api/admin/like")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_like_bp.get("/list")
@openapi.summary("获取点赞列表")
async def get_like_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取点赞列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    user_id = request.args.get("user_id")
    target_type = request.args.get("target_type")
    logger.info(f"管理员{admin_id}查询点赞列表:page={page},page_size={page_size}")
    query = db.query(Like)
    if user_id:
        query = query.filter(Like.user_id == user_id)
    if target_type:
        query = query.filter(Like.target_type == target_type)
    total = query.count()
    likes = query.order_by(Like.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    like_list = []
    for l in likes:
        user = db.query(User).filter(User.id == l.user_id).first()
        target_title = ""
        if l.target_type == "post":
            post = db.query(Post).filter(Post.id == l.target_id).first()
            target_title = post.title if post else ""
        elif l.target_type == "comment":
            comment = db.query(Comment).filter(Comment.id == l.target_id).first()
            target_title = comment.content[:50] if comment else ""
        like_list.append({"like_id": l.id, "user": {"user_id": user.id, "username": user.username, "avatar": user.avatar} if user else None, "target_id": l.target_id, "target_type": l.target_type, "target_title": target_title, "created_at": str(l.created_at)})
    logger.info(f"管理员{admin_id}查询点赞列表成功:共{total}条,返回{len(like_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": like_list, "total": total, "page": page, "page_size": page_size}})

@admin_like_bp.delete("/<like_id>")
@openapi.summary("删除点赞")
async def delete_like(request, like_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除点赞失败:admin_id无效,like_id={like_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}删除点赞:like_id={like_id}")
    like = db.query(Like).filter(Like.id == like_id).first()
    if not like:
        logger.warning(f"删除点赞失败:点赞不存在,like_id={like_id}")
        return response.json({"code": 404, "msg": "点赞不存在"})
    db.delete(like)
    db.commit()
    logger.info(f"管理员{admin_id}删除点赞成功:like_id={like_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_like_bp.post("/batch-delete")
@openapi.summary("批量删除点赞")
async def batch_delete_like(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除点赞失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除点赞失败:ids为空")
        return response.json({"code": 400, "msg": "ids不能为空"})
    logger.info(f"管理员{admin_id}批量删除点赞:ids={ids}")
    deleted = db.query(Like).filter(Like.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除点赞成功:deleted={deleted}")
    return response.json({"code": 200, "msg": f"成功删除{deleted}条点赞"})
