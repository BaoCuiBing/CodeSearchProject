# 管理后台搜索记录管理接口文档

## 文件路径
`router/admin_search_history_router.py`

## 蓝图配置
- **蓝图名称**: `admin_search_history`
- **URL前缀**: `/api/admin/search-history`

## 接口列表

### 1. 获取搜索记录列表（管理端）
- **路径**: `/api/admin/search-history/list`
- **方法**: `GET`
- **函数名**: `get_search_history_list`
- **OpenAPI摘要**: 获取搜索记录列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词筛选 | Query |

#### 请求示例
```
GET /api/admin/search-history/list?page=1&page_size=20&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "search_id": 1,
                "user": {"user_id": 5, "username": "张三", "avatar": "/static/imgs/avatar/default.png"},
                "keyword": "Python教程",
                "created_at": "2024-01-15 10:30:00"
            }
        ],
        "total": 25,
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

### 2. 删除搜索记录（管理端）
- **路径**: `/api/admin/search-history/<search_id>`
- **方法**: `DELETE`
- **函数名**: `delete_search_history`
- **OpenAPI摘要**: 删除搜索记录

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| search_id | int | 搜索记录ID |

#### 请求示例
```
DELETE /api/admin/search-history/1?admin_id=1
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
    "msg": "搜索记录不存在"
}
```

---

### 3. 批量删除搜索记录（管理端）
- **路径**: `/api/admin/search-history/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_search_history`
- **OpenAPI摘要**: 批量删除搜索记录

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 搜索记录ID列表 | Body (JSON) |

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
    "msg": "成功删除3条记录"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "ids不能为空"
}
```
