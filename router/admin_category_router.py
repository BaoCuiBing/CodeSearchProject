from datetime import datetime, timedelta
from sanic import Blueprint, response
from sanic_ext import openapi
from sqlalchemy import func
from models.model import User, Category, Post
from models.db_init import get_db_session

admin_category_bp = Blueprint("admin_category", url_prefix="/api/admin/category")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_category_bp.get("/list")
@openapi.summary("获取分类列表")
async def get_category_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "sort")
    order = request.args.get("order", "asc")
    query = db.query(Category)
    if keyword:
        query = query.filter(Category.name.contains(keyword))
    sort_map = {"name": Category.name, "sort": Category.sort}
    order_func = sort_map.get(sort, Category.sort).desc() if order == "desc" else sort_map.get(sort, Category.sort).asc()
    total = query.count()
    categories = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    category_list = []
    for c in categories:
        post_count = db.query(Post).filter(Post.category_id == c.id).count()
        category_list.append({"category_id": c.id, "name": c.name, "icon": c.icon, "sort": c.sort, "post_count": post_count, "created_at": str(c.created_at), "updated_at": str(c.updated_at)})
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": category_list, "total": total, "page": page, "page_size": page_size}})

@admin_category_bp.post("/")
@openapi.summary("创建分类")
async def create_category(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    name = data.get("name")
    if not name:
        return response.json({"code": 400, "msg": "分类名称不能为空"})
    exist = db.query(Category).filter(Category.name == name).first()
    if exist:
        return response.json({"code": 400, "msg": "分类名称已存在"})
    category = Category(name=name, icon=data.get("icon"), sort=data.get("sort", 0))
    db.add(category)
    db.commit()
    return response.json({"code": 200, "msg": "创建成功", "data": {"category_id": category.id, "name": category.name, "icon": category.icon, "sort": category.sort, "created_at": str(category.created_at)}})

@admin_category_bp.put("/")
@openapi.summary("编辑分类")
async def edit_category(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    category_id = data.get("category_id")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return response.json({"code": 404, "msg": "分类不存在"})
    if "name" in data:
        category.name = data["name"]
    if "icon" in data:
        category.icon = data["icon"]
    if "sort" in data:
        category.sort = data["sort"]
    db.commit()
    return response.json({"code": 200, "msg": "更新成功", "data": {"category_id": category.id, "name": category.name, "sort": category.sort, "updated_at": str(category.updated_at)}})

@admin_category_bp.delete("/<category_id>")
@openapi.summary("删除分类")
async def delete_category(request, category_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return response.json({"code": 404, "msg": "分类不存在"})
    post_count = db.query(Post).filter(Post.category_id == category_id).count()
    if post_count > 0:
        move_to_id = request.args.get("move_to_id")
        if not move_to_id:
            return response.json({"code": 400, "msg": "该分类下有文章，请先迁移"})
        db.query(Post).filter(Post.category_id == category_id).update({"category_id": move_to_id})
    db.delete(category)
    db.commit()
    return response.json({"code": 200, "msg": "删除成功", "data": {"deleted_id": category_id, "moved_to_id": int(request.args.get("move_to_id", 0))}})

@admin_category_bp.post("/batch-action")
@openapi.summary("批量操作分类")
async def batch_action_categories(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        return response.json({"code": 400, "msg": "请选择要操作的分类"})
    if action == "delete":
        for cid in ids:
            category = db.query(Category).filter(Category.id == cid).first()
            if category:
                db.delete(category)
    else:
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    return response.json({"code": 200, "msg": "批量操作成功", "data": {"processed_count": len(ids)}})
