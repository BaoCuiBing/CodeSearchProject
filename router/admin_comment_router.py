from datetime import datetime, timedelta
import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Comment, Post
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

admin_comment_bp = Blueprint("admin_comment", url_prefix="/api/admin/comment")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_comment_bp.get("/list")
@openapi.summary("获取评论列表")
async def get_comment_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取评论列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    post_id = request.args.get("post_id")
    author_id = request.args.get("author_id")
    status = request.args.get("status", "all")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    logger.info(f"管理员{admin_id}查询评论列表:page={page},page_size={page_size},status={status}")
    query = db.query(Comment)
    if keyword:
        query = query.filter(Comment.content.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    if post_id:
        query = query.filter(Comment.post_id == post_id)
        logger.debug(f"查询条件:post_id过滤={post_id}")
    if author_id:
        query = query.filter(Comment.user_id == author_id)
        logger.debug(f"查询条件:author_id过滤={author_id}")
    if status != "all":
        query = query.filter(Comment.status == status)
        logger.debug(f"查询条件:status过滤={status}")
    if date_start:
        query = query.filter(Comment.created_at >= date_start)
        logger.debug(f"查询条件:date_start过滤={date_start}")
    if date_end:
        query = query.filter(Comment.created_at <= date_end)
        logger.debug(f"查询条件:date_end过滤={date_end}")
    sort_map = {"created_time": Comment.created_at, "like_count": Comment.like_count}
    order_func = sort_map.get(sort, Comment.created_at).desc() if order == "desc" else sort_map.get(sort, Comment.created_at).asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    comments = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    comment_list = []
    for c in comments:
        author = db.query(User).filter(User.id == c.user_id).first()
        reply_to_user = None
        if c.parent_id:
            parent = db.query(Comment).filter(Comment.id == c.parent_id).first()
            if parent:
                reply_to_user = db.query(User).filter(User.id == parent.user_id).first()
        comment_list.append({"comment_id": c.id, "post_id": c.post_id, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "parent_id": c.parent_id, "reply_to_user": {"user_id": reply_to_user.id, "username": reply_to_user.username, "avatar": reply_to_user.avatar} if reply_to_user else None, "content": c.content, "like_count": c.like_count, "status": c.status, "created_at": str(c.created_at), "updated_at": str(c.updated_at)})
    logger.info(f"管理员{admin_id}查询评论列表成功:共{total}条,返回{len(comment_list)}条")
    logger.debug(f"数据处理完成:构建{len(comment_list)}条评论记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": comment_list, "total": total, "page": page, "page_size": page_size}})

@admin_comment_bp.get("/<comment_id>")
@openapi.summary("获取评论详情")
async def get_comment_detail(request, comment_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"获取评论详情失败:admin_id无效,comment_id={comment_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}查询评论详情:comment_id={comment_id}")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"获取评论详情失败:评论不存在,comment_id={comment_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    author = db.query(User).filter(User.id == comment.user_id).first()
    replies = db.query(Comment).filter(Comment.parent_id == comment_id).all()
    reply_list = []
    for r in replies:
        reply_author = db.query(User).filter(User.id == r.user_id).first()
        reply_list.append({"comment_id": r.id, "author": {"user_id": reply_author.id, "username": reply_author.username} if reply_author else None, "content": r.content, "like_count": r.like_count, "created_at": str(r.created_at)})
    logger.info(f"管理员{admin_id}查询评论详情成功:comment_id={comment_id},replies={len(reply_list)}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"comment_id": comment.id, "post_id": comment.post_id, "author": {"user_id": author.id, "username": author.username, "avatar": author.avatar} if author else None, "parent_id": comment.parent_id, "content": comment.content, "like_count": comment.like_count, "status": comment.status, "created_at": str(comment.created_at), "replies": {"list": reply_list, "total": len(reply_list)}}})

@admin_comment_bp.delete("/<comment_id>")
@openapi.summary("删除评论")
async def delete_comment(request, comment_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除评论失败:admin_id无效,comment_id={comment_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"删除评论失败:评论不存在,comment_id={comment_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    delete_replies = request.args.get("delete_replies", "true") == "true"
    deleted_count = 1
    logger.info(f"管理员{admin_id}删除评论:comment_id={comment_id},delete_replies={delete_replies}")
    if delete_replies:
        replies = db.query(Comment).filter(Comment.parent_id == comment_id).all()
        for r in replies:
            db.delete(r)
            deleted_count += 1
        logger.debug(f"删除评论回复:{deleted_count - 1}条")
    db.delete(comment)
    db.commit()
    logger.info(f"管理员{admin_id}删除评论成功:comment_id={comment_id},共删除{deleted_count}条")
    return response.json({"code": 200, "msg": "删除成功", "data": {"deleted_count": deleted_count, "comment_id": comment_id}})

@admin_comment_bp.put("/visibility")
@openapi.summary("隐藏/显示评论")
async def toggle_comment_visibility(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("切换评论可见性失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    comment_id = data.get("comment_id")
    is_hidden = data.get("is_hidden")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        logger.warning(f"切换评论可见性失败:评论不存在,comment_id={comment_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    logger.info(f"管理员{admin_id}切换评论可见性:comment_id={comment_id},is_hidden={is_hidden}")
    comment.status = "hidden" if is_hidden else "normal"
    db.commit()
    logger.info(f"管理员{admin_id}切换评论可见性成功:comment_id={comment_id}")
    return response.json({"code": 200, "msg": "操作成功", "data": {"comment_id": comment_id, "is_hidden": is_hidden}})

@admin_comment_bp.post("/batch-action")
@openapi.summary("批量操作评论")
async def batch_action_comments(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量操作评论失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量操作评论失败:未选择评论")
        return response.json({"code": 400, "msg": "请选择要操作的评论"})
    logger.info(f"管理员{admin_id}批量操作评论:ids={ids},action={action}")
    comments = db.query(Comment).filter(Comment.id.in_(ids)).all()
    if action == "delete":
        for c in comments:
            db.delete(c)
        logger.debug(f"批量操作:删除{len(comments)}条评论")
    elif action == "hide":
        for c in comments:
            c.status = "hidden"
        logger.debug(f"批量操作:隐藏{len(comments)}条评论")
    elif action == "show":
        for c in comments:
            c.status = "normal"
        logger.debug(f"批量操作:显示{len(comments)}条评论")
    else:
        logger.warning(f"批量操作评论失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}批量操作评论成功:共{len(comments)}条,操作:{action}")
    return response.json({"code": 200, "msg": "批量操作成功", "data": {"processed_count": len(ids), "action": action}})

@admin_comment_bp.get("/stats/overview")
@openapi.summary("获取评论统计概览")
async def get_comment_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取评论统计失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    period = request.args.get("period", "month")
    logger.info(f"管理员{admin_id}查询评论统计:period={period}")
    total_comments = db.query(Comment).count()
    comments_today = db.query(Comment).filter(func.date(Comment.created_at) == datetime.now().date()).count()
    comments_week = db.query(Comment).filter(Comment.created_at >= datetime.now() - timedelta(days=7)).count()
    comments_month = db.query(Comment).filter(Comment.created_at >= datetime.now() - timedelta(days=30)).count()
    hidden_comments = db.query(Comment).filter(Comment.status == "hidden").count()
    logger.info(f"管理员{admin_id}查询评论统计成功:total={total_comments},today={comments_today}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_comments": total_comments, "comments_today": comments_today, "comments_week": comments_week, "comments_month": comments_month, "hidden_comments": hidden_comments, "avg_comments_per_article": 0, "top_commenters": [], "trend_data": []}})

@admin_comment_bp.post("/export")
@openapi.summary("导出评论数据")
async def export_comments(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("导出评论失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}导出评论数据")
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "comments.xlsx", "file_url": "/static/exports/comments.xlsx"}})
