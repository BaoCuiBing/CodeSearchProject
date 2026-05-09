import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from models.model import User, SearchHistory

logger = logging.getLogger(__name__)
admin_search_history_bp = Blueprint("admin_search_history", url_prefix="/api/admin/search-history")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_search_history_bp.get("/list")
@openapi.summary("获取搜索记录列表")
async def get_search_history_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取搜索记录列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    logger.info(f"管理员{admin_id}查询搜索记录列表:page={page},page_size={page_size}")
    query = db.query(SearchHistory)
    if keyword:
        query = query.filter(SearchHistory.keyword.like(f"%{keyword}%"))
    total = query.count()
    records = query.order_by(SearchHistory.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    record_list = []
    for r in records:
        user = db.query(User).filter(User.id == r.user_id).first()
        record_list.append({"search_id": r.id, "user": {"user_id": user.id, "username": user.username, "avatar": user.avatar} if user else None, "keyword": r.keyword, "created_at": str(r.created_at)})
    logger.info(f"管理员{admin_id}查询搜索记录列表成功:共{total}条,返回{len(record_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": record_list, "total": total, "page": page, "page_size": page_size}})

@admin_search_history_bp.delete("/<search_id>")
@openapi.summary("删除搜索记录")
async def delete_search_history(request, search_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除搜索记录失败:admin_id无效,search_id={search_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}删除搜索记录:search_id={search_id}")
    record = db.query(SearchHistory).filter(SearchHistory.id == search_id).first()
    if not record:
        logger.warning(f"删除搜索记录失败:记录不存在,search_id={search_id}")
        return response.json({"code": 404, "msg": "搜索记录不存在"})
    db.delete(record)
    db.commit()
    logger.info(f"管理员{admin_id}删除搜索记录成功:search_id={search_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_search_history_bp.post("/batch-delete")
@openapi.summary("批量删除搜索记录")
async def batch_delete_search_history(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除搜索记录失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除搜索记录失败:ids为空")
        return response.json({"code": 400, "msg": "ids不能为空"})
    logger.info(f"管理员{admin_id}批量删除搜索记录:ids={ids}")
    deleted = db.query(SearchHistory).filter(SearchHistory.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除搜索记录成功:删除{deleted}条")
    return response.json({"code": 200, "msg": f"成功删除{deleted}条记录"})
