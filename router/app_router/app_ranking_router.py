import logging
from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Post, Follow, Comment
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

ranking_bp = Blueprint("ranking", url_prefix="/api/ranking")

@ranking_bp.get("/list")
@openapi.summary("获取各类排行榜数据")
async def get_ranking_list(request):
    db = request.ctx.db
    rank_type = request.args.get("type")
    period = request.args.get("period", "week")
    limit = int(request.args.get("limit", 50))
    user_id = request.args.get("user_id")
    if rank_type not in ["user_active", "user_fans", "article_hot", "question_hot", "contributor", "tag_hot"]:
        logger.warning(f"获取排行榜失败:类型不支持,type={rank_type}")
        return response.json({"code": 400, "msg": "排行榜类型不支持"})
    logger.info(f"查询排行榜:type={rank_type},period={period}")
    now = datetime.now()
    if period == "day":
        start_time = now - timedelta(days=1)
    elif period == "week":
        start_time = now - timedelta(days=7)
    elif period == "month":
        start_time = now - timedelta(days=30)
    else:
        start_time = None
    rank_list = []
    total = 0
    my_rank = None
    if rank_type == "user_active":
        query = db.query(User).filter(User.status == "active")
        total = query.count()
        users = query.all()
        user_scores = []
        for u in users:
            articles = db.query(Post).filter(Post.user_id == u.id, Post.type == "article")
            if start_time:
                articles = articles.filter(Post.created_at >= start_time)
            article_count = articles.count()
            comments = db.query(Comment).filter(Comment.user_id == u.id)
            if start_time:
                comments = comments.filter(Comment.created_at >= start_time)
            comment_count = comments.count()
            likes = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.like_count)).scalar() or 0
            score = article_count * 10 + comment_count * 5 + likes * 2
            user_scores.append({"user_id": u.id, "username": u.username, "avatar": u.avatar, "score": score, "article_count": article_count, "comment_count": comment_count, "like_count": likes})
        user_scores.sort(key=lambda x: x["score"], reverse=True)
        rank_list = [{"rank": i+1, **u} for i, u in enumerate(user_scores[:limit])]
        if user_id:
            for i, u in enumerate(user_scores):
                if str(u["user_id"]) == str(user_id):
                    my_rank = i + 1
                    break
    elif rank_type == "user_fans":
        query = db.query(User).filter(User.status == "active")
        total = query.count()
        users = query.all()
        user_fans = []
        for u in users:
            fans_count = db.query(Follow).filter(Follow.following_id == u.id).count()
            user_fans.append({"user_id": u.id, "username": u.username, "avatar": u.avatar, "fans_count": fans_count})
        user_fans.sort(key=lambda x: x["fans_count"], reverse=True)
        rank_list = [{"rank": i+1, **u} for i, u in enumerate(user_fans[:limit])]
        if user_id:
            for i, u in enumerate(user_fans):
                if str(u["user_id"]) == str(user_id):
                    my_rank = i + 1
                    break
    elif rank_type in ["article_hot", "question_hot"]:
        post_type = "article" if rank_type == "article_hot" else "question"
        query = db.query(Post).filter(Post.type == post_type, Post.status == "published")
        if start_time:
            query = query.filter(Post.created_at >= start_time)
        total = query.count()
        posts = query.order_by(Post.like_count.desc(), Post.view_count.desc()).limit(limit).all()
        for i, p in enumerate(posts):
            author = db.query(User).filter(User.id == p.user_id).first()
            hot_score = (p.view_count or 0) + (p.like_count or 0) * 5 + (p.comment_count or 0) * 3
            rank_list.append({"rank": i+1, "post_id": p.id, "title": p.title, "type": p.type, "author": {"user_id": author.id, "username": author.username} if author else None, "view_count": p.view_count, "like_count": p.like_count, "comment_count": p.comment_count, "hot_score": hot_score})
    elif rank_type == "contributor":
        query = db.query(User).filter(User.status == "active")
        total = query.count()
        users = query.all()
        user_contrib = []
        for u in users:
            posts = db.query(Post).filter(Post.user_id == u.id, Post.status == "published")
            if start_time:
                posts = posts.filter(Post.created_at >= start_time)
            post_count = posts.count()
            comments = db.query(Comment).filter(Comment.user_id == u.id)
            if start_time:
                comments = comments.filter(Comment.created_at >= start_time)
            comment_count = comments.count()
            contribution_score = post_count * 20 + comment_count * 5
            user_contrib.append({"user_id": u.id, "username": u.username, "avatar": u.avatar, "contribution_score": contribution_score, "post_count": post_count, "comment_count": comment_count})
        user_contrib.sort(key=lambda x: x["contribution_score"], reverse=True)
        rank_list = [{"rank": i+1, **u} for i, u in enumerate(user_contrib[:limit])]
        if user_id:
            for i, u in enumerate(user_contrib):
                if str(u["user_id"]) == str(user_id):
                    my_rank = i + 1
                    break
    elif rank_type == "tag_hot":
        from models.model import Tag
        query = db.query(Tag).filter(Tag.status == "active")
        total = query.count()
        tags = query.order_by(Tag.post_count.desc()).limit(limit).all()
        rank_list = [{"rank": i+1, "tag_id": t.id, "name": t.name, "post_count": t.post_count or 0} for i, t in enumerate(tags)]
    logger.info(f"获取排行榜成功:type={rank_type},count={len(rank_list)}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"type": rank_type, "period": period, "list": rank_list, "total": total, "my_rank": my_rank}})

@ranking_bp.get("/my-rank")
@openapi.summary("获取当前用户在各榜单的排名")
async def get_my_ranking(request):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取我的排名失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    rank_type = request.args.get("type")
    period = request.args.get("period", "week")
    logger.info(f"查询我的排名:user_id={user_id}")
    result = {}
    types = [rank_type] if rank_type else ["user_active", "user_fans", "contributor"]
    for rt in types:
        if rt == "user_active":
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                article_count = db.query(Post).filter(Post.user_id == user_id, Post.type == "article").count()
                comment_count = db.query(Comment).filter(Comment.user_id == user_id).count()
                like_count = db.query(Post).filter(Post.user_id == user_id).with_entities(func.sum(Post.like_count)).scalar() or 0
                score = article_count * 10 + comment_count * 5 + like_count * 2
                users = db.query(User).filter(User.status == "active").all()
                rank = 1
                for u in users:
                    u_articles = db.query(Post).filter(Post.user_id == u.id, Post.type == "article").count()
                    u_comments = db.query(Comment).filter(Comment.user_id == u.id).count()
                    u_likes = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.like_count)).scalar() or 0
                    u_score = u_articles * 10 + u_comments * 5 + u_likes * 2
                    if u_score > score:
                        rank += 1
                result["user_active"] = {"rank": rank, "score": score}
        elif rt == "user_fans":
            fans_count = db.query(Follow).filter(Follow.following_id == user_id).count()
            users = db.query(User).filter(User.status == "active").all()
            rank = 1
            for u in users:
                u_fans = db.query(Follow).filter(Follow.following_id == u.id).count()
                if u_fans > fans_count:
                    rank += 1
            result["user_fans"] = {"rank": rank, "fans_count": fans_count}
        elif rt == "contributor":
            post_count = db.query(Post).filter(Post.user_id == user_id, Post.status == "published").count()
            comment_count = db.query(Comment).filter(Comment.user_id == user_id).count()
            contribution_score = post_count * 20 + comment_count * 5
            users = db.query(User).filter(User.status == "active").all()
            rank = 1
            for u in users:
                u_posts = db.query(Post).filter(Post.user_id == u.id, Post.status == "published").count()
                u_comments = db.query(Comment).filter(Comment.user_id == u.id).count()
                u_score = u_posts * 20 + u_comments * 5
                if u_score > contribution_score:
                    rank += 1
            result["contributor"] = {"rank": rank, "contribution_score": contribution_score}
    return response.json({"code": 200, "msg": "获取成功", "data": result})