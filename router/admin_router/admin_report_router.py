from datetime import datetime, timedelta
import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Report, Post, Comment, PostTag, Favorite, Like
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
admin_report_bp = Blueprint("admin_report", url_prefix="/api/admin/report")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_report_bp.get("/list")
@openapi.summary("获取举报列表")
async def get_report_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取举报列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    target_type = request.args.get("target_type")
    status = request.args.get("status")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    logger.info(f"管理员{admin_id}查询举报列表:page={page},page_size={page_size},target_type={target_type},status={status}")
    query = db.query(Report)
    if target_type:
        query = query.filter(Report.target_type == target_type)
        logger.debug(f"查询条件:target_type过滤={target_type}")
    if status:
        query = query.filter(Report.status == status)
        logger.debug(f"查询条件:status过滤={status}")
    order_func = Report.created_at.desc() if order == "desc" else Report.created_at.asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    reports = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    report_list = []
    for r in reports:
        reporter = db.query(User).filter(User.id == r.reporter_id).first()
        handler = db.query(User).filter(User.id == r.handler_id).first() if r.handler_id else None
        target_title = None
        target_content = None
        if r.target_type == "post":
            post = db.query(Post).filter(Post.id == r.target_id).first()
            if post:
                target_title = post.title
                target_content = post.summary
        elif r.target_type == "comment":
            comment = db.query(Comment).filter(Comment.id == r.target_id).first()
            if comment:
                target_content = comment.content[:100]
        report_list.append({"report_id": r.id, "reporter": {"user_id": reporter.id, "username": reporter.username} if reporter else None, "target_id": r.target_id, "target_type": r.target_type, "target_title": target_title, "target_content": target_content, "reason": r.reason, "status": r.status, "handler": {"user_id": handler.id, "username": handler.username} if handler else None, "handle_note": r.handle_note, "created_at": str(r.created_at)})
    logger.info(f"管理员{admin_id}查询举报列表成功:共{total}条,返回{len(report_list)}条")
    logger.debug(f"数据处理完成:构建{len(report_list)}条举报记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": report_list, "total": total, "page": page, "page_size": page_size}})

@admin_report_bp.get("/<report_id>")
@openapi.summary("获取举报详情")
async def get_report_detail(request, report_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"获取举报详情失败:admin_id无效,report_id={report_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}查询举报详情:report_id={report_id}")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        logger.warning(f"获取举报详情失败:举报不存在,report_id={report_id}")
        return response.json({"code": 404, "msg": "举报不存在"})
    reporter = db.query(User).filter(User.id == report.reporter_id).first()
    handler = db.query(User).filter(User.id == report.handler_id).first() if report.handler_id else None
    target_title = None
    target_content = None
    if report.target_type == "post":
        post = db.query(Post).filter(Post.id == report.target_id).first()
        if post:
            target_title = post.title
            target_content = post.content[:200]
    elif report.target_type == "comment":
        comment = db.query(Comment).filter(Comment.id == report.target_id).first()
        if comment:
            target_content = comment.content[:200]
    logger.info(f"管理员{admin_id}查询举报详情成功:report_id={report_id},target_type={report.target_type}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"report_id": report.id, "reporter": {"user_id": reporter.id, "username": reporter.username} if reporter else None, "target_id": report.target_id, "target_type": report.target_type, "target_title": target_title, "target_content": target_content, "reason": report.reason, "status": report.status, "handler": {"user_id": handler.id, "username": handler.username} if handler else None, "handle_note": report.handle_note, "created_at": str(report.created_at)}})

@admin_report_bp.post("/handle")
@openapi.summary("处理举报")
async def handle_report(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("处理举报失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        logger.warning(f"处理举报失败:举报不存在,report_id={report_id}")
        return response.json({"code": 404, "msg": "举报不存在"})
    logger.info(f"管理员{admin_id}处理举报:report_id={report_id},action={action}")
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    if action == "approve":
        report.status = "handled"
        logger.debug(f"处理操作:通过举报")
        if data.get("delete_target"):
            if report.target_type == "post":
                post = db.query(Post).filter(Post.id == report.target_id).first()
                if post:
                    db.query(PostTag).filter(PostTag.post_id == report.target_id).delete()
                    db.query(Comment).filter(Comment.post_id == report.target_id).delete()
                    db.query(Favorite).filter(Favorite.post_id == report.target_id).delete()
                    db.query(Like).filter(Like.target_id == report.target_id, Like.target_type == "post").delete()
                    db.delete(post)
                    logger.debug(f"删除目标文章:post_id={report.target_id}")
            elif report.target_type == "comment":
                comment = db.query(Comment).filter(Comment.id == report.target_id).first()
                if comment:
                    db.query(Like).filter(Like.target_id == report.target_id, Like.target_type == "comment").delete()
                    db.delete(comment)
                    logger.debug(f"删除目标评论:comment_id={report.target_id}")
    elif action == "reject":
        report.status = "rejected"
        logger.debug(f"处理操作:拒绝举报")
    else:
        logger.warning(f"处理举报失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}处理举报成功:report_id={report_id},action={action}")
    return response.json({"code": 200, "msg": "处理成功", "data": {"report_id": report.id, "action": action, "status": report.status, "handled_at": str(datetime.now())}})

@admin_report_bp.post("/batch-handle")
@openapi.summary("批量处理举报")
async def batch_handle_reports(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量处理举报失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量处理举报失败:未选择举报")
        return response.json({"code": 400, "msg": "请选择要处理的举报"})
    logger.info(f"管理员{admin_id}批量处理举报:ids={ids},action={action}")
    reports = db.query(Report).filter(Report.id.in_(ids)).all()
    for r in reports:
        r.handler_id = admin_id
        r.handle_note = data.get("handle_note")
        r.status = "handled" if action == "approve" else "rejected"
    logger.debug(f"批量处理:{len(reports)}条举报,操作:{action}")
    db.commit()
    logger.info(f"管理员{admin_id}批量处理举报成功:共{len(reports)}条")
    return response.json({"code": 200, "msg": "批量处理成功", "data": {"processed_count": len(ids), "action": action}})

@admin_report_bp.post("/article/handle")
@openapi.summary("处理举报文章")
async def handle_reported_article(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("处理举报文章失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        logger.warning(f"处理举报文章失败:举报不存在,report_id={report_id}")
        return response.json({"code": 404, "msg": "举报不存在"})
    post = db.query(Post).filter(Post.id == report.target_id).first()
    if not post:
        logger.warning(f"处理举报文章失败:文章不存在,target_id={report.target_id}")
        return response.json({"code": 404, "msg": "文章不存在"})
    logger.info(f"管理员{admin_id}处理举报文章:report_id={report_id},post_id={post.id},action={action}")
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    deleted = False
    if action == "delete":
        db.delete(post)
        deleted = True
        report.status = "handled"
        logger.debug(f"处理操作:删除文章")
    elif action == "ignore":
        report.status = "rejected"
        logger.debug(f"处理操作:忽略举报")
    elif action == "warn":
        report.status = "handled"
        logger.debug(f"处理操作:警告作者")
    elif action == "ban_author":
        author = db.query(User).filter(User.id == post.user_id).first()
        if author:
            author.status = "banned"
            logger.debug(f"处理操作:封禁作者,user_id={post.user_id}")
        report.status = "handled"
    else:
        logger.warning(f"处理举报文章失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}处理举报文章成功:post_id={post.id},action={action}")
    return response.json({"code": 200, "msg": "处理成功", "data": {"post_id": post.id, "action": action, "deleted": deleted}})

@admin_report_bp.post("/comment/handle")
@openapi.summary("处理举报评论")
async def handle_reported_comment(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("处理举报评论失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        logger.warning(f"处理举报评论失败:举报不存在,report_id={report_id}")
        return response.json({"code": 404, "msg": "举报不存在"})
    comment = db.query(Comment).filter(Comment.id == report.target_id).first()
    if not comment:
        logger.warning(f"处理举报评论失败:评论不存在,target_id={report.target_id}")
        return response.json({"code": 404, "msg": "评论不存在"})
    logger.info(f"管理员{admin_id}处理举报评论:report_id={report_id},comment_id={comment.id},action={action}")
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    deleted = False
    if action == "delete":
        db.delete(comment)
        deleted = True
        report.status = "handled"
        logger.debug(f"处理操作:删除评论")
    elif action == "ignore":
        report.status = "rejected"
        logger.debug(f"处理操作:忽略举报")
    elif action == "warn":
        report.status = "handled"
        logger.debug(f"处理操作:警告作者")
    elif action == "ban_author":
        author = db.query(User).filter(User.id == comment.user_id).first()
        if author:
            author.status = "banned"
            logger.debug(f"处理操作:封禁作者,user_id={comment.user_id}")
        report.status = "handled"
    else:
        logger.warning(f"处理举报评论失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    if data.get("report_ids"):
        db.query(Report).filter(Report.id.in_(data["report_ids"])).update({"status": "handled", "handler_id": admin_id, "handle_note": data.get("handle_note")})
        logger.debug(f"批量更新关联举报:report_ids={data['report_ids']}")
    db.commit()
    logger.info(f"管理员{admin_id}处理举报评论成功:comment_id={comment.id},action={action}")
    return response.json({"code": 200, "msg": "处理成功", "data": {"comment_id": comment.id, "action": action, "deleted": deleted}})
