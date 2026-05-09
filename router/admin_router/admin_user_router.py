from datetime import datetime, timedelta
import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from sqlalchemy import func
from models.model import User, Post, Comment, Follow, Favorite, Like, Notification
from utils.password_analysis import generate_salt, hash_password, verify_password

logger = logging.getLogger(__name__)
admin_user_bp = Blueprint("admin_user", url_prefix="/api/admin/user")

@admin_user_bp.get("/list")
@openapi.summary("获取用户列表")
async def get_user_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        logger.warning("获取用户列表失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning(f"获取用户列表失败:admin_id={admin_id}不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    status = request.args.get("status", "all")
    sort = request.args.get("sort", "created_time")
    order = request.args.get("order", "desc")
    register_start = request.args.get("register_start")
    register_end = request.args.get("register_end")
    logger.info(f"管理员{admin_id}查询用户列表:page={page},page_size={page_size},keyword={keyword},status={status},sort={sort},order={order}")
    query = db.query(User)
    if keyword:
        query = query.filter(User.username.contains(keyword) | User.usernumber.contains(keyword) | User.email.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    if status != "all":
        query = query.filter(User.status == status)
        logger.debug(f"查询条件:status过滤={status}")
    if register_start:
        query = query.filter(User.created_at >= register_start)
        logger.debug(f"查询条件:register_start={register_start}")
    if register_end:
        query = query.filter(User.created_at <= register_end)
        logger.debug(f"查询条件:register_end={register_end}")
    sort_map = {"created_time": User.created_at, "last_login": User.last_login_time}
    order_func = sort_map.get(sort, User.created_at).desc() if order == "desc" else sort_map.get(sort, User.created_at).asc()
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    users = query.order_by(order_func).offset((page - 1) * page_size).limit(page_size).all()
    logger.info(f"管理员{admin_id}查询用户列表成功:共{total}条,返回{len(users)}条")
    user_list = []
    for u in users:
        article_count = db.query(Post).filter(Post.user_id == u.id, Post.type == "article").count()
        question_count = db.query(Post).filter(Post.user_id == u.id, Post.type == "question").count()
        comment_count = db.query(Comment).filter(Comment.user_id == u.id).count()
        follower_count = db.query(Follow).filter(Follow.following_id == u.id).count()
        following_count = db.query(Follow).filter(Follow.follower_id == u.id).count()
        like_count = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.like_count)).scalar() or 0
        view_count = db.query(Post).filter(Post.user_id == u.id).with_entities(func.sum(Post.view_count)).scalar() or 0
        user_list.append({"user_id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "phone": u.phone, "avatar": u.avatar, "status": u.status, "role": u.role, "article_count": article_count, "question_count": question_count, "comment_count": comment_count, "follower_count": follower_count, "following_count": following_count, "like_count": like_count, "view_count": view_count, "last_login_time": str(u.last_login_time) if u.last_login_time else None, "created_at": str(u.created_at)})
    logger.debug(f"数据处理完成:构建{len(user_list)}条用户记录")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": user_list, "total": total, "page": page, "page_size": page_size}})

@admin_user_bp.get("/<user_id>")
@openapi.summary("获取用户详情")
async def get_user_detail(request, user_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        logger.warning("获取用户详情失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning(f"获取用户详情失败:admin_id={admin_id}不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    logger.info(f"管理员{admin_id}查询用户详情:user_id={user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"获取用户详情失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    article_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "article").count()
    question_count = db.query(Post).filter(Post.user_id == user.id, Post.type == "question").count()
    comment_count = db.query(Comment).filter(Comment.user_id == user.id).count()
    favorite_count = db.query(Favorite).filter(Favorite.user_id == user.id).count()
    follower_count = db.query(Follow).filter(Follow.following_id == user.id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
    like_received = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.like_count)).scalar() or 0
    like_given = db.query(Like).filter(Like.user_id == user.id).count()
    view_count = db.query(Post).filter(Post.user_id == user.id).with_entities(func.sum(Post.view_count)).scalar() or 0
    logger.info(f"管理员{admin_id}查询用户详情成功:username={user.username}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"user_id": user.id, "usernumber": user.usernumber, "username": user.username, "email": user.email, "phone": user.phone, "avatar": user.avatar, "bio": user.bio, "location": user.location, "website": user.website, "github": user.github, "status": user.status, "role": user.role, "stats": {"article_count": article_count, "question_count": question_count, "comment_count": comment_count, "favorite_count": favorite_count, "follower_count": follower_count, "following_count": following_count, "like_received": like_received, "like_given": like_given, "view_count": view_count}, "created_at": str(user.created_at), "last_login_time": str(user.last_login_time) if user.last_login_time else None, "login_ip": user.login_ip, "device_info": user.device_info, "is_verified": bool(user.is_verified), "ban_reason": user.ban_reason, "ban_expire_time": str(user.ban_expire_time) if user.ban_expire_time else None}})

@admin_user_bp.post("/")
@openapi.summary("创建用户")
async def create_user(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("创建用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("创建用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    username = data.get("username")
    usernumber = data.get("usernumber")
    password = data.get("password")
    email = data.get("email", "")
    phone = data.get("phone", "")
    role = data.get("role", "user")
    avatar = data.get("avatar", "")
    bio = data.get("bio", "")
    location = data.get("location", "")
    website = data.get("website", "")
    github = data.get("github", "")
    if not username or not usernumber or not password:
        logger.warning("创建用户失败:必填字段为空")
        return response.json({"code": 400, "msg": "用户名、账号、密码不能为空"})
    exist_user = db.query(User).filter(User.usernumber == usernumber).first()
    if exist_user:
        logger.warning(f"创建用户失败:账号已存在,usernumber={usernumber}")
        return response.json({"code": 400, "msg": "账号已存在"})
    logger.info(f"管理员{admin_id}创建用户:username={username},usernumber={usernumber}")
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    new_user = User(username=username, usernumber=usernumber, password=hashed_password, salt=salt, email=email if email else None, phone=phone if phone else None, role=role, avatar=avatar if avatar else None, bio=bio if bio else None, location=location if location else None, website=website if website else None, github=github if github else None)
    db.add(new_user)
    db.commit()
    logger.info(f"管理员{admin_id}创建用户成功:user_id={new_user.id},username={username}")
    return response.json({"code": 200, "msg": "创建成功", "data": {"user_id": new_user.id, "username": new_user.username}})

@admin_user_bp.post("/ban")
@openapi.summary("封禁/解封用户")
async def toggle_user_ban(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("封禁用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("封禁用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    action = data.get("action")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"封禁用户失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    if action == "ban":
        reason = data.get("reason")
        if not reason:
            logger.warning("封禁用户失败:封禁原因为空")
            return response.json({"code": 400, "msg": "封禁原因不能为空"})
        duration = data.get("duration", 7)
        logger.info(f"管理员{admin_id}封禁用户:user_id={user_id},reason={reason},duration={duration}")
        user.status = "banned"
        user.ban_reason = reason
        if duration > 0:
            user.ban_expire_time = datetime.now() + timedelta(days=duration)
        else:
            user.ban_expire_time = None
        msg = "已封禁该用户"
    elif action == "unban":
        logger.info(f"管理员{admin_id}解封用户:user_id={user_id}")
        user.status = "active"
        user.ban_reason = None
        user.ban_expire_time = None
        msg = "已解封该用户"
    elif action == "toggle":
        if user.status == "banned":
            logger.info(f"管理员{admin_id}解封用户:user_id={user_id}")
            user.status = "active"
            user.ban_reason = None
            user.ban_expire_time = None
            msg = "已解封该用户"
        else:
            logger.info(f"管理员{admin_id}封禁用户:user_id={user_id}")
            user.status = "banned"
            user.ban_reason = "管理员操作"
            user.ban_expire_time = None
            msg = "已封禁该用户"
    else:
        logger.warning(f"封禁用户失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}封禁/解封用户成功:user_id={user_id},action={action}")
    return response.json({"code": 200, "msg": msg, "data": {"user_id": user.id, "status": user.status, "ban_reason": user.ban_reason, "ban_expire_time": str(user.ban_expire_time) if user.ban_expire_time else None}})

@admin_user_bp.delete("/<user_id>")
@openapi.summary("删除用户")
async def delete_user(request, user_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        logger.warning("删除用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("删除用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"删除用户失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    if user.role == "admin":
        admin_count = db.query(User).filter(User.role == "admin").count()
        if admin_count <= 1:
            logger.warning(f"删除用户失败:系统中只有一个管理员,user_id={user_id}")
            return response.json({"code": 400, "msg": "系统中至少需要保留一个管理员账号"})
    logger.info(f"管理员{admin_id}删除用户:user_id={user_id},username={user.username}")
    from models.model import Report, SearchHistory, Favorite, Like, Follow, Message, Notification, Post, Comment, SystemMessageTarget, SystemMessage, File
    db.query(File).filter(File.user_id == user_id).delete()
    db.query(Report).filter(Report.reporter_id == user_id).delete()
    db.query(Report).filter(Report.handler_id == user_id).delete()
    db.query(SearchHistory).filter(SearchHistory.user_id == user_id).delete()
    db.query(Favorite).filter(Favorite.user_id == user_id).delete()
    db.query(Like).filter(Like.user_id == user_id).delete()
    db.query(Follow).filter((Follow.follower_id == user_id) | (Follow.following_id == user_id)).delete()
    db.query(Message).filter((Message.from_user_id == user_id) | (Message.to_user_id == user_id)).delete()
    db.query(Notification).filter(Notification.user_id == user_id).delete()
    db.query(SystemMessageTarget).filter(SystemMessageTarget.user_id == user_id).delete()
    db.query(SystemMessage).filter(SystemMessage.sender_id == user_id).delete()
    db.query(Comment).filter(Comment.user_id == user_id).delete()
    db.query(Post).filter(Post.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    logger.info(f"管理员{admin_id}删除用户成功:user_id={user_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_user_bp.put("/")
@openapi.summary("编辑用户信息")
async def edit_user_info(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("编辑用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("编辑用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"编辑用户失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"管理员{admin_id}编辑用户:user_id={user_id}")
    if "username" in data:
        user.username = data["username"]
        logger.debug(f"更新字段:username={data['username']}")
    if "email" in data:
        user.email = data["email"]
        logger.debug(f"更新字段:email={data['email']}")
    if "role" in data:
        user.role = data["role"]
        logger.debug(f"更新字段:role={data['role']}")
    if "bio" in data:
        user.bio = data["bio"]
        logger.debug(f"更新字段:bio={data['bio']}")
    if "is_verified" in data:
        user.is_verified = 1 if data["is_verified"] else 0
        logger.debug(f"更新字段:is_verified={data['is_verified']}")
    if "avatar" in data and data["avatar"]:
        user.avatar = data["avatar"]
        logger.debug(f"更新字段:avatar={data['avatar']}")
    if "phone" in data:
        user.phone = data["phone"] if data["phone"] else None
        logger.debug(f"更新字段:phone={data['phone']}")
    if "location" in data:
        user.location = data["location"] if data["location"] else None
        logger.debug(f"更新字段:location={data['location']}")
    if "website" in data:
        user.website = data["website"] if data["website"] else None
        logger.debug(f"更新字段:website={data['website']}")
    if "github" in data:
        user.github = data["github"] if data["github"] else None
        logger.debug(f"更新字段:github={data['github']}")
    db.commit()
    logger.info(f"管理员{admin_id}编辑用户成功:user_id={user_id}")
    return response.json({"code": 200, "msg": "编辑成功"})

@admin_user_bp.post("/reset-password")
@openapi.summary("重置用户密码")
async def reset_user_password(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("重置密码失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("重置密码失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    user_id = data.get("user_id")
    new_password = data.get("new_password")
    if not new_password or len(new_password) < 6:
        logger.warning("重置密码失败:新密码长度不足")
        return response.json({"code": 400, "msg": "新密码不能少于6位"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"重置密码失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"管理员{admin_id}重置用户密码:user_id={user_id}")
    salt = generate_salt()
    user.salt = salt
    user.password = hash_password(new_password, salt)
    db.commit()
    logger.info(f"管理员{admin_id}重置用户密码成功:user_id={user_id}")
    return response.json({"code": 200, "msg": "密码重置成功"})

@admin_user_bp.post("/batch-action")
@openapi.summary("批量操作用户")
async def batch_action_users(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("批量操作用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("批量操作用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    ids = data.get("ids", [])
    action = data.get("action")
    if not ids:
        logger.warning("批量操作用户失败:未选择用户")
        return response.json({"code": 400, "msg": "请选择要操作的用户"})
    logger.info(f"管理员{admin_id}批量操作用户:ids={ids},action={action}")
    users = db.query(User).filter(User.id.in_(ids)).all()
    if action == "ban":
        for u in users:
            u.status = "banned"
        logger.debug(f"批量操作:封禁{len(users)}个用户")
    elif action == "unban":
        for u in users:
            u.status = "active"
        logger.debug(f"批量操作:解封{len(users)}个用户")
    elif action == "delete":
        admin_count = db.query(User).filter(User.role == "admin").count()
        admin_ids_in_list = [u.id for u in users if u.role == "admin"]
        if len(admin_ids_in_list) > 0 and (admin_count - len(admin_ids_in_list)) < 1:
            logger.warning(f"批量删除用户失败:尝试删除最后一个管理员,ids={ids}")
            return response.json({"code": 400, "msg": "系统中至少需要保留一个管理员账号"})
        for u in users:
            db.delete(u)
        logger.debug(f"批量操作:删除{len(users)}个用户")
    else:
        logger.warning(f"批量操作用户失败:无效操作,action={action}")
        return response.json({"code": 400, "msg": "无效操作"})
    db.commit()
    logger.info(f"管理员{admin_id}批量操作用户成功:共{len(users)}条,操作:{action}")
    return response.json({"code": 200, "msg": "批量操作成功"})

@admin_user_bp.post("/batch-delete")
@openapi.summary("批量删除用户")
async def batch_delete_users(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("批量删除用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("批量删除用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除用户失败:未选择用户")
        return response.json({"code": 400, "msg": "请选择要删除的用户"})
    logger.info(f"管理员{admin_id}批量删除用户:ids={ids}")
    users = db.query(User).filter(User.id.in_(ids)).all()
    admin_count = db.query(User).filter(User.role == "admin").count()
    admin_ids_in_list = [u.id for u in users if u.role == "admin"]
    if len(admin_ids_in_list) > 0 and (admin_count - len(admin_ids_in_list)) < 1:
        logger.warning(f"批量删除用户失败:尝试删除最后一个管理员,ids={ids}")
        return response.json({"code": 400, "msg": "系统中至少需要保留一个管理员账号"})
    for u in users:
        db.delete(u)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除用户成功:共{len(users)}条")
    return response.json({"code": 200, "msg": "批量删除成功", "data": {"deleted_count": len(users)}})

@admin_user_bp.post("/export")
@openapi.summary("导出用户数据")
async def export_users(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("导出用户失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("导出用户失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    logger.info(f"管理员{admin_id}导出用户数据")
    users = db.query(User).all()
    user_list = [{"user_id": u.id, "usernumber": u.usernumber, "username": u.username, "email": u.email, "role": u.role, "status": u.status, "created_at": str(u.created_at)} for u in users]
    logger.info(f"管理员{admin_id}导出用户成功:共{len(user_list)}条")
    return response.json({"code": 200, "msg": "导出成功", "data": {"filename": "users.xlsx", "file_url": "/static/exports/users.xlsx"}})

@admin_user_bp.get("/stats/overview")
@openapi.summary("获取用户统计概览")
async def get_user_stats_overview(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    if not admin_id:
        logger.warning("获取用户统计失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("获取用户统计失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    period = request.args.get("period", "month")
    logger.info(f"管理员{admin_id}查询用户统计:period={period}")
    total_users = db.query(User).count()
    new_users_today = db.query(User).filter(func.date(User.created_at) == datetime.now().date()).count()
    new_users_week = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=7)).count()
    new_users_month = db.query(User).filter(User.created_at >= datetime.now() - timedelta(days=30)).count()
    active_users = db.query(User).filter(User.status == "active").count()
    banned_users = db.query(User).filter(User.status == "banned").count()
    verified_users = db.query(User).filter(User.is_verified == 1).count()
    logger.info(f"管理员{admin_id}查询用户统计成功:total={total_users},today={new_users_today}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"total_users": total_users, "new_users_today": new_users_today, "new_users_week": new_users_week, "new_users_month": new_users_month, "active_users": active_users, "banned_users": banned_users, "verified_users": verified_users, "growth_rate": round((new_users_month / total_users * 100) if total_users > 0 else 0, 2), "trend_data": []}})

@admin_user_bp.post("/<user_id>/notify")
@openapi.summary("发送系统消息给用户")
async def send_system_notification_to_user(request, user_id):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    if not admin_id:
        logger.warning("发送用户通知失败:缺少admin_id参数")
        return response.json({"code": 403, "msg": "权限不足"})
    admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
    if not admin:
        logger.warning("发送用户通知失败:admin_id不是管理员")
        return response.json({"code": 403, "msg": "权限不足"})
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        logger.warning("发送用户通知失败:标题和内容为空")
        return response.json({"code": 400, "msg": "标题和内容不能为空"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"发送用户通知失败:用户不存在,user_id={user_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    logger.info(f"管理员{admin_id}发送通知给用户:user_id={user_id},title={title}")
    return response.json({"code": 200, "msg": "通知已发送"})
