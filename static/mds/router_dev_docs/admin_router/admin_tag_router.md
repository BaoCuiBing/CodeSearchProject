# 管理后台标签管理接口文档

## 文件路径
`router/admin_tag_router.py`

## 蓝图配置
- **蓝图名称**: `admin_tag`
- **URL前缀**: `/api/admin/tag`

## 接口列表

### 1. 获取标签列表（管理端）
- **路径**: `/api/admin/tag/list`
- **方法**: `GET`
- **函数名**: `get_tag_list`
- **OpenAPI摘要**: 获取所有标签列表（UI图27）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词（标签名称/描述） | Query |
| category_id | int | no | 所属分类ID筛选 | Query |
| sort | string | no | 排序：name/count/article_count/created_time，默认name | Query |
| order | string | no | 排序方向：asc/desc，默认asc | Query |
| status | string | no | 状态：active/disabled/all，默认all | Query |

#### 请求示例
```
GET /api/admin/tag/list?page=1&page_size=20&sort=name&order=asc&admin_id=1
```

> 注：post_count为tags表字段，question_count为动态统计字段，从posts表按type='question'且关联post_tags表统计
#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "tag_id": 1,
                "name": "Python",
                "slug": "python",
                "description": "Python编程语言相关文章",
                "icon": "/static/uploads/tags/python.png",
                "color": "#3776ab",
                "category_id": 1,
                "category_name": "编程语言",
                "post_count": 500,
                "question_count": 200,
                "is_hot": true,
                "is_recommend": true,
                "status": "active",
                "sort_order": 1,
                "created_at": "2023-01-01 00:00:00",
                "updated_at": "2024-01-10 10:00:00"
            }
        ],
        "total": 120,
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

### 2. 创建标签（管理端）
- **路径**: `/api/admin/tag`
- **方法**: `POST`
- **函数名**: `create_tag`
- **OpenAPI摘要**: 创建新标签

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| name | string | yes | 标签名称（2-20字符） | Body (JSON) |
| description | string | no | 标签描述（最多100字） | Body (JSON) |
| icon | string | no | 标签图标URL | Body (JSON) |
| color | string | no | 标签颜色（十六进制） | Body (JSON) |
| category_id | int | no | 所属分类ID | Body (JSON) |
| is_recommend | bool | no | 是否推荐标签 | Body (JSON) |
| sort_order | int | no | 排序权重，默认0 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "name": "TypeScript",
    "description": "TypeScript编程语言相关",
    "icon": "/static/uploads/tags/typescript.png",
    "color": "#3178c6",
    "category_id": 1,
    "is_recommend": true,
    "sort_order": 5
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "标签名称已存在"
}
```

---

### 3. 编辑标签（管理端）
- **路径**: `/api/admin/tag`
- **方法**: `PUT`
- **函数名**: `edit_tag`
- **OpenAPI摘要**: 编辑标签信息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| tag_id | int | yes | 标签ID | Body (JSON) |
| name | string | no | 标签名称 | Body (JSON) |
| description | string | no | 标签描述 | Body (JSON) |
| icon | string | no | 标签图标URL | Body (JSON) |
| color | string | no | 标签颜色 | Body (JSON) |
| category_id | int | no | 所属分类ID | Body (JSON) |
| is_recommend | bool | no | 是否推荐 | Body (JSON) |
| is_hot | bool | no | 是否热门 | Body (JSON) |
| status | string | no | 状态：active/disabled | Body (JSON) |
| sort_order | int | no | 排序权重 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "tag_id": 1,
    "name": "TypeScript（更新）",
    "description": "TypeScript最新教程",
    "is_hot": true,
    "status": "active",
    "sort_order": 3
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "标签不存在"
}
```

---

### 4. 删除标签（管理端）
- **路径**: `/api/admin/tag/<tag_id>`
- **方法**: `DELETE`
- **函数名**: `delete_tag`
- **OpenAPI摘要**: 删除标签（需处理关联文章）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| tag_id | int | 标签ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| merge_to_id | int | yes | 合并到目标标签ID（有文章关联时必填） | Query |


#### 请求示例
```
DELETE /api/admin/tag/1?admin_id=1&merge_to_id=2
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "该标签下有文章，请先合并"
}
```

---

### 5. 批量操作标签（管理端）
- **路径**: `/api/admin/tag/batch-action`
- **方法**: `POST`
- **函数名**: `batch_action_tags`
- **OpenAPI摘要**: 批量操作多个标签

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 标签ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作类型：enable/disable/delete/recommend/unrecommend/set_hot/unset_hot | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [3, 4, 5],
    "action": "set_hot"
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要操作的标签"
}
```

---

### 6. 获取标签详情（管理端）
- **路径**: `/api/admin/tag/<tag_id>/detail`
- **方法**: `GET`
- **函数名**: `get_tag_detail`
- **OpenAPI摘要**: 获取标签详细信息及统计数据

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| tag_id | int | 标签ID |

#### 请求示例
```
GET /api/admin/tag/1/detail?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "tag_id": 1,
        "name": "Python",
        "slug": "python",
        "description": "Python编程语言相关文章",
        "icon": "/static/uploads/tags/python.png",
        "color": "#3776ab",
        "category_id": 1,
        "category_name": "编程语言",
        "status": "active",
        "stats": {
            "article_count": 500,
            "question_count": 200,
            "today_articles": 5,
            "week_articles": 35,
            "month_articles": 120,
            "total_views": 100000,
            "avg_views_per_article": 200
        },
        "related_tags": [
            {"tag_id": 2, "name": "Django", "relation_count": 80},
            {"tag_id": 3, "name": "Flask", "relation_count": 60}
        ],
        "top_authors": [
            {"user_id": 1, "username": "张三", "count": 50}
        ],
        "recent_articles": [
            {"post_id": 101, "title": "Python 3.12新特性", "created_at": "2024-01-15"}
        ],
        "trend_data": [
            {"date": "2024-01-01", "articles": 8},
            {"date": "2024-01-02", "articles": 12}
        ]
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "标签不存在"
}
```

---

### 7. 获取标签统计概览（管理端）
- **路径**: `/api/admin/tag/stats/overview`
- **方法**: `GET`
- **函数名**: `get_tag_stats_overview`
- **OpenAPI摘要**: 获取标签统计数据概览

#### 请求示例
```
GET /api/admin/tag/stats/overview?admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "total_tags": 120,
        "active_tags": 115,
        "disabled_tags": 5,
        "hot_tags": 20,
        "recommend_tags": 30,
        "tags_no_article": 15,
        "total_categories": 8,
        "top_categories": [
            {"name": "编程语言", "tag_count": 25, "article_count": 800},
            {"name": "Web开发", "tag_count": 20, "article_count": 600}
        ],
        "top_tags": [
            {"name": "Python", "article_count": 500},
            {"name": "JavaScript", "article_count": 400}
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

### 8. 合并标签（管理端）
- **路径**: `/api/admin/tag/merge`
- **方法**: `POST`
- **函数名**: `merge_tags`
- **OpenAPI摘要**: 将多个标签合并到一个目标标签

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| source_ids | array | yes | 要合并的源标签ID列表 | Body (JSON) |
| target_id | int | yes | 目标标签ID（保留） | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "source_ids": [3, 4],
    "target_id": 1
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "目标标签不存在"
}
```
