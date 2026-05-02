# 标签路由接口文档

## 文件路径
`router/app_tag_router.py`

## 蓝图配置
- **蓝图名称**: `tag`
- **URL前缀**: `/api/tag`

## 接口列表

### 1. 获取标签列表（APP端）
- **路径**: `/api/tag/list`
- **方法**: `GET`
- **函数名**: `get_tag_list`
- **OpenAPI摘要**: 获取所有标签列表（UI图08）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词 | Query |
| sort | string | no | 排序：name/count/hot，默认name | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 标签列表数据 |
| data.list | array | 标签列表 |
| data.total | int | 总数 |
| data.list[].tag_id | int | 标签ID |
| data.list[].name | string | 标签名称 |
| data.list[].slug | string | 标签别名 |
| data.list[].description | string | 标签描述 |
| data.list[].icon | string | 标签图标URL |
| data.list[].color | string | 标签颜色 |
| data.list[].post_count | int | 关联内容数（动态查询post_tags表统计） |
| data.list[].is_hot | bool | 是否热门 |

#### 请求示例
```
GET /api/tag/list?page=1&page_size=20&sort=count
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "排序参数无效"
}
```

---

### 2. 获取标签详情（APP端）
- **路径**: `/api/tag/<tag_id>`
- **方法**: `GET`
- **函数名**: `get_tag_detail`
- **OpenAPI摘要**: 获取标签详情信息（UI图16）

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| tag_id | int | 标签ID |

#### 请求示例
```
GET /api/tag/1
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 标签详情 |
| data.tag_id | int | 标签ID |
| data.name | string | 标签名称 |
| data.slug | string | 标签别名 |
| data.description | string | 标签描述 |
| data.icon | string | 标签图标URL |
| data.color | string | 标签颜色 |
| data.post_count | int | 关联内容数（动态查询post_tags表统计） |
| data.is_hot | bool | 是否热门 |
| data.is_recommend | bool | 是否推荐 |
| data.created_at | datetime | 创建时间 |

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "标签不存在"
}
```

---

### 3. 获取标签下的文章列表（APP端）
- **路径**: `/api/tag/<tag_id>/articles`
- **方法**: `GET`
- **函数名**: `get_tag_articles`
- **OpenAPI摘要**: 获取标签下的文章/问题列表

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| tag_id | int | 标签ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| type | string | no | 类型：article/question/all，默认all | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| sort | string | no | 排序：time/hot，默认time | Query |

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
| data.list[].created_at | datetime | 创建时间 |

#### 请求示例
```
GET /api/tag/1/articles?type=all&page=1&page_size=20&sort=hot
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "标签不存在"
}
```

---

### 4. 获取热门标签（APP端）
- **路径**: `/api/tag/hot`
- **方法**: `GET`
- **函数名**: `get_hot_tags`
- **OpenAPI摘要**: 获取热门标签（用于首页展示）

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| limit | int | no | 返回数量限制，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 热门标签列表 |
| data[].tag_id | int | 标签ID |
| data[].name | string | 标签名称 |
| data[].slug | string | 标签别名 |
| data[].icon | string | 标签图标URL |
| data[].color | string | 标签颜色 |
| data[].post_count | int | 关联内容数（动态查询post_tags表统计） |

#### 请求示例
```
GET /api/tag/hot?limit=10
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "返回数量超出限制"
}
```
