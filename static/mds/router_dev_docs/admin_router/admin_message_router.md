# 管理后台消息管理接口文档

## 文件路径
`router/admin_message_router.py`

## 蓝图配置
- **蓝图名称**: `admin_system_message`
- **URL前缀**: `/api/admin/system_messages`

## 接口列表

### 1. 获取系统消息列表（管理端）
- **路径**: `/api/admin/system_messages/list`
- **方法**: `GET`
- **函数名**: `get_system_messages_list`
- **OpenAPI摘要**: 获取系统消息通知列表（UI图29）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| type | string | no | 消息类型：all/system/announcement，默认all | Query |
| status | string | no | 发送状态：draft/sent/all，默认all | Query |
| keyword | string | no | 搜索关键词（标题/内容） | Query |
| sort | string | no | 排序：created_time/send_time/read_count，默认created_time | Query |
| order | string | no | 排序方向：asc/desc，默认desc | Query |

#### 请求示例
```
GET /api/admin/system_messages/list?page=1&page_size=20&type=all&status=all&sort=created_time&order=desc&admin_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "admin_id不能为空"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "system_message_id": 1,
                "type": "announcement",
                "title": "系统维护通知",
                "content": "系统将于2024年1月20日进行维护升级...",
                "target_type": "all",
                "target_count": 1500,
                "read_count": 1200,
                "status": "sent",
                "is_top": true,
                "priority": "high",
                "sender": {"user_id": 1, "username": "超级管理员"},
                "send_time": "2024-01-15 09:00:00",
                "created_at": "2024-01-14 16:00:00",
                "updated_at": "2024-01-15 09:00:00"
            }
        ],
        "total": 85,
        "page": 1,
        "page_size": 20
    }
}
```

---

### 2. 创建系统消息（管理端）
- **路径**: `/api/admin/system_messages`
- **方法**: `POST`
- **函数名**: `create_system_message`
- **OpenAPI摘要**: 创建新的系统消息/公告

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| title | string | yes | 消息标题（最多100字） | Body (JSON) |
| content | string | yes | 消息内容（支持HTML） | Body (JSON) |
| type | string | yes | 消息类型：system/announcement | Body (JSON) |
| target_type | string | yes | 目标类型：all/user_list | Body (JSON) |
| target_ids | array | no | 目标用户ID列表（target_type=user_list时必填；target_type=all时可不传或传空数组） | Body (JSON) |
| priority | string | no | 优先级：low/medium/high，默认medium | Body (JSON) |
| is_top | bool | no | 是否置顶显示 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "title": "系统维护通知",
    "content": "<p>系统将于2024年1月20日进行维护升级...</p>",
    "type": "announcement",
    "target_type": "all",
    "target_ids": [],
    "priority": "high",
    "is_top": true
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "创建成功",
    "data": {
        "system_message_id": 10,
        "type": "announcement",
        "title": "系统维护通知",
        "status": "draft",
        "created_at": "2024-01-15 10:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "消息标题不能为空"
}
```

---

### 3. 编辑系统消息（管理端）
- **路径**: `/api/admin/system_messages`
- **方法**: `PUT`
- **函数名**: `edit_system_message`
- **OpenAPI摘要**: 编辑系统消息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| system_message_id | int | yes | 消息ID | Body (JSON) |
| title | string | no | 消息标题 | Body (JSON) |
| content | string | no | 消息内容 | Body (JSON) |
| type | string | no | 消息类型 | Body (JSON) |
| priority | string | no | 优先级 | Body (JSON) |
| is_top | bool | no | 是否置顶 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "system_message_id": 1,
    "title": "系统维护通知（更新）",
    "content": "<p>更新后的维护通知内容...</p>",
    "type": "announcement",
    "priority": "medium",
    "is_top": false
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "更新成功",
    "data": {
        "system_message_id": 1,
        "type": "announcement",
        "title": "系统维护通知（更新）",
        "updated_at": "2024-01-15 11:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "消息不存在"
}
```

---

### 4. 删除系统消息（管理端）
- **路径**: `/api/admin/system_messages/<system_message_id>`
- **方法**: `DELETE`
- **函数名**: `delete_system_message`
- **OpenAPI摘要**: 删除系统消息

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| system_message_id | int | 消息ID |

#### 请求示例
```
DELETE /api/admin/system_messages/1?admin_id=1
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
    "msg": "消息不存在"
}
```

---

### 5. 发送消息（管理端）
- **路径**: `/api/admin/system_messages/send`
- **方法**: `POST`
- **函数名**: `send_system_message`
- **OpenAPI摘要**: 发送草稿状态的消息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| system_message_id | int | yes | 消息ID | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "system_message_id": 1
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "发送成功",
    "data": {
        "system_message_id": 1,
        "status": "sent",
        "send_time": "2024-01-15 10:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "该消息已发送，不能重复发送"
}
```

---

### 6. 批量删除消息（管理端）
- **路径**: `/api/admin/system_messages/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_messages`
- **OpenAPI摘要**: 批量删除多条系统消息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 消息ID列表，如[1,2,3] | Body (JSON) |

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
    "msg": "删除成功",
    "data": {
        "deleted_count": 3
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要删除的消息"
}
```

---

### 7. 发送消息给指定用户（管理端）
- **路径**: `/api/admin/system_messages/send-to-user`
- **方法**: `POST`
- **函数名**: `send_system_notification_to_user`
- **OpenAPI摘要**: 发送消息给指定用户

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| user_id | int | yes | 目标用户ID | Body (JSON) |
| title | string | yes | 消息标题 | Body (JSON) |
| content | string | yes | 消息内容 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "user_id": 5,
    "title": "系统通知",
    "content": "您的文章已被推荐到首页"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "发送成功",
    "data": {
        "notification_id": 1,
        "user_id": 5,
        "created_at": "2024-01-15 10:30:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

### 8. 获取消息统计概览（管理端）
- **路径**: `/api/admin/system_messages/stats/overview`
- **方法**: `GET`
- **函数名**: `get_message_stats_overview`
- **OpenAPI摘要**: 获取消息统计数据概览

#### 请求示例
```
GET /api/admin/system_messages/stats/overview?admin_id=1
```

> 注：target_count/read_count从system_message_targets表按message_id统计

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "total_messages": 85,
        "sent_today": 3,
        "sent_week": 18,
        "draft_count": 5,
        "total_read_count": 25000,
        "avg_read_rate": 75.5,
        "by_type": {
            "system": 45,
            "announcement": 40
        },
        "trend_data": [
            {"date": "2024-01-01", "sent": 2, "read": 500},
            {"date": "2024-01-02", "sent": 3, "read": 800}
        ]
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

### 8. 获取消息详情（管理端）
- **路径**: `/api/admin/system_messages/<system_message_id>/detail`
- **方法**: `GET`
- **函数名**: `get_system_message_detail`
- **OpenAPI摘要**: 获取系统消息详情及阅读情况

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| system_message_id | int | 消息ID |

#### 请求示例
```
GET /api/admin/system_messages/1/detail?admin_id=1
```

> 注：target_count/read_count从system_message_targets表按message_id统计

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "system_message_id": 1,
        "type": "announcement",
        "title": "系统维护通知",
        "content": "<p>系统将于...</p>",
        "status": "sent",
        "stats": {
            "target_count": 1500,
            "read_count": 1200,
            "unread_count": 300,
            "read_rate": 80.0,
        },
        "read_users": [
            {"user_id": 1, "username": "张三", "read_time": "2024-01-15 10:00:00"}
        ],
        "unread_users": [
            {"user_id": 10, "username": "赵六"}
        ],
        "created_at": "2024-01-14 16:00:00",
        "send_time": "2024-01-15 09:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "消息不存在"
}
```

---

### 9. 发送消息给指定用户（管理端）
- **路径**: `/api/admin/system_messages/send-to-user`
- **方法**: `POST`
- **函数名**: `send_system_notification_to_user`
- **OpenAPI摘要**: 向指定用户发送系统通知

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| system_message_id | int | yes | 系统消息ID | Body (JSON) |
| user_id | int | yes | 目标用户ID | Body (JSON) |
| title | string | yes | 通知标题 | Body (JSON) |
| content | string | yes | 通知内容 | Body (JSON) |
| type | string | no | 通知类型：warning/info/success，默认info | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "system_message_id": 1,
    "user_id": 5,
    "title": "账号异常提醒",
    "content": "检测到您的账号在异地登录，请确认是否为本人操作。",
    "type": "warning"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "发送成功",
    "data": {
        "notification_id": 50,
        "user_id": 5,
        "created_at": "2024-01-15 10:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```
