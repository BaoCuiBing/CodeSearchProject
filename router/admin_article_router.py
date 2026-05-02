import json
from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Category, Tag, PostTag, Comment
from models.db_init import get_db_session

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
    query = db.query(Post)
    if type_filter != "all":
        query = query.filter(Post.type == type_filter)
    if status != "all":
        query = query.filter(Post.status == status)
    if keyword:
        query = query.filter(Post.title.contains(keyword) | Post.content.contains(keyword))
    if author_id:
        query = query.filter(Post.user_id == author_id)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if tag_id:
        query = query.join(PostTag).filter(PostTag.tag_id == tag_id)
    if date_start:
        query = query.filter(Post.created_at >= date_start)
    if date_end:
        query = query.filter(Post.created_at <= date_end)
    if is_top != "all":
        query = query.filter(Post.is_top == (1 if is_top == "yes" else 0))
    sort_map = {"created_time": Post.created_at, "updated_time": Post.updated_at, "view_count": Post.view_count, "like_count": Post.like_count, "comment_count": Post.comment_count}
    order_func = sort_map.get(sort, Post.created_at).desc() if order == "desc" else sort_map.get(sort, Post.created_at).asc()
    total = query.count()
    posts = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        category = db.query(Category).filter(Category.id == p.category_id).first() if p.category_id else None
        tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == p.id).all()
        cover_image = json.loads(p.cover_image) if p.cover_image else None
        post_list.append({"post_id": p.id, "type": p.type, "title": p.title, "summary": p.summary, "cover_image": cover_image, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "category": {"category_id": category.id, "name": category.name} if category else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "status": p.status, "is_top": bool(p.is_top), "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "created_at": str(p.created_at), "updated_at": str(p.updated_at)})
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": post_list, "total": total, "page": page, "page_size": page_size}})

@admin_article_bp.get("/<post_id>")
@openapi.summary("获取文章详情")
async def get_content_detail(request, post_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return response.json({"code": 404, "msg": "文章不存在"})
    author = db.query(User).filter(User.id == post.user_id).first()
    category = db.query(Category).filter(Category.id == post.category_id).first() if post.category_id else None
    tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == post.id).all()
    cover_image = json.loads(post.cover_image) if post.cover_image else None
    return response.json({"code": 200, "msg": "获取成功", "data": {"post_id": post.id, "type": post.type, "title": post.title, "content": post.content, "summary": post.summary, "cover_image": cover_image, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar, "email": author.email} if author else None, "category": {"category_id": category.id, "name": category.name} if category else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "status": post.status, "is_top": bool(post.is_top), "stats": {"view_count": post.view_count, "like_count": post.like_count, "comment_count": post.comment_count}, "created_at": str(post.created_at), "updated_at": str(post.updated_at)}})

@admin_article_bp.put("/")
@openapi.summary("编辑文章")
async def edit_content(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post_id = data.get("post_id")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return response.json({"code": 404, "msg": "文章不存在"})
    if "title" in data:
        post.title = data["title"]
    if "content" in data:
        post.content = data["content"]
    if "summary" in data:
        post.summary = data["summary"]
    if "cover_image" in data:
        post.cover_image = json.dumps(data["cover_image"])
    if "category_id" in data:
        post.category_id = data["category_id"]
    if "tags" in data:
        db.query(PostTag).filter(PostTag.post_id == post_id).delete()
        for tag_id in data["tags"]:
            post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.add(post_tag)
    if "status" in data:
        post.status = data["status"]
    if "is_top" in data:
        post.is_top = 1 if data["is_top"] else 0
    db.commit()
    return response.json({"code": 200, "msg": "更新成功"})

@admin_article_bp.delete("/<post_id>")
@openapi.summary("删除文章")
async def delete_content(request, post_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return response.json({"code": 404, "msg": "文章不存在"})
    db.query(PostTag).filter(PostTag.post_id == post_id).delete()
    db.query(Comment).filter(Comment.post_id == post_id).delete()
    db.delete(post)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@admin_article_bp.post("/batch-action")
@openapi.summary("批量操作文章")
async def batch_action_content(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择要操作的文章"})
    posts = db.query(Post).filter(Post.id.in_(ids)).all()
    if action == "publish":
        for p in posts:
            p.status = "published"
    elif action == "unpublish":
        for p in posts:
            p.status = "draft"
    elif action == "delete":
        for p in posts:
            db.query(PostTag).filter(PostTag.post_id == p.id).delete()
            db.delete(p)
    elif action == "top":
        for p in posts:
            p.is_top = 1
    elif action == "untop":
        for p in posts:
            p.is_top = 0
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "批量操作成功"})

@admin_article_bp.post("/top")
@openapi.summary("设置置顶/取消置顶")
async def toggle_content_top(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    post_id = data.get("post_id")
    is_top = data.get("is_top")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return response.json({"code": 404, "msg": "文章不存在"})
    post.is_top = 1 if is_top else 0
    db.commit()
    return response.json({"code": 200, "msg": "操作成功"})

@admin_article_bp.get("/stats/overview")
@openapi.summary("获取文章统计概览")
async def get_content_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "month")
    total_articles = db.query(Post).filter(Post.type == "article").count()
    total_questions = db.query(Post).filter(Post.type == "question").count()
    published_today = db.query(Post).filter(func.date(Post.created_at) == datetime.now().date()).count()
    published_week = db.query(Post).filter(Post.created_at >= datetime.now() - timedelta(days=7)).count()
    draft_count = db.query(Post).filter(Post.status == "draft").count()
    hidden_count = db.query(Post).filter(Post.status == "hidden").count()
    total_views = db.query(Post).with_entities(func.sum(Post.view_count)).scalar() or 0
    total_likes = db.query(Post).with_entities(func.sum(Post.like_count)).scalar() or 0
    total_comments = db.query(Comment).count()
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_articles": total_articles, "total_questions": total_questions, "published_today": published_today, "published_week": published_week, "draft_count": draft_count, "hidden_count": hidden_count, "total_views": total_views, "total_likes": total_likes, "total_comments": total_comments, "avg_views_per_article": round(total_views / total_articles) if total_articles > 0 else 0, "top_categories": [], "trend_data": []}})

@admin_article_bp.post("/export")
@openapi.summary("导出文章数据")
async def export_contents(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "posts.xlsx", "file_url": "/static/exports/posts.xlsx"}})
