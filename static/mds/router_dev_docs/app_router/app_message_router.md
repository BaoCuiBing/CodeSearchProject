# 消息通知路由接口文档

## 文件路径
`router/app_message_router.py`

## 蓝图配置
- **蓝图名称**: `message`
- **URL前缀**: `/api/message`

## 接口列表

### 1. 获取通知列表（APP端）
- **路径**: `/api/message/notifications`
- **方法**: `GET`
- **函数名**: `get_notifications`
- **OpenAPI摘要**: 获取系统通知列表（UI图10）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| type | string | no | 通知类型：all/system/system_msg/comment/like/follow，默认all | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 通知数据 |
| data.list | array | 通知列表 |
| data.total | int | 总数 |
| data.unread_count | int | 未读数 |
| data.list[].notification_id | int | 通知ID |
| data.list[].type | string | 通知类型：system/system_msg/comment/like/follow |
| data.list[].content | string | 通知内容 |
| data.list[].is_read | bool | 是否已读 |
| data.list[].created_at | datetime | 创建时间 |
| data.list[].related_id | int | 关联ID（评论/点赞/关注通知关联对应目标ID） |
| data.list[].actor | object | 操作者信息（用户ID、用户名、头像） |

#### 请求示例
```
GET /api/message/notifications?user_id=1&type=all&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 2. 标记通知为已读（APP端）
- **路径**: `/api/message/notification/read`
- **方法**: `PUT`
- **函数名**: `mark_notification_read`
- **OpenAPI摘要**: 标记单条通知为已读

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| notification_id | int | yes | 通知ID | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
PUT /api/message/notification/read
Content-Type: application/json

{
    "user_id": 1,
    "notification_id": 1
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "通知不存在"
}
```

---

### 3. 标记所有通知为已读（APP端）
- **路径**: `/api/message/notifications/read-all`
- **方法**: `PUT`
- **函数名**: `mark_all_notifications_read`
- **OpenAPI摘要**: 标记所有通知为已读（同时标记系统公告为已读）

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |

#### 请求示例
```
PUT /api/message/notifications/read-all
Content-Type: application/json

{
    "user_id": 1
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 4. 删除通知（APP端）
- **路径**: `/api/message/notification/<notification_id>`
- **方法**: `DELETE`
- **函数名**: `delete_notification`
- **OpenAPI摘要**: 删除单条通知

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| notification_id | int | 通知ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
DELETE /api/message/notification/1?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "通知不存在"
}
```

---

### 5. 获取未读通知数量（APP端）
- **路径**: `/api/message/notification/unread-count`
- **方法**: `GET`
- **函数名**: `get_unread_notification_count`
- **OpenAPI摘要**: 获取未读通知数量（用于显示红点）

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 未读统计 |
| data.total | int | 总未读数 |
| data.comment | int | 评论未读数 |
| data.like | int | 点赞未读数 |
| data.follow | int | 关注未读数 |
| data.system | int | 系统消息未读数 |
| data.system_msg | int | 系统公告未读数 |
| data.chat_unread | int | 私信未读数 |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |

#### 请求示例
```
GET /api/message/notification/unread-count?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 6. 获取私信会话列表（APP端）
- **路径**: `/api/message/conversations`
- **方法**: `GET`
- **函数名**: `get_conversations`
- **OpenAPI摘要**: 获取私信会话列表（UI图20）

> 注：会话通过messages表动态聚合，按(from_user_id, to_user_id)配对分组，取每组最新一条消息作为会话摘要。无独立会话表。

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 会话数据 |
| data.list | array | 会话列表 |
| data.total | int | 总数 |
| data.list[].user | object | 对话用户信息（用户ID、用户名、头像） |
| data.list[].last_message | string | 最后一条消息 |
| data.list[].last_time | datetime | 最后消息时间 |
| data.list[].unread_count | int | 未读消息数（动态查询messages表统计） |

#### 请求示例
```
GET /api/message/conversations?user_id=1&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 7. 获取会话消息详情（APP端）
- **路径**: `/api/message/conversation/user/<to_user_id>`
- **方法**: `GET`
- **函数名**: `get_conversation_messages`
- **OpenAPI摘要**: 获取与指定用户的消息记录（UI图21）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| to_user_id | int | 对方用户ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 消息数据 |
| data.list | array | 消息列表 |
| data.total | int | 总数 |
| data.list[].message_id | int | 消息ID |
| data.list[].from_user_id | int | 发送者用户ID |
| data.list[].to_user_id | int | 接收者用户ID |
| data.list[].content | string | 消息内容 |
| data.list[].is_read | bool | 是否已读 |
| data.list[].created_at | datetime | 发送时间 |

#### 请求示例
```
GET /api/message/conversation/user/2?user_id=1&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

#### 响应示例（失败：缺少参数）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 8. 标记会话消息为已读（APP端）
- **路径**: `/api/message/conversation/read`
- **方法**: `PUT`
- **函数名**: `mark_conversation_read`
- **OpenAPI摘要**: 标记指定用户发来的所有私信为已读

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| from_user_id | int | yes | 发送者用户ID | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
PUT /api/message/conversation/read
Content-Type: application/json

{
    "user_id": 1,
    "from_user_id": 2
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "参数错误"
}
```

---

### 9. 发送私信（APP端）
- **路径**: `/api/message/send`
- **方法**: `POST`
- **函数名**: `send_private_message`
- **OpenAPI摘要**: 发送私信给指定用户

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| from_user_id | int | yes | 发送者用户ID | Body (JSON) |
| to_user_id | int | yes | 接收者用户ID | Body (JSON) |
| content | string | yes | 消息内容（最多500字） | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 消息信息 |
| data.message_id | int | 消息ID |

#### 请求示例
```
POST /api/message/send
Content-Type: application/json

{
    "from_user_id": 1,
    "to_user_id": 2,
    "content": "你好，想请教一个问题"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "消息内容不能为空"
}
```

---

### 10. 删除会话（APP端）
- **路径**: `/api/message/conversation/user/<to_user_id>`
- **方法**: `DELETE`
- **函数名**: `delete_conversation`
- **OpenAPI摘要**: 删除与指定用户的所有消息

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| to_user_id | int | 对方用户ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
DELETE /api/message/conversation/user/2?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

#### 响应示例（失败：缺少参数）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```
