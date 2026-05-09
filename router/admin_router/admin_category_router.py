from datetime import datetime, timedelta
import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import User, Category, Post

logger = logging.getLogger(__name__)
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
        logger.warning("获取分类列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "sort")
    order = request.args.get("order", "asc")
    logger.info(f"管理员{admin_id}查询分类列表:page={page},page_size={page_size},keyword={keyword}")
    query = db.query(Category)
    if keyword:
        query = query.filter(Category.name.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    sort_map = {"name": Category.name, "sort": Category.sort}
    order_func = sort_map.get(sort, Category.sort).desc() if order == "desc" else sort_map.get(sort, Category.sort).asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    categories = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    category_list = []
    for c in categories:
        post_count = db.query(Post).filter(Post.category_id == c.id).count()
        category_list.append({"category_id": c.id, "name": c.name, "description": c.description, "icon": c.icon, "sort": c.sort, "post_count": post_count, "created_at": str(c.created_at), "updated_at": str(c.updated_at)})
    logger.info(f"管理员{admin_id}查询分类列表成功:共{total}条,返回{len(category_list)}条")
    logger.debug(f"数据处理完成:构建{len(category_list)}条分类记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": category_list, "total": total, "page": page, "page_size": page_size}})

@admin_category_bp.post("/")
@openapi.summary("创建分类")
async def create_category(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("创建分类失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    name = data.get("name")
    if not name:
        logger.warning("创建分类失败:分类名称为空")
        return response.json({"code": 400, "msg": "分类名称不能为空"})
    exist = db.query(Category).filter(Category.name == name).first()
    if exist:
        logger.warning(f"创建分类失败:分类名称已存在,name={name}")
        return response.json({"code": 400, "msg": "分类名称已存在"})
    logger.info(f"管理员{admin_id}创建分类:name={name}")
    category = Category(name=name, description=data.get("description"), icon=data.get("icon"), sort=data.get("sort", 0))
    db.add(category)
    db.commit()
    logger.info(f"管理员{admin_id}创建分类成功:category_id={category.id}")
    return response.json({"code": 200, "msg": "创建成功", "data": {"category_id": category.id, "name": category.name, "description": category.description, "icon": category.icon, "sort": category.sort, "created_at": str(category.created_at)}})

@admin_category_bp.put("/")
@openapi.summary("编辑分类")
async def edit_category(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("编辑分类失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    category_id = data.get("category_id")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        logger.warning(f"编辑分类失败:分类不存在,category_id={category_id}")
        return response.json({"code": 404, "msg": "分类不存在"})
    logger.info(f"管理员{admin_id}编辑分类:category_id={category_id}")
    if "name" in data:
        category.name = data["name"]
        logger.debug(f"更新字段:name={data['name']}")
    if "description" in data:
        category.description = data["description"]
        logger.debug(f"更新字段:description={data['description']}")
    if "sort" in data:
        category.sort = data["sort"]
        logger.debug(f"更新字段:sort={data['sort']}")
    if "icon" in data:
        category.icon = data["icon"]
        logger.debug(f"更新字段:icon={data['icon']}")
    db.commit()
    logger.info(f"管理员{admin_id}编辑分类成功:category_id={category_id}")
    return response.json({"code": 200, "msg": "更新成功", "data": {"category_id": category.id, "name": category.name, "description": category.description, "icon": category.icon, "sort": category.sort, "updated_at": str(category.updated_at)}})

@admin_category_bp.delete("/<category_id>")
@openapi.summary("删除分类")
async def delete_category(request, category_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除分类失败:admin_id无效,category_id={category_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        logger.warning(f"删除分类失败:分类不存在,category_id={category_id}")
        return response.json({"code": 404, "msg": "分类不存在"})
    post_count = db.query(Post).filter(Post.category_id == category_id).count()
    logger.info(f"管理员{admin_id}删除分类:category_id={category_id},post_count={post_count}")
    if post_count > 0:
        move_to_id = request.args.get("move_to_id")
        if move_to_id and move_to_id != "0":
            db.query(Post).filter(Post.category_id == category_id).update({"category_id": move_to_id})
            logger.debug(f"文章迁移:category_id={category_id}->move_to_id={move_to_id}")
        else:
            from models.model import PostTag, Comment, Favorite, Like
            post_ids = [p.id for p in db.query(Post).filter(Post.category_id == category_id).all()]
            for pid in post_ids:
                db.query(PostTag).filter(PostTag.post_id == pid).delete()
                db.query(Comment).filter(Comment.post_id == pid).delete()
                db.query(Favorite).filter(Favorite.post_id == pid).delete()
                db.query(Like).filter(Like.target_id == pid, Like.target_type == "post").delete()
            db.query(Post).filter(Post.category_id == category_id).delete()
            logger.debug(f"删除分类关联文章:category_id={category_id},删除{post_count}篇文章")
    db.delete(category)
    db.commit()
    logger.info(f"管理员{admin_id}删除分类成功:category_id={category_id}")
    return response.json({"code": 200, "msg": "删除成功", "data": {"deleted_id": category_id, "moved_to_id": int(request.args.get("move_to_id", 0))}})

@admin_category_bp.post("/batch-action")
@openapi.summary("批量操作分类")
async def batch_action_categories(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量操作分类失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量操作分类失败:未选择分类")
        return response.json({"code": 400, "msg": "请选择要操作的分类"})
    logger.info(f"管理员{admin_id}批量操作分类:ids={ids},action={action}")
    if action == "delete":
        from models.model import PostTag, Comment, Favorite, Like
        for cid in ids:
            category = db.query(Category).filter(Category.id == cid).first()
            if category:
                post_ids = [p.id for p in db.query(Post).filter(Post.category_id == cid).all()]
                for pid in post_ids:
                    db.query(PostTag).filter(PostTag.post_id == pid).delete()
                    db.query(Comment).filter(Comment.post_id == pid).delete()
                    db.query(Favorite).filter(Favorite.post_id == pid).delete()
                    db.query(Like).filter(Like.target_id == pid, Like.target_type == "post").delete()
                db.query(Post).filter(Post.category_id == cid).delete()
                db.delete(category)
        logger.debug(f"批量操作:删除{len(ids)}个分类及关联文章")
    else:
        logger.warning(f"批量操作分类失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}批量操作分类成功:共{len(ids)}条,操作:{action}")
    return response.json({"code": 200, "msg": "批量操作成功", "data": {"processed_count": len(ids)}})

@admin_category_bp.post("/batch-delete")
@openapi.summary("批量删除分类")
async def batch_delete_categories(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除分类失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除分类失败:未选择分类")
        return response.json({"code": 400, "msg": "请选择要删除的分类"})
    logger.info(f"管理员{admin_id}批量删除分类:ids={ids}")
    from models.model import PostTag, Comment, Favorite, Like
    for cid in ids:
        category = db.query(Category).filter(Category.id == cid).first()
        if category:
            post_ids = [p.id for p in db.query(Post).filter(Post.category_id == cid).all()]
            for pid in post_ids:
                db.query(PostTag).filter(PostTag.post_id == pid).delete()
                db.query(Comment).filter(Comment.post_id == pid).delete()
                db.query(Favorite).filter(Favorite.post_id == pid).delete()
                db.query(Like).filter(Like.target_id == pid, Like.target_type == "post").delete()
            db.query(Post).filter(Post.category_id == cid).delete()
            db.delete(category)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除分类成功:共{len(ids)}个")
    return response.json({"code": 200, "msg": "批量删除成功", "data": {"deleted_count": len(ids)}})
