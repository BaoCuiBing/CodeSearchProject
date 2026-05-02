from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Report, Post, Comment
from models.db_init import get_db_session

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
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    target_type = request.args.get("target_type")
    status = request.args.get("status")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    query = db.query(Report)
    if target_type:
        query = query.filter(Report.target_type == target_type)
    if status:
        query = query.filter(Report.status == status)
    order_func = Report.created_at.desc() if order == "desc" else Report.created_at.asc()
    total = query.count()
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
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": report_list, "total": total, "page": page, "page_size": page_size}})

@admin_report_bp.get("/<report_id>")
@openapi.summary("获取举报详情")
async def get_report_detail(request, report_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
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
    return response.json({"code": 200, "msg": "获取成功", "data": {"report_id": report.id, "reporter": {"user_id": reporter.id, "username": reporter.username} if reporter else None, "target_id": report.target_id, "target_type": report.target_type, "target_title": target_title, "target_content": target_content, "reason": report.reason, "status": report.status, "handler": {"user_id": handler.id, "username": handler.username} if handler else None, "handle_note": report.handle_note, "created_at": str(report.created_at)}})

@admin_report_bp.post("/handle")
@openapi.summary("处理举报")
async def handle_report(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return response.json({"code": 404, "msg": "举报不存在"})
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    if action == "approve":
        report.status = "handled"
        if data.get("delete_target"):
            if report.target_type == "post":
                post = db.query(Post).filter(Post.id == report.target_id).first()
                if post:
                    db.delete(post)
            elif report.target_type == "comment":
                comment = db.query(Comment).filter(Comment.id == report.target_id).first()
                if comment:
                    db.delete(comment)
    elif action == "reject":
        report.status = "rejected"
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "处理成功", "data": {"report_id": report.id, "action": action, "status": report.status, "handled_at": str(datetime.now())}})

@admin_report_bp.post("/batch-handle")
@openapi.summary("批量处理举报")
async def batch_handle_reports(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择要处理的举报"})
    reports = db.query(Report).filter(Report.id.in_(ids)).all()
    for r in reports:
        r.handler_id = admin_id
        r.handle_note = data.get("handle_note")
        r.status = "handled" if action == "approve" else "rejected"
    db.commit()
    return response.json({"code": 200, "msg": "批量处理成功", "data": {"processed_count": len(ids), "action": action}})

@admin_report_bp.post("/article/handle")
@openapi.summary("处理举报文章")
async def handle_reported_article(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return response.json({"code": 404, "msg": "举报不存在"})
    post = db.query(Post).filter(Post.id == report.target_id).first()
    if not post:
        return response.json({"code": 404, "msg": "文章不存在"})
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    deleted = False
    if action == "delete":
        db.delete(post)
        deleted = True
        report.status = "handled"
    elif action == "ignore":
        report.status = "rejected"
    elif action == "warn":
        report.status = "handled"
    elif action == "ban_author":
        author = db.query(User).filter(User.id == post.user_id).first()
        if author:
            author.status = "banned"
        report.status = "handled"
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "处理成功", "data": {"post_id": post.id, "action": action, "deleted": deleted}})

@admin_report_bp.post("/comment/handle")
@openapi.summary("处理举报评论")
async def handle_reported_comment(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    report_id = data.get("report_id")
    action = data.get("action")
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        return response.json({"code": 404, "msg": "举报不存在"})
    comment = db.query(Comment).filter(Comment.id == report.target_id).first()
    if not comment:
        return response.json({"code": 404, "msg": "评论不存在"})
    report.handler_id = admin_id
    report.handle_note = data.get("handle_note")
    deleted = False
    if action == "delete":
        db.delete(comment)
        deleted = True
        report.status = "handled"
    elif action == "ignore":
        report.status = "rejected"
    elif action == "warn":
        report.status = "handled"
    elif action == "ban_author":
        author = db.query(User).filter(User.id == comment.user_id).first()
        if author:
            author.status = "banned"
        report.status = "handled"
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    if data.get("report_ids"):
        db.query(Report).filter(Report.id.in_(data["report_ids"])).update({"status": "handled", "handler_id": admin_id, "handle_note": data.get("handle_note")})
    db.commit()
    return response.json({"code": 200, "msg": "处理成功", "data": {"comment_id": comment.id, "action": action, "deleted": deleted}})
