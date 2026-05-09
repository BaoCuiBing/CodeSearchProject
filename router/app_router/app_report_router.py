import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from models.model import Report, Post, Comment, User

logger = logging.getLogger(__name__)
report_bp = Blueprint("report", url_prefix="/api/report")

@report_bp.post("/")
@openapi.summary("用户提交举报")
async def submit_report(request):
    db = request.ctx.db
    data = request.json
    reporter_id = data.get("reporter_id")
    target_id = data.get("target_id")
    target_type = data.get("target_type")
    reason = data.get("reason")
    if not reporter_id or not target_id or not target_type or not reason:
        logger.warning("提交举报失败:参数为空")
        return response.json({"code": 400, "msg": "参数错误"})
    if len(reason) > 500:
        logger.warning("提交举报失败:原因超出限制")
        return response.json({"code": 400, "msg": "举报原因最多500字"})
    if target_type not in ["post", "comment", "user"]:
        logger.warning(f"提交举报失败:类型无效,target_type={target_type}")
        return response.json({"code": 400, "msg": "目标类型无效"})
    exist = db.query(Report).filter(Report.reporter_id == reporter_id, Report.target_id == target_id).first()
    if exist:
        logger.warning(f"提交举报失败:重复举报,reporter_id={reporter_id},target_id={target_id}")
        return response.json({"code": 400, "msg": "您已举报过该内容"})
    reporter = db.query(User).filter(User.id == reporter_id).first()
    if not reporter:
        logger.warning(f"提交举报失败:用户不存在,reporter_id={reporter_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"提交举报:reporter_id={reporter_id},target_id={target_id},target_type={target_type}")
    new_report = Report(reporter_id=reporter_id, target_id=target_id, target_type=target_type, reason=reason)
    db.add(new_report)
    db.commit()
    logger.info(f"提交举报成功:report_id={new_report.id}")
    return response.json({"code": 200, "msg": "举报提交成功", "data": {"report_id": new_report.id}})

@report_bp.get("/my-reports")
@openapi.summary("获取我的举报列表")
async def get_my_reports(request):
    db = request.ctx.db
    reporter_id = request.args.get("reporter_id")
    if not reporter_id:
        logger.warning("获取举报列表失败:reporter_id为空")
        return response.json({"code": 400, "msg": "reporter_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    status = request.args.get("status", "all")
    logger.info(f"查询举报列表:reporter_id={reporter_id}")
    query = db.query(Report).filter(Report.reporter_id == reporter_id)
    if status != "all":
        query = query.filter(Report.status == status)
    total = query.count()
    reports = query.order_by(Report.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    report_list = []
    for r in reports:
        target_title = ""
        if r.target_type == "post":
            post = db.query(Post).filter(Post.id == r.target_id).first()
            target_title = post.title if post else ""
        elif r.target_type == "comment":
            comment = db.query(Comment).filter(Comment.id == r.target_id).first()
            target_title = comment.content[:50] if comment else ""
        report_list.append({"report_id": r.id, "target_id": r.target_id, "target_type": r.target_type, "target_title": target_title, "reason": r.reason, "status": r.status, "handle_note": r.handle_note, "created_at": str(r.created_at)})
    logger.info(f"获取举报列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": report_list, "total": total, "page": page, "page_size": page_size}})