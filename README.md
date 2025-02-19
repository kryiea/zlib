# E-Book Search 项目

这是一个基于Vue.js和Flask的电子书搜索系统。

## 项目结构

```
- frontend/  # 前端Vue.js项目
  - dist/    # 构建后的静态文件
- backend/   # 后端Flask项目
  - app/     # Flask应用
  - platforms/ # 搜索平台实现
  - utils/   # 工具函数
```

## 部署说明

### 环境要求

- Python 3.12+
- Node.js 14+

### 后端部署

1. 创建并激活Python虚拟环境：
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. 安装依赖：
```bash
pip install -r backend/requirements.txt
```

3. 启动后端服务：
```bash
cd backend
python app.py
```

### 前端部署

前端已经构建完成，静态文件位于 `frontend/dist` 目录下。你可以：

1. 直接使用Web服务器（如Nginx）托管 `frontend/dist` 目录
2. 或者使用Python的HTTP服务器快速预览：
```bash
python -m http.server 8080 --directory frontend/dist
```

## 访问应用

- 前端页面：http://localhost:8080
- 后端API：http://localhost:5000

## 注意事项

1. 确保后端API地址在前端配置正确（vue.config.js中）
2. 建议在生产环境中使用正式的Web服务器（如Nginx）来托管前端静态文件
3. 可以根据需要修改后端服务的端口号和其他配置