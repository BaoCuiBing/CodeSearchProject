from sanic import Sanic
from sanic.response import text, json
from sanic_cors import CORS
import os
import config
from models.db_init import init_database
from router.user_router import user_bp
from router.upload_router import upload_bp

app = Sanic("CodeSearchProject")
CORS(app)
app.blueprint(user_bp)
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
    return text("Hello, CodeSearchProject!")

@app.get("/health")
async def health_check(request):
    """健康检查接口"""
    return json({"status": "ok"})

if __name__ == "__main__":
    init_app()
    app.run(host=config.SANIC_HOST, port=config.SANIC_PORT, debug=True)
