---
title: SSH 使用指南
slug: ssh-guide
description: SSH 远程登录和管理的完整指南，包含配置、密钥管理、端口转发和常见问题解决
excerpt: 掌握 SSH 远程连接和安全配置
categories:
  - Linux
  - 网络
tags:
  - ssh
  - 远程连接
  - 安全
  - 速查手册
---

## SSH 基础

### 连接到远程服务器
```bash
# 基本连接
ssh user@hostname

# 指定端口
ssh -p 2222 user@hostname

# 使用 IP 地址
ssh user@192.168.1.100

# 使用配置文件中的主机名
ssh myserver
```

### SSH 配置文件 (~/.ssh/config)
```bash
# 创建或编辑配置文件
vim ~/.ssh/config
```

配置文件示例：
```
Host myserver
    HostName example.com
    User username
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60

Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_key
```

---

## SSH 密钥管理

### 生成 SSH 密钥
```bash
# 生成 RSA 密钥（默认）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 生成 Ed25519 密钥（推荐，更安全且更快）
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 密钥文件
| 文件 | 说明 |
|------|------|
| `~/.ssh/id_rsa` | 私钥（保密） |
| `~/.ssh/id_rsa.pub` | 公钥（可分享） |
| `~/.ssh/id_ed25519` | Ed25519 私钥 |
| `~/.ssh/id_ed25519.pub` | Ed25519 公钥 |

### 复制公钥到远程服务器
```bash
# 手动复制
ssh-copy-id user@hostname

# 指定端口
ssh-copy-id -p 2222 user@hostname

# 手动方法
cat ~/.ssh/id_rsa.pub | ssh user@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 多密钥管理
```bash
# 添加密钥到代理
ssh-add ~/.ssh/id_rsa

# 列出已添加的密钥
ssh-add -l

# 删除所有密钥
ssh-add -D

# 删除特定密钥
ssh-add -d ~/.ssh/id_rsa
```

---

## SSH 端口转发

### 本地端口转发
```bash
# 将本地 8080 端口转发到远程服务器的 localhost:80
ssh -L 8080:localhost:80 user@remote

# 将本地 3306 端口转发到远程数据库
ssh -L 3306:database.example.com:3306 user@remote
```

### 远程端口转发
```bash
# 将远程服务器的 8080 端口转发到本地 localhost:80
ssh -R 8080:localhost:80 user@remote

# 使用 GatewayPorts 允许远程服务器公开端口
ssh -R 0.0.0.0:8080:localhost:80 user@remote
```

### 动态端口转发（SOCKS 代理）
```bash
# 创建 SOCKS 代理
ssh -D 1080 user@remote

# 配置应用程序使用代理 localhost:1080
```

### X11 转发（运行图形程序）
```bash
ssh -X user@remote

# 运行图形应用程序
firefox
```

---

## SSH 高级用法

### 在远程服务器上执行命令
```bash
# 执行单个命令
ssh user@remote "ls -la"

# 执行多个命令
ssh user@remote "cd /var/log && tail -f syslog"

# 执行本地脚本
cat script.sh | ssh user@remote "bash"

# 从远程复制文件
ssh user@remote "cat /path/to/file" > localfile
```

### 文件传输
```bash
# 下载文件
scp user@remote:/path/to/file /local/path

# 上传文件
scp /local/file user@remote:/remote/path

# 递归传输目录
scp -r /local/dir user@remote:/remote/path

# 指定端口
scp -P 2222 file user@remote:/remote/path

# 使用 rsync（更高效）
rsync -avz /local/ user@remote:/remote/
```

### SSH 隧道持久化
```bash
# 使用 autossh 保持连接
autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -L 8080:localhost:80 user@remote

# 使用 tmux/screen 保持会话
screen -S tunnel
ssh -L 8080:localhost:80 user@remote
# 按 Ctrl+a d 分离会话
```

---

## SSH 安全配置

### 服务器配置 (/etc/ssh/sshd_config)
```bash
# 禁用 root 登录
PermitRootLogin no

# 禁用密码登录（仅允许密钥）
PasswordAuthentication no

# 更改默认端口
Port 2222

# 限制登录用户
AllowUsers user1 user2

# 登录失败限制
MaxAuthTries 3
LoginGraceTime 30

# 使用更安全的加密算法
Ciphers aes256-gcm@openssh.com,chacha20-poly1305@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
```

重启 SSH 服务：
```bash
# Ubuntu/Debian
sudo systemctl restart sshd

# CentOS/RHEL
sudo systemctl restart sshd
```

### 客户端安全实践
```bash
# 使用更安全的密钥类型
ssh-keygen -t ed25519

# 为密钥设置密码
ssh-keygen -t ed25519 -C "email@example.com"

# 限制特定用途的密钥
# 在 authorized_keys 中添加选项:
command="command" no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-rsa ...
```

---

## 故障排查

### 连接问题
```bash
# 详细输出
ssh -vvv user@remote

# 测试连接
ssh -o ConnectTimeout=5 user@remote

# 检查 SSH 服务状态
systemctl status sshd
```

### 权限问题
```bash
# 检查文件权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys

# 检查 SELinux (CentOS/RHEL)
ls -Z ~/.ssh/authorized_keys
restorecon -R -v ~/.ssh
```

### 密钥被拒绝
```bash
# 验证公钥是否已添加
ssh-copy-id -i ~/.ssh/id_rsa.pub user@remote

# 检查 authorized_keys 文件
cat ~/.ssh/authorized_keys
```

---

## 实用示例

### SSH Jump Host（跳板机）
```bash
# 通过跳板机连接到目标服务器
ssh -J jumpuser@jumphost targetuser@target

# 在配置文件中设置
Host jump
    HostName jumphost.com
    User jumpuser

Host target
    HostName target.com
    User targetuser
    ProxyJump jump
```

### 并行执行命令
```bash
# 在多台服务器上执行相同命令
for server in server1 server2 server3; do
    ssh user@$server "uptime"
done

# 使用 parallel
parallel -j 3 ssh user@{} "uptime" ::: server1 server2 server3
```

### SSH 带宽限制
```bash
# 限制 scp 传输速度（100KB/s）
scp -l 800 file user@remote:/path/

# 使用 pv (pipe viewer)
pv file | ssh user@remote "cat > /path/to/file"
```
