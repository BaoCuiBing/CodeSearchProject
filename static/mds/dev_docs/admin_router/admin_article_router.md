# 管理后台文章管理接口文档

## 文件路径
`router/admin_article_router.py`

## 蓝图配置
- **蓝图名称**: `admin_article`
- **URL前缀**: `/api/admin/article`

## 接口列表

### 1. 获取文章列表（管理端）
- **路径**: `/api/admin/article/list`
- **方法**: `GET`
- **函数名**: `get_content_list`
- **OpenAPI摘要**: 获取文章/问题列表（UI图25）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| type | string | no | 类型筛选：article/question/all，默认all | Query |
| keyword | string | no | 搜索关键词（标题/内容/作者） | Query |
| status | string | no | 状态：published/draft/hidden/all，默认published | Query |
| author_id | int | no | 作者ID筛选 | Query |
| tag_id | int | no | 标签ID筛选 | Query |
| category_id | int | no | 分类ID筛选 | Query |
| sort | string | no | 排序：created_time/updated_time/view_count/like_count/comment_count，默认created_time | Query |
| order | string | no | 排序方向：asc/desc，默认desc | Query |
| date_start | string | no | 发布时间开始（YYYY-MM-DD） | Query |
| date_end | string | no | 发布时间结束（YYYY-MM-DD） | Query |
| is_top | string | no | 是否置顶：yes/no/all，默认all | Query |

#### 请求示例
```
GET /api/admin/article/list?admin_id=1&page=1&page_size=20&type=all&status=published&sort=created_time&order=desc
```

> 注：cover_image字段在数据库中存储为TEXT类型（JSON字符串格式），响应时解析为对象返回
#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "post_id": 1,
                "type": "article",
                "title": "Python入门教程",
                "summary": "这是一篇关于Python基础知识的详细教程...",
                "cover_image": {"imgs":["/static/uploads/cover1.jpg"]},
                "author": {
                    "user_id": 1,
                    "username": "张三",
                    "avatar": "/static/uploads/avatar1.jpg"
                },
                "category": {"category_id": 1, "name": "编程语言"},
                "tags": [{"tag_id": 1, "name": "Python"}, {"tag_id": 2, "name": "入门"}],
                "status": "published",
                "is_top": false,
                "view_count": 5000,
                "like_count": 200,
                "comment_count": 50,
                "created_at": "2024-01-10 14:30:00",
                "updated_at": "2024-01-12 09:00:00"
            }
        ],
        "total": 3200,
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

### 2. 获取文章详情（管理端）
- **路径**: `/api/admin/article/<post_id>`
- **方法**: `GET`
- **函数名**: `get_content_detail`
- **OpenAPI摘要**: 获取文章/问题详情（含完整内容和统计数据）（UI图26）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |

#### 请求示例
```
GET /api/admin/article/1?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "post_id": 1,
        "type": "article",
        "title": "Python入门教程",
        "content": "# Python入门\n\nPython是一门优秀的编程语言...",
        "summary": "这是一篇关于Python基础知识的详细教程...",
        "cover_image": {"imgs":["/static/uploads/cover1.jpg"]},
        "author": {
            "user_id": 1,
            "username": "张三",
            "avatar": "/static/uploads/avatar1.jpg",
            "email": "zhangsan@example.com"
        },
        "category": {"category_id": 1, "name": "编程语言"},
        "tags": [{"tag_id": 1, "name": "Python"}, {"tag_id": 2, "name": "入门"}],
        "status": "published",
        "is_top": false,
        "stats": {
            "view_count": 5000,
            "like_count": 200,
            "comment_count": 50
        },
        "created_at": "2024-01-10 14:30:00",
        "updated_at": "2024-01-12 09:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 3. 编辑文章（管理端）
- **路径**: `/api/admin/article`
- **方法**: `PUT`
- **函数名**: `edit_content`
- **OpenAPI摘要**: 管理员编辑文章/问题内容

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| post_id | int | yes | 文章ID | Body (JSON) |
| title | string | no | 标题 | Body (JSON) |
| content | string | no | 内容（Markdown） | Body (JSON) |
| summary | string | no | 摘要 | Body (JSON) |
| cover_image | object | no | 封面图片（JSON格式:{"imgs":["url1","url2"]}） | Body (JSON) |
| category_id | int | no | 分类ID | Body (JSON) |
| tags | array | no | 标签ID列表 | Body (JSON) |
| status | string | no | 状态：published/draft/hidden | Body (JSON) |
| is_top | bool | no | 是否置顶 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "post_id": 1,
    "title": "Python入门教程（修订版）",
    "content": "# Python入门\n\n更新后的内容...",
    "summary": "修订后的摘要",
    "cover_image": {"imgs":["/static/uploads/cover1.jpg"]},
    "category_id": 1,
    "tags": [1, 2],
    "status": "published",
    "is_top": false
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 4. 删除文章（管理端）
- **路径**: `/api/admin/article/<post_id>`
- **方法**: `DELETE`
- **函数名**: `delete_content`
- **OpenAPI摘要**: 删除文章/问题（硬删除）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| reason | string | no | 删除原因 | Query |
| notify_author | bool | no | 是否通知作者，默认true | Query |

#### 请求示例
```
DELETE /api/admin/article/1?admin_id=1&reason=包含违规内容&notify_author=true
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 5. 批量操作文章（管理端）
- **路径**: `/api/admin/article/batch-action`
- **方法**: `POST`
- **函数名**: `batch_action_content`
- **OpenAPI摘要**: 批量操作多篇文章

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 文章ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作类型：publish/unpublish/delete/top/untop | Body (JSON) |
| reason | string | no | 操作原因 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [1, 2, 3],
    "action": "delete",
    "reason": "批量清理违规内容"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要操作的文章"
}
```

---

### 6. 设置置顶/取消置顶（管理端）
- **路径**: `/api/admin/article/top`
- **方法**: `POST`
- **函数名**: `toggle_content_top`
- **OpenAPI摘要**: 设置或取消文章置顶

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| post_id | int | yes | 文章ID | Body (JSON) |
| is_top | bool | yes | 是否置顶 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "post_id": 1,
    "is_top": true
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 7. 获取文章统计（管理端）
- **路径**: `/api/admin/article/stats/overview`
- **方法**: `GET`
- **函数名**: `get_content_stats_overview`
- **OpenAPI摘要**: 获取文章统计概览数据（用于仪表盘）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：today/yesterday/week/month/year/all，默认month | Query |

#### 请求示例
```
GET /api/admin/article/stats/overview?admin_id=1&period=month
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "total_articles": 2500,
        "total_questions": 700,
        "published_today": 25,
        "published_week": 180,
        "draft_count": 120,
        "hidden_count": 50,
        "total_views": 500000,
        "total_likes": 25000,
        "total_comments": 8000,
        "avg_views_per_article": 200,
        "top_categories": [
            {"name": "编程语言", "count": 800},
            {"name": "Web开发", "count": 600}
        ],
        "trend_data": [
            {"date": "2024-01-01", "articles": 20, "questions": 8},
            {"date": "2024-01-02", "articles": 25, "questions": 10}
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

### 8. 导出文章数据（管理端）
- **路径**: `/api/admin/article/export`
- **方法**: `POST`
- **函数名**: `export_contents`
- **OpenAPI摘要**: 导出文章数据为Excel/CSV文件

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
    "filters": {"status": "published", "type": "article"},
    "fields": ["post_id", "title", "author", "view_count", "created_at"]
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "导出成功",
    "data": {
        "filename": "posts.xlsx",
        "file_url": "/static/exports/posts.xlsx"
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
