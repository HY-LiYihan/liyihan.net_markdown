---
title: Linux 包管理器速查手册
slug: linux-package-managers
description: Linux 下各发行版包管理器（apt、yum、dnf、pacman）的使用指南和命令速查
excerpt: 掌握 Linux 包管理器的使用方法
categories:
  - Linux
  - 系统管理
tags:
  - apt
  - yum
  - dnf
  - pacman
  - package
  - 速查手册
---

# Linux 包管理器速查手册

## apt/dpkg (Debian/Ubuntu)

### 常用命令

#### 更新软件源
```bash
sudo apt update
```

#### 升级软件包
```bash
sudo apt upgrade
sudo apt full-upgrade
```

#### 安装软件包
```bash
sudo apt install package_name
sudo apt install package1 package2
```

#### 卸载软件包
```bash
# 仅卸载软件包，保留配置文件
sudo apt remove package_name

# 卸载软件包并删除配置文件
sudo apt purge package_name

# 删除不再需要的依赖包
sudo apt autoremove
```

#### 搜索软件包
```bash
apt search keyword
apt list --installed | grep keyword
```

#### 显示软件包信息
```bash
apt show package_name
apt-cache show package_name
```

#### 添加/删除 PPA 源
```bash
# 添加 PPA 源
sudo add-apt-repository ppa:user/ppa-name

# 删除 PPA 源
sudo add-apt-repository --remove ppa:user/ppa-name
```

#### dpkg 命令
```bash
# 安装 .deb 包
sudo dpkg -i package.deb

# 列出已安装的包
dpkg -l

# 查看包信息
dpkg -I package.deb

# 查看包文件列表
dpkg -L package_name

# 查找文件属于哪个包
dpkg -S /path/to/file
```

---

## yum/dnf (CentOS/RHEL)

### 常用命令

#### 更新软件源
```bash
sudo yum update
sudo dnf update
```

#### 安装软件包
```bash
sudo yum install package_name
sudo dnf install package_name
```

#### 卸载软件包
```bash
sudo yum remove package_name
sudo dnf remove package_name

# 删除不再需要的依赖包
sudo yum autoremove
sudo dnf autoremove
```

#### 搜索软件包
```bash
yum search keyword
dnf search keyword
```

#### 显示软件包信息
```bash
yum info package_name
dnf info package_name
```

#### 列出已安装的包
```bash
yum list installed
dnf list installed
```

#### 清理缓存
```bash
sudo yum clean all
sudo dnf clean all
```

---

## pacman (Arch Linux)

### 常用命令

#### 更新软件源
```bash
sudo pacman -Sy
```

#### 升级系统
```bash
sudo pacman -Syu
```

#### 安装软件包
```bash
sudo pacman -S package_name
sudo pacman -S package1 package2
```

#### 卸载软件包
```bash
# 仅卸载软件包
sudo pacman -R package_name

# 卸载软件包及依赖
sudo pacman -Rs package_name

# 卸载软件包、依赖及配置文件
sudo pacman -Rns package_name
```

#### 搜索软件包
```bash
pacman -Ss keyword
```

#### 显示软件包信息
```bash
pacman -Si package_name
```

#### 列出已安装的包
```bash
pacman -Q
pacman -Q | grep keyword
```

#### 查看文件属于哪个包
```bash
pacman -Qo /path/to/file
```

#### 安装本地包
```bash
sudo pacman -U package.pkg.tar.zst
```

---

## 命令对比表

| 操作 | apt | yum/dnf | pacman |
|------|-----|---------|--------|
| 更新源 | `apt update` | - | `pacman -Sy` |
| 升级系统 | `apt upgrade` | `yum update` | `pacman -Syu` |
| 安装包 | `apt install` | `yum install` | `pacman -S` |
| 卸载包 | `apt remove` | `yum remove` | `pacman -R` |
| 删除配置 | `apt purge` | `yum remove` | `pacman -Rns` |
| 搜索包 | `apt search` | `yum search` | `pacman -Ss` |
| 显示信息 | `apt show` | `yum info` | `pacman -Si` |
| 列出已安装 | `apt list --installed` | `yum list installed` | `pacman -Q` |

---

## 实用示例

### 批量安装开发工具
```bash
# Debian/Ubuntu
sudo apt install build-essential git curl wget vim

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install git curl wget vim

# Arch Linux
sudo pacman -S base-devel git curl wget vim
```

### 查找并安装特定版本
```bash
# Debian/Ubuntu
apt-cache madison package_name
sudo apt install package_name=version

# CentOS/RHEL
yum --showduplicates list package_name
sudo yum install package_name-version

# Arch Linux（需要使用 AUR）
pacman -Ss package_name
```

### 清理系统
```bash
# Debian/Ubuntu
sudo apt autoremove
sudo apt autoclean

# CentOS/RHEL
sudo yum autoremove
sudo yum clean all

# Arch Linux
sudo pacman -Qtdq | sudo pacman -Rns -
```

### 查看包依赖
```bash
# Debian/Ubuntu
apt-cache depends package_name
apt-cache rdepends package_name

# CentOS/RHEL
yum deplist package_name

# Arch Linux
pactree package_name
```
