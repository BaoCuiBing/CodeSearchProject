import os
import logging
from datetime import datetime
from sanic import Blueprint, response
from utils.openapi_helper import openapi
import config

logger = logging.getLogger(__name__)
log_bp = Blueprint("log_router", url_prefix="/api/log")
os.makedirs(config.LOG_DIR, exist_ok=True)

web_logger = logging.getLogger("web_log")
web_logger.setLevel(logging.INFO)
if not web_logger.handlers:
    file_handler = logging.FileHandler(config.WEB_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", "%Y-%m-%d %H:%M:%S"))
    web_logger.addHandler(file_handler)

@log_bp.post("/send")
@openapi.summary("接收前端日志")
async def receive_frontend_log(request):
    data = request.json
    level = data.get("level", "info").upper()
    message = data.get("message")
    module = data.get("module", "unknown")
    user_id = data.get("user_id")
    if not message:
        logger.warning("接收前端日志失败:消息为空")
        return response.json({"code": 400, "msg": "日志消息不能为空"})
    log_msg = f"[前端][{module}] user_id={user_id},IP={request.ip}: {message}"
    level_map = {"DEBUG": web_logger.debug, "INFO": web_logger.info, "WARN": web_logger.warning, "WARNING": web_logger.warning, "ERROR": web_logger.error, "CRITICAL": web_logger.critical}
    log_func = level_map.get(level, web_logger.info)
    log_func(log_msg)
    return response.json({"code": 200, "msg": "日志接收成功"})
