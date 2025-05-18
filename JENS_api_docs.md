# Jens Blog RESTful API 文档

本文档详细描述了Jens Blog系统提供的RESTful API接口，供前端或第三方应用集成使用。

## 基本信息

- 基础URL: `/api/v1`
- 数据格式: JSON
- 认证方式: Token认证或Session认证
- 版本控制: 在URL路径中使用版本号

## 认证

除了公开资源外，所有API请求均需要认证。认证可通过以下两种方式实现：

### 1. Session认证（Cookie认证）

适用于浏览器环境下的前端应用，使用Django的会话认证。

### 2. Token认证

适用于移动应用或第三方客户端，需要在请求头中加入token：

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## 资源和端点

### 用户资源

#### 获取认证令牌

- **URL**: `/auth/token/`
- **方法**: `POST`
- **说明**: 获取认证令牌
- **请求体**:
  ```json
  {
    "username": "existinguser",
    "password": "securepassword"
  }
  ```
- **响应** (200 OK):
  ```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 10,
    "username": "existinguser"
  }
  ```

#### 用户注册

- **URL**: `/users/`
- **方法**: `POST`
- **说明**: 创建新用户
- **请求体**:
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "password2": "securepassword",
    "verification_code": "123456"
  }
  ```
- **响应** (201 Created):
  ```json
  {
    "id": 10,
    "username": "newuser",
    "email": "user@example.com",
    "_links": {
      "self": "/api/v1/users/10/",
      "profile": "/api/v1/users/10/profile/"
    }
  }
  ```

#### 获取当前用户信息

- **URL**: `/users/me/`
- **方法**: `GET`
- **说明**: 获取当前登录用户的详细信息
- **响应** (200 OK):
  ```json
  {
    "id": 10,
    "username": "currentuser",
    "email": "user@example.com",
    "profile": {
      "avatar": "/media/avatars/user_profile.jpg",
      "bio": "用户简介",
      "website": "https://example.com",
      "location": "北京"
    },
    "_links": {
      "self": "/api/v1/users/10/",
      "profile": "/api/v1/users/10/profile/",
      "posts": "/api/v1/users/10/posts/"
    }
  }
  ```

#### 获取特定用户信息

- **URL**: `/users/{id}/`
- **方法**: `GET`
- **说明**: 获取指定ID用户的公开信息
- **响应** (200 OK):
  ```json
  {
    "id": 5,
    "username": "otheruser",
    "profile": {
      "avatar": "/media/avatars/other_profile.jpg",
      "bio": "其他用户简介",
      "website": "https://example.org"
    },
    "_links": {
      "self": "/api/v1/users/5/",
      "posts": "/api/v1/users/5/posts/"
    }
  }
  ```

#### 更新用户资料

- **URL**: `/users/{id}/profile/`
- **方法**: `PUT` 或 `PATCH`
- **说明**: 更新用户资料（只能更新自己的资料）
- **请求体** (PATCH示例):
  ```json
  {
    "bio": "新的个人简介",
    "website": "https://newsite.com",
    "location": "上海"
  }
  ```
- **响应** (200 OK):
  ```json
  {
    "avatar": "/media/avatars/user_profile.jpg",
    "bio": "新的个人简介",
    "website": "https://newsite.com",
    "location": "上海",
    "_links": {
      "user": "/api/v1/users/10/",
      "self": "/api/v1/users/10/profile/"
    }
  }
  ```

### 文章资源

#### 获取文章列表

- **URL**: `/posts/`
- **方法**: `GET`
- **说明**: 获取文章列表，支持分页和筛选
- **查询参数**:
  - `page`: 页码，默认1
  - `per_page`: 每页条数，默认10
  - `category`: 按分类筛选
  - `tag`: 按标签筛选
  - `author`: 按作者ID筛选
  - `q`: 搜索关键词
  - `sort`: 排序方式(`-created` 最新创建, `views` 浏览量, `-views` 浏览量降序)
- **响应** (200 OK):
  ```json
  {
    "count": 100,
    "next": "/api/v1/posts/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "文章标题",
        "excerpt": "文章摘要...",
        "author": {
          "id": 1,
          "username": "author",
          "_links": {
            "self": "/api/v1/users/1/"
          }
        },
        "created_time": "2023-05-10T12:00:00Z",
        "views": 120,
        "category": {
          "id": 1,
          "name": "技术",
          "_links": {
            "self": "/api/v1/categories/1/"
          }
        },
        "tags": [
          {
            "id": 1, 
            "name": "Python",
            "_links": {
              "self": "/api/v1/tags/1/"
            }
          },
          {
            "id": 2, 
            "name": "Django",
            "_links": {
              "self": "/api/v1/tags/2/"
            }
          }
        ],
        "_links": {
          "self": "/api/v1/posts/1/",
          "comments": "/api/v1/posts/1/comments/"
        }
      }
    ]
  }
  ```

#### 获取文章详情

- **URL**: `/posts/{id}/`
- **方法**: `GET`
- **说明**: 获取单篇文章详情
- **响应** (200 OK):
  ```json
  {
    "id": 1,
    "title": "文章标题",
    "content": "文章完整内容...",
    "excerpt": "文章摘要...",
    "author": {
      "id": 1,
      "username": "author",
      "profile": {
        "avatar": "/media/avatars/author_profile.jpg"
      },
      "_links": {
        "self": "/api/v1/users/1/"
      }
    },
    "created_time": "2023-05-10T12:00:00Z",
    "modified_time": "2023-05-15T15:30:00Z",
    "views": 120,
    "category": {
      "id": 1,
      "name": "技术",
      "_links": {
        "self": "/api/v1/categories/1/"
      }
    },
    "tags": [
      {
        "id": 1, 
        "name": "Python",
        "_links": {
          "self": "/api/v1/tags/1/"
        }
      },
      {
        "id": 2, 
        "name": "Django",
        "_links": {
          "self": "/api/v1/tags/2/"
        }
      }
    ],
    "_links": {
      "self": "/api/v1/posts/1/",
      "author": "/api/v1/users/1/",
      "comments": "/api/v1/posts/1/comments/"
    }
  }
  ```

#### 创建文章

- **URL**: `/posts/`
- **方法**: `POST`
- **说明**: 创建新文章
- **请求体**:
  ```json
  {
    "title": "新文章标题",
    "content": "文章内容...",
    "excerpt": "文章摘要...",
    "category": 1,
    "tags": [1, 2]
  }
  ```
- **响应** (201 Created):
  ```json
  {
    "id": 42,
    "title": "新文章标题",
    "content": "文章内容...",
    "excerpt": "文章摘要...",
    "author": {
      "id": 10,
      "username": "currentuser"
    },
    "created_time": "2023-06-05T14:30:00Z",
    "modified_time": "2023-06-05T14:30:00Z",
    "views": 0,
    "category": {
      "id": 1,
      "name": "技术"
    },
    "tags": [
      {"id": 1, "name": "Python"},
      {"id": 2, "name": "Django"}
    ],
    "_links": {
      "self": "/api/v1/posts/42/",
      "comments": "/api/v1/posts/42/comments/"
    }
  }
  ```

#### 更新文章

- **URL**: `/posts/{id}/`
- **方法**: `PUT` 或 `PATCH`
- **说明**: 更新文章（仅文章作者可操作）
- **请求体** (PATCH示例):
  ```json
  {
    "title": "更新后的标题",
    "content": "更新后的内容..."
  }
  ```
- **响应** (200 OK): 返回更新后的文章详情

#### 删除文章

- **URL**: `/posts/{id}/`
- **方法**: `DELETE`
- **说明**: 删除文章（仅文章作者可操作）
- **响应** (204 No Content): 无响应体

#### 获取用户发布的文章

- **URL**: `/users/{user_id}/posts/`
- **方法**: `GET`
- **说明**: 获取指定用户发布的所有文章
- **响应**: 与获取文章列表相同格式

### 评论资源

#### 获取文章评论

- **URL**: `/posts/{post_id}/comments/`
- **方法**: `GET`
- **说明**: 获取文章的所有评论
- **响应** (200 OK):
  ```json
  [
    {
      "id": 1,
      "content": "评论内容...",
      "author": {
        "id": 2,
        "username": "commenter",
        "profile": {
          "avatar": "/media/avatars/commenter_profile.jpg"
        },
        "_links": {
          "self": "/api/v1/users/2/"
        }
      },
      "created_time": "2023-05-11T10:20:00Z",
      "parent": null,
      "replies": [
        {
          "id": 2,
          "content": "回复内容...",
          "author": {
            "id": 3,
            "username": "replier",
            "_links": {
              "self": "/api/v1/users/3/"
            }
          },
          "created_time": "2023-05-11T11:00:00Z",
          "parent": 1,
          "_links": {
            "self": "/api/v1/comments/2/"
          }
        }
      ],
      "_links": {
        "self": "/api/v1/comments/1/",
        "post": "/api/v1/posts/1/"
      }
    }
  ]
  ```

#### 创建评论

- **URL**: `/posts/{post_id}/comments/`
- **方法**: `POST`
- **说明**: 对文章发表评论
- **请求体**:
  ```json
  {
    "content": "评论内容...",
    "parent": null  // 如果是回复其他评论，填写父评论ID
  }
  ```
- **响应** (201 Created): 返回创建的评论详情

#### 获取单个评论

- **URL**: `/comments/{id}/`
- **方法**: `GET`
- **说明**: 获取单个评论详情
- **响应** (200 OK): 返回评论详情

#### 更新评论

- **URL**: `/comments/{id}/`
- **方法**: `PUT` 或 `PATCH`
- **说明**: 更新评论（仅评论作者可操作）
- **请求体**:
  ```json
  {
    "content": "更新后的评论内容..."
  }
  ```
- **响应** (200 OK): 返回更新后的评论详情

#### 删除评论

- **URL**: `/comments/{id}/`
- **方法**: `DELETE`
- **说明**: 删除评论（评论作者或文章作者可操作）
- **响应** (204 No Content): 无响应体

### 分类资源

#### 获取所有分类

- **URL**: `/categories/`
- **方法**: `GET`
- **说明**: 获取所有文章分类
- **响应** (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "技术",
      "description": "技术相关文章",
      "post_count": 25,
      "_links": {
        "self": "/api/v1/categories/1/",
        "posts": "/api/v1/categories/1/posts/"
      }
    }
  ]
  ```

#### 获取分类下的文章

- **URL**: `/categories/{id}/posts/`
- **方法**: `GET`
- **说明**: 获取特定分类下的所有文章
- **响应**: 与获取文章列表相同格式

#### 获取分类详情

- **URL**: `/categories/{id}/`
- **方法**: `GET`
- **说明**: 获取分类详情
- **响应** (200 OK):
  ```json
  {
    "id": 1,
    "name": "技术",
    "description": "技术相关文章",
    "post_count": 25,
    "_links": {
      "self": "/api/v1/categories/1/",
      "posts": "/api/v1/categories/1/posts/"
    }
  }
  ```

### 标签资源

#### 获取所有标签

- **URL**: `/tags/`
- **方法**: `GET`
- **说明**: 获取所有文章标签
- **响应** (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "Python",
      "post_count": 15,
      "_links": {
        "self": "/api/v1/tags/1/",
        "posts": "/api/v1/tags/1/posts/"
      }
    }
  ]
  ```

#### 获取标签下的文章

- **URL**: `/tags/{id}/posts/`
- **方法**: `GET`
- **说明**: 获取包含特定标签的所有文章
- **响应**: 与获取文章列表相同格式

#### 获取标签详情

- **URL**: `/tags/{id}/`
- **方法**: `GET`
- **说明**: 获取标签详情
- **响应** (200 OK):
  ```json
  {
    "id": 1,
    "name": "Python",
    "post_count": 15,
    "_links": {
      "self": "/api/v1/tags/1/",
      "posts": "/api/v1/tags/1/posts/"
    }
  }
  ```

## HTTP状态码

API使用标准HTTP状态码表示请求结果：

- **200 OK**: 请求成功
- **201 Created**: 资源创建成功
- **204 No Content**: 请求成功，无返回内容（常用于删除操作）
- **400 Bad Request**: 请求参数有误
- **401 Unauthorized**: 未认证
- **403 Forbidden**: 权限不足
- **404 Not Found**: 资源不存在
- **405 Method Not Allowed**: 不支持的HTTP方法
- **409 Conflict**: 资源冲突
- **422 Unprocessable Entity**: 请求格式正确但语义错误
- **429 Too Many Requests**: 请求频率超限
- **500 Internal Server Error**: 服务器内部错误

## 错误响应

错误响应使用统一格式，包含错误信息：

```json
{
  "error": {
    "status": 404,
    "message": "资源不存在",
    "details": "找不到ID为123的文章"
  }
}
```

字段级别的错误：

```json
{
  "error": {
    "status": 400,
    "message": "验证错误",
    "validation_errors": {
      "title": ["标题不能为空"],
      "content": ["内容长度必须大于10个字符"]
    }
  }
}
```

## 分页

列表资源默认采用分页返回，分页信息包含在响应中：

```json
{
  "count": 100,        // 总记录数
  "next": "/api/v1/posts/?page=2",    // 下一页链接，无下一页则为null
  "previous": null,     // 上一页链接，无上一页则为null
  "results": []         // 当前页的数据
}
```

## 资源过滤和排序

大多数集合资源支持过滤和排序：

- 过滤：使用查询参数指定过滤条件，例如 `/api/v1/posts/?category=1&tag=2`
- 排序：使用`sort`参数指定排序字段，字段名前加`-`表示降序，例如 `/api/v1/posts/?sort=-created_time`

## 限速

为保护API不被滥用，我们对API请求进行了限速控制：

- 匿名用户: 60次/小时/IP
- 认证用户: 1000次/小时/用户

超过限制将返回429状态码和相应的错误信息。

## HATEOAS

所有资源响应都包含`_links`对象，提供相关资源的链接，支持API的可发现性和自描述性：

```json
"_links": {
  "self": "/api/v1/posts/1/",
  "author": "/api/v1/users/1/",
  "comments": "/api/v1/posts/1/comments/"
}
```

## 版本控制

API版本在URL中标识，当前版本为v1 (`/api/v1/`)。当API发生不兼容变更时，将创建新版本（如`/api/v2/`），旧版本会在一段时间内继续支持。 