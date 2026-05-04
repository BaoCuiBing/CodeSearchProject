from datetime import datetime, timedelta
import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Tag, Post, PostTag
from models.db_init import get_db_session

logger = logging.getLogger(__name__)

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
        logger.warning("获取标签列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    logger.info(f"管理员{admin_id}查询标签列表:page={page},page_size={page_size},keyword={keyword}")
    query = db.query(Tag)
    if keyword:
        query = query.filter(Tag.name.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    sort_map = {"name": Tag.name, "post_count": Tag.post_count}
    order_func = sort_map.get(sort, Tag.name).desc() if order == "desc" else sort_map.get(sort, Tag.name).asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    tags = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    tag_list = []
    for t in tags:
        tag_list.append({"tag_id": t.id, "name": t.name, "slug": t.slug, "description": t.description, "color": t.color, "is_hot": bool(t.is_hot), "is_recommend": bool(t.is_recommend), "category_id": t.category_id, "sort_order": t.sort_order, "status": t.status, "post_count": t.post_count, "created_at": str(t.created_at), "updated_at": str(t.updated_at)})
    logger.info(f"管理员{admin_id}查询标签列表成功:共{total}条,返回{len(tag_list)}条")
    logger.debug(f"数据处理完成:构建{len(tag_list)}条标签记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": tag_list, "total": total, "page": page, "page_size": page_size}})

@admin_tag_bp.get("/<tag_id>")
@openapi.summary("获取标签详情")
async def get_tag_detail(request, tag_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取标签详情失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}查询标签详情:tag_id={tag_id}")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        logger.warning(f"获取标签详情失败:标签不存在,tag_id={tag_id}")
        return response.json({"code": 404, "msg": "标签不存在"})
    logger.info(f"管理员{admin_id}查询标签详情成功:name={tag.name}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"tag_id": tag.id, "name": tag.name, "slug": tag.slug, "description": tag.description, "color": tag.color, "is_hot": bool(tag.is_hot), "is_recommend": bool(tag.is_recommend), "category_id": tag.category_id, "sort_order": tag.sort_order, "status": tag.status, "post_count": tag.post_count, "created_at": str(tag.created_at), "updated_at": str(tag.updated_at)}})

@admin_tag_bp.post("/")
@openapi.summary("创建标签")
async def create_tag(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("创建标签失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    name = data.get("name")
    if not name:
        logger.warning("创建标签失败:标签名称为空")
        return response.json({"code": 400, "msg": "标签名称不能为空"})
    exist = db.query(Tag).filter(Tag.name == name).first()
    if exist:
        logger.warning(f"创建标签失败:标签名称已存在,name={name}")
        return response.json({"code": 400, "msg": "标签名称已存在"})
    logger.info(f"管理员{admin_id}创建标签:name={name}")
    tag = Tag(name=name, slug=data.get("slug", ""), description=data.get("description"), color=data.get("color"), is_hot=data.get("is_hot", 0), is_recommend=data.get("is_recommend", 0), category_id=data.get("category_id"), sort_order=data.get("sort_order", 0), status=data.get("status", "active"))
    db.add(tag)
    db.commit()
    logger.info(f"管理员{admin_id}创建标签成功:tag_id={tag.id}")
    return response.json({"code": 200, "msg": "创建成功", "data": {"tag_id": tag.id, "name": tag.name, "slug": tag.slug, "description": tag.description, "color": tag.color, "is_hot": bool(tag.is_hot), "is_recommend": bool(tag.is_recommend), "category_id": tag.category_id, "sort_order": tag.sort_order, "status": tag.status, "post_count": tag.post_count, "created_at": str(tag.created_at)}})

@admin_tag_bp.put("/")
@openapi.summary("编辑标签")
async def edit_tag(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("编辑标签失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    tag_id = data.get("tag_id")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        logger.warning(f"编辑标签失败:标签不存在,tag_id={tag_id}")
        return response.json({"code": 404, "msg": "标签不存在"})
    logger.info(f"管理员{admin_id}编辑标签:tag_id={tag_id}")
    if "name" in data:
        tag.name = data["name"]
        logger.debug(f"更新字段:name={data['name']}")
    if "slug" in data:
        tag.slug = data["slug"]
        logger.debug(f"更新字段:slug={data['slug']}")
    if "description" in data:
        tag.description = data["description"]
        logger.debug(f"更新字段:description={data['description']}")
    if "color" in data:
        tag.color = data["color"]
        logger.debug(f"更新字段:color={data['color']}")
    if "is_hot" in data:
        tag.is_hot = data["is_hot"]
        logger.debug(f"更新字段:is_hot={data['is_hot']}")
    if "is_recommend" in data:
        tag.is_recommend = data["is_recommend"]
        logger.debug(f"更新字段:is_recommend={data['is_recommend']}")
    if "category_id" in data:
        tag.category_id = data["category_id"]
        logger.debug(f"更新字段:category_id={data['category_id']}")
    if "sort_order" in data:
        tag.sort_order = data["sort_order"]
        logger.debug(f"更新字段:sort_order={data['sort_order']}")
    if "status" in data:
        tag.status = data["status"]
        logger.debug(f"更新字段:status={data['status']}")
    db.commit()
    logger.info(f"管理员{admin_id}编辑标签成功:tag_id={tag_id}")
    return response.json({"code": 200, "msg": "更新成功", "data": {"tag_id": tag.id, "name": tag.name, "slug": tag.slug, "description": tag.description, "color": tag.color, "is_hot": bool(tag.is_hot), "is_recommend": bool(tag.is_recommend), "category_id": tag.category_id, "sort_order": tag.sort_order, "status": tag.status, "post_count": tag.post_count, "updated_at": str(tag.updated_at)}})

@admin_tag_bp.delete("/<tag_id>")
@openapi.summary("删除标签")
async def delete_tag(request, tag_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除标签失败:admin_id无效,tag_id={tag_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        logger.warning(f"删除标签失败:标签不存在,tag_id={tag_id}")
        return response.json({"code": 404, "msg": "标签不存在"})
    logger.info(f"管理员{admin_id}删除标签:tag_id={tag_id}")
    post_tag_count = db.query(PostTag).filter(PostTag.tag_id == tag_id).count()
    db.query(PostTag).filter(PostTag.tag_id == tag_id).delete()
    db.delete(tag)
    db.commit()
    logger.debug(f"删除关联文章标签:共{post_tag_count}条")
    logger.info(f"管理员{admin_id}删除标签成功:tag_id={tag_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_tag_bp.post("/batch-action")
@openapi.summary("批量操作标签")
async def batch_action_tags(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量操作标签失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量操作标签失败:未选择标签")
        return response.json({"code": 400, "msg": "请选择要操作的标签"})
    logger.info(f"管理员{admin_id}批量操作标签:ids={ids},action={action}")
    if action == "delete":
        for tid in ids:
            tag = db.query(Tag).filter(Tag.id == tid).first()
            if tag:
                db.query(PostTag).filter(PostTag.tag_id == tid).delete()
                db.delete(tag)
        logger.debug(f"批量操作:删除{len(ids)}个标签")
    else:
        logger.warning(f"批量操作标签失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}批量操作标签成功:共{len(ids)}条")
    return response.json({"code": 200, "msg": "批量操作成功", "data": {"processed_count": len(ids)}})

@admin_tag_bp.post("/batch-delete")
@openapi.summary("批量删除标签")
async def batch_delete_tags(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除标签失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除标签失败:未选择标签")
        return response.json({"code": 400, "msg": "请选择要删除的标签"})
    logger.info(f"管理员{admin_id}批量删除标签:ids={ids}")
    for tid in ids:
        tag = db.query(Tag).filter(Tag.id == tid).first()
        if tag:
            db.query(PostTag).filter(PostTag.tag_id == tid).delete()
            db.delete(tag)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除标签成功:共{len(ids)}个")
    return response.json({"code": 200, "msg": "批量删除成功", "data": {"deleted_count": len(ids)}})

@admin_tag_bp.get("/stats/overview")
@openapi.summary("获取标签统计概览")
async def get_tag_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取标签统计失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    logger.info(f"管理员{admin_id}查询标签统计")
    total_tags = db.query(Tag).count()
    new_tags_week = db.query(Tag).filter(Tag.created_at >= datetime.now() - timedelta(days=7)).count()
    new_tags_month = db.query(Tag).filter(Tag.created_at >= datetime.now() - timedelta(days=30)).count()
    top_tags = db.query(Tag).order_by(Tag.post_count.desc()).limit(10).all()
    logger.info(f"管理员{admin_id}查询标签统计成功:total={total_tags},week_new={new_tags_week}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_tags": total_tags, "new_tags_week": new_tags_week, "new_tags_month": new_tags_month, "avg_posts_per_tag": 0, "top_tags": [{"tag_id": t.id, "name": t.name, "post_count": t.post_count} for t in top_tags], "trend_data": []}})
