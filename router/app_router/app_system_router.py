import logging
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import SystemSetting
from models.db_init import get_db_session

logger = logging.getLogger(__name__)
system_bp = Blueprint("system", url_prefix="/api/system")

@system_bp.get("/carousel")
@openapi.summary("获取首页轮播图")
async def get_carousel(request):
    db = request.ctx.db
    logger.info("查询轮播图配置")
    setting = db.query(SystemSetting).filter(SystemSetting.key == "carousel_imgs").first()
    if not setting:
        logger.warning("获取轮播图失败:配置不存在")
        return response.json({"code": 404, "msg": "轮播图配置不存在"})
    try:
        data = eval(setting.value)
        imgs = data.get("imgs", [])
        logger.info(f"获取轮播图成功:count={len(imgs)}")
        return response.json({"code": 200, "msg": "获取成功", "data": imgs})
    except Exception as e:
        logger.error(f"解析轮播图配置失败:{str(e)}")
        return response.json({"code": 500, "msg": "轮播图配置格式错误"})
