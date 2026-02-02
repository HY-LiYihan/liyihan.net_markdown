#!/usr/bin/env python3
import os
import shutil
import frontmatter
from pathlib import Path
from datetime import datetime

ARTICLES_DIR = 'articles'
DEPLOY_DIR = 'deploy'
VERSION_FILE = 'VERSION'

def get_file_info(filepath):
    """获取文件信息"""
    try:
        post = frontmatter.load(filepath)
        stat = os.stat(filepath)
        return {
            'filename': os.path.basename(filepath),
            'title': post.get('title', Path(filepath).stem),
            'category': post.get('categories', [''])[0] if post.get('categories') else '',
            'slug': post.get('slug', ''),
            'size': stat.st_size
        }
    except Exception as e:
        print(f"[WARNING] Failed to parse {filepath}: {e}")
        return {
            'filename': os.path.basename(filepath),
            'title': Path(filepath).stem,
            'category': '',
            'slug': '',
            'size': 0
        }

def scan_articles():
    """扫描 articles/ 中的所有文章"""
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles

    for file in os.listdir(ARTICLES_DIR):
        if file.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, file)
            info = get_file_info(filepath)
            articles.append(info)

    return sorted(articles, key=lambda x: x['filename'])

def prepare_deploy():
    """准备部署包"""

    # 1. 读取当前版本
    if not os.path.exists(VERSION_FILE):
        print("[ERROR] VERSION file not found")
        return False

    current_version = open(VERSION_FILE, 'r').read().strip()
    print(f"[INFO] Preparing deployment for {current_version}...")

    # 2. 扫描文章
    articles = scan_articles()
    if not articles:
        print("[WARNING] No articles found in articles/")
        return False

    # 3. 清空并创建 deploy 目录
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    os.makedirs(DEPLOY_DIR)

    # 4. 复制所有文章到 deploy/
    print(f"[INFO] Found {len(articles)} articles in articles/")
    for article in articles:
        src = os.path.join(ARTICLES_DIR, article['filename'])
        dst = os.path.join(DEPLOY_DIR, article['filename'])
        shutil.copy2(src, dst)
        print(f"  [+] {article['filename']}")

    # 5. 生成 manifest.txt
    manifest_path = os.path.join(DEPLOY_DIR, 'manifest.txt')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(f"Deployment Package for {current_version}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"\nTotal files: {len(articles)}\n")
        f.write(f"\nFiles:\n")
        for article in sorted(articles, key=lambda x: x['filename']):
            f.write(f"  - {article['filename']}\n")

    # 6. 完成
    print(f"\n[OK] Deployment package prepared at {DEPLOY_DIR}/")
    print(f"[INFO] Total files: {len(articles)}")
    print(f"[INFO] Upload all files from {DEPLOY_DIR}/ to HALO")

    return True

def main():
    import sys
    try:
        success = prepare_deploy()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to prepare deployment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
