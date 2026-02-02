---
title: Linux 压缩解压速查手册
slug: linux-compression-cheatsheet
description: Linux 下各种压缩格式（tar、gzip、zip、7z 等）的压缩解压命令及工具安装指南
excerpt: 全面介绍 Linux 下常见压缩格式的使用方法
categories:
  - Linux
  - 系统管理
tags:
  - compression
  - tar
  - gzip
  - zip
  - 7z
  - 速查手册
---

# Linux 压缩解压速查手册

## 安装压缩工具

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tar gzip bzip2 xz-utils zip unzip p7zip-full
```

### CentOS/RHEL
```bash
sudo yum install tar gzip bzip2 xz zip unzip p7zip
```

### macOS
```bash
brew install gnu-tar gzip bzip2 xz zip unzip p7zip
```

## tar 归档和压缩

### 基本语法
```bash
tar [选项] [归档文件] [文件/目录]
```

### 常用选项
| 选项 | 说明 |
|------|------|
| `-c` | 创建新的归档文件 |
| `-x` | 解压归档文件 |
| `-t` | 查看归档文件内容 |
| `-v` | 显示详细过程 |
| `-f` | 指定归档文件名 |
| `-z` | 使用 gzip 压缩/解压 |
| `-j` | 使用 bzip2 压缩/解压 |
| `-J` | 使用 xz 压缩/解压 |
| `-C` | 指定解压目录 |

### 常用命令
```bash
# 创建 tar 归档（未压缩）
tar -cvf archive.tar file1 file2 directory/

# 创建 tar.gz 压缩文件
tar -czvf archive.tar.gz file1 file2 directory/

# 创建 tar.bz2 压缩文件
tar -cjvf archive.tar.bz2 file1 file2 directory/

# 创建 tar.xz 压缩文件
tar -cJvf archive.tar.xz file1 file2 directory/

# 解压 tar.gz 文件
tar -xzvf archive.tar.gz

# 解压 tar.gz 到指定目录
tar -xzvf archive.tar.gz -C /path/to/directory/

# 查看归档文件内容
tar -tzvf archive.tar.gz
```

## gzip 压缩

### 基本命令
```bash
# 压缩文件（删除原文件）
gzip file.txt

# 压缩文件（保留原文件）
gzip -k file.txt

# 解压文件
gunzip file.txt.gz

# 查看压缩文件内容
gzip -l file.txt.gz
```

## bzip2 压缩

### 基本命令
```bash
# 压缩文件
bzip2 file.txt

# 解压文件
bunzip2 file.txt.bz2

# 查看压缩文件信息
bzip2 -l file.txt.bz2
```

## xz 压缩

### 基本命令
```bash
# 压缩文件
xz file.txt

# 解压文件
unxz file.txt.xz

# 查看压缩文件信息
xz -l file.txt.xz
```

## zip 压缩

### 基本命令
```bash
# 创建 zip 文件
zip archive.zip file1 file2 directory/

# 递归压缩目录
zip -r archive.zip directory/

# 解压 zip 文件
unzip archive.zip

# 解压到指定目录
unzip archive.zip -d /path/to/directory/

# 查看 zip 文件内容
unzip -l archive.zip

# 压缩时排除某些文件
zip -r archive.zip directory/ -x "*.log" "*.tmp"
```

## 7z 压缩

### 基本命令
```bash
# 创建 7z 文件
7z a archive.7z file1 file2 directory/

# 递归压缩目录
7z a -r archive.7z directory/

# 解压 7z 文件
7z x archive.7z

# 解压到指定目录
7z x archive.7z -o/path/to/directory/

# 查看压缩文件内容
7z l archive.7z

# 使用密码压缩
7z a -p archive.7z file.txt
```

## 常用格式对比

| 格式 | 扩展名 | 压缩率 | 速度 | 适用场景 |
|------|--------|--------|------|----------|
| gzip | .gz | 中等 | 快 | 日常使用，兼容性好 |
| bzip2 | .bz2 | 高 | 慢 | 需要高压缩率的场景 |
| xz | .xz | 最高 | 最慢 | 长期存储，需要高压缩率 |
| zip | .zip | 中等 | 快 | 跨平台交换 |
| 7z | .7z | 很高 | 中等 | 需要高压缩率和多种格式 |

## 实用示例

### 备份目录
```bash
# 备份整个目录到 tar.gz
tar -czvf backup_$(date +%Y%m%d).tar.gz /path/to/directory/
```

### 压缩并排除文件
```bash
# 排除 .git 目录和日志文件
tar -czvf archive.tar.gz --exclude='.git' --exclude='*.log' directory/
```

### 分卷压缩
```bash
# 创建分卷压缩文件（每卷 100M）
tar -czvf - directory/ | split -b 100M - archive.tar.gz.

# 合并分卷
cat archive.tar.gz.* | tar -xzvf -
```

### 批量解压
```bash
# 批量解压所有 .tar.gz 文件
for file in *.tar.gz; do tar -xzvf "$file"; done
```
