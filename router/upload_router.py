import os
import uuid
import logging
from sanic import Blueprint, response
from utils.openapi_helper import openapi
import config
from models.model import File
from utils.oss_option import oss_client

logger = logging.getLogger(__name__)
upload_bp = Blueprint("upload", url_prefix="/api/upload")
UPLOAD_DIR = os.path.join(config.PROJECT_DIR, "static", "uploads")
MAX_SIZE = config.MAX_UPLOAD_SIZE * 1024 * 1024  # 字节

@upload_bp.post("/file")
@openapi.summary("文件上传")
async def upload_file(request):
    db = request.ctx.db
    file = request.files.get("file")
    if not file:
        logger.warning("文件上传失败:未选择文件")
        return response.json({"code": 400, "msg": "未选择文件"})
    file_body = file.body
    if len(file_body) > MAX_SIZE:
        logger.warning(f"文件上传失败:文件过大,{len(file_body)}字节")
        return response.json({"code": 400, "msg": f"文件大小超过{config.MAX_UPLOAD_SIZE}MB限制"})
    logger.info(f"文件上传:filename={file.name},size={len(file_body)}字节")
    ext = os.path.splitext(file.name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    if config.USE_OSS:
        object_key = f"uploads/{unique_name}"
        local_tmp_path = os.path.join(UPLOAD_DIR, unique_name)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(local_tmp_path, "wb") as f:
            f.write(file_body)
        oss_client.upload_file(object_key, local_tmp_path)
        os.remove(local_tmp_path)
        file_url = f"https://{config.OSS_BUCKET_NAME}.oss-{config.OSS_REGION}.aliyuncs.com/{object_key}"
        file_path = object_key
        logger.info(f"文件上传OSS成功:object_key={object_key}")
    else:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, unique_name)
        with open(file_path, "wb") as f:
            f.write(file_body)
        file_url = f"/static/uploads/{unique_name}"
        logger.info(f"文件上传本地成功:file_path={file_path}")
    user_id = request.form.get("user_id")
    user_id = int(user_id) if user_id else None
    file_record = File(user_id=user_id, filename=file.name, file_path=file_path, file_size=len(file_body), file_type=ext.lstrip("."), file_url=file_url)
    db.add(file_record)
    db.commit()
    logger.info(f"文件上传成功:file_url={file_url},user_id={user_id}")
    return response.json({"code": 200, "msg": "上传成功", "data": {"filename": file.name, "file_url": file_url}})
