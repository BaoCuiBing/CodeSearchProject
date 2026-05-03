import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import Post, Comment, User, Like
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

comment_bp = Blueprint("comment", url_prefix="/api/comment")

@comment_bp.get("/list/<post_id>")
@openapi.summary("获取文章评论列表")
async def get_comment_list(request, post_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    sort = request.args.get("sort", "time")
    logger.info(f"查询评论列表:post_id={post_id}")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"获取评论列表失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    query = db.query(Comment).filter(Comment.post_id == post_id, Comment.status == "normal", Comment.parent_id == None)
    if sort == "hot":
        query = query.order_by(Comment.like_count.desc(), Comment.created_at.asc())
    else:
        query = query.order_by(Comment.created_at.asc())
    total = query.count()
    comments = query.offset((page - 1) * page_size).limit(page_size).all()
    comment_list = []
    for c in comments:
        user = db.query(User).filter(User.id == c.user_id).first()
        is_liked = False
        if user_id:
            is_liked = db.query(Like).filter(Like.user_id == user_id, Like.target_id == c.id, Like.target_type == "comment").first() is not None
        replies = db.query(Comment).filter(Comment.parent_id == c.id).all()
        reply_list = []
        for r in replies:
            reply_user = db.query(User).filter(User.id == r.user_id).first()
            parent_comment = db.query(Comment).filter(Comment.id == r.parent_id).first()
            reply_to_user = db.query(User).filter(User.id == parent_comment.user_id).first() if parent_comment else None
            reply_list.append({"comment_id": r.id, "user": {"user_id": reply_user.id, "username": reply_user.username, "avatar": reply_user.avatar} if reply_user else None, "content": r.content, "reply_to": {"user_id": reply_to_user.id, "username": reply_to_user.username} if reply_to_user else None, "like_count": r.like_count, "is_liked": False, "created_at": str(r.created_at)})
        comment_list.append({"comment_id": c.id, "user": {"user_id": user.id, "username": user.username, "avatar": user.avatar} if user else None, "content": c.content, "parent_id": c.parent_id, "reply_to": None, "like_count": c.like_count, "is_liked": is_liked, "created_at": str(c.created_at), "replies": reply_list})
    logger.info(f"获取评论列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": comment_list, "total": total, "page": page, "page_size": page_size}})

@comment_bp.post("/")
@openapi.summary("发布评论或回复")
async def create_comment(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    content = data.get("content")
    parent_id = data.get("parent_id")
    if not user_id or not post_id:
        logger.warning("发布评论失败:参数为空")
        return response.json({"code": 400, "msg": "参数错误"})
    if not content:
        logger.warning("发布评论失败:内容为空")
        return response.json({"code": 400, "msg": "评论内容不能为空"})
    if len(content) > 1000:
        logger.warning("发布评论失败:内容超出限制")
        return response.json({"code": 400, "msg": "评论内容最多1000字"})
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"发布评论失败:文章不存在,post_id={post_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    if parent_id:
        parent = db.query(Comment).filter(Comment.id == parent_id).first()
        if not parent:
            logger.warning(f"发布评论失败:父评论不存在,parent_id={parent_id}")
            return response.json({"code": 404, "msg": "父评论不存在"})
    logger.info(f"发布评论:user_id={user_id},post_id={post_id}")
    new_comment = Comment(user_id=user_id, post_id=post_id, content=content, parent_id=parent_id)
    db.add(new_comment)
    post.comment_count = (post.comment_count or 0) + 1
    db.commit()
    logger.info(f"发布评论成功:comment_id={new_comment.id}")
    return response.json({"code": 200, "msg": "评论成功", "data": {"comment_id": new_comment.id}})

@comment_bp.delete("/<comment_id>")
@openapi.summary("删除评论")
async def delete_comment(request, comment_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("删除评论失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    user_id = int(user_id)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"删除评论失败:评论不存在,comment_id={comment_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    if comment.user_id != user_id:
        logger.warning(f"删除评论失败:无权操作,user_id={user_id}")
        return response.json({"code": 403, "msg": "无权删除此评论"})
    logger.info(f"删除评论:comment_id={comment_id}")
    db.query(Comment).filter(Comment.parent_id == comment_id).delete()
    db.query(Like).filter(Like.target_id == comment_id, Like.target_type == "comment").delete()
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if post:
        post.comment_count = max(0, (post.comment_count or 0) - 1)
    db.delete(comment)
    db.commit()
    logger.info(f"删除评论成功:comment_id={comment_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@comment_bp.post("/like")
@openapi.summary("点赞或取消点赞评论")
async def toggle_comment_like(request):
    db = request.ctx.db
    data = request.json
    user_id = data.get("user_id")
    comment_id = data.get("comment_id")
    if not user_id or not comment_id:
        logger.warning("点赞评论失败:参数为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"点赞评论失败:评论不存在,comment_id={comment_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    like = db.query(Like).filter(Like.user_id == user_id, Like.target_id == comment_id, Like.target_type == "comment").first()
    if like:
        db.delete(like)
        comment.like_count = max(0, (comment.like_count or 0) - 1)
        is_liked = False
    else:
        db.add(Like(user_id=user_id, target_id=comment_id, target_type="comment"))
        comment.like_count = (comment.like_count or 0) + 1
        is_liked = True
    db.commit()
    return response.json({"code": 200, "msg": "操作成功", "data": {"is_liked": is_liked, "like_count": comment.like_count}})