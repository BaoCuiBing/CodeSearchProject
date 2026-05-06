# 管理后台关注管理接口文档

## 文件路径
`router/admin_follow_router.py`

## 蓝图配置
- **蓝图名称**: `admin_follow`
- **URL前缀**: `/api/admin/follow`

## 接口列表

### 1. 获取关注列表（管理端）
- **路径**: `/api/admin/follow/list`
- **方法**: `GET`
- **函数名**: `get_follow_list`
- **OpenAPI摘要**: 获取关注列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| follower_id | int | no | 粉丝用户ID | Query |
| following_id | int | no | 被关注用户ID | Query |

#### 请求示例
```
GET /api/admin/follow/list?page=1&page_size=20&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "follow_id": 1,
                "follower": {"user_id": 5, "username": "张三", "avatar": "/static/imgs/avatar/default.png"},
                "following": {"user_id": 10, "username": "李四", "avatar": "/static/imgs/avatar/default.png"},
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

### 2. 删除关注（管理端）
- **路径**: `/api/admin/follow/<follow_id>`
- **方法**: `DELETE`
- **函数名**: `delete_follow`
- **OpenAPI摘要**: 删除关注

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| follow_id | int | 关注ID |

#### 请求示例
```
DELETE /api/admin/follow/1?admin_id=1
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
    "msg": "关注不存在"
}
```

---

### 3. 批量删除关注（管理端）
- **路径**: `/api/admin/follow/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_follow`
- **OpenAPI摘要**: 批量删除关注

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 关注ID列表，如[1,2,3] | Body (JSON) |

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
    "msg": "成功删除3条关注"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "ids不能为空"
}
```
