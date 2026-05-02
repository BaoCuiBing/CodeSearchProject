# 用户路由接口文档

## 文件路径
`router/app_user_router.py`

## 蓝图配置
- **蓝图名称**: `user`
- **URL前缀**: `/api/user`

## 接口列表

### 1. 用户注册（APP端）
- **路径**: `/api/user/register`
- **方法**: `POST`
- **函数名**: `register`
- **OpenAPI摘要**: 用户注册

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| usernumber | string | yes | 账号（字母、数字、下划线，6-20位） | Body (JSON) |
| username | string | yes | 用户名 | Body (JSON) |
| password | string | yes | 密码 | Body (JSON) |
| email | string | no | 邮箱 | Body (JSON) |

#### 请求示例
```json
{
    "usernumber": "user001",
    "username": "测试用户",
    "password": "123456",
    "email": "test@example.com"
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 用户信息（注册成功时） |
| data.user_id | int | 用户ID |
| data.username | string | 用户名 |
| data.role | string | 角色：user/admin |

#### 响应示例
```json
{
    "code": 200,
    "msg": "注册成功",
    "data": {
        "user_id": 1,
        "username": "测试用户",
        "role": "user"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "账号已存在"
}
```

---

### 2. 用户登录（APP端）
- **路径**: `/api/user/login`
- **方法**: `POST`
- **函数名**: `login`
- **OpenAPI摘要**: 用户登录

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 位置 |
|--------|------|------|------|------|
| usernumber | string | yes | 账号（字母、数字、下划线，6-20位） | Body (JSON) |
| password | string | yes | 密码 | Body (JSON) |

#### 请求示例
```json
{
    "usernumber": "user001",
    "password": "123456"
}
```

#### 响应格式
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码 |
| msg | string | 提示信息 |
| data | object | 用户信息（登录成功时） |
| data.user_id | int | 用户ID |
| data.username | string | 用户名 |
| data.role | string | 角色：user/admin |

#### 响应示例（成功）
```json
{
    "code": 200,
    "msg": "登录成功",
    "data": {
        "user_id": 1,
        "username": "测试用户",
        "role": "user"
    }
}
```

#### 响应示例（失败）
```json
{
    "code": 400,
    "msg": "账号或密码错误"
}
```

#### 响应示例（失败：账号被封禁）
```json
{
    "code": 403,
    "msg": "账号被封禁",
    "data": {
        "ban_reason": "发布违规内容",
        "ban_expire_time": "2024-01-22 10:30:00"
    }
}
```
