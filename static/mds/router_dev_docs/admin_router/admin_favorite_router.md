# 管理后台收藏管理接口文档

## 文件路径
`router/admin_favorite_router.py`

## 蓝图配置
- **蓝图名称**: `admin_favorite`
- **URL前缀**: `/api/admin/favorite`

## 接口列表

### 1. 获取收藏列表（管理端）
- **路径**: `/api/admin/favorite/list`
- **方法**: `GET`
- **函数名**: `get_favorite_list`
- **OpenAPI摘要**: 获取收藏列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| user_id | int | no | 收藏用户ID | Query |
| post_id | int | no | 文章ID | Query |

#### 请求示例
```
GET /api/admin/favorite/list?page=1&page_size=20&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "favorite_id": 1,
                "user": {"user_id": 5, "username": "张三", "avatar": "/static/imgs/avatar/default.png"},
                "post": {
                    "post_id": 100,
                    "title": "Python入门教程",
                    "type": "original",
                    "user": {"user_id": 10, "username": "作者李四"}
                },
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

### 2. 删除收藏（管理端）
- **路径**: `/api/admin/favorite/<favorite_id>`
- **方法**: `DELETE`
- **函数名**: `delete_favorite`
- **OpenAPI摘要**: 删除收藏

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| favorite_id | int | 收藏ID |

#### 请求示例
```
DELETE /api/admin/favorite/1?admin_id=1
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
    "msg": "收藏不存在"
}
```

---

### 3. 批量删除收藏（管理端）
- **路径**: `/api/admin/favorite/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_favorite`
- **OpenAPI摘要**: 批量删除收藏

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 收藏ID列表，如[1,2,3] | Body (JSON) |

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
    "msg": "成功删除3条收藏"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "ids不能为空"
}
```
