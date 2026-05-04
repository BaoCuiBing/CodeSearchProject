# 管理后台文件管理接口文档

## 文件路径
`router/admin_file_router.py`

## 蓝图配置
- **蓝图名称**: `admin_file`
- **URL前缀**: `/api/admin/file`

## 接口列表

### 1. 获取文件列表（管理端）
- **路径**: `/api/admin/file/list`
- **方法**: `GET`
- **函数名**: `get_file_list`
- **OpenAPI摘要**: 获取文件列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页条数，默认20 | Query |
| keyword | string | no | 文件名关键词搜索 | Query |

#### 请求示例
```
GET /api/admin/file/list?admin_id=1&page=1&page_size=20
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "file_id": 1,
                "filename": "cover.jpg",
                "file_path": "/static/uploads/cover.jpg",
                "file_size": 102400,
                "file_type": "image/jpeg",
                "file_url": "/static/uploads/cover.jpg",
                "created_at": "2024-01-15 10:30:00"
            }
        ],
        "total": 100,
        "page": 1,
        "page_size": 20
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "admin_id不能为空"
}
```

---

### 2. 删除文件（管理端）
- **路径**: `/api/admin/file/<file_id>`
- **方法**: `DELETE`
- **函数名**: `delete_file`
- **OpenAPI摘要**: 删除文件

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| file_id | int | 文件ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |

#### 请求示例
```
DELETE /api/admin/file/1?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "删除成功"
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文件不存在"
}
```

---

### 3. 批量删除文件（管理端）
- **路径**: `/api/admin/file/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_files`
- **OpenAPI摘要**: 批量删除文件

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 文件ID列表，如[1,2,3] | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [1, 2, 3]
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "批量删除成功",
    "data": {
        "deleted_count": 3
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要删除的文件"
}
```
