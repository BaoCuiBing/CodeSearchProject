# 管理后台私信管理接口文档

## 文件路径
`router/admin_private_message_router.py`

## 蓝图配置
- **蓝图名称**: `admin_private_message`
- **URL前缀**: `/api/admin/private_message`

## 接口列表

### 1. 获取私信列表（管理端）
- **路径**: `/api/admin/private_message/list`
- **方法**: `GET`
- **函数名**: `get_private_message_list`
- **OpenAPI摘要**: 获取私信列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| from_user_id | int | no | 发送用户ID | Query |
| to_user_id | int | no | 接收用户ID | Query |
| is_read | int | no | 已读状态：0-未读，1-已读 | Query |

#### 请求示例
```
GET /api/admin/private_message/list?page=1&page_size=20&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "message_id": 1,
                "from_user": {"user_id": 5, "username": "张三", "avatar": "/static/imgs/avatar/default.png"},
                "to_user": {"user_id": 10, "username": "李四", "avatar": "/static/imgs/avatar/default.png"},
                "content": "你好，这是一条私信内容",
                "is_read": 0,
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

### 2. 获取私信详情（管理端）
- **路径**: `/api/admin/private_message/<message_id>/detail`
- **方法**: `GET`
- **函数名**: `get_private_message_detail`
- **OpenAPI摘要**: 获取私信详情

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| message_id | int | 私信ID |

#### 请求示例
```
GET /api/admin/private_message/1/detail?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "message_id": 1,
        "from_user": {"user_id": 5, "username": "张三", "avatar": "/static/imgs/avatar/default.png"},
        "to_user": {"user_id": 10, "username": "李四", "avatar": "/static/imgs/avatar/default.png"},
        "content": "你好，这是一条私信内容",
        "is_read": 0,
        "created_at": "2024-01-15 10:30:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "私信不存在"
}
```

---

### 3. 删除私信（管理端）
- **路径**: `/api/admin/private_message/<message_id>`
- **方法**: `DELETE`
- **函数名**: `delete_private_message`
- **OpenAPI摘要**: 删除私信

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| message_id | int | 私信ID |

#### 请求示例
```
DELETE /api/admin/private_message/1?admin_id=1
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
    "msg": "私信不存在"
}
```

---

### 4. 批量删除私信（管理端）
- **路径**: `/api/admin/private_message/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_private_message`
- **OpenAPI摘要**: 批量删除私信

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 私信ID列表，如[1,2,3] | Body (JSON) |

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
    "msg": "成功删除3条私信"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "ids不能为空"
}
```
