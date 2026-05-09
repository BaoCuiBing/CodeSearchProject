import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import Category, Post
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
category_bp = Blueprint("category", url_prefix="/api/category")

@category_bp.get("/list")
@openapi.summary("获取所有分类列表")
async def get_categories(request):
    db = request.ctx.db
    logger.info("查询分类列表")
    try:
        categories = db.query(Category).order_by(Category.sort.asc(), Category.id.asc()).all()
        cat_list = []
        for c in categories:
            post_count = db.query(Post).filter(Post.category_id == c.id, Post.status == "published").count()
            cat_list.append({"category_id": c.id, "name": c.name, "description": c.description, "icon": c.icon, "sort": c.sort, "post_count": post_count})
        logger.info(f"获取分类列表成功:count={len(cat_list)}")
        return response.json({"code": 200, "msg": "获取成功", "data": cat_list})
    except Exception as e:
        logger.error(f"获取分类列表失败:{str(e)}")
        return response.json({"code": 500, "msg": "服务器内部错误"})