import json
import re
import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Tag, PostTag, Comment, Like, Favorite, Category, Follow
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

article_bp = Blueprint("article", url_prefix="/api/article")

@article_bp.post("/")
@openapi.summary("发布文章或问题")
async def create_article(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    post_type = data.get("type")
    title = data.get("title")
    content = data.get("content")
    if not user_id:
        logger.warning("发布文章失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    if post_type not in ["article", "question"]:
        logger.warning(f"发布文章失败:类型无效,type={post_type}")
        return response.json({"code": 400, "msg": "文章类型无效"})
    if not title:
        logger.warning("发布文章失败:标题为空")
        return response.json({"code": 400, "msg": "标题不能为空"})
    if not content:
        logger.warning("发布文章失败:内容为空")
        return response.json({"code": 400, "msg": "内容不能为空"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"发布文章失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    summary = data.get("summary")
    if not summary:
        summary = re.sub(r'[#\*\[\]\(\)]', '', content)[:200]
    cover_image = json.dumps(data["cover_image"]) if data.get("cover_image") else None
    category_id = data.get("category_id")
    tags = data.get("tags", [])
    logger.info(f"发布文章:user_id={user_id},type={post_type},title={title}")
    new_post = Post(user_id=user_id, type=post_type, title=title, content=content, summary=summary, cover_image=cover_image, category_id=category_id)
    db.add(new_post)
    db.flush()
    for tag_id in tags:
        post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
        db.add(post_tag)
    db.commit()
    logger.info(f"发布文章成功:post_id={new_post.id}")
    return response.json({"code": 200, "msg": "发布成功", "data": {"post_id": new_post.id}})

@article_bp.get("/<post_id>")
@openapi.summary("获取文章或问题详情")
async def get_article_detail(request, post_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    logger.info(f"查询文章详情:post_id={post_id}")
    post = db.query(Post).filter(Post.id == post_id, Post.status == "published").first()
    if not post:
        logger.warning(f"获取文章详情失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    post.view_count = (post.view_count or 0) + 1
    db.commit()
    author = db.query(User).filter(User.id == post.user_id).first()
    category = db.query(Category).filter(Category.id == post.category_id).first() if post.category_id else None
    tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == post.id).all()
    favorite_count = db.query(Favorite).filter(Favorite.post_id == post.id).count()
    is_liked = False
    is_favorited = False
    is_followed = False
    if user_id:
        is_liked = db.query(Like).filter(Like.user_id == user_id, Like.target_id == post.id, Like.target_type == "post").first() is not None
        is_favorited = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.post_id == post.id).first() is not None
        is_followed = db.query(Follow).filter(Follow.follower_id == user_id, Follow.following_id == post.user_id).first() is not None
    cover_image = json.loads(post.cover_image) if post.cover_image else None
    logger.info(f"获取文章详情成功:title={post.title}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"post_id": post.id, "type": post.type, "title": post.title, "content": post.content, "summary": post.summary, "cover_image": cover_image, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "category": {"category_id": category.id, "name": category.name} if category else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "view_count": post.view_count, "like_count": post.like_count, "comment_count": post.comment_count, "favorite_count": favorite_count, "created_at": str(post.created_at), "updated_at": str(post.updated_at), "is_liked": is_liked, "is_favorited": is_favorited, "is_followed": is_followed}})

@article_bp.put("/")
@openapi.summary("编辑文章或问题")
async def update_article(request):
    db = request.ctx.db
    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")
    if not post_id or not user_id:
        logger.warning("编辑文章失败:必填字段为空")
        return response.json({"code": 400, "msg": "参数错误"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"编辑文章失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    if post.user_id != user_id:
        logger.warning(f"编辑文章失败:无权操作,user_id={user_id},post_id={post_id}")
        return response.json({"code": 403, "msg": "无权编辑此文章"})
    logger.info(f"编辑文章:post_id={post_id},user_id={user_id}")
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
            db.add(PostTag(post_id=post_id, tag_id=tag_id))
    db.commit()
    logger.info(f"编辑文章成功:post_id={post_id}")
    return response.json({"code": 200, "msg": "更新成功"})

@article_bp.delete("/<post_id>")
@openapi.summary("删除文章或问题")
async def delete_article(request, post_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("删除文章失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    user_id = int(user_id)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"删除文章失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    if post.user_id != user_id:
        logger.warning(f"删除文章失败:无权操作,user_id={user_id}")
        return response.json({"code": 403, "msg": "无权删除此文章"})
    logger.info(f"删除文章:post_id={post_id},user_id={user_id}")
    db.query(PostTag).filter(PostTag.post_id == post_id).delete()
    db.query(Comment).filter(Comment.post_id == post_id).delete()
    db.query(Like).filter(Like.target_id == post_id, Like.target_type == "post").delete()
    db.query(Favorite).filter(Favorite.post_id == post_id).delete()
    db.delete(post)
    db.commit()
    logger.info(f"删除文章成功:post_id={post_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@article_bp.get("/list")
@openapi.summary("获取文章或问题列表")
async def get_article_list(request):
    db = request.ctx.db
    post_type = request.args.get("type", "all")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    sort = request.args.get("sort", "time")
    tag_id = request.args.get("tag_id")
    category_id = request.args.get("category_id")
    user_id = request.args.get("user_id")
    logger.info(f"查询文章列表:type={post_type},page={page},sort={sort}")
    query = db.query(Post).filter(Post.status == "published")
    if post_type != "all":
        query = query.filter(Post.type == post_type)
    if tag_id:
        query = query.join(PostTag).filter(PostTag.tag_id == tag_id)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if user_id:
        query = query.filter(Post.user_id == user_id)
    if sort == "time":
        query = query.order_by(Post.created_at.desc())
    elif sort == "hot":
        query = query.order_by(Post.like_count.desc(), Post.view_count.desc())
    elif sort == "recommend":
        query = query.order_by(Post.is_top.desc(), Post.created_at.desc())
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        favorite_count = db.query(Favorite).filter(Favorite.post_id == p.id).count()
        tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == p.id).all()
        post_list.append({"post_id": p.id, "type": p.type, "title": p.title, "summary": p.summary, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "favorite_count": favorite_count, "created_at": str(p.created_at)})
    logger.info(f"获取文章列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": post_list, "total": total, "page": page, "page_size": page_size}})

@article_bp.post("/like")
@openapi.summary("点赞或取消点赞")
async def toggle_like(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    if not user_id or not post_id:
        logger.warning("点赞失败:参数为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"点赞失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    like = db.query(Like).filter(Like.user_id == user_id, Like.target_id == post_id, Like.target_type == "post").first()
    if like:
        db.delete(like)
        post.like_count = max(0, (post.like_count or 0) - 1)
        is_liked = False
        logger.info(f"取消点赞:user_id={user_id},post_id={post_id}")
    else:
        db.add(Like(user_id=user_id, target_id=post_id, target_type="post"))
        post.like_count = (post.like_count or 0) + 1
        is_liked = True
        logger.info(f"点赞:user_id={user_id},post_id={post_id}")
    db.commit()
    return response.json({"code": 200, "msg": "操作成功", "data": {"is_liked": is_liked, "like_count": post.like_count}})

@article_bp.get("/recommend")
@openapi.summary("获取首页推荐文章")
async def get_recommend_articles(request):
    db = request.ctx.db
    rec_type = request.args.get("type", "all")
    limit = int(request.args.get("limit", 10))
    random_flag = request.args.get("random", "false").lower() == "true"
    if limit > 50:
        logger.warning("获取推荐失败:数量超出限制")
        return response.json({"code": 400, "msg": "返回数量超出限制"})
    query = db.query(Post).filter(Post.status == "published")
    if rec_type == "hot_question":
        query = query.filter(Post.type == "question")
    elif rec_type == "recommend_article":
        query = query.filter(Post.type == "article")
    if random_flag:
        query = query.order_by(func.rand()).limit(limit)
    else:
        query = query.order_by(Post.like_count.desc(), Post.view_count.desc()).limit(limit)
    posts = query.all()
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == p.id).all()
        post_list.append({"post_id": p.id, "type": p.type, "title": p.title, "summary": p.summary, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "created_at": str(p.created_at)})
    logger.info(f"获取推荐文章成功:count={len(post_list)}")
    return response.json({"code": 200, "msg": "获取成功", "data": post_list})

@article_bp.get("/<post_id>/toc")
@openapi.summary("获取文章目录结构")
async def get_article_toc(request, post_id):
    db = request.ctx.db
    logger.info(f"获取文章目录:post_id={post_id}")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"获取目录失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    toc = []
    lines = post.content.split('\n')
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            anchor = re.sub(r'[^\w\u4e00-\u9fa5-]', '', text.lower()).replace(' ', '-')
            toc.append({"level": level, "text": text, "anchor": anchor})
    logger.info(f"获取文章目录成功:count={len(toc)}")
    return response.json({"code": 200, "msg": "获取成功", "data": toc})