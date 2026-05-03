# 评论路由接口文档

## 文件路径
`router/app_comment_router.py`

## 蓝图配置
- **蓝图名称**: `comment`
- **URL前缀**: `/api/comment`

## 接口列表

### 1. 获取评论列表（APP端）
- **路径**: `/api/comment/list/<post_id>`
- **方法**: `GET`
- **函数名**: `get_comment_list`
- **OpenAPI摘要**: 获取文章/问题的评论列表

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章/问题ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID（用于计算is_liked） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| sort | string | no | 排序：time/hot，默认time | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 评论数据 |
| data.list | array | 评论列表 |
| data.total | int | 总数 |
| data.list[].comment_id | int | 评论ID |
| data.list[].user | object | 评论者信息 |
| data.list[].content | string | 评论内容 |
| data.list[].parent_id | int | 父评论ID（回复时） |
| data.list[].reply_to | object | 被回复者信息（动态查询父评论用户） |
| data.list[].like_count | int | 点赞数 |
| data.list[].is_liked | bool | 当前用户是否点赞（动态查询likes表） |
| data.list[].created_at | datetime | 创建时间 |
| data.list[].replies | array | 子回复列表（仅一级评论，动态查询parent_id匹配的子评论） |

> 注：评论仅支持1层嵌套，不允许多层回复。reply_to通过parent_id关联查询父评论的user信息。

#### 请求示例
```
GET /api/comment/list/100?user_id=1&page=1&page_size=20&sort=time
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 2. 发布评论（APP端）
- **路径**: `/api/comment`
- **方法**: `POST`
- **函数名**: `create_comment`
- **OpenAPI摘要**: 发布评论或回复

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| post_id | int | yes | 文章/问题ID | Body (JSON) |
| content | string | yes | 评论内容（最多1000字） | Body (JSON) |
| parent_id | int | no | 父评论ID（回复评论时传入） | Body (JSON) |

#### 请求示例
```json
{
    "user_id": 1,
    "post_id": 100,
    "content": "这篇文章写得太好了，感谢分享！",
    "parent_id": null
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 创建的评论信息 |
| data.comment_id | int | 评论ID |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "评论内容不能为空"
}
```

---

### 3. 删除评论（APP端）
- **路径**: `/api/comment/<comment_id>`
- **方法**: `DELETE`
- **函数名**: `delete_comment`
- **OpenAPI摘要**: 删除自己的评论

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| comment_id | int | 评论ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID（用于校验评论作者权限） | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
DELETE /api/comment/1?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 403,
    "msg": "无权删除此评论"
}
```

---

### 4. 点赞/取消点赞评论（APP端）
- **路径**: `/api/comment/like`
- **方法**: `POST`
- **函数名**: `toggle_comment_like`
- **OpenAPI摘要**: 点赞或取消点赞评论

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| comment_id | int | yes | 评论ID | Body (JSON) |

#### 请求示例
```
POST /api/comment/like
Content-Type: application/json

{
    "user_id": 1,
    "comment_id": 1
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 操作结果 |
| data.is_liked | bool | 是否已点赞 |
| data.like_count | int | 当前点赞数 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```
