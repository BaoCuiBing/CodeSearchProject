from sanic import Sanic
from sanic.response import html, json
from sanic_cors import CORS
from sanic_ext import Extend
import os
import logging
import config
from models.db_init import init_database
from router.admin_user_router import admin_user_bp
from router.admin_view_router import admin_view_bp
from router.upload_router import upload_bp
from router.admin_auth_router import admin_auth_bp
from router.admin_article_router import admin_article_bp
from router.admin_category_router import admin_category_bp
from router.admin_comment_router import admin_comment_bp
from router.admin_message_router import admin_message_bp
from router.admin_report_router import admin_report_bp
from router.admin_stats_router import admin_stats_bp
from router.admin_system_router import admin_system_bp
from router.admin_tag_router import admin_tag_bp
from router.admin_file_router import admin_file_bp
from router.log_router import log_bp

os.makedirs(config.LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Sanic("CodeSearchProject")
CORS(app)
extend = Extend(app)
app.blueprint(admin_user_bp)  # 用户管理路由
app.blueprint(admin_view_bp)  # 管理后台视图路由
app.blueprint(upload_bp)  # 文件上传路由
app.blueprint(admin_auth_bp)  # 管理员认证路由
app.blueprint(admin_article_bp)  # 内容管理路由
app.blueprint(admin_category_bp)  # 分类管理路由
app.blueprint(admin_comment_bp)  # 评论管理路由
app.blueprint(admin_message_bp)  # 消息管理路由
app.blueprint(admin_report_bp)  # 举报管理路由
app.blueprint(admin_stats_bp)  # 数据统计路由
app.blueprint(admin_system_bp)  # 系统设置路由
app.blueprint(admin_tag_bp)  # 标签管理路由
app.blueprint(admin_file_bp)  # 文件管理路由
app.blueprint(log_bp)  # 日志路由
static_path = os.path.join(config.PROJECT_DIR, "static")
app.static("/static", static_path, name="static_files")

db_instance = None

@app.listener("before_server_start")
async def init_app(app, loop):
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
    app.run(host=config.SANIC_HOST, port=config.SANIC_PORT, debug=True)
