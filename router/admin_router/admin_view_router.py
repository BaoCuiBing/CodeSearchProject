from sanic import Blueprint
from sanic.response import file
import os
import logging
import config

logger = logging.getLogger(__name__)
admin_view_bp = Blueprint("admin_view", url_prefix="/admin")
template_dir = os.path.join(config.PROJECT_DIR, "template")

async def render_template(template_name):
    template_path = os.path.join(template_dir, template_name)
    if not os.path.exists(template_path):
        logger.warning(f"模板文件不存在:{template_name}")
        return file(os.path.join(template_dir, "404.html"))
    logger.debug(f"渲染模板:{template_name}")
    return await file(template_path)

@admin_view_bp.get("/login")
async def admin_login_page(request):
    logger.info(f"访问登录页面,IP={request.ip}")
    return await render_template("login.html")

@admin_view_bp.get("/")
async def admin_index_page(request):
    logger.info(f"访问管理后台首页,IP={request.ip}")
    return await render_template("index.html")

@admin_view_bp.get("/dashboard")
async def admin_dashboard_page(request):
    logger.debug(f"访问仪表盘页面,IP={request.ip}")
    return await render_template("admin/dashboard.html")

@admin_view_bp.get("/users")
async def admin_users_page(request):
    logger.debug(f"访问用户管理页面,IP={request.ip}")
    return await render_template("admin/users.html")

@admin_view_bp.get("/articles")
async def admin_articles_page(request):
    logger.debug(f"访问文章管理页面,IP={request.ip}")
    return await render_template("admin/articles.html")

@admin_view_bp.get("/article/<id>")
async def admin_article_detail_page(request, id):
    logger.debug(f"访问文章详情页面:article_id={id},IP={request.ip}")
    return await render_template("admin/article_detail.html")

@admin_view_bp.get("/tags")
async def admin_tags_page(request):
    logger.debug(f"访问标签管理页面,IP={request.ip}")
    return await render_template("admin/tags.html")

@admin_view_bp.get("/comments")
async def admin_comments_page(request):
    logger.debug(f"访问评论管理页面,IP={request.ip}")
    return await render_template("admin/comments.html")

@admin_view_bp.get("/messages")
async def admin_messages_page(request):
    logger.debug(f"访问消息管理页面,IP={request.ip}")
    return await render_template("admin/messages.html")

@admin_view_bp.get("/settings")
async def admin_settings_page(request):
    logger.debug(f"访问系统设置页面,IP={request.ip}")
    return await render_template("admin/settings.html")

@admin_view_bp.get("/stats")
async def admin_stats_page(request):
    logger.debug(f"访问统计页面,IP={request.ip}")
    return await render_template("admin/stats.html")

@admin_view_bp.get("/files")
async def admin_files_page(request):
    logger.debug(f"访问文件管理页面,IP={request.ip}")
    return await render_template("admin/files.html")

@admin_view_bp.get("/user-behavior")
async def admin_user_behavior_page(request):
    logger.debug(f"访问用户行为管理页面,IP={request.ip}")
    return await render_template("admin/user_behavior.html")

@admin_view_bp.get("/profile")
async def admin_profile_page(request):
    logger.debug(f"访问个人资料页面,IP={request.ip}")
    return await render_template("admin/profile.html")

@admin_view_bp.get("/dialogs/<path:path>")
async def admin_dialogs_page(request, path):
    logger.debug(f"访问对话框页面:path={path},IP={request.ip}")
    return await render_template("admin/dialogs/" + path)
