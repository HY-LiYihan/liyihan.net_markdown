---
title: 常用系统管理命令
slug: linux-system-commands
description: Linux 系统管理常用命令速查，包含进程管理、磁盘管理、网络命令等
excerpt: 掌握 Linux 系统管理的核心命令
categories:
  - Linux
  - 系统管理
tags:
  - system
  - process
  - network
  - 速查手册
---

## 进程管理

### 查看进程
```bash
# 查看所有进程
ps aux

# 查看特定用户的进程
ps -u username

# 实时查看进程
top

# 实时查看进程（更友好）
htop

# 查看进程树
pstree

# 查看特定进程
ps -ef | grep processname
```

### 进程控制
```bash
# 终止进程（PID）
kill <pid>

# 强制终止进程
kill -9 <pid>

# 按名称终止进程
killall processname

# 按名称强制终止进程
killall -9 processname

# 暂停进程
kill -STOP <pid>

# 恢复进程
kill -CONT <pid>
```

### 进程优先级
```bash
# 查看进程优先级
ps -eo pid,ni,cmd

# 以低优先级运行（nice: 19最低，-20最高）
nice -n 19 command

# 修改运行中进程的优先级
renice +5 <pid>

# 以指定优先级运行
nice -n -10 command
```

### 后台运行
```bash
# 后台运行命令
command &

# 将前台进程转到后台
Ctrl+z
bg

# 将后台进程转到前台
fg

# 查看后台任务
jobs

# 将任务转到前台
fg %1
```

---

## 系统监控

### 系统信息
```bash
# 查看系统信息
uname -a

# 查看系统版本
cat /etc/os-release

# 查看内核版本
uname -r

# 查看系统运行时间
uptime

# 查看系统负载
uptime
top
htop
```

### CPU 监控
```bash
# 查看 CPU 信息
cat /proc/cpuinfo

# 查看 CPU 使用率
top
htop

# 查看 CPU 核心数
nproc
```

### 内存监控
```bash
# 查看内存使用情况
free -h

# 详细内存信息
vmstat

# 内存使用详情
cat /proc/meminfo
```

### 磁盘监控
```bash
# 查看磁盘使用情况
df -h

# 查看目录大小
du -sh directory

# 查看目录下文件大小
du -h --max-depth=1 directory

# 查看磁盘 I/O
iostat
iotop
```

### 网络监控
```bash
# 查看网络连接
netstat -tunlp
ss -tunlp

# 查看网络流量
iftop
nethogs

# 查看网络接口
ifconfig
ip a
```

---

## 磁盘管理

### 磁盘分区
```bash
# 查看磁盘分区
fdisk -l

# 管理磁盘分区
fdisk /dev/sda

# GPT 分区工具
parted /dev/sda
```

### 磁盘挂载
```bash
# 创建挂载点
sudo mkdir /mnt/data

# 挂载磁盘
sudo mount /dev/sdb1 /mnt/data

# 卸载磁盘
sudo umount /mnt/data

# 查看挂载信息
mount
df -h
```

### 自动挂载 (/etc/fstab)
```
/dev/sdb1    /mnt/data    ext4    defaults    0    2
```

### 磁盘检查和修复
```bash
# 检查磁盘
sudo fsck /dev/sdb1

# 强制检查
sudo fsck -f /dev/sdb1

# 检查时自动修复
sudo fsck -y /dev/sdb1
```

---

## 日志管理

### 系统日志
```bash
# 查看系统日志
sudo journalctl

# 实时查看日志
sudo journalctl -f

# 查看特定服务的日志
sudo journalctl -u service_name

# 查看最近的日志
sudo journalctl -n 100

# 查看今天的日志
sudo journalctl --since today
```

### 传统日志
```bash
# 系统日志
tail -f /var/log/syslog
tail -f /var/log/messages

# 认证日志
tail -f /var/log/auth.log

# 内核日志
dmesg
tail -f /var/log/kern.log

# Cron 日志
tail -f /var/log/cron
```

### 日志轮转
```bash
# 配置文件
/etc/logrotate.conf
/etc/logrotate.d/

# 手动轮转
sudo logrotate -f /etc/logrotate.conf
```

---

## 网络配置

### 网络接口
```bash
# 查看网络接口
ip a
ifconfig

# 启用网络接口
sudo ip link set eth0 up

# 禁用网络接口
sudo ip link set eth0 down

# 配置 IP 地址
sudo ip addr add 192.168.1.100/24 dev eth0

# 删除 IP 地址
sudo ip addr del 192.168.1.100/24 dev eth0
```

### 路由表
```bash
# 查看路由表
ip route
route -n

# 添加默认网关
sudo ip route add default via 192.168.1.1

# 添加静态路由
sudo ip route add 192.168.2.0/24 via 192.168.1.254
```

### DNS 配置
```bash
# 配置 DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# 查看 DNS 配置
cat /etc/resolv.conf
```

### 网络测试
```bash
# 测试网络连通性
ping example.com

# 测试端口连接
telnet example.com 80
nc -zv example.com 80

# 追踪路由
traceroute example.com
tracepath example.com

# DNS 查询
nslookup example.com
dig example.com

# 测试带宽
speedtest-cli
```

---

## 用户管理

### 用户操作
```bash
# 添加用户
sudo adduser username
sudo useradd -m username

# 删除用户
sudo deluser username
sudo userdel -r username

# 修改用户
sudo usermod -aG group username

# 查看用户信息
id username
```

### 密码管理
```bash
# 修改密码
passwd

# 修改用户密码
sudo passwd username

# 锁定账户
sudo passwd -l username

# 解锁账户
sudo passwd -u username
```

### 用户组
```bash
# 创建用户组
sudo groupadd groupname

# 删除用户组
sudo groupdel groupname

# 将用户添加到组
sudo usermod -aG group username

# 查看用户组
groups username
```

### sudo 权限
```bash
# 编辑 sudo 配置
sudo visudo

# 示例配置
username ALL=(ALL:ALL) ALL

# 允许用户执行特定命令
username ALL=(ALL) /usr/bin/systemctl restart nginx
```

---

## 服务管理

### systemd 服务
```bash
# 启动服务
sudo systemctl start service_name

# 停止服务
sudo systemctl stop service_name

# 重启服务
sudo systemctl restart service_name

# 重新加载配置
sudo systemctl reload service_name

# 查看服务状态
sudo systemctl status service_name

# 开机自启
sudo systemctl enable service_name

# 取消开机自启
sudo systemctl disable service_name

# 查看开机自启服务
systemctl list-unit-files --type=service
```

### 服务日志
```bash
# 查看服务日志
sudo journalctl -u service_name

# 实时查看服务日志
sudo journalctl -fu service_name

# 查看最近的日志
sudo journalctl -u service_name -n 100
```

---

## 防火墙管理

### UFW (Ubuntu/Debian)
```bash
# 启用防火墙
sudo ufw enable

# 禁用防火墙
sudo ufw disable

# 查看状态
sudo ufw status

# 允许端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 拒绝端口
sudo ufw deny 22/tcp

# 删除规则
sudo ufw delete allow 80/tcp

# 允许 IP
sudo ufw allow from 192.168.1.100
```

### firewalld (CentOS/RHEL)
```bash
# 启动防火墙
sudo systemctl start firewalld
sudo systemctl enable firewalld

# 查看状态
sudo firewall-cmd --state

# 允许端口
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-service=http

# 重载配置
sudo firewall-cmd --reload

# 查看规则
sudo firewall-cmd --list-all
```

---

## 定时任务

### Cron 任务
```bash
# 编辑当前用户的 cron 任务
crontab -e

# 列出当前用户的 cron 任务
crontab -l

# 删除当前用户的 cron 任务
crontab -r

# 编辑特定用户的 cron 任务
sudo crontab -u username -e
```

### Cron 语法
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-6, 0=周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 示例
```bash
# 每天凌晨 2 点执行
0 2 * * * /path/to/script.sh

# 每小时执行
0 * * * * /path/to/script.sh

# 每周一执行
0 2 * * 1 /path/to/script.sh

# 每 5 分钟执行
*/5 * * * * /path/to/script.sh

# 每月 1 号凌晨执行
0 0 1 * * /path/to/script.sh
```

---

## 实用技巧

### 查找文件
```bash
# 按名称查找文件
find /path -name filename

# 按类型查找
find /path -type f

# 按大小查找
find /path -size +100M

# 按时间查找
find /path -mtime -7

# 查找后执行命令
find /path -name "*.log" -delete
find /path -name "*.sh" -exec chmod +x {} \;
```

### 系统清理
```bash
# 清理包缓存
sudo apt clean
sudo apt autoremove

# 清理旧内核
sudo apt autoremove --purge

# 清理日志
sudo journalctl --vacuum-time=7d

# 清理临时文件
sudo rm -rf /tmp/*
```

### 系统备份
```bash
# 备份整个系统
sudo rsync -aAXv / /backup/path

# 备份特定目录
rsync -avz /path/to/source /path/to/destination

# 压缩备份
tar -czvf backup_$(date +%Y%m%d).tar.gz /path/to/backup
```
