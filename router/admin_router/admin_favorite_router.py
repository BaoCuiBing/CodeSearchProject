import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from models.model import User, Favorite, Post

logger = logging.getLogger(__name__)
admin_favorite_bp = Blueprint("admin_favorite", url_prefix="/api/admin/favorite")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_favorite_bp.get("/list")
@openapi.summary("获取收藏列表")
async def get_favorite_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取收藏列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    user_id = request.args.get("user_id")
    post_id = request.args.get("post_id")
    logger.info(f"管理员{admin_id}查询收藏列表:page={page},page_size={page_size}")
    query = db.query(Favorite)
    if user_id:
        query = query.filter(Favorite.user_id == user_id)
    if post_id:
        query = query.filter(Favorite.post_id == post_id)
    total = query.count()
    favorites = query.order_by(Favorite.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    fav_list = []
    for f in favorites:
        user = db.query(User).filter(User.id == f.user_id).first()
        post = db.query(Post).filter(Post.id == f.post_id).first()
        post_author = db.query(User).filter(User.id == post.user_id).first() if post else None
        fav_list.append({"favorite_id": f.id, "user": {"user_id": user.id, "username": user.username, "avatar": user.avatar} if user else None, "post": {"post_id": post.id, "title": post.title, "type": post.type, "user": {"user_id": post_author.id, "username": post_author.username} if post_author else None} if post else None, "created_at": str(f.created_at)})
    logger.info(f"管理员{admin_id}查询收藏列表成功:共{total}条,返回{len(fav_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": fav_list, "total": total, "page": page, "page_size": page_size}})

@admin_favorite_bp.delete("/<favorite_id>")
@openapi.summary("删除收藏")
async def delete_favorite(request, favorite_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除收藏失败:admin_id无效,favorite_id={favorite_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}删除收藏:favorite_id={favorite_id}")
    fav = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not fav:
        logger.warning(f"删除收藏失败:收藏不存在,favorite_id={favorite_id}")
        return response.json({"code": 404, "msg": "收藏不存在"})
    db.delete(fav)
    db.commit()
    logger.info(f"管理员{admin_id}删除收藏成功:favorite_id={favorite_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_favorite_bp.post("/batch-delete")
@openapi.summary("批量删除收藏")
async def batch_delete_favorite(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除收藏失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除收藏失败:ids为空")
        return response.json({"code": 400, "msg": "ids不能为空"})
    logger.info(f"管理员{admin_id}批量删除收藏:ids={ids}")
    deleted = db.query(Favorite).filter(Favorite.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除收藏成功:deleted={deleted}")
    return response.json({"code": 200, "msg": f"成功删除{deleted}条收藏"})
