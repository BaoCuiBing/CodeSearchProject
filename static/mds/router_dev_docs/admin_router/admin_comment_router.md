# 管理后台评论管理接口文档

## 文件路径
`router/admin_comment_router.py`

## 蓝图配置
- **蓝图名称**: `admin_comment`
- **URL前缀**: `/api/admin/comment`

## 接口列表

### 1. 获取评论列表（管理端）
- **路径**: `/api/admin/comment/list`
- **方法**: `GET`
- **函数名**: `get_comment_list`
- **OpenAPI摘要**: 获取所有评论列表（UI图28）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词（评论内容/用户名） | Query |
| post_id | int | no | 关联文章ID | Query |
| author_id | int | no | 评论者用户ID | Query |
| status | string | no | 状态：normal/hidden/all，默认all | Query |
| sort | string | no | 排序：created_time/like_count，默认created_time | Query |
| order | string | no | 排序方向：asc/desc，默认desc | Query |
| date_start | string | no | 评论时间开始（YYYY-MM-DD） | Query |
| date_end | string | no | 评论时间结束（YYYY-MM-DD） | Query |

#### 请求示例
```
GET /api/admin/comment/list?admin_id=1&page=1&page_size=20&status=all&sort=created_time&order=desc
```

> 注：reply_to_user根据parent_id关联comments表查询父评论作者信息

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
                "comment_id": 1,
                "post_id": 100,
                "author": {
                    "user_id": 5,
                    "username": "李四",
                    "avatar": "/static/uploads/avatar5.jpg"
                },
                "parent_id": null,
                "reply_to_user": null,
                "content": "这篇文章写得太好了，感谢分享！",
                "like_count": 10,
                "status": "normal",
                "created_at": "2024-01-11 16:20:00",
                "updated_at": "2024-01-11 16:20:00"
            }
        ],
        "total": 8500,
        "page": 1,
        "page_size": 20
    }
}
```

---

### 2. 获取评论详情（管理端）
- **路径**: `/api/admin/comment/<comment_id>`
- **方法**: `GET`
- **函数名**: `get_comment_detail`
- **OpenAPI摘要**: 获取评论详情（含回复列表）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| comment_id | int | 评论ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| include_replies | bool | no | 是否包含回复列表，默认true | Query |
| reply_page | int | no | 回复页码，默认1 | Query |
| reply_page_size | int | no | 回复每页数量，默认20 | Query |

#### 请求示例
```
GET /api/admin/comment/1?admin_id=1&include_replies=true&reply_page=1&reply_page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "评论不存在"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "comment_id": 1,
        "post_id": 100,
        "author": {
            "user_id": 5,
            "username": "李四",
            "avatar": "/static/uploads/avatar5.jpg"
        },
        "parent_id": null,
        "content": "这篇文章写得太好了，感谢分享！",
        "like_count": 10,
        "status": "normal",
        "created_at": "2024-01-11 16:20:00",
        "replies": {
            "list": [
                {
                    "comment_id": 2,
                    "author": {"user_id": 6, "username": "王五"},
                    "content": "同意楼上观点",
                    "like_count": 2,
                    "created_at": "2024-01-11 17:00:00"
                }
            ],
            "total": 3
        }
    }
}
```

---

### 3. 删除评论（管理端）
- **路径**: `/api/admin/comment/<comment_id>`
- **方法**: `DELETE`
- **函数名**: `delete_comment`
- **OpenAPI摘要**: 删除评论（支持删除所有回复）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| comment_id | int | 评论ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| delete_replies | bool | no | 是否同时删除所有回复，默认true | Query |
| reason | string | no | 删除原因 | Query |
| notify_author | bool | no | 是否通知作者，默认false | Query |

#### 请求示例
```
DELETE /api/admin/comment/1?admin_id=1&delete_replies=true&reason=包含不当言论&notify_author=true
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "删除成功",
    "data": {
        "deleted_count": 4,
        "comment_id": 1
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "评论不存在"
}
```

---

### 4. 隐藏/显示评论（管理端）
- **路径**: `/api/admin/comment/visibility`
- **方法**: `PUT`
- **函数名**: `toggle_comment_visibility`
- **OpenAPI摘要**: 隐藏或显示评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| comment_id | int | yes | 评论ID | Body (JSON) |
| is_hidden | bool | yes | 是否隐藏 | Body (JSON) |
| reason | string | no | 隐藏原因 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "comment_id": 1,
    "is_hidden": true,
    "reason": "包含广告信息"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "操作成功",
    "data": {
        "comment_id": 1,
        "is_hidden": true
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "评论不存在"
}
```

---

### 5. 回复评论（管理端）
- **路径**: `/api/admin/comment/reply`
- **方法**: `POST`
- **函数名**: `reply_comment`
- **OpenAPI摘要**: 管理员回复评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| comment_id | int | yes | 被回复的评论ID | Body (JSON) |
| content | string | yes | 回复内容 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "comment_id": 1,
    "content": "感谢您的反馈，我们会尽快处理。"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "回复成功",
    "data": {
        "reply_id": 10
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "评论ID和回复内容不能为空"
}
```

---

### 6. 批量操作评论（管理端）
- **路径**: `/api/admin/comment/batch-action`
- **方法**: `POST`
- **函数名**: `batch_action_comments`
- **OpenAPI摘要**: 批量操作多条评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 评论ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作类型：delete/hide/show | Body (JSON) |
| reason | string | no | 操作原因 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [1, 2, 3],
    "action": "delete",
    "reason": "批量清理违规评论"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "批量操作成功",
    "data": {
        "processed_count": 3,
        "action": "delete"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要操作的评论"
}
```

---

### 7. 获取评论统计概览（管理端）
- **路径**: `/api/admin/comment/stats/overview`
- **方法**: `GET`
- **函数名**: `get_comment_stats_overview`
- **OpenAPI摘要**: 获取评论统计概览数据

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：today/yesterday/week/month/year/all，默认month | Query |

#### 请求示例
```
GET /api/admin/comment/stats/overview?admin_id=1&period=month
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "total_comments": 8500,
        "comments_today": 85,
        "comments_week": 600,
        "comments_month": 2500,
        "hidden_comments": 45,
        "avg_comments_per_article": 2.7,
        "top_commenters": [
            {"user_id": 5, "username": "李四", "comment_count": 300}
        ],
        "trend_data": [
            {"date": "2024-01-01", "count": 70},
            {"date": "2024-01-02", "count": 90}
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

### 8. 导出评论数据（管理端）
- **路径**: `/api/admin/comment/export`
- **方法**: `POST`
- **函数名**: `export_comments`
- **OpenAPI摘要**: 导出评论数据为Excel/CSV文件

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| format | string | no | 导出格式：excel/csv，默认excel | Body (JSON) |
| filters | object | no | 筛选条件 | Body (JSON) |
| fields | array | no | 要导出的字段 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "format": "excel",
    "filters": {"status": "normal"},
    "fields": ["comment_id", "content", "author", "created_at"]
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "导出成功",
    "data": {
        "filename": "comments.xlsx",
        "file_url": "/static/exports/comments.xlsx"
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

### 9. 批量删除评论（管理端）
- **路径**: `/api/admin/comment/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_delete_comments`
- **OpenAPI摘要**: 批量删除评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 评论ID列表，如[1,2,3] | Body (JSON) |

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
    "msg": "请选择要删除的评论"
}
```
