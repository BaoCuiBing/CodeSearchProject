import json
import logging
from datetime import datetime, timedelta
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import User, Post, Category, Tag, PostTag, Comment, Favorite, Like

logger = logging.getLogger(__name__)
admin_article_bp = Blueprint("admin_article", url_prefix="/api/admin/article")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_article_bp.get("/list")
@openapi.summary("获取文章列表")
async def get_content_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取文章列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    type_filter = request.args.get("type", "all")
    keyword = request.args.get("keyword")
    status = request.args.get("status", "published")
    author_id = request.args.get("author_id")
    tag_id = request.args.get("tag_id")
    category_id = request.args.get("category_id")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    is_top = request.args.get("is_top", "all")
    logger.info(f"管理员{admin_id}查询文章列表:page={page},page_size={page_size},type={type_filter},keyword={keyword},status={status}")
    query = db.query(Post)
    if type_filter != "all":
        query = query.filter(Post.type == type_filter)
        logger.debug(f"查询条件:type过滤={type_filter}")
    if status != "all":
        query = query.filter(Post.status == status)
        logger.debug(f"查询条件:status过滤={status}")
    if keyword:
        query = query.filter(Post.title.contains(keyword) | Post.content.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    if author_id:
        query = query.filter(Post.user_id == author_id)
        logger.debug(f"查询条件:author_id={author_id}")
    if category_id:
        query = query.filter(Post.category_id == category_id)
        logger.debug(f"查询条件:category_id={category_id}")
    if tag_id:
        query = query.join(PostTag).filter(PostTag.tag_id == tag_id)
        logger.debug(f"查询条件:tag_id={tag_id}")
    if date_start:
        query = query.filter(Post.created_at >= date_start)
        logger.debug(f"查询条件:date_start={date_start}")
    if date_end:
        query = query.filter(Post.created_at <= date_end)
        logger.debug(f"查询条件:date_end={date_end}")
    if is_top != "all":
        query = query.filter(Post.is_top == (1 if is_top == "yes" else 0))
        logger.debug(f"查询条件:is_top={is_top}")
    sort_map = {"created_time": Post.created_at, "updated_time": Post.updated_at, "view_count": Post.view_count, "like_count": Post.like_count, "comment_count": Post.comment_count}
    order_func = sort_map.get(sort, Post.created_at).desc() if order == "desc" else sort_map.get(sort, Post.created_at).asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    posts = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    logger.info(f"管理员{admin_id}查询文章列表成功:共{total}条,返回{len(posts)}条")
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        category = db.query(Category).filter(Category.id == p.category_id).first() if p.category_id else None
        tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == p.id).all()
        cover_image = json.loads(p.cover_image) if p.cover_image else None
        post_list.append({"post_id": p.id, "type": p.type, "title": p.title, "summary": p.summary, "cover_image": cover_image, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "category": {"category_id": category.id, "name": category.name} if category else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "status": p.status, "is_top": bool(p.is_top), "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "created_at": str(p.created_at), "updated_at": str(p.updated_at)})
    logger.debug(f"数据处理完成:构建{len(post_list)}条文章记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": post_list, "total": total, "page": page, "page_size": page_size}})

@admin_article_bp.get("/<post_id>")
@openapi.summary("获取文章详情")
async def get_content_detail(request, post_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"获取文章详情失败:admin_id无效,post_id={post_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}查询文章详情:post_id={post_id}")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"获取文章详情失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    author = db.query(User).filter(User.id == post.user_id).first()
    category = db.query(Category).filter(Category.id == post.category_id).first() if post.category_id else None
    tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == post.id).all()
    cover_image = json.loads(post.cover_image) if post.cover_image else None
    logger.info(f"管理员{admin_id}查询文章详情成功:title={post.title}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"post_id": post.id, "type": post.type, "title": post.title, "content": post.content, "summary": post.summary, "cover_image": cover_image, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar, "email": author.email} if author else None, "category": {"category_id": category.id, "name": category.name} if category else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "status": post.status, "is_top": bool(post.is_top), "stats": {"view_count": post.view_count, "like_count": post.like_count, "comment_count": post.comment_count}, "created_at": str(post.created_at), "updated_at": str(post.updated_at)}})

@admin_article_bp.post("/")
@openapi.summary("创建文章")
async def create_content(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("创建文章失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        logger.warning("创建文章失败:标题或内容为空")
        return response.json({"code": 400, "msg": "标题和内容不能为空"})
    logger.info(f"管理员{admin_id}创建文章:title={title}")
    post_type = data.get("post_type", "article")
    summary = data.get("summary", "")
    cover_image = data.get("cover_image")
    if isinstance(cover_image, dict):
        cover_image = json.dumps(cover_image)
    category_id = data.get("category_id")
    status = data.get("status", "published")
    is_top = 1 if data.get("is_top") else 0
    post = Post(user_id=admin.id, type=post_type, title=title, content=content, summary=summary, cover_image=cover_image, category_id=category_id, status=status, is_top=is_top)
    db.add(post)
    db.commit()
    logger.info(f"管理员{admin_id}创建文章成功:post_id={post.id}")
    return response.json({"code": 200, "msg": "创建成功", "data": {"post_id": post.id}})

@admin_article_bp.put("/")
@openapi.summary("编辑文章")
async def edit_content(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("编辑文章失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post_id = data.get("post_id")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"编辑文章失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    logger.info(f"管理员{admin_id}编辑文章:post_id={post_id}")
    if "title" in data:
        post.title = data["title"]
        logger.debug(f"更新字段:title={data['title']}")
    if "content" in data:
        post.content = data["content"]
        logger.debug("更新字段:content")
    if "summary" in data:
        post.summary = data["summary"]
        logger.debug(f"更新字段:summary={data['summary']}")
    if "cover_image" in data:
        post.cover_image = data["cover_image"] if isinstance(data["cover_image"], str) else json.dumps(data["cover_image"])
        logger.debug("更新字段:cover_image")
    if "category_id" in data:
        cat_id = data["category_id"]
        post.category_id = int(cat_id) if cat_id and cat_id != "" else None
        logger.debug(f"更新字段:category_id={cat_id}")
    if "tags" in data:
        db.query(PostTag).filter(PostTag.post_id == post_id).delete()
        for tag_id in data["tags"]:
            post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.add(post_tag)
        logger.debug(f"更新字段:tags={data['tags']}")
    if "status" in data:
        post.status = data["status"]
        logger.debug(f"更新字段:status={data['status']}")
    if "is_top" in data:
        post.is_top = 1 if data["is_top"] else 0
        logger.debug(f"更新字段:is_top={data['is_top']}")
    db.commit()
    logger.info(f"管理员{admin_id}编辑文章成功:post_id={post_id}")
    return response.json({"code": 200, "msg": "更新成功"})

@admin_article_bp.delete("/<post_id>")
@openapi.summary("删除文章")
async def delete_content(request, post_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除文章失败:admin_id无效,post_id={post_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"删除文章失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    logger.info(f"管理员{admin_id}删除文章:post_id={post_id},title={post.title}")
    db.query(PostTag).filter(PostTag.post_id == post_id).delete()
    db.query(Comment).filter(Comment.post_id == post_id).delete()
    db.query(Favorite).filter(Favorite.post_id == post_id).delete()
    db.query(Like).filter(Like.target_id == post_id, Like.target_type == "post").delete()
    db.delete(post)
    db.commit()
    logger.info(f"管理员{admin_id}删除文章成功:post_id={post_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_article_bp.post("/batch-action")
@openapi.summary("批量操作文章")
async def batch_action_content(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量操作文章失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量操作文章失败:未选择文章")
        return response.json({"code": 400, "msg": "请选择要操作的文章"})
    logger.info(f"管理员{admin_id}批量操作文章:ids={ids},action={action}")
    posts = db.query(Post).filter(Post.id.in_(ids)).all()
    if action == "publish":
        for p in posts:
            p.status = "published"
        logger.debug(f"批量操作:发布{len(posts)}篇文章")
    elif action == "unpublish":
        for p in posts:
            p.status = "draft"
        logger.debug(f"批量操作:取消发布{len(posts)}篇文章")
    elif action == "delete":
        for p in posts:
            db.query(PostTag).filter(PostTag.post_id == p.id).delete()
            db.query(Comment).filter(Comment.post_id == p.id).delete()
            db.query(Favorite).filter(Favorite.post_id == p.id).delete()
            db.query(Like).filter(Like.target_id == p.id, Like.target_type == "post").delete()
            db.delete(p)
        logger.debug(f"批量操作:删除{len(posts)}篇文章")
    elif action == "top":
        for p in posts:
            p.is_top = 1
        logger.debug(f"批量操作:置顶{len(posts)}篇文章")
    elif action == "untop":
        for p in posts:
            p.is_top = 0
        logger.debug(f"批量操作:取消置顶{len(posts)}篇文章")
    else:
        logger.warning(f"批量操作文章失败:无效操作,{action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}批量操作文章成功:共{len(posts)}条,操作:{action}")
    return response.json({"code": 200, "msg": "批量操作成功"})

@admin_article_bp.post("/top")
@openapi.summary("设置置顶/取消置顶")
async def toggle_content_top(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("设置置顶失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post_id = data.get("post_id")
    is_top = data.get("is_top")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"设置置顶失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    logger.info(f"管理员{admin_id}设置文章置顶:post_id={post_id},is_top={is_top}")
    post.is_top = 1 if is_top else 0
    db.commit()
    logger.info(f"管理员{admin_id}设置文章置顶成功:post_id={post_id}")
    return response.json({"code": 200, "msg": "操作成功"})

@admin_article_bp.post("/toggle-status")
@openapi.summary("切换文章显示/隐藏状态")
async def toggle_content_status(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("切换文章状态失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post_id = data.get("post_id")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"切换文章状态失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    logger.info(f"管理员{admin_id}切换文章状态:post_id={post_id},current_status={post.status}")
    post.status = "published" if post.status == "hidden" else "hidden"
    db.commit()
    logger.info(f"管理员{admin_id}切换文章状态成功:post_id={post_id},new_status={post.status}")
    return response.json({"code": 200, "msg": "操作成功"})

@admin_article_bp.get("/stats/overview")
@openapi.summary("获取文章统计概览")
async def get_content_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取文章统计失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "month")
    logger.info(f"管理员{admin_id}查询文章统计:period={period}")
    total_articles = db.query(Post).filter(Post.type == "article").count()
    total_questions = db.query(Post).filter(Post.type == "question").count()
    published_today = db.query(Post).filter(func.date(Post.created_at) == datetime.now().date()).count()
    published_week = db.query(Post).filter(Post.created_at >= datetime.now() - timedelta(days=7)).count()
    draft_count = db.query(Post).filter(Post.status == "draft").count()
    hidden_count = db.query(Post).filter(Post.status == "hidden").count()
    total_views = db.query(Post).with_entities(func.sum(Post.view_count)).scalar() or 0
    total_likes = db.query(Post).with_entities(func.sum(Post.like_count)).scalar() or 0
    total_comments = db.query(Comment).count()
    logger.info(f"管理员{admin_id}查询文章统计成功:articles={total_articles},views={total_views}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_articles": total_articles, "total_questions": total_questions, "published_today": published_today, "published_week": published_week, "draft_count": draft_count, "hidden_count": hidden_count, "total_views": total_views, "total_likes": total_likes, "total_comments": total_comments, "avg_views_per_article": round(total_views / total_articles) if total_articles > 0 else 0, "top_categories": [], "trend_data": []}})

@admin_article_bp.post("/export")
@openapi.summary("导出文章数据")
async def export_contents(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("导出文章失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}导出文章数据")
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "posts.xlsx", "file_url": "/static/exports/posts.xlsx"}})
