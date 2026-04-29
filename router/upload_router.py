import os
from sanic import Blueprint, response
from sanic_ext import openapi
import config

upload_bp = Blueprint("upload", url_prefix="/api/upload")
UPLOAD_DIR = os.path.join(config.PROJECT_DIR, "static", "uploads")

@upload_bp.post("/file")
@openapi.summary("文件上传")
async def upload_file(request):
    file = request.files.get("file")
    if not file:
        return response.json({"code": 400, "msg": "未选择文件"})
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.name)
    file.save(file_path)
    file_url = f"/static/uploads/{file.name}"
    return response.json({"code": 200, "msg": "上传成功", "data": {"filename": file.name, "url": file_url}})
