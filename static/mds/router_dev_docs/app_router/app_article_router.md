# 文章/问题路由接口文档

## 文件路径
`router/app_article_router.py`

## 蓝图配置
- **蓝图名称**: `article`
- **URL前缀**: `/api/article`

## 接口列表

### 1. 发布文章/问题（APP端）
- **路径**: `/api/article`
- **方法**: `POST`
- **函数名**: `create_article`
- **OpenAPI摘要**: 发布新文章或问题

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 作者用户ID | Body (JSON) |
| type | string | yes | 类型：article/question | Body (JSON) |
| title | string | yes | 标题 | Body (JSON) |
| content | string | yes | 内容（支持Markdown） | Body (JSON) |
| summary | string | no | 摘要（不填则自动截取） | Body (JSON) |
| tags | array | no | 标签ID列表，如[1,2,3] | Body (JSON) |
| category_id | int | no | 分类ID | Body (JSON) |
| cover_image | object | no | 封面图片（JSON格式:{"imgs":["url1","url2"]}，url为上传后返回的地址） | Body (JSON) |

#### 请求示例
```json
{
    "user_id": 1,
    "type": "article",
    "title": "Python入门教程",
    "content": "# Python入门\n\nPython是一门优秀的编程语言...",
    "summary": "这是一篇关于Python基础知识的详细教程",
    "tags": [1, 2],
    "category_id": 1,
    "cover_image": {"imgs":["/static/uploads/cover1.jpg"]}
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 创建的文章/问题信息 |
| data.post_id | int | 文章/问题ID |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "标题不能为空"
}
```

---

### 2. 获取文章/问题详情（APP端）
- **路径**: `/api/article/<post_id>`
- **方法**: `GET`
- **函数名**: `get_article_detail`
- **OpenAPI摘要**: 获取文章或问题详情

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章/问题ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | no | 当前用户ID（用于计算is_liked/is_favorited，不传则返回false） | Query |

#### 请求示例
```
GET /api/article/1?user_id=1
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 文章详情数据 |
| data.post_id | int | ID |
| data.type | string | 类型：article/question |
| data.title | string | 标题 |
| data.content | string | 内容（Markdown） |
| data.summary | string | 摘要 |
| data.author | object | 作者信息 |
| data.tags | array | 标签列表 |
| data.category | object | 分类信息 |
| data.view_count | int | 浏览量 |
| data.like_count | int | 点赞数 |
| data.comment_count | int | 评论数 |
| data.favorite_count | int | 收藏数（动态查询favorites表统计） |
| data.created_at | datetime | 创建时间 |
| data.updated_at | datetime | 更新时间 |
| data.is_liked | bool | 当前用户是否点赞（动态查询likes表） |
| data.is_favorited | bool | 当前用户是否收藏（动态查询favorites表） |

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```

---

### 3. 编辑文章/问题（APP端）
- **路径**: `/api/article`
- **方法**: `PUT`
- **函数名**: `update_article`
- **OpenAPI摘要**: 编辑文章或问题

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| post_id | int | yes | 文章/问题ID | Body (JSON) |
| user_id | int | yes | 当前用户ID（用于校验作者权限） | Body (JSON) |
| title | string | no | 标题 | Body (JSON) |
| content | string | no | 内容 | Body (JSON) |
| summary | string | no | 摘要 | Body (JSON) |
| tags | array | no | 标签ID列表 | Body (JSON) |
| category_id | int | no | 分类ID | Body (JSON) |
| cover_image | object | no | 封面图片（JSON格式:{"imgs":["url1","url2"]}，url为上传后返回的地址） | Body (JSON) |

#### 请求示例
```json
{
    "post_id": 1,
    "user_id": 1,
    "title": "Python入门教程（修订版）",
    "content": "# Python入门\n\n更新后的内容...",
    "summary": "修订后的摘要",
    "tags": [1, 2],
    "category_id": 1,
    "cover_image": {"imgs":["/static/uploads/cover1.jpg"]}
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 响应示例（失败）
```json
{
    "code": 403,
    "msg": "无权编辑此文章"
}
```

---

### 4. 删除文章/问题（APP端）
- **路径**: `/api/article/<post_id>`
- **方法**: `DELETE`
- **函数名**: `delete_article`
- **OpenAPI摘要**: 删除文章或问题

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章/问题ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID（用于校验作者权限） | Query |

#### 请求示例
```
DELETE /api/article/1?user_id=1
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 响应示例（失败）
```json
{
    "code": 403,
    "msg": "无权删除此文章"
}
```

---

### 5. 获取文章列表（APP端）
- **路径**: `/api/article/list`
- **方法**: `GET`
- **函数名**: `get_article_list`
- **OpenAPI摘要**: 获取文章/问题列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| type | string | no | 类型筛选：article/question/all，默认all | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| sort | string | no | 排序：time/hot/recommend，默认time | Query |
| tag_id | int | no | 标签ID筛选 | Query |
| category_id | int | no | 分类ID筛选 | Query |
| user_id | int | no | 用户ID（查看某用户的文章） | Query |

#### 请求示例
```
GET /api/article/list?type=all&page=1&page_size=20&sort=time
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 文章列表数据 |
| data.list | array | 文章列表 |
| data.total | int | 总数 |
| data.list[].post_id | int | 文章ID |
| data.list[].type | string | 类型：article/question |
| data.list[].title | string | 标题 |
| data.list[].summary | string | 摘要 |
| data.list[].author | object | 作者信息 |
| data.list[].view_count | int | 浏览量 |
| data.list[].like_count | int | 点赞数 |
| data.list[].comment_count | int | 评论数 |
| data.list[].favorite_count | int | 收藏数（动态查询favorites表统计） |
| data.list[].created_at | datetime | 创建时间 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "参数错误"
}
```

---

### 6. 点赞/取消点赞（APP端）
- **路径**: `/api/article/like`
- **方法**: `POST`
- **函数名**: `toggle_like`
- **OpenAPI摘要**: 点赞或取消点赞

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Body (JSON) |
| post_id | int | yes | 文章/问题ID | Body (JSON) |

#### 请求示例
```
POST /api/article/like
Content-Type: application/json

{
    "user_id": 1,
    "post_id": 1
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

---

### 7. 获取首页推荐（APP端）
- **路径**: `/api/article/recommend`
- **方法**: `GET`
- **函数名**: `get_recommend_articles`
- **OpenAPI摘要**: 获取首页推荐文章

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| type | string | no | 类型：hot_question/recommend_article，默认混合 | Query |
| limit | int | no | 返回数量限制，默认10 | Query |
| random | bool | no | 是否随机返回，默认false | Query |

#### 请求示例
```
GET /api/article/recommend?type=hot_question&limit=10&random=true
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 推荐文章列表 |
| data[].post_id | int | 文章ID |
| data[].type | string | 类型：article/question |
| data[].title | string | 标题 |
| data[].summary | string | 摘要 |
| data[].author | object | 作者信息 |
| data[].view_count | int | 浏览量 |
| data[].like_count | int | 点赞数 |
| data[].comment_count | int | 评论数 |
| data[].created_at | datetime | 创建时间 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "参数错误"
}
```

---

### 8. 获取文章目录（APP端）
- **路径**: `/api/article/<post_id>/toc`
- **方法**: `GET`
- **函数名**: `get_article_toc`
- **OpenAPI摘要**: 获取文章目录结构（用于锚点导航）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | int | 文章ID |

#### 请求示例
```
GET /api/article/1/toc
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 目录结构 |
| data[].level | int | 标题级别（1-6） |
| data[].text | string | 标题文本 |
| data[].anchor | string | 锚点ID |

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "文章不存在"
}
```
