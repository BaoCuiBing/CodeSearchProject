from sanic import Sanic
from sanic.response import html, json
from sanic_cors import CORS
from sanic_ext import Extend
from sanic.worker.manager import WorkerManager
import os
import logging
import config
from models.db_init import init_database
from router.admin_router.admin_user_router import admin_user_bp
from router.admin_router.admin_view_router import admin_view_bp
from router.upload_router import upload_bp
from router.admin_router.admin_auth_router import admin_auth_bp
from router.admin_router.admin_article_router import admin_article_bp
from router.admin_router.admin_category_router import admin_category_bp
from router.admin_router.admin_comment_router import admin_comment_bp
from router.admin_router.admin_favorite_router import admin_favorite_bp
from router.admin_router.admin_like_router import admin_like_bp
from router.admin_router.admin_follow_router import admin_follow_bp
from router.admin_router.admin_private_message_router import admin_private_message_bp
from router.admin_router.admin_message_router import admin_message_bp
from router.admin_router.admin_report_router import admin_report_bp
from router.admin_router.admin_search_history_router import admin_search_history_bp
from router.admin_router.admin_stats_router import admin_stats_bp
from router.admin_router.admin_system_router import admin_system_bp
from router.admin_router.admin_tag_router import admin_tag_bp
from router.admin_router.admin_file_router import admin_file_bp
from router.log_router import log_bp
from router.app_router.app_user_router import user_bp
from router.app_router.app_profile_router import profile_bp
from router.app_router.app_article_router import article_bp
from router.app_router.app_category_router import category_bp
from router.app_router.app_tag_router import tag_bp
from router.app_router.app_comment_router import comment_bp
from router.app_router.app_follow_router import follow_bp
from router.app_router.app_favorite_router import favorite_bp
from router.app_router.app_message_router import message_bp
from router.app_router.app_search_router import search_bp
from router.app_router.app_ranking_router import ranking_bp
from router.app_router.app_report_router import report_bp
from router.app_router.app_system_router import system_bp

os.makedirs(config.LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(config.LOG_FILE, encoding="utf-8"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
WorkerManager.THRESHOLD = config.SANIC_THRESHOLD  # worker ack超时(单位0.1s)
app = Sanic("CodeSearchProject")
CORS(app)

@app.on_request
async def cors_preflight(request):
    if request.method == "OPTIONS":
        return json({}, status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Max-Age": "86400"
        })

@app.on_response
async def cors_headers(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
extend = Extend(app)
app.blueprint(admin_user_bp)  # 用户管理路由
app.blueprint(admin_view_bp)  # 管理后台视图路由
app.blueprint(upload_bp)  # 文件上传路由
app.blueprint(admin_auth_bp)  # 管理员认证路由
app.blueprint(admin_article_bp)  # 内容管理路由
app.blueprint(admin_category_bp)  # 分类管理路由
app.blueprint(admin_comment_bp)  # 评论管理路由
app.blueprint(admin_favorite_bp)  # 收藏管理路由
app.blueprint(admin_like_bp)  # 点赞管理路由
app.blueprint(admin_follow_bp)  # 关注管理路由
app.blueprint(admin_private_message_bp)  # 私信管理路由
app.blueprint(admin_message_bp)  # 消息管理路由
app.blueprint(admin_report_bp)  # 举报管理路由
app.blueprint(admin_search_history_bp)  # 搜索记录管理路由
app.blueprint(admin_stats_bp)  # 数据统计路由
app.blueprint(admin_system_bp)  # 系统设置路由
app.blueprint(admin_tag_bp)  # 标签管理路由
app.blueprint(admin_file_bp)  # 文件管理路由
app.blueprint(log_bp)  # 日志路由
app.blueprint(user_bp)  # APP用户路由
app.blueprint(profile_bp)  # APP用户资料路由
app.blueprint(article_bp)  # APP文章路由
app.blueprint(category_bp)  # APP分类路由
app.blueprint(tag_bp)  # APP标签路由
app.blueprint(comment_bp)  # APP评论路由
app.blueprint(follow_bp)  # APP关注路由
app.blueprint(favorite_bp)  # APP收藏路由
app.blueprint(message_bp)  # APP消息路由
app.blueprint(search_bp)  # APP搜索路由
app.blueprint(ranking_bp)  # APP排行榜路由
app.blueprint(report_bp)  # APP举报路由
app.blueprint(system_bp)  # APP系统配置路由
static_path = os.path.join(config.PROJECT_DIR, "static")
app.static("/static", static_path, name="static_files")
db_instance = None

@app.listener("before_server_start")
async def init_app(app):
    """初始化应用,创建数据库表"""
    global db_instance
    db_instance = init_database()

@app.on_request
async def inject_db(request):
    """注入数据库会话到请求上下文"""
    request.ctx.db = db_instance.get_session()

@app.on_response
async def close_db(request, response):
    """请求结束后关闭数据库会话"""
    if hasattr(request.ctx, "db"):
        request.ctx.db.close()

@app.get("/")
async def index(request):
    """首页接口,路由到登录页"""
    template_path = os.path.join(config.PROJECT_DIR, "template", "login.html")
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    return html(content)

if __name__ == "__main__":
    app.run(host=config.SANIC_HOST, port=config.SANIC_PORT, debug=True, auto_reload=True)
