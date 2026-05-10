import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
from models.model import SystemSetting

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

@system_bp.get("/about")
@openapi.summary("获取关于我们页面配置")
async def get_about_config(request):
    db = request.ctx.db
    logger.info("查询关于我们页面配置")
    setting = db.query(SystemSetting).filter(SystemSetting.key == "about_config").first()
    if not setting:
        logger.warning("获取关于我们配置失败:配置不存在")
        return response.json({"code": 404, "msg": "关于我们配置不存在"})
    try:
        data = eval(setting.value)
        logger.info("获取关于我们配置成功")
        return response.json({"code": 200, "msg": "获取成功", "data": data})
    except Exception as e:
        logger.error(f"解析关于我们配置失败:{str(e)}")
        return response.json({"code": 500, "msg": "关于我们配置格式错误"})
