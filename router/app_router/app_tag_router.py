import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import Tag, PostTag, Post, User

logger = logging.getLogger(__name__)
tag_bp = Blueprint("tag", url_prefix="/api/tag")

@tag_bp.get("/list")
@openapi.summary("获取所有标签列表")
async def get_tag_list(request):
    db = request.ctx.db
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "name")
    logger.info(f"查询标签列表:page={page},sort={sort}")
    query = db.query(Tag).filter(Tag.status == "active")
    if keyword:
        query = query.filter(Tag.name.contains(keyword))
    if sort == "count":
        query = query.order_by(Tag.post_count.desc())
    elif sort == "hot":
        query = query.filter(Tag.is_hot == 1).order_by(Tag.post_count.desc())
    else:
        query = query.order_by(Tag.name.asc())
    total = query.count()
    tags = query.offset((page - 1) * page_size).limit(page_size).all()
    tag_list = []
    for t in tags:
        tag_list.append({"tag_id": t.id, "name": t.name, "slug": t.slug, "description": t.description, "icon": t.icon, "color": t.color, "post_count": t.post_count or 0, "is_hot": bool(t.is_hot)})
    logger.info(f"获取标签列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": tag_list, "total": total, "page": page, "page_size": page_size}})

@tag_bp.get("/<tag_id>")
@openapi.summary("获取标签详情")
async def get_tag_detail(request, tag_id):
    db = request.ctx.db
    logger.info(f"查询标签详情:tag_id={tag_id}")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        logger.warning(f"获取标签详情失败:标签不存在,tag_id={tag_id}")
        return response.json({"code": 404, "msg": "标签不存在"})
    logger.info(f"获取标签详情成功:name={tag.name}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"tag_id": tag.id, "name": tag.name, "slug": tag.slug, "description": tag.description, "icon": tag.icon, "color": tag.color, "post_count": tag.post_count or 0, "is_hot": bool(tag.is_hot), "is_recommend": bool(tag.is_recommend), "created_at": str(tag.created_at)}})

@tag_bp.get("/<tag_id>/articles")
@openapi.summary("获取标签下的文章列表")
async def get_tag_articles(request, tag_id):
    db = request.ctx.db
    post_type = request.args.get("type", "all")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    sort = request.args.get("sort", "time")
    logger.info(f"查询标签文章:tag_id={tag_id},type={post_type}")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        logger.warning(f"获取标签文章失败:标签不存在,tag_id={tag_id}")
        return response.json({"code": 404, "msg": "标签不存在"})
    query = db.query(Post).join(PostTag).filter(PostTag.tag_id == tag_id, Post.status == "published")
    if post_type != "all":
        query = query.filter(Post.type == post_type)
    if sort == "hot":
        query = query.order_by(Post.like_count.desc(), Post.view_count.desc())
    else:
        query = query.order_by(Post.created_at.desc())
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        post_list.append({"post_id": p.id, "type": p.type, "title": p.title, "summary": p.summary, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "created_at": str(p.created_at)})
    logger.info(f"获取标签文章成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": post_list, "total": total, "page": page, "page_size": page_size}})

@tag_bp.get("/hot")
@openapi.summary("获取热门标签")
async def get_hot_tags(request):
    db = request.ctx.db
    limit = int(request.args.get("limit", 20))
    if limit > 100:
        logger.warning("获取热门标签失败:数量超出限制")
        return response.json({"code": 400, "msg": "返回数量超出限制"})
    logger.info(f"查询热门标签:limit={limit}")
    tags = db.query(Tag).filter(Tag.is_hot == 1, Tag.status == "active").order_by(Tag.post_count.desc()).limit(limit).all()
    tag_list = [{"tag_id": t.id, "name": t.name, "slug": t.slug, "icon": t.icon, "color": t.color, "post_count": t.post_count or 0} for t in tags]
    logger.info(f"获取热门标签成功:count={len(tag_list)}")
    return response.json({"code": 200, "msg": "获取成功", "data": tag_list})