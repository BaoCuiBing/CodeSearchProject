import os
import uuid
from sanic import Blueprint, response
from sanic_ext import openapi
import config
from models.model import File
from models.db_init import get_db_session

upload_bp = Blueprint("upload", url_prefix="/api/upload")
UPLOAD_DIR = os.path.join(config.PROJECT_DIR, "static", "uploads")
MAX_SIZE = config.MAX_UPLOAD_SIZE * 1024 * 1024  # 字节

@upload_bp.post("/file")
@openapi.summary("文件上传")
async def upload_file(request, db):
    file = request.files.get("file")
    if not file:
        return response.json({"code": 400, "msg": "未选择文件"})
    file_body = file.body
    if len(file_body) > MAX_SIZE:
        return response.json({"code": 400, "msg": f"文件大小超过{config.MAX_UPLOAD_SIZE}MB限制"})
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(file_body)
    file_url = f"/static/uploads/{unique_name}"
    file_record = File(user_id=0, filename=file.name, file_path=file_path, file_size=len(file_body), file_type=ext.lstrip("."), file_url=file_url)
    db.add(file_record)
    db.commit()
    return response.json({"code": 200, "msg": "上传成功", "data": {"filename": file.name, "url": file_url}})
