# E-Book Search 项目

这是一个基于Vue.js和Flask的电子书搜索系统。

支持多种搜索平台，包括zlibrary等等。

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

- Python 3.6+
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

> **注意**：如果遇到非ASCII字符错误（如`SyntaxError: Non-ASCII character '\xe5' in file app.py`），请在Python文件顶部添加编码声明：
> ```python
> # -*- coding: utf-8 -*-
> ```
> 这行代码应该放在文件的第一行或第二行（如果第一行是shebang）。

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

### CentOS系统部署指南

#### 解决镜像问题

在CentOS系统上，有时会遇到镜像服务器连接问题（如HTTP 502错误）。以下是几种解决方法：

1. 更换YUM镜像源（推荐）：
```bash
# 备份原镜像源配置
sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup

# 下载阿里云镜像源配置
sudo curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
# 或者使用腾讯云镜像
# sudo curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo

# 清除缓存并生成新缓存
sudo yum clean all
sudo yum makecache

# 再次尝试安装Python
sudo yum install python3 -y
```

2. 如果仍然无法通过YUM安装，可以直接从源代码编译安装Python：

```bash
# 安装编译依赖
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y

# 下载Python源码（可以选择合适的版本）
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz

# 如果wget命令不可用，先安装wget
# sudo yum install wget -y

# 解压源码
tar xzf Python-3.12.0.tgz
cd Python-3.12.0

# 配置、编译和安装
./configure --enable-optimizations
sudo make altinstall

# 验证安装
python3.12 --version
```

3. 使用离线安装包（适用于完全无法连接外网的情况）：
   - 在有网络的机器上下载所需的RPM包及其依赖
   - 使用U盘等方式传输到目标服务器
   - 使用`rpm -ivh *.rpm`命令进行本地安装

#### 完整安装流程

1. 安装Python 3：
```bash
# 更新系统并安装Python 3
sudo yum update -y
sudo yum install python3 python3-devel python3-pip -y

# 验证安装
python3 --version
```

2. 修复pip（如果遇到"No module named 'pip._internal'"错误）：
```bash
# 方法1：重新安装pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# 方法2：使用ensurepip模块（如果可用）
python3 -m ensurepip --upgrade
```

3. 安装pip和虚拟环境：
```bash
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

4. 克隆项目并设置环境：
```bash
# 克隆项目（如果使用git）
# git clone <项目地址> zlib
# cd zlib

# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate
```

5. 安装项目依赖：
```bash
pip install -r backend/requirements.txt
```

6. 启动后端服务：
```bash
cd backend
python app.py
```

6. 部署前端：
```bash
# 使用Python的HTTP服务器快速预览
python -m http.server 8080 --directory frontend/dist

# 或者安装并配置Nginx
sudo yum install nginx -y
sudo vi /etc/nginx/conf.d/ebook-search.conf
```

Nginx配置示例：
```
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或IP

    location / {
        root /path/to/zlib/frontend/dist;  # 替换为实际路径
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

7. 启动Nginx：
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 后台运行Python应用

在生产环境中，需要让Python应用在后台持续运行，即使关闭终端也不会停止。以下是几种常用方法：

1. 使用nohup命令（简单方法）：
```bash
cd backend
nohup python app.py > ../logs/app.out 2>&1 &
```
这会将输出重定向到logs/app.out文件，并在后台运行应用。可以通过`ps aux | grep python`查看进程。

2. 使用Screen会话管理（开发环境推荐）：
```bash
# 安装screen
sudo yum install screen -y

# 创建新会话
screen -S zlib-backend

# 在screen会话中启动应用
cd backend
python app.py

# 按Ctrl+A然后按D可以分离会话
# 重新连接会话：
screen -r zlib-backend
```

3. 使用Systemd服务（生产环境推荐）：
```bash
# 创建服务文件
sudo vi /etc/systemd/system/zlib-backend.service
```

服务文件内容：
```
[Unit]
Description=ZLib Backend Service
After=network.target

[Service]
User=<your_username>
WorkingDirectory=/path/to/zlib/backend
Environment="PATH=/path/to/zlib/.venv/bin"
ExecStart=/path/to/zlib/.venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：
```bash
sudo systemctl daemon-reload
sudo systemctl start zlib-backend
sudo systemctl enable zlib-backend

# 查看状态
sudo systemctl status zlib-backend
# 查看日志
sudo journalctl -u zlib-backend
```

4. 使用Supervisor进程管理（推荐）：
```bash
# 安装supervisor
sudo yum install supervisor -y
sudo systemctl enable supervisord
sudo systemctl start supervisord

# 创建配置文件
sudo vi /etc/supervisord.d/zlib-backend.ini
```

配置文件内容：
```
[program:zlib-backend]
command=/path/to/zlib/.venv/bin/python app.py
directory=/path/to/zlib/backend
user=<your_username>
autostart=true
autorestart=true
stdout_logfile=/path/to/zlib/logs/supervisor_stdout.log
stderr_logfile=/path/to/zlib/logs/supervisor_stderr.log
environment=PATH="/path/to/zlib/.venv/bin"
```

应用supervisor配置并管理：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start zlib-backend

# 查看状态
sudo supervisorctl status
```

## 注意事项

1. 确保后端API地址在前端配置正确（vue.config.js中）
2. 建议在生产环境中使用正式的Web服务器（如Nginx）来托管前端静态文件
3. 可以根据需要修改后端服务的端口号和其他配置
4. CentOS系统中可能需要配置防火墙以允许访问相应端口：
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp  # 后端API端口
sudo firewall-cmd --permanent --add-port=8080/tcp  # 前端页面端口
sudo firewall-cmd --reload
```

## 前端演示
![image](1.png)