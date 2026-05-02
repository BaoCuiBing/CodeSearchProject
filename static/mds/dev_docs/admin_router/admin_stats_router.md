# 管理后台数据统计接口文档

## 文件路径
`router/admin_stats_router.py`

## 蓝图配置
- **蓝图名称**: `admin_stats`
- **URL前缀**: `/api/admin/stats`

## 接口列表

### 1. 获取仪表盘概览数据（管理端）
- **路径**: `/api/admin/stats/dashboard`
- **方法**: `GET`
- **函数名**: `get_dashboard_overview`
- **OpenAPI摘要**: 获取管理后台首页仪表盘数据（UI图23）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：today/yesterday/week/month/year/custom，默认week | Query |
| date_start | string | no | 自定义开始时间（YYYY-MM-DD） | Query |
| date_end | string | no | 自定义结束时间（YYYY-MM-DD） | Query |

#### 请求示例
```
GET /api/admin/stats/dashboard?period=week&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "summary": {
            "total_users": 1520,
            "new_users": 105,
            "total_articles": 2500,
            "new_articles": 180,
            "total_questions": 700,
            "new_questions": 65,
            "total_comments": 8500,
            "new_comments": 600,
            "total_views": 500000,
            "new_views": 35000,
            "active_users_today": 380,
            "reported_items": 18
        },
        "growth_rates": {
            "user_growth": 12.5,
            "article_growth": 8.3,
            "question_growth": -2.1,
            "comment_growth": 15.7,
            "view_growth": 22.4
        },
        "trend_charts": {
            "users_trend": [
                {"date": "2024-01-08", "value": 12},
                {"date": "2024-01-09", "value": 15},
                {"date": "2024-01-10", "value": 18}
            ],
            "articles_trend": [
                {"date": "2024-01-08", "value": 25},
                {"date": "2024-01-09", "value": 28},
                {"date": "2024-01-10", "value": 30}
            ],
            "views_trend": [
                {"date": "2024-01-08", "value": 5000},
                {"date": "2024-01-09", "value": 5500},
                {"date": "2024-01-10", "value": 6000}
            ]
        },
        "quick_actions": [
            {"type": "reported", "count": 18, "url": "/admin/messages/reports"},
            {"type": "banned_users", "count": 12, "url": "/admin/users?status=banned"}
        ],
        "recent_activities": [
            {"time": "5分钟前", "user": "张三", "action": "发布了文章", "target": "Python高级技巧", "type": "article"},
            {"time": "10分钟前", "user": "李四", "action": "注册了账号", "target": null, "type": "user"}
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

### 2. 获取用户统计分析（管理端）
- **路径**: `/api/admin/stats/users`
- **方法**: `GET`
- **函数名**: `get_user_statistics`
- **OpenAPI摘要**: 获取详细的用户统计数据（UI图31）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：day/week/month/year/all，默认month | Query |

#### 请求示例
```
GET /api/admin/stats/users?period=month&admin_id=1
```

> 注：所有统计字段均为动态计算

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "overview": {
            "total_users": 1520,
            "active_users": 380,
            "new_users_month": 420,
            "verified_users": 85,
            "banned_users": 12,
            "churn_rate": 3.2,
            "retention_rate": 68.5
        },
        "registration_trend": [
            {"date": "2024-01-01", "count": 12, "cumulative": 1100},
            {"date": "2024-01-02", "count": 18, "cumulative": 1118}
        ],
        "user_distribution": {
            "by_role": [
                {"name": "普通用户", "count": 1495, "percentage": 98.4},
                {"name": "管理员", "count": 25, "percentage": 1.6}
            ],
            "by_registration_period": [
                {"name": "近一个月", "count": 420},
                {"name": "1-3个月", "count": 380},
                {"name": "3-6个月", "count": 320},
                {"name": "6个月以上", "count": 400}
            ],
            "by_activity_level": [
                {"name": "高度活跃", "count": 150},
                {"name": "活跃", "count": 230},
                {"name": "一般", "count": 400},
                {"name": "不活跃", "count": 740}
            ]
        },
        "top_contributors": [
            {"rank": 1, "user_id": 1, "username": "张三", "articles": 50, "comments": 200, "likes_received": 1500},
            {"rank": 2, "user_id": 5, "username": "李四", "articles": 45, "comments": 180, "likes_received": 1200}
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

### 3. 获取文章统计分析（管理端）
- **路径**: `/api/admin/stats/content`
- **方法**: `GET`
- **函数名**: `get_content_statistics`
- **OpenAPI摘要**: 获取详细的文章统计数据

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：day/week/month/year/all，默认month | Query |

#### 请求示例
```
GET /api/admin/stats/content?period=month&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "overview": {
            "total_articles": 2500,
            "total_questions": 700,
            "total_comments": 8500,
            "published_today": 25,
            "published_week": 180,
            "avg_views_per_article": 200,
            "avg_comments_per_article": 3.4,
            "content_growth_rate": 8.3
        },
        "publishing_trend": {
            "articles": [
                {"date": "2024-01-01", "count": 20},
                {"date": "2024-01-02", "count": 25}
            ],
            "questions": [
                {"date": "2024-01-01", "count": 8},
                {"date": "2024-01-02", "count": 10}
            ],
            "comments": [
                {"date": "2024-01-01", "count": 70},
                {"date": "2024-01-02", "count": 90}
            ]
        },
        "category_distribution": [
            {"name": "编程语言", "article_count": 800, "question_count": 200, "percentage": 32.0},
            {"name": "Web开发", "article_count": 600, "question_count": 180, "percentage": 24.0},
            {"name": "数据库", "article_count": 400, "question_count": 120, "percentage": 16.0}
        ],
        "tag_distribution": [
            {"name": "Python", "count": 500, "percentage": 20.0},
            {"name": "JavaScript", "count": 400, "percentage": 16.0},
            {"name": "Java", "count": 300, "percentage": 12.0}
        ],
        "popular_content": [
            {"post_id": 1, "title": "Python入门教程", "views": 5000, "likes": 200, "comments": 50},
            {"post_id": 2, "title": "Vue3实战指南", "views": 4500, "likes": 180, "comments": 42}
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

### 4. 获取搜索关键词统计（管理端）
- **路径**: `/api/admin/stats/search-keywords`
- **方法**: `GET`
- **函数名**: `get_search_keyword_stats`
- **OpenAPI摘要**: 获取热门搜索词和搜索趋势

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| period | string | no | 统计周期：day/week/month，默认week | Query |
| limit | int | no | 返回数量限制，默认50 | Query |

#### 请求示例
```
GET /api/admin/stats/search-keywords?period=week&limit=50&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "top_keywords": [
            {"keyword": "Python入门", "search_count": 5000, "trend": "up", "growth_rate": 15.2},
            {"keyword": "Vue3教程", "search_count": 3500, "trend": "up", "growth_rate": 22.5},
            {"keyword": "MySQL优化", "search_count": 2800, "trend": "stable", "growth_rate": 2.1}
        ],
        "search_volume_trend": [
            {"date": "2024-01-08", "total_searches": 2000, "unique_keywords": 500},
            {"date": "2024-01-09", "total_searches": 2200, "unique_keywords": 550}
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

### 5. 导出统计报告（管理端）
- **路径**: `/api/admin/stats/export-report`
- **方法**: `POST`
- **函数名**: `export_statistics_report`
- **OpenAPI摘要**: 导出完整的统计报告为PDF或Excel文件

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| report_type | string | yes | 报告类型：comprehensive/user/content/search | Body (JSON) |
| format | string | no | 导出格式：pdf/excel，默认pdf | Body (JSON) |
| period | string | no | 统计周期，默认month | Body (JSON) |
| date_start | string | no | 开始日期 | Body (JSON) |
| date_end | string | no | 结束日期 | Body (JSON) |
| include_charts | bool | 是否包含图表，默认true | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "report_type": "comprehensive",
    "format": "excel",
    "period": "month",
    "date_start": "2024-01-01",
    "date_end": "2024-01-31",
    "include_charts": true
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "导出成功",
    "data": {
        "filename": "report_20240115.xlsx",
        "file_url": "/static/exports/report_20240115.xlsx"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "报告类型不支持"
}
```

---

### 6. 获取对比分析数据（管理端）
- **路径**: `/api/admin/stats/compare`
- **方法**: `GET`
- **函数名**: `get_comparison_data`
- **OpenAPI摘要**: 获取不同时间段的数据对比分析

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| metric | string | yes | 指标类型：users/articles/comments/views | Query |
| period1_start | string | yes | 对比时间段1开始（YYYY-MM-DD） | Query |
| period1_end | string | yes | 对比时间段1结束（YYYY-MM-DD） | Query |
| period2_start | string | yes | 对比时间段2开始（YYYY-MM-DD） | Query |
| period2_end | string | yes | 对比时间段2结束（YYYY-MM-DD） | Query |

#### 请求示例
```
GET /api/admin/stats/compare?metric=users&period1_start=2024-01-01&period1_end=2024-01-07&period2_start=2024-01-08&period2_end=2024-01-14&admin_id=1
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "metric": "users",
        "period1": {
            "label": "2024年1月第1周",
            "start": "2024-01-01",
            "end": "2024-01-07",
            "value": 280,
            "daily_avg": 40
        },
        "period2": {
            "label": "2024年1月第2周",
            "start": "2024-01-08",
            "end": "2024-01-14",
            "value": 350,
            "daily_avg": 50
        },
        "change": {
            "absolute": 70,
            "percentage": 25.0,
            "trend": "up"
        }
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "指标类型不支持"
}
```
