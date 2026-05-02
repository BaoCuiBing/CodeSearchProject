from sanic import Sanic
from sanic.response import html, json
from sanic_cors import CORS
import os
import config
from models.db_init import init_database
from router.admin_user_router import admin_user_bp
from router.admin_view_router import admin_view_bp
from router.upload_router import upload_bp

app = Sanic("CodeSearchProject")
CORS(app)
app.blueprint(admin_user_bp)
app.blueprint(admin_view_bp)
app.blueprint(upload_bp)
static_path = os.path.join(config.PROJECT_DIR, "static")
app.static("/static", static_path, name="static_files")

def init_app():
    """初始化应用,创建数据库表"""
    db = init_database()
    app.ctx.db = db

@app.get("/")
async def index(request):
    """首页接口"""
    template_path = os.path.join(config.PROJECT_DIR, "template", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    return html(content)

if __name__ == "__main__":
    init_app()
    app.run(host=config.SANIC_HOST, port=config.SANIC_PORT, debug=True)
