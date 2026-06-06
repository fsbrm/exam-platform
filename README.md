# 智备考 - 智能备考与学习数据分析平台

基于 Spring Boot + Vue 3 的考研智能刷题平台，支持 408 计算机综合和高等数学，集成 AI 解题助手与学习数据分析仪表盘。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Spring Boot 3.2 + MyBatis-Plus + MySQL + Redis + JWT + Knife4j |
| 前端 | Vue 3 + TypeScript + Element Plus + ECharts 5 + Pinia + Vite |
| AI | DeepSeek API（解题助手 + 错题分析） |

## 功能模块

- 📚 **导航首页**：品牌展示、科目入口、功能介绍
- 👤 **用户系统**：注册/登录/JWT认证/个人中心
- 📖 **科目章节**：408四大模块 + 高数七大模块，预留英语/政治扩展
- 📝 **刷题模块**：章节练习、随机练习、即时反馈
- ⏱️ **模拟考试**：限时考试、自动组卷、自动评分、逐题回顾
- 📋 **错题本**：自动收集、重做、移除
- ⭐ **收藏与笔记**：题目收藏、学习笔记
- 🤖 **AI 助手**：DeepSeek驱动的智能解题与薄弱点分析
- 📊 **学习分析**：ECharts仪表盘、正确率趋势、科目雷达图
- ⚙️ **管理后台**：题库CRUD、Excel导入导出、用户管理

## 快速开始

### 环境要求

- JDK 21+
- Node.js 18+
- MySQL 8.0+
- Redis

### 1. 数据库初始化

在 MySQL 中执行初始化脚本：

```sql
source backend/src/main/resources/db/migration/init.sql
```

### 2. 配置修改

编辑 `backend/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    username: root        # 改为你的MySQL用户名
    password: root        # 改为你的MySQL密码
  data:
    redis:
      host: localhost     # Redis地址

ai:
  deepseek:
    api-key: your-key     # 填入DeepSeek API Key
```

### 3. 启动后端

```bash
cd backend
# 安装Maven后执行
mvn spring-boot:run
```

或使用 Maven Wrapper：

```bash
cd backend
mvnw spring-boot:run
```

### 4. 安装前端依赖并启动

```bash
cd frontend
npm install
npm run dev
```

### 5. 访问

- 前端：http://localhost:3000
- 后端API文档：http://localhost:8080/doc.html
- 默认管理员：admin / 123456

### 6. 导入种子数据

```sql
source backend/src/main/resources/db/migration/seed.sql
```

## 项目结构

```
exam-platform/
├── backend/                         # Spring Boot 后端
│   ├── src/main/java/com/exam/
│   │   ├── config/                  # 配置类（MyBatis-Plus、CORS、Redis）
│   │   ├── controller/              # REST控制器
│   │   ├── service/                 # 业务逻辑层
│   │   ├── mapper/                  # MyBatis-Plus Mapper
│   │   ├── entity/                  # 数据库实体
│   │   ├── dto/                     # 请求DTO
│   │   ├── vo/                      # 响应VO
│   │   ├── common/                  # 统一返回、异常处理
│   │   └── security/                # JWT认证、Spring Security
│   └── src/main/resources/
│       ├── application.yml          # 主配置文件
│       └── db/migration/            # SQL脚本
│           ├── init.sql             # 建表+初始数据
│           └── seed.sql             # 种子题目（40+道）
│
├── frontend/                        # Vue 3 前端
│   ├── src/
│   │   ├── views/                   # 页面组件
│   │   │   ├── home/                # 首页
│   │   │   ├── auth/                # 登录/注册
│   │   │   ├── subjects/            # 科目章节
│   │   │   ├── practice/            # 刷题页面
│   │   │   ├── exam/                # 模拟考试
│   │   │   ├── wrong/               # 错题本
│   │   │   ├── analytics/           # 学习分析
│   │   │   ├── ai/                  # AI助手
│   │   │   ├── profile/             # 个人中心
│   │   │   └── admin/               # 管理后台
│   │   ├── router/                  # 路由配置
│   │   ├── stores/                  # Pinia状态管理
│   │   ├── api/                     # Axios请求封装
│   │   └── utils/                   # 工具函数
│   └── vite.config.ts
│
└── docs/                            # 文档
```

## 部署方案

| 服务 | 免费方案 | 付费方案 |
|------|---------|---------|
| 前端 | Vercel / Netlify | 阿里云学生机 + Nginx |
| 后端 | Railway / Render | 腾讯云学生机 + Docker |
| 数据库 | Railway MySQL / PlanetScale | 服务器自建 MySQL |
| Redis | Upstash 免费层 | 服务器自建 Redis |
