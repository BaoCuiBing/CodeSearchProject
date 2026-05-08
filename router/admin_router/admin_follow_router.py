import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, Follow
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
admin_follow_bp = Blueprint("admin_follow", url_prefix="/api/admin/follow")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_follow_bp.get("/list")
@openapi.summary("获取关注列表")
async def get_follow_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取关注列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    follower_id = request.args.get("follower_id")
    following_id = request.args.get("following_id")
    logger.info(f"管理员{admin_id}查询关注列表:page={page},page_size={page_size}")
    query = db.query(Follow)
    if follower_id:
        query = query.filter(Follow.follower_id == follower_id)
    if following_id:
        query = query.filter(Follow.following_id == following_id)
    total = query.count()
    follows = query.order_by(Follow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    follow_list = []
    for f in follows:
        follower = db.query(User).filter(User.id == f.follower_id).first()
        following = db.query(User).filter(User.id == f.following_id).first()
        follow_list.append({"follow_id": f.id, "follower": {"user_id": follower.id, "username": follower.username, "avatar": follower.avatar} if follower else None, "following": {"user_id": following.id, "username": following.username, "avatar": following.avatar} if following else None, "created_at": str(f.created_at)})
    logger.info(f"管理员{admin_id}查询关注列表成功:共{total}条,返回{len(follow_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": follow_list, "total": total, "page": page, "page_size": page_size}})

@admin_follow_bp.delete("/<follow_id>")
@openapi.summary("删除关注")
async def delete_follow(request, follow_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除关注失败:admin_id无效,follow_id={follow_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}删除关注:follow_id={follow_id}")
    follow = db.query(Follow).filter(Follow.id == follow_id).first()
    if not follow:
        logger.warning(f"删除关注失败:关注不存在,follow_id={follow_id}")
        return response.json({"code": 404, "msg": "关注不存在"})
    db.delete(follow)
    db.commit()
    logger.info(f"管理员{admin_id}删除关注成功:follow_id={follow_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_follow_bp.post("/batch-delete")
@openapi.summary("批量删除关注")
async def batch_delete_follow(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除关注失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除关注失败:ids为空")
        return response.json({"code": 400, "msg": "ids不能为空"})
    logger.info(f"管理员{admin_id}批量删除关注:ids={ids}")
    deleted = db.query(Follow).filter(Follow.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除关注成功:deleted={deleted}")
    return response.json({"code": 200, "msg": f"成功删除{deleted}条关注"})
