# 排行榜路由接口文档

## 文件路径
`router/app_ranking_router.py`

## 蓝图配置
- **蓝图名称**: `ranking`
- **URL前缀**: `/api/ranking`

## 接口列表

### 1. 获取排行榜列表（APP端）
- **路径**: `/api/ranking/list`
- **方法**: `GET`
- **函数名**: `get_ranking_list`
- **OpenAPI摘要**: 获取各类排行榜数据（UI图17）

> 注：排行榜均为实时计算。热榜hot_score基于多个维度排名（浏览量、点赞数、评论数、收藏数）的加权平均值算出。

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| type | string | yes | 排行榜类型：user_active/user_fans/article_hot/question_hot/contributor/tag_hot | Query |
| period | string | no | 时间周期：day/week/month/all，默认week | Query |
| limit | int | no | 返回数量限制，默认50 | Query |

#### 响应格式（用户活跃榜）
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "type": "user_active",
        "period": "week",
        "list": [
            {
                "rank": 1,
                "user_id": 1,
                "username": "张三",
                "avatar": "/static/uploads/avatar1.jpg",
                "score": 1500,
                "article_count": 20,
                "comment_count": 50,
                "like_count": 300
            }
        ],
        "total": 100,
        "my_rank": null
    }
}
```

#### 响应格式（文章热榜）
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "type": "article_hot",
        "period": "week",
        "list": [
            {
                "rank": 1,
                "post_id": 1,
                "title": "Python入门教程",
                "type": "article",
                "author": {"user_id": 1, "username": "张三"},
                "view_count": 5000,
                "like_count": 200,
                "comment_count": 50,
                "hot_score": 8500
            }
        ],
        "total": 100
    }
}
```

#### 请求示例
```
GET /api/ranking/list?type=article_hot&period=week&limit=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "排行榜类型不支持"
}
```

---

### 2. 获取我的排名（APP端）
- **路径**: `/api/ranking/my-rank`
- **方法**: `GET`
- **函数名**: `get_my_ranking`
- **OpenAPI摘要**: 获取当前用户在各榜单的排名

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| type | string | no | 榜单类型，不传则返回所有榜单排名 | Query |
| period | string | no | 时间周期，默认week | Query |

#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "user_active": {"rank": 15, "score": 800},
        "user_fans": {"rank": 8, "fans_count": 500},
        "contributor": {"rank": 20, "contribution_score": 600}
    }
}
```

#### 请求示例
```
GET /api/ranking/my-rank?user_id=1&type=user_active&period=week
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```
