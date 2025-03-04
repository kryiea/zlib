# E-Book Search 部署问题排查指南

如果您在服务器上部署 E-Book Search 项目后无法访问，请按照以下步骤进行排查：

## 1. 检查后端服务是否正常运行

```bash
# 检查后端进程是否存在
ps aux | grep python

# 检查后端日志
cat logs/app.log
```

确保后端服务正在监听 `0.0.0.0:5000`（而不仅仅是 localhost 或 127.0.0.1）。

## 2. 检查防火墙设置

确保服务器防火墙允许访问相应端口：

```bash
# CentOS/RHEL
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-port=5000/tcp  # 后端API端口
sudo firewall-cmd --permanent --add-port=80/tcp    # Nginx/前端端口
sudo firewall-cmd --reload

# Ubuntu/Debian
sudo ufw status
sudo ufw allow 5000/tcp
sudo ufw allow 80/tcp
```

## 3. 检查云服务提供商安全组/网络设置

如果您使用的是云服务器（如阿里云、腾讯云、AWS等），请检查安全组设置，确保已开放相应端口的入站流量。

## 4. Nginx 配置检查

确保 Nginx 配置正确：

```bash
# 检查配置语法
sudo nginx -t

# 查看错误日志
sudo cat /var/log/nginx/error.log
```

确保您的 Nginx 配置包含正确的 API 代理设置，参考项目中的 `nginx.conf.example` 文件：

```
location /api/ {
    proxy_pass http://localhost:5000/;  # 后端服务地址
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 5. 前端构建与部署

确保前端已正确构建并部署：

```bash
# 重新构建前端
cd frontend
npm run build

# 确保 dist 目录中的文件已正确部署到 Nginx 指定的目录
```

## 6. API 请求路径问题

检查浏览器开发者工具中的网络请求，确认 API 请求是否正确发送到服务器，以及是否有跨域或其他错误。

如果 API 请求返回 404，可能是因为：
- Nginx 配置中的 API 代理路径不正确
- 后端服务未运行或监听的地址/端口不正确

## 7. 域名与 HTTPS 问题

如果您使用域名和 HTTPS，请确保：
- DNS 记录已正确设置
- SSL 证书已正确配置
- 前端请求使用正确的协议（HTTP 或 HTTPS）

## 8. SELinux 问题（CentOS/RHEL）

如果您使用的是 CentOS 或 RHEL，SELinux 可能会阻止 Nginx 代理请求：

```bash
# 检查 SELinux 状态
getenforce

# 临时禁用 SELinux 进行测试
sudo setenforce 0

# 如果确认是 SELinux 导致的问题，可以配置正确的上下文而不是禁用它
sudo setsebool -P httpd_can_network_connect 1
```

## 9. 修改后端绑定地址

如果您直接通过 IP:PORT 访问后端（不使用 Nginx），请确保后端绑定到 `0.0.0.0`：

在 `.env` 文件中设置（如果使用）：
```
HOST=0.0.0.0
PORT=5000
```

或直接修改 `config.py` 中的默认值。

## 10. 检查网络连通性

```bash
# 从服务器内部测试后端服务
curl http://localhost:5000/zlibrary/s/test

# 从其他机器测试服务器连通性
telnet your_server_ip 80
telnet your_server_ip 5000
```

## 常见错误与解决方案

### 1. 前端无法连接到后端 API

**症状**：页面加载，但搜索无响应，浏览器控制台显示 API 请求错误

**解决方案**：
- 确保前端代码中的 API 请求地址正确配置
- 检查 Nginx 的 API 代理配置
- 确保后端服务正在运行

### 2. 502 Bad Gateway

**症状**：访问 API 时 Nginx 返回 502 错误

**解决方案**：
- 确保后端服务正在运行
- 检查 Nginx 错误日志
- 确认 Nginx 配置中的后端地址正确

### 3. 404 Not Found

**症状**：API 请求返回 404

**解决方案**：
- 检查 API 路径是否正确
- 确认后端路由配置正确
- 检查 Nginx 的 location 配置

## 其他提示

- 使用 `systemctl status nginx` 和 `systemctl status <your-backend-service>` 检查服务状态
- 检查系统日志 `journalctl -xe` 查找可能的错误
- 临时使用 `python -m http.server 8080 --directory frontend/dist` 测试前端静态文件是否可访问
- 使用 `flask run --host=0.0.0.0 --port=5000` 直接启动后端进行测试

如果按照以上步骤排查后仍然无法解决问题，请检查服务器日志获取更详细的错误信息。