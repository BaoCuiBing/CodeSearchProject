from sanic import Blueprint
from sanic.response import file
import os
import config

admin_view_bp = Blueprint("admin_view", url_prefix="/admin")
template_dir = os.path.join(config.PROJECT_DIR, "template")

async def render_template(template_name):
    """使用Sanic内置file方法返回HTML文件"""
    template_path = os.path.join(template_dir, template_name)
    return await file(template_path)

@admin_view_bp.get("/login")
async def admin_login_page(request):
    return await render_template("login.html")

@admin_view_bp.get("/")
async def admin_index_page(request):
    return await render_template("index.html")

@admin_view_bp.get("/dashboard")
async def admin_dashboard_page(request):
    return await render_template("admin/dashboard.html")

@admin_view_bp.get("/users")
async def admin_users_page(request):
    return await render_template("admin/users.html")

@admin_view_bp.get("/articles")
async def admin_articles_page(request):
    return await render_template("admin/articles.html")

@admin_view_bp.get("/article/<id>")
async def admin_article_detail_page(request, id):
    return await render_template("admin/article_detail.html")

@admin_view_bp.get("/tags")
async def admin_tags_page(request):
    return await render_template("admin/tags.html")

@admin_view_bp.get("/comments")
async def admin_comments_page(request):
    return await render_template("admin/comments.html")

@admin_view_bp.get("/messages")
async def admin_messages_page(request):
    return await render_template("admin/messages.html")

@admin_view_bp.get("/settings")
async def admin_settings_page(request):
    return await render_template("admin/settings.html")

@admin_view_bp.get("/stats")
async def admin_stats_page(request):
    return await render_template("admin/stats.html")

@admin_view_bp.get("/files")
async def admin_files_page(request):
    return await render_template("admin/files.html")

@admin_view_bp.get("/profile")
async def admin_profile_page(request):
    return await render_template("admin/profile.html")

@admin_view_bp.get("/dialogs/<path:path>")
async def admin_dialogs_page(request, path):
    return await render_template("admin/dialogs/" + path)
