from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Tag, Post, PostTag
from models.db_init import get_db_session

admin_tag_bp = Blueprint("admin_tag", url_prefix="/api/admin/tag")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_tag_bp.get("/list")
@openapi.summary("获取标签列表")
async def get_tag_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    query = db.query(Tag)
    if keyword:
        query = query.filter(Tag.name.contains(keyword))
    sort_map = {"name": Tag.name, "post_count": Tag.post_count}
    order_func = sort_map.get(sort, Tag.name).desc() if order == "desc" else sort_map.get(sort, Tag.name).asc()
    total = query.count()
    tags = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    tag_list = []
    for t in tags:
        tag_list.append({"tag_id": t.id, "name": t.name, "post_count": t.post_count, "created_at": str(t.created_at), "updated_at": str(t.updated_at)})
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": tag_list, "total": total, "page": page, "page_size": page_size}})

@admin_tag_bp.post("/")
@openapi.summary("创建标签")
async def create_tag(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    name = data.get("name")
    if not name:
        return response.json({"code": 400, "msg": "标签名称不能为空"})
    exist = db.query(Tag).filter(Tag.name == name).first()
    if exist:
        return response.json({"code": 400, "msg": "标签名称已存在"})
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    return response.json({"code": 200, "msg": "创建成功", "data": {"tag_id": tag.id, "name": tag.name, "post_count": tag.post_count, "created_at": str(tag.created_at)}})

@admin_tag_bp.put("/")
@openapi.summary("编辑标签")
async def edit_tag(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    tag_id = data.get("tag_id")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return response.json({"code": 404, "msg": "标签不存在"})
    if "name" in data:
        tag.name = data["name"]
    db.commit()
    return response.json({"code": 200, "msg": "更新成功", "data": {"tag_id": tag.id, "name": tag.name, "post_count": tag.post_count, "updated_at": str(tag.updated_at)}})

@admin_tag_bp.delete("/<tag_id>")
@openapi.summary("删除标签")
async def delete_tag(request, tag_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return response.json({"code": 404, "msg": "标签不存在"})
    db.query(PostTag).filter(PostTag.tag_id == tag_id).delete()
    db.delete(tag)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功"})

@admin_tag_bp.post("/batch-action")
@openapi.summary("批量操作标签")
async def batch_action_tags(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择要操作的标签"})
    if action == "delete":
        for tid in ids:
            tag = db.query(Tag).filter(Tag.id == tid).first()
            if tag:
                db.query(PostTag).filter(PostTag.tag_id == tid).delete()
                db.delete(tag)
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "批量操作成功", "data": {"processed_count": len(ids)}})

@admin_tag_bp.get("/stats/overview")
@openapi.summary("获取标签统计概览")
async def get_tag_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    total_tags = db.query(Tag).count()
    new_tags_week = db.query(Tag).filter(Tag.created_at >= datetime.now() - timedelta(days=7)).count()
    new_tags_month = db.query(Tag).filter(Tag.created_at >= datetime.now() - timedelta(days=30)).count()
    top_tags = db.query(Tag).order_by(Tag.post_count.desc()).limit(10).all()
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_tags": total_tags, "new_tags_week": new_tags_week, "new_tags_month": new_tags_month, "avg_posts_per_tag": 0, "top_tags": [{"tag_id": t.id, "name": t.name, "post_count": t.post_count} for t in top_tags], "trend_data": []}})
