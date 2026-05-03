# 收藏/关注路由接口文档

## 文件路径
`router/app_favorite_router.py`

## 蓝图配置
- **蓝图名称**: `favorite`
- **URL前缀**: `/api/favorite`

## 接口列表

### 1. 获取我的收藏列表（APP端）
- **路径**: `/api/favorite/list`
- **方法**: `GET`
- **函数名**: `get_my_favorites`
- **OpenAPI摘要**: 获取当前用户收藏的文章列表（UI图11）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| type | string | no | 类型筛选：article/question/all，默认all | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| sort | string | no | 排序：time/title，默认time | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 收藏列表数据 |
| data.list | array | 收藏列表 |
| data.total | int | 总数 |
| data.list[].post_id | int | 文章/问题ID |
| data.list[].post | object | 收藏的文章/问题信息 |
| data.list[].post.post_id | int | 文章/问题ID |
| data.list[].post.title | string | 标题 |
| data.list[].post.type | string | 类型：article/question |
| data.list[].post.summary | string | 摘要 |
| data.list[].post.cover_image | object | 封面图片 |
| data.list[].created_at | datetime | 收藏时间 |

#### 请求示例
```
GET /api/favorite/list?user_id=1&type=all&page=1&page_size=20&sort=time
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 2. 批量取消收藏（APP端）
- **路径**: `/api/favorite/batch-delete`
- **方法**: `POST`
- **函数名**: `batch_remove_favorites`
- **OpenAPI摘要**: 批量取消收藏

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| ids | array | yes | 文章/问题ID列表，如[1,2,3] | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 操作结果 |
| data.deleted_count | int | 成功取消数量 |

#### 请求示例
```json
{
    "user_id": 1,
    "ids": [1, 2, 3]
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要取消的收藏"
}
```

---

### 3. 检查是否已收藏（APP端）
- **路径**: `/api/favorite/check/<post_id>`
- **方法**: `GET`
- **函数名**: `check_is_favorited`
- **OpenAPI摘要**: 检查当前用户是否已收藏某篇文章/问题

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章/问题ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 结果 |
| data.is_favorited | bool | 是否已收藏 |

#### 请求示例
```
GET /api/favorite/check/100?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 4. 收藏/取消收藏（APP端）
- **路径**: `/api/favorite/toggle`
- **方法**: `POST`
- **函数名**: `toggle_favorite`
- **OpenAPI摘要**: 收藏或取消收藏

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| post_id | int | yes | 文章/问题ID | Body (JSON) |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 操作结果 |
| data.is_favorited | bool | 是否已收藏 |
| data.favorite_count | int | 当前收藏数（动态查询favorites表统计） |

#### 请求示例
```
POST /api/favorite/toggle
Content-Type: application/json

{
    "user_id": 1,
    "post_id": 100
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```
