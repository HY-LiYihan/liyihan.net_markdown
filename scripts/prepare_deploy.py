#!/usr/bin/env python3
import os
import shutil
import csv
from pathlib import Path
from datetime import datetime

ARTICLES_DIR = 'articles'
DEPLOY_DIR = 'deploy'
VERSION_FILE = 'VERSION'
VERSIONS_CSV = 'versions.csv'
STAGING_DIR = 'staging'

def read_versions_csv():
    """读取 versions.csv"""
    if not os.path.exists(VERSIONS_CSV):
        return {}

    versions = {}
    with open(VERSIONS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            versions[row['article_path']] = row

    return versions

def write_versions_csv(records):
    """写入 versions.csv"""
    fieldnames = ['article_path', 'version', 'published_at', 'is_deployed', 'title', 'description', 'excerpt', 'category', 'tags', 'slug']

    with open(VERSIONS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def scan_articles():
    """扫描 articles/ 中的所有文章"""
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles

    for file in os.listdir(ARTICLES_DIR):
        if file.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, file)
            articles.append({'filename': file})

    return sorted(articles, key=lambda x: x['filename'])

def check_deploy_folder():
    """检查 deploy 文件夹是否有文件"""
    if not os.path.exists(DEPLOY_DIR):
        return []

    files = []
    for item in os.listdir(DEPLOY_DIR):
        if item.endswith('.md'):
            files.append(item)

    return files

def move_to_staging(files):
    """将文件移动回 staging"""
    if not files:
        return

    for filename in files:
        src = os.path.join(DEPLOY_DIR, filename)
        # 确定分类（从 versions.csv 获取）
        versions_dict = read_versions_csv()
        if filename in versions_dict:
            category = versions_dict[filename].get('category', '').split('|')[0]
            dst_dir = os.path.join(STAGING_DIR, category)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            dst = os.path.join(dst_dir, filename)
            shutil.copy2(src, dst)
            print(f"  [→] {filename} → staging/{category}/")

    shutil.rmtree(DEPLOY_DIR)
    print(f"[OK] Deploy folder cleared, files moved back to staging")

def deploy_articles(target_version):
    """部署指定版本的未部署文章"""

    # 1. 读取版本信息
    versions_dict = read_versions_csv()
    print(f"[INFO] Reading version info from {VERSIONS_CSV}...")

    # 2. 确定要部署的文件
    files_to_deploy = []
    for article_path, record in versions_dict.items():
        version = record.get('version', '')
        is_deployed = record.get('is_deployed', 'False')

        if version == target_version and is_deployed.lower() == 'false':
            files_to_deploy.append({'filename': article_path})

    if not files_to_deploy:
        print(f"[INFO] No undeployed articles found for version {target_version}")
        return False

    # 3. 检查 deploy 文件夹
    existing_files = check_deploy_folder()
    if existing_files:
        print(f"\n[WARNING] Found {len(existing_files)} files in {DEPLOY_DIR}/")
        print("Files:")
        for file in existing_files:
            print(f"  - {file}")

        print("\nOptions:")
        print("  [1] Discard these files (delete)")
        print("  [2] Move them back to staging")

        choice = input("\nYour choice (1/2): ").strip()

        if choice == '1':
            shutil.rmtree(DEPLOY_DIR)
            print(f"[OK] Deploy folder cleared")
        elif choice == '2':
            move_to_staging(existing_files)
        else:
            print("[CANCELLED] Operation cancelled")
            return False

    # 4. 清空并创建 deploy 目录
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    os.makedirs(DEPLOY_DIR)

    # 5. 复制文件到 deploy/
    print(f"\n[INFO] Found {len(files_to_deploy)} undeployed articles for version {target_version}")
    for article in files_to_deploy:
        src = os.path.join(ARTICLES_DIR, article['filename'])
        dst = os.path.join(DEPLOY_DIR, article['filename'])
        shutil.copy2(src, dst)
        print(f"  [+] {article['filename']}")

    # 6. 生成 manifest.txt
    manifest_path = os.path.join(DEPLOY_DIR, 'manifest.txt')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(f"Deployment Package for {target_version}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"\nTotal files: {len(files_to_deploy)}\n")
        f.write(f"\nFiles:\n")
        for article in sorted(files_to_deploy, key=lambda x: x['filename']):
            f.write(f"  - {article['filename']}\n")

    # 7. 等待确认
    print(f"\n[INFO] Deployment package prepared at {DEPLOY_DIR}/")
    print(f"[INFO] Total files: {len(files_to_deploy)}")
    print(f"[INFO] Upload all files from {DEPLOY_DIR}/ to HALO")
    print("\n" + "=" * 60)
    print("Waiting for deployment confirmation...")
    print("=" * 60)

    confirmed = False
    while not confirmed:
        choice = input("Deployment completed? (y/n): ").strip().lower()
        if choice == 'y':
            confirmed = True
        elif choice == 'n':
            print("[CANCELLED] Deployment not confirmed")
            return False

    # 8. 确认完成后的处理
    print("\n[INFO] Updating deployment status...")

    # 更新 CSV 中的 is_deployed
    updated_records = []
    for article_path, record in versions_dict.items():
        updated_record = record.copy()
        if article_path in [f['filename'] for f in files_to_deploy]:
            updated_record['is_deployed'] = 'True'
        updated_records.append(updated_record)

    write_versions_csv(updated_records)

    # 清空 deploy 文件夹
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)

    print(f"[OK] Deployment status updated")
    print(f"[OK] {len(files_to_deploy)} articles marked as deployed")
    print(f"[OK] Deploy folder cleared")

    return True

def prepare_deploy(version=None):
    """准备部署包"""

    # 1. 读取当前版本
    if not os.path.exists(VERSION_FILE):
        print("[ERROR] VERSION file not found")
        return False

    target_version = version
    if not target_version:
        target_version = open(VERSION_FILE, 'r').read().strip()

    print(f"[INFO] Preparing deployment for {target_version}...")

    # 2. 部署文章
    success = deploy_articles(target_version)

    return success

def main():
    import sys

    version = None
    if len(sys.argv) > 1:
        if sys.argv[1] == '--version' and len(sys.argv) > 2:
            version = sys.argv[2]

    try:
        success = prepare_deploy(version)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Failed to prepare deployment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
