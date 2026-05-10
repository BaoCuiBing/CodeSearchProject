# 搜索路由接口文档

## 文件路径
`router/app_search_router.py`

## 蓝图配置
- **蓝图名称**: `search`
- **URL前缀**: `/api/search`

## 接口列表

### 1. 搜索文章（APP端）
- **路径**: `/api/search`
- **方法**: `GET`
- **函数名**: `search_content`
- **OpenAPI摘要**: 搜索文章/问题

> 注：搜索成功后自动记录搜索历史到search_history表（需传user_id）。

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | no | 当前用户ID（用于记录搜索历史，不传则不记录） | Query |
| keyword | string | yes | 搜索关键词 | Query |
| type | string | no | 搜索类型：article/question/all，默认all | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| sort | string | no | 排序方式：time/hot/relevance，默认relevance | Query |
| tag_id | int | no | 标签ID筛选 | Query |

#### 请求示例
```
GET /api/search?user_id=1&keyword=Python&type=all&page=1&page_size=20&sort=relevance
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 搜索结果数据 |
| data.list | array | 结果列表 |
| data.total | int | 总数 |
| data.page | int | 当前页 |
| data.page_size | int | 每页数量 |
| data.search_history_id | int | 搜索历史记录ID |
| data.list[].post_id | int | 文章/问题ID |
| data.list[].title | string | 标题 |
| data.list[].type | string | 类型：article/question |
| data.list[].summary | string | 摘要 |
| data.list[].author | object | 作者信息 |
| data.list[].tags | array | 标签列表 |
| data.list[].view_count | int | 浏览量 |
| data.list[].like_count | int | 点赞数 |
| data.list[].comment_count | int | 评论数 |
| data.list[].created_at | datetime | 创建时间 |

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "搜索关键词不能为空"
}
```

---

### 2. 搜索建议（APP端）
- **路径**: `/api/search/suggest`
- **方法**: `GET`
- **函数名**: `search_suggest`
- **OpenAPI摘要**: 搜索关键词联想

> 注：搜索建议基于search_history表的关键词频率统计，按搜索次数降序返回匹配的关键词。

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| keyword | string | yes | 输入的关键词（至少2个字符） | Query |
| limit | int | no | 返回数量限制，默认10 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 建议关键词列表 |
| data[].keyword | string | 关键词 |
| data[].count | int | 搜索次数 |

#### 请求示例
```
GET /api/search/suggest?keyword=Py&limit=5
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "关键词至少需要2个字符"
}
```

---

### 3. 热门搜索（APP端）
- **路径**: `/api/search/hot`
- **方法**: `GET`
- **函数名**: `hot_search`
- **OpenAPI摘要**: 获取热门搜索关键词

#### 请求参数
无

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | array | 热门搜索列表 |
| data[].keyword | string | 关键词 |
| data[].count | int | 搜索次数 |
| data[].rank | int | 排名 |

#### 请求示例
```
GET /api/search/hot
```

#### 响应示例（失败）
```json
{
    "code": 500,
    "msg": "服务器内部错误"
}
```

---

### 4. 搜索历史（APP端）
- **路径**: `/api/search/history`
- **方法**: `GET`
- **函数名**: `get_search_history`
- **OpenAPI摘要**: 获取搜索历史记录

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 搜索历史数据 |
| data.list | array | 历史记录列表 |
| data.total | int | 总数 |
| data.list[].search_history_id | int | 记录ID |
| data.list[].keyword | string | 搜索关键词 |
| data.list[].created_at | datetime | 搜索时间 |

#### 请求示例
```
GET /api/search/history?user_id=1&page=1&page_size=20
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 5. 清空搜索历史（APP端）
- **路径**: `/api/search/history/clear`
- **方法**: `DELETE`
- **函数名**: `clear_search_history`
- **OpenAPI摘要**: 清空搜索历史记录

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
DELETE /api/search/history/clear?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "user_id不能为空"
}
```

---

### 6. 删除单条搜索历史（APP端）
- **路径**: `/api/search/history/<search_history_id>`
- **方法**: `DELETE`
- **函数名**: `delete_search_history_item`
- **OpenAPI摘要**: 删除单条搜索历史

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| search_history_id | int | 历史记录ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| user_id | int | yes | 当前用户ID | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |

#### 请求示例
```
DELETE /api/search/history/1?user_id=1
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "历史记录不存在"
}
```

---

### 7. 搜索筛选条件（APP端）
- **路径**: `/api/search/filters`
- **方法**: `GET`
- **函数名**: `get_search_filters`
- **OpenAPI摘要**: 获取搜索筛选选项

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| type | string | no | 文章类型（用于返回对应标签） | Query |

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 筛选条件 |
| data.types | array | 文章类型选项 |
| data.sorts | array | 排序选项 |
| data.tags | array | 标签选项 |
| data.tags[].tag_id | int | 标签ID |
| data.tags[].name | string | 标签名称 |

#### 请求示例
```
GET /api/search/filters?type=article
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "文章类型参数无效"
}
```
