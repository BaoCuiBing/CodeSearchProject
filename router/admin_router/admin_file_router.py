from datetime import datetime
import logging
import os
from sanic import Blueprint, response
from sanic_ext import openapi
from models.model import User, File
from models.db_init import get_db_session
from utils.oss_option import oss_client
import config

logger = logging.getLogger(__name__)
admin_file_bp = Blueprint("admin_file", url_prefix="/api/admin/file")

def check_admin(db, admin_id):
    if not admin_id:
        return None
    return db.query(User).filter(User.id == admin_id, User.role == "admin").first()

@admin_file_bp.get("/list")
@openapi.summary("获取文件列表")
async def get_file_list(request):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("获取文件列表失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    keyword = request.args.get("keyword")
    logger.info(f"管理员{admin_id}查询文件列表:page={page},page_size={page_size},keyword={keyword}")
    query = db.query(File)
    if keyword:
        query = query.filter(File.filename.contains(keyword))
        logger.debug(f"查询条件:keyword过滤={keyword}")
    total = query.count()
    logger.debug(f"查询结果:total={total}")
    files = query.order_by(File.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    file_list = []
    for f in files:
        file_list.append({"file_id": f.id, "filename": f.filename, "file_path": f.file_path, "file_size": f.file_size, "file_type": f.file_type, "file_url": f.file_url, "created_at": str(f.created_at)})
    logger.info(f"管理员{admin_id}查询文件列表成功:共{total}条,返回{len(file_list)}条")
    return response.json({"code": 200, "msg": "获取成功", "data": {"list": file_list, "total": total, "page": page, "page_size": page_size}})

@admin_file_bp.delete("/<file_id>")
@openapi.summary("删除文件")
async def delete_file(request, file_id):
    db = request.ctx.db
    admin_id = request.args.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning(f"删除文件失败:admin_id无效,file_id={file_id}")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    file_record = db.query(File).filter(File.id == file_id).first()
    if not file_record:
        logger.warning(f"删除文件失败:文件不存在,file_id={file_id}")
        return response.json({"code": 404, "msg": "文件不存在"})
    logger.info(f"管理员{admin_id}删除文件:file_id={file_id},filename={file_record.filename}")
    if config.USE_OSS:
        object_key = file_record.file_path if file_record.file_path.startswith("uploads/") else f"uploads/{os.path.basename(file_record.file_path)}"
        try:
            oss_client.delete_file(object_key)
            logger.debug(f"删除OSS文件:{object_key}")
        except Exception as e:
            logger.error(f"删除OSS文件失败:{object_key},error={str(e)}")
    else:
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
            logger.debug(f"删除物理文件:{file_record.file_path}")
    db.delete(file_record)
    db.commit()
    logger.info(f"管理员{admin_id}删除文件成功:file_id={file_id}")
    return response.json({"code": 200, "msg": "删除成功"})

@admin_file_bp.post("/batch-delete")
@openapi.summary("批量删除文件")
async def batch_delete_files(request):
    db = request.ctx.db
    data = request.json
    admin_id = data.get("admin_id")
    admin = check_admin(db, admin_id)
    if not admin:
        logger.warning("批量删除文件失败:admin_id无效")
        return response.json({"code": 400, "msg": "admin_id不能为空"})
    ids = data.get("ids", [])
    if not ids:
        logger.warning("批量删除文件失败:未选择文件")
        return response.json({"code": 400, "msg": "请选择要删除的文件"})
    logger.info(f"管理员{admin_id}批量删除文件:ids={ids}")
    file_records = db.query(File).filter(File.id.in_(ids)).all()
    for f in file_records:
        if config.USE_OSS:
            object_key = f.file_path if f.file_path.startswith("uploads/") else f"uploads/{os.path.basename(f.file_path)}"
            try:
                oss_client.delete_file(object_key)
            except Exception as e:
                logger.error(f"批量删除OSS文件失败:{object_key},error={str(e)}")
        else:
            if os.path.exists(f.file_path):
                os.remove(f.file_path)
        db.delete(f)
    db.commit()
    logger.info(f"管理员{admin_id}批量删除文件成功:共{len(file_records)}个")
    return response.json({"code": 200, "msg": "批量删除成功", "data": {"deleted_count": len(file_records)}})
