# 管理后台分类管理接口文档

## 文件路径
`router/admin_category_router.py`

## 蓝图配置
- **蓝图名称**: `admin_category`
- **URL前缀**: `/api/admin/category`

## 接口列表

### 1. 获取分类列表（管理端）
- **路径**: `/api/admin/category/list`
- **方法**: `GET`
- **函数名**: `get_category_list`
- **OpenAPI摘要**: 获取所有分类列表

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| page | int | no | 页码，默认1 | Query |
| page_size | int | no | 每页数量，默认20 | Query |
| keyword | string | no | 搜索关键词 | Query |
| sort | string | no | 排序：name/sort/post_count，默认sort | Query |
| order | string | no | 排序方向：asc/desc，默认asc | Query |

#### 请求示例
```
GET /api/admin/category/list?admin_id=1&page=1&page_size=20&sort=sort&order=asc
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "admin_id不能为空"
}
```

> 注：post_count为动态统计字段，从posts表按category_id聚合统计
#### 响应格式
```json
{
    "code": 200,
    "msg": "获取成功",
    "data": {
        "list": [
            {
                "category_id": 1,
                "name": "编程语言",
                "icon": "/static/uploads/categories/code.png",
                "sort": 1,
                "post_count": 500,
                "created_at": "2023-01-01 00:00:00",
                "updated_at": "2024-01-10 10:00:00"
            }
        ],
        "total": 10,
        "page": 1,
        "page_size": 20
    }
}
```

---

### 2. 创建分类（管理端）
- **路径**: `/api/admin/category`
- **方法**: `POST`
- **函数名**: `create_category`
- **OpenAPI摘要**: 创建新分类

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| name | string | yes | 分类名称（2-20字符） | Body (JSON) |
| icon | string | no | 分类图标URL | Body (JSON) |
| sort | int | no | 排序权重，默认0 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "name": "前端开发",
    "icon": "/static/uploads/categories/frontend.png",
    "sort": 2
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "创建成功",
    "data": {
        "category_id": 5,
        "name": "前端开发",
        "icon": "/static/uploads/categories/frontend.png",
        "sort": 2,
        "created_at": "2024-01-15 10:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "分类名称已存在"
}
```

---

### 3. 编辑分类（管理端）
- **路径**: `/api/admin/category`
- **方法**: `PUT`
- **函数名**: `edit_category`
- **OpenAPI摘要**: 编辑分类信息

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| category_id | int | yes | 分类ID | Body (JSON) |
| name | string | no | 分类名称 | Body (JSON) |
| icon | string | no | 分类图标URL | Body (JSON) |
| sort | int | no | 排序权重 | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "category_id": 1,
    "name": "前端开发（更新）",
    "icon": "/static/uploads/categories/frontend2.png",
    "sort": 1
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "更新成功",
    "data": {
        "category_id": 1,
        "name": "前端开发（更新）",
        "sort": 1,
        "updated_at": "2024-01-15 11:00:00"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 404,
    "msg": "分类不存在"
}
```

---

### 4. 删除分类（管理端）
- **路径**: `/api/admin/category/<category_id>`
- **方法**: `DELETE`
- **函数名**: `delete_category`
- **OpenAPI摘要**: 删除分类

#### 路径参数
| 参数名 | 类型 | 说明 |
|--------|------|------|
| category_id | int | 分类ID |

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Query |
| move_to_id | int | yes | 关联文章迁移到目标分类ID（有文章关联时必填） | Query |

#### 请求示例
```
DELETE /api/admin/category/3?admin_id=1&move_to_id=2
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "删除成功",
    "data": {
        "deleted_id": 3,
        "moved_to_id": 2
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "该分类下有文章，请先迁移"
}
```

---

### 5. 批量操作分类（管理端）
- **路径**: `/api/admin/category/batch-action`
- **方法**: `POST`
- **函数名**: `batch_action_categories`
- **OpenAPI摘要**: 批量操作多个分类

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| admin_id | int | yes | 管理员ID（需校验users.role=admin） | Body (JSON) |
| ids | array | yes | 分类ID列表，如[1,2,3] | Body (JSON) |
| action | string | yes | 操作类型：delete | Body (JSON) |

#### 请求示例
```json
{
    "admin_id": 1,
    "ids": [3, 4],
    "action": "delete"
}
```

#### 响应格式
```json
{
    "code": 200,
    "msg": "批量操作成功",
    "data": {
        "processed_count": 2
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "请选择要操作的分类"
}
```
