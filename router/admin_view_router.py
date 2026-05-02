from sanic import Blueprint
from sanic.response import html
from jinja2 import Environment, FileSystemLoader
import os
import config

admin_view_bp = Blueprint("admin_view", url_prefix="/admin")
template_dir = os.path.join(config.PROJECT_DIR, "template", "admin")
jinja_env = Environment(loader=FileSystemLoader(template_dir), variable_start_string="{[", variable_end_string="]}")

def render_template(template_name, **context):
    template = jinja_env.get_template(template_name)
    return html(template.render(**context))

@admin_view_bp.get("/login")
async def admin_login_page(request):
    return render_template("login.html")

@admin_view_bp.get("/")
async def admin_dashboard_page(request):
    return render_template("dashboard.html")

@admin_view_bp.get("/users")
async def admin_users_page(request):
    return render_template("users.html")

@admin_view_bp.get("/articles")
async def admin_articles_page(request):
    return render_template("articles.html")

@admin_view_bp.get("/article/<id>")
async def admin_article_detail_page(request, id):
    return render_template("article_detail.html", id=id)

@admin_view_bp.get("/tags")
async def admin_tags_page(request):
    return render_template("tags.html")

@admin_view_bp.get("/comments")
async def admin_comments_page(request):
    return render_template("comments.html")

@admin_view_bp.get("/messages")
async def admin_messages_page(request):
    return render_template("messages.html")

@admin_view_bp.get("/settings")
async def admin_settings_page(request):
    return render_template("settings.html")

@admin_view_bp.get("/stats")
async def admin_stats_page(request):
    return render_template("stats.html")

@admin_view_bp.get("/files")
async def admin_files_page(request):
    return render_template("files.html")

@admin_view_bp.get("/profile")
async def admin_profile_page(request):
    return render_template("profile.html")
