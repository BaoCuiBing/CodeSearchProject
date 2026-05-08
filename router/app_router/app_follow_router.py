import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, Follow
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
follow_bp = Blueprint("follow", url_prefix="/api/follow")

@follow_bp.get("/following")
@openapi.summary("获取我关注的用户列表")
async def get_my_following_users(request):
    db = request.ctx.db
    follower_id = request.args.get("follower_id")
    if not follower_id:
        logger.warning("获取关注列表失败:follower_id为空")
        return response.json({"code": 400, "msg": "follower_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询关注列表:follower_id={follower_id}")
    query = db.query(Follow).filter(Follow.follower_id == follower_id)
    total = query.count()
    follows = query.order_by(Follow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    follow_list = []
    for f in follows:
        user = db.query(User).filter(User.id == f.following_id).first()
        is_mutual = db.query(Follow).filter(Follow.follower_id == f.following_id, Follow.following_id == follower_id).first() is not None
        follow_list.append({"user_id": user.id, "username": user.username, "avatar": user.avatar, "bio": user.bio, "is_mutual": is_mutual, "created_at": str(f.created_at)})
    logger.info(f"获取关注列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": follow_list, "total": total, "page": page, "page_size": page_size}})

@follow_bp.get("/followers")
@openapi.summary("获取我的粉丝列表")
async def get_my_followers(request):
    db = request.ctx.db
    following_id = request.args.get("following_id")
    if not following_id:
        logger.warning("获取粉丝列表失败:following_id为空")
        return response.json({"code": 400, "msg": "following_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询粉丝列表:following_id={following_id}")
    query = db.query(Follow).filter(Follow.following_id == following_id)
    total = query.count()
    follows = query.order_by(Follow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    follow_list = []
    for f in follows:
        user = db.query(User).filter(User.id == f.follower_id).first()
        is_followed_back = db.query(Follow).filter(Follow.follower_id == following_id, Follow.following_id == f.follower_id).first() is not None
        follow_list.append({"user_id": user.id, "username": user.username, "avatar": user.avatar, "bio": user.bio, "is_followed_back": is_followed_back, "created_at": str(f.created_at)})
    logger.info(f"获取粉丝列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": follow_list, "total": total, "page": page, "page_size": page_size}})

@follow_bp.post("/user")
@openapi.summary("关注或取消关注用户")
async def toggle_follow_user(request):
    db = request.ctx.db
    data = request.json
    follower_id = data.get("follower_id")
    following_id = data.get("following_id")
    if not follower_id or not following_id:
        logger.warning("关注失败:参数为空")
        return response.json({"code": 400, "msg": "参数错误"})
    if follower_id == following_id:
        logger.warning("关注失败:不能关注自己")
        return response.json({"code": 400, "msg": "不能关注自己"})
    follower = db.query(User).filter(User.id == follower_id).first()
    if not follower:
        logger.warning(f"关注失败:用户不存在,follower_id={follower_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    following = db.query(User).filter(User.id == following_id).first()
    if not following:
        logger.warning(f"关注失败:用户不存在,following_id={following_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    follow = db.query(Follow).filter(Follow.follower_id == follower_id, Follow.following_id == following_id).first()
    if follow:
        db.delete(follow)
        is_followed = False
        logger.info(f"取消关注:follower_id={follower_id},following_id={following_id}")
    else:
        db.add(Follow(follower_id=follower_id, following_id=following_id))
        is_followed = True
        logger.info(f"关注:follower_id={follower_id},following_id={following_id}")
    db.commit()
    follower_count = db.query(Follow).filter(Follow.following_id == following_id).count()
    return response.json({"code": 200, "msg": "操作成功", "data": {"is_followed": is_followed, "follower_count": follower_count}})

@follow_bp.get("/user/<follower_id>/following")
@openapi.summary("获取指定用户的关注列表")
async def get_following_list(request, follower_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取关注列表失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询用户关注列表:follower_id={follower_id}")
    user = db.query(User).filter(User.id == follower_id).first()
    if not user:
        logger.warning(f"获取关注列表失败:用户不存在,follower_id={follower_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    query = db.query(Follow).filter(Follow.follower_id == follower_id)
    total = query.count()
    follows = query.order_by(Follow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    follow_list = []
    for f in follows:
        target_user = db.query(User).filter(User.id == f.following_id).first()
        is_mutual = db.query(Follow).filter(Follow.follower_id == f.following_id, Follow.following_id == follower_id).first() is not None
        follow_list.append({"user_id": target_user.id, "username": target_user.username, "avatar": target_user.avatar, "bio": target_user.bio, "is_mutual": is_mutual, "created_at": str(f.created_at)})
    logger.info(f"获取关注列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": follow_list, "total": total, "page": page, "page_size": page_size}})

@follow_bp.get("/user/<following_id>/followers")
@openapi.summary("获取指定用户的粉丝列表")
async def get_followers_list(request, following_id):
    db = request.ctx.db
    user_id = request.args.get("user_id")
    if not user_id:
        logger.warning("获取粉丝列表失败:user_id为空")
        return response.json({"code": 400, "msg": "user_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    logger.info(f"查询用户粉丝列表:following_id={following_id}")
    user = db.query(User).filter(User.id == following_id).first()
    if not user:
        logger.warning(f"获取粉丝列表失败:用户不存在,following_id={following_id}")
        return response.json({"code": 404, "msg": "用户不存在"})
    query = db.query(Follow).filter(Follow.following_id == following_id)
    total = query.count()
    follows = query.order_by(Follow.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    follow_list = []
    for f in follows:
        fan_user = db.query(User).filter(User.id == f.follower_id).first()
        is_followed_back = db.query(Follow).filter(Follow.follower_id == following_id, Follow.following_id == f.follower_id).first() is not None
        follow_list.append({"user_id": fan_user.id, "username": fan_user.username, "avatar": fan_user.avatar, "bio": fan_user.bio, "is_followed_back": is_followed_back, "created_at": str(f.created_at)})
    logger.info(f"获取粉丝列表成功:total={total}")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": follow_list, "total": total, "page": page, "page_size": page_size}})