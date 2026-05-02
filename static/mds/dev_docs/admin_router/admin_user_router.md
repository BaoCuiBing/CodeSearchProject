# 管理后台用户管理接口文档

## 文件路径
`router/admin_user_router.py`

## 蓝图配置
- **蓝图名称**: `admin_user`
- **URL前缀**: `/api/admin/user`

## 接口列表

### 1. 获取用户列表（管理端）
- **路径**: `/api/admin/user/list`
- **方法**: `GET`
- **函数名**: `get_user_list`
- **OpenAPI摘要**: 获取所有用户列表（UI图24）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词（用户名/账号/邮箱） | Query |
| status | string | no | 状态筛选：active/banned/all，默认all | Query |
| sort | string | no | 排序：created_time/last_login/article_count/follower_count，默认created_time | Query |
| order | string | no | 排序方向：asc/desc，默认desc | Query |
| register_start | string | no | 注册时间开始（YYYY-MM-DD） | Query |
| register_end | string | no | 注册时间结束（YYYY-MM-DD） | Query |

#### 请求示例
```
GET /api/admin/user/list?admin_id=1&page=1&page_size=20&status=all&sort=created_time&order=desc
```

> 注：question_count从posts表按user_id+type='question'统计；like_count/view_count从posts表按user_id聚合sum；comment_count从comments表按user_id统计；follower_count从follows表按following_id统计；following_count从follows表按follower_id统计

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "user_id": 1,
                "usernumber": "user001",
                "username": "张三",
                "email": "zhangsan@example.com",
                "avatar": "/static/uploads/avatar1.jpg",
                "status": "active",
                "role": "user",
                "article_count": 15,
                "question_count": 8,
                "comment_count": 50,
                "follower_count": 120,
                "following_count": 30,
                "like_count": 500,
                "view_count": 10000,
                "last_login_time": "2024-01-15 10:30:00",
                "created_at": "2023-06-01 08:00:00"
            }
        ],
        "total": 1500,
        "page": 1,
        "page_size": 20
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 403,
    "msg": "权限不足"
}
```

---

### 2. 获取用户详情（管理端）
- **路径**: `/api/admin/user/<user_id>`
- **方法**: `GET`
- **函数名**: `get_user_detail`
- **OpenAPI摘要**: 获取用户详细信息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | int | 用户ID |

#### 请求示例
```
GET /api/admin/user/1?admin_id=1
```

> 注：question_count从posts表按user_id+type='question'统计；comment_count从comments表按user_id统计；favorite_count从favorites表按user_id统计；like_received从posts表按user_id聚合sum(like_count)；like_given从likes表按user_id统计；view_count从posts表按user_id聚合sum(view_count)；follower_count/following_count同list接口

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "user_id": 1,
        "usernumber": "user001",
        "username": "张三",
        "email": "zhangsan@example.com",
        "phone": "138****1234",
        "avatar": "/static/uploads/avatar1.jpg",
        "bio": "全栈开发工程师",
        "location": "北京",
        "website": "https://example.com",
        "github": "https://github.com/zhangsan",
        "status": "active",
        "role": "user",
        "stats": {
                "article_count": 15,
                "question_count": 8,
                "comment_count": 50,
                "favorite_count": 30,
                "follower_count": 120,
                "following_count": 30,
                "like_received": 800,
                "like_given": 300,
                "view_count": 10000,
            },
        "created_at": "2023-06-01 08:00:00",
        "last_login_time": "2024-01-15 10:30:00",
        "login_ip": "192.168.1.100",
        "device_info": "Chrome/Windows",
        "is_verified": true,
        "ban_reason": null,
        "ban_expire_time": null
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

---

### 3. 封禁/解封用户（管理端）
- **路径**: `/api/admin/user/ban`
- **方法**: `POST`
- **函数名**: `toggle_user_ban`
- **OpenAPI摘要**: 封禁或解封用户账号

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| user_id | int | yes | 用户ID | Body (JSON) |
| action | string | yes | 操作：ban/unban | Body (JSON) |
| reason | string | yes | 封禁原因（封禁时必填） | Body (JSON) |
| duration | int | no | 封禁时长（天），0表示永久，默认7 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "user_id": 1,
    "action": "ban",
    "reason": "发布违规内容",
    "duration": 7
}
```

#### 响应示例（封禁）
```json
{
    "code": 200,
    "msg": "已封禁该用户",
    "data": {
        "user_id": 1,
        "status": "banned",
        "ban_reason": "发布违规文章",
        "ban_expire_time": "2024-01-22 10:30:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "封禁原因不能为空"
}
```

---

### 4. 删除用户（管理端）
- **路径**: `/api/admin/user/<user_id>`
- **方法**: `DELETE`
- **函数名**: `delete_user`
- **OpenAPI摘要**: 删除用户账号（硬删除）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| user_id | int | 用户ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| reason | string | no | 删除原因 | Query |

#### 请求示例
```
DELETE /api/admin/user/1?admin_id=1&reason=用户请求注销账号
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

---

### 5. 编辑用户信息（管理端）
- **路径**: `/api/admin/user`
- **方法**: `PUT`
- **函数名**: `edit_user_info`
- **OpenAPI摘要**: 管理员编辑用户基本信息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| user_id | int | yes | 用户ID | Body (JSON) |
| username | string | no | 用户名 | Body (JSON) |
| email | string | no | 邮箱 | Body (JSON) |
| role | string | no | 角色：user/admin | Body (JSON) |
| bio | string | no | 个人简介 | Body (JSON) |
| is_verified | bool | no | 是否认证用户 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "user_id": 1,
    "username": "张三（认证）",
    "email": "newemail@example.com",
    "role": "user",
    "bio": "更新后的个人简介",
    "is_verified": true
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "用户不存在"
}
```

---

### 6. 重置用户密码（管理端）
- **路径**: `/api/admin/user/reset-password`
- **方法**: `POST`
- **函数名**: `reset_user_password`
- **OpenAPI摘要**: 重置指定用户的密码

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| user_id | int | yes | 用户ID | Body (JSON) |
| new_password | string | yes | 新密码（6位以上） | Body (JSON) |
| notify_user | bool | no | 是否通知用户，默认true | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "user_id": 1,
    "new_password": "newpass123",
    "notify_user": true
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "新密码不能少于6位"
}
```

---

### 7. 批量操作用户（管理端）
- **路径**: `/api/admin/user/batch-action`
- **方法**: `POST`
- **函数名**: `batch_action_users`
- **OpenAPI摘要**: 批量操作多个用户

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 用户ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作类型：ban/unban/delete/approve/unapprove | Body (JSON) |
| reason | string | no | 操作原因 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [5, 6, 7],
    "action": "ban",
    "reason": "批量封禁违规用户"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要操作的用户"
}
```

---

### 8. 导出用户数据（管理端）
- **路径**: `/api/admin/user/export`
- **方法**: `POST`
- **函数名**: `export_users`
- **OpenAPI摘要**: 导出用户数据为Excel/CSV文件

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| format | string | no | 导出格式：excel/csv，默认excel | Body (JSON) |
| filters | object | no | 筛选条件（与list接口相同） | Body (JSON) |
| fields | array | no | 要导出的字段列表 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "format": "excel",
    "filters": {"status": "active"},
    "fields": ["user_id", "username", "email", "created_at"]
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "导出成功",
    "data": {
        "filename": "users.xlsx",
        "file_url": "/static/exports/users.xlsx"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "导出格式不支持"
}
```

---

### 9. 获取用户统计概览（管理端）
- **路径**: `/api/admin/user/stats/overview`
- **方法**: `GET`
- **函数名**: `get_user_stats_overview`
- **OpenAPI摘要**: 获取用户统计数据概览（用于仪表盘）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：today/yesterday/week/month/year/all，默认month | Query |

#### 请求示例
```
GET /api/admin/user/stats/overview?admin_id=1&period=month
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "total_users": 1520,
        "new_users_today": 15,
        "new_users_week": 105,
        "new_users_month": 420,
        "active_users": 380,
        "banned_users": 12,
        "verified_users": 85,
        "growth_rate": 12.5,
        "trend_data": [
            {"date": "2024-01-01", "count": 12},
            {"date": "2024-01-02", "count": 18},
            {"date": "2024-01-03", "count": 15}
        ]
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 403,
    "msg": "权限不足"
}
```
