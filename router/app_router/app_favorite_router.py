import json
import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import Favorite, Post, User
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

favorite_bp = Blueprint("favorite", url_prefix="/api/favorite")

@favorite_bp.get("/list")
@openapi.summary("获取我的收藏列表")
async def get_my_favorites(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取收藏列表失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    post_type = request.args.get("type", "all")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    sort = request.args.get("sort", "time")
    logger.info(f"查询收藏列表:user_id={user_id}")
    query = db.query(Favorite).filter(Favorite.user_id == user_id).join(Post)
    if post_type != "all":
        query = query.filter(Post.type == post_type)
    if sort == "title":
        query = query.order_by(Post.title.asc())
    else:
        query = query.order_by(Favorite.created_at.desc())
    total = query.count()
    favorites = db.query(Favorite, Post).join(Post, Favorite.post_id == Post.id).filter(Favorite.user_id == user_id).offset((page - 1) * page_size).limit(page_size).all()
    fav_list = []
    for fav, post in favorites:
        cover_image = json.loads(post.cover_image) if post.cover_image else None
        fav_list.append({"post_id": post.id, "post": {"post_id": post.id, "title": post.title, "type": post.type, "summary": post.summary, "cover_image": cover_image}, "created_at": str(fav.created_at)})
    logger.info(f"获取收藏列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": fav_list, "total": total, "page": page, "page_size": page_size}})

@favorite_bp.post("/batch-delete")
@openapi.summary("批量取消收藏")
async def batch_remove_favorites(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    ids = data.get("ids", [])
    if not user_id:
        logger.warning("批量取消收藏失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    if not ids:
        logger.warning("批量取消收藏失败:未选择收藏")
        return response.json({"code": 400, "msg": "请选择要取消的收藏"})
    logger.info(f"批量取消收藏:user_id={user_id},count={len(ids)}")
    deleted = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.post_id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"批量取消收藏成功:deleted={deleted}")
    return response.json({"code": 200, "msg": "取消成功", "data": {"deleted_count": deleted}})

@favorite_bp.get("/check/<post_id>")
@openapi.summary("检查是否已收藏")
async def check_is_favorited(request, post_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("检查收藏失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    logger.info(f"检查收藏:user_id={user_id},post_id={post_id}")
    fav = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.post_id == post_id).first()
    return response.json({"code": 200, "msg": "查询成功", "data": {"is_favorited": fav is not None}})

@favorite_bp.post("/toggle")
@openapi.summary("收藏或取消收藏")
async def toggle_favorite(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    if not user_id or not post_id:
        logger.warning("收藏失败:参数为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"收藏失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    fav = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.post_id == post_id).first()
    if fav:
        db.delete(fav)
        is_favorited = False
        logger.info(f"取消收藏:user_id={user_id},post_id={post_id}")
    else:
        db.add(Favorite(user_id=user_id, post_id=post_id))
        is_favorited = True
        logger.info(f"收藏:user_id={user_id},post_id={post_id}")
    db.commit()
    favorite_count = db.query(Favorite).filter(Favorite.post_id == post_id).count()
    return response.json({"code": 200, "msg": "操作成功", "data": {"is_favorited": is_favorited, "favorite_count": favorite_count}})