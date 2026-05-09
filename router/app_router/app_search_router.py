import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import Post, User, Tag, PostTag, SearchHistory, Category

logger = logging.getLogger(__name__)
search_bp = Blueprint("search", url_prefix="/api/search")

@search_bp.get("/")
@openapi.summary("搜索文章或问题")
async def search_content(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    keyword = request.args.get("keyword")
    if not keyword:
        logger.warning("搜索失败:关键词为空")
        return response.json({"code": 400, "msg": "搜索关键词不能为空"})
    if len(keyword) < 2:
        logger.warning("搜索失败:关键词长度不足")
        return response.json({"code": 400, "msg": "关键词至少需要2个字符"})
    search_type = request.args.get("type", "all")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    sort = request.args.get("sort", "relevance")
    tag_id = request.args.get("tag_id")
    logger.info(f"搜索内容:keyword={keyword},type={search_type}")
    query = db.query(Post).filter(Post.status == "published")
    query = query.filter(Post.title.contains(keyword) | Post.content.contains(keyword))
    if search_type != "all":
        query = query.filter(Post.type == search_type)
    if tag_id:
        query = query.join(PostTag).filter(PostTag.tag_id == tag_id)
    if sort == "time":
        query = query.order_by(Post.created_at.desc())
    elif sort == "hot":
        query = query.order_by(Post.like_count.desc(), Post.view_count.desc())
    else:
        query = query.order_by(Post.like_count.desc())
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    search_history_id = None
    if user_id:
        history = SearchHistory(user_id=user_id, keyword=keyword)
        db.add(history)
        db.flush()
        search_history_id = history.id
        db.commit()
    post_list = []
    for p in posts:
        author = db.query(User).filter(User.id == p.user_id).first()
        tags = db.query(Tag).join(PostTag).filter(PostTag.post_id == p.id).all()
        post_list.append({"post_id": p.id, "title": p.title, "type": p.type, "summary": p.summary, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "tags": [{"tag_id": t.id, "name": t.name} for t in tags], "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "created_at": str(p.created_at)})
    logger.info(f"搜索成功:total={total}")
    return response.json({"code": 200, "msg": "搜索成功", "data": {"list": post_list, "total": total, "page": page, "page_size": page_size, "search_history_id": search_history_id}})

@search_bp.get("/suggest")
@openapi.summary("搜索关键词联想")
async def search_suggest(request):
    db = request.ctx.db
    keyword = request.args.get("keyword")
    if not keyword or len(keyword) < 2:
        logger.warning("搜索建议失败:关键词长度不足")
        return response.json({"code": 400, "msg": "关键词至少需要2个字符"})
    limit = int(request.args.get("limit", 10))
    logger.info(f"搜索建议:keyword={keyword}")
    suggests = db.query(SearchHistory.keyword, func.count(SearchHistory.id).label('count')).filter(SearchHistory.keyword.contains(keyword)).group_by(SearchHistory.keyword).order_by(func.count(SearchHistory.id).desc()).limit(limit).all()
    result = [{"keyword": s.keyword, "count": s.count} for s in suggests]
    return response.json({"code": 200, "msg": "获取成功", "data": result})

@search_bp.get("/hot")
@openapi.summary("获取热门搜索关键词")
async def hot_search(request):
    db = request.ctx.db
    logger.info("查询热门搜索")
    try:
        hot = db.query(SearchHistory.keyword, func.count(SearchHistory.id).label('count')).group_by(SearchHistory.keyword).order_by(func.count(SearchHistory.id).desc()).limit(10).all()
        result = [{"keyword": h.keyword, "count": h.count, "rank": i+1} for i, h in enumerate(hot)]
        return response.json({"code": 200, "msg": "获取成功", "data": result})
    except Exception as e:
        logger.error(f"获取热门搜索失败:{str(e)}")
        return response.json({"code": 500, "msg": "服务器内部错误"})

@search_bp.get("/history")
@openapi.summary("获取搜索历史记录")
async def get_search_history(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取搜索历史失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询搜索历史:user_id={user_id}")
    query = db.query(SearchHistory).filter(SearchHistory.user_id == user_id)
    total = query.count()
    histories = query.order_by(SearchHistory.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    hist_list = [{"search_history_id": h.id, "keyword": h.keyword, "created_at": str(h.created_at)} for h in histories]
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": hist_list, "total": total, "page": page, "page_size": page_size}})

@search_bp.delete("/history/clear")
@openapi.summary("清空搜索历史记录")
async def clear_search_history(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("清空搜索历史失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    db.query(SearchHistory).filter(SearchHistory.user_id == user_id).delete()
    db.commit()
    return response.json({"code": 200, "msg": "清空成功"})

@search_bp.delete("/history/<search_history_id>")
@openapi.summary("删除单条搜索历史")
async def delete_search_history_item(request, search_history_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("删除搜索历史失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    history = db.query(SearchHistory).filter(SearchHistory.id == search_history_id, SearchHistory.user_id == user_id).first()
    if not history:
        logger.warning(f"删除搜索历史失败:记录不存在,search_history_id={search_history_id}")
        return response.json({"code": 404, "msg": "历史记录不存在"})
    db.delete(history)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@search_bp.get("/filters")
@openapi.summary("获取搜索筛选选项")
async def get_search_filters(request):
    db = request.ctx.db
    search_type = request.args.get("type")
    if search_type and search_type not in ["article", "question", "all"]:
        logger.warning(f"获取筛选失败:类型无效,type={search_type}")
        return response.json({"code": 400, "msg": "文章类型参数无效"})
    tags = []
    if search_type:
        tags = db.query(Tag).filter(Tag.status == "active").order_by(Tag.post_count.desc()).limit(20).all()
    tag_list = [{"tag_id": t.id, "name": t.name} for t in tags]
    return response.json({"code": 200, "msg": "获取成功", "data": {"types": ["all", "article", "question"], "sorts": ["relevance", "time", "hot"], "tags": tag_list}})