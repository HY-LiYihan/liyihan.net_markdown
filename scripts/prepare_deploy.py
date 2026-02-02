#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

VERSION_FILE = 'VERSION'
VERSIONS_DIR = 'versions'
DEPLOY_DIR = 'deploy'
CATEGORIES = ['Linux', '工具', '开发']

def get_file_list(directory):
    """获取目录下所有 Markdown 文件（递归）"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, directory)
                files.append(rel_path)
    return files

def prepare_deploy():
    """准备部署包（只包含新增内容）"""

    # 1. 读取当前版本
    if not os.path.exists(VERSION_FILE):
        print("[ERROR] VERSION file not found")
        return False

    current_version = open(VERSION_FILE, 'r').read().strip()
    print(f"[INFO] Preparing deployment for {current_version}...")

    # 2. 获取上一个版本
    parts = current_version.split('.')
    if len(parts) != 2:
        print("[ERROR] Invalid version format")
        return False

    major, minor = int(parts[0][1:]), int(parts[1])
    if minor == 0:
        previous_version = None
        print("[INFO] First version, deploying all files...")
    else:
        previous_version = f"v{major}.{minor-1}"
        print(f"[INFO] Previous version: {previous_version}")

    # 3. 清空并创建 deploy 目录
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    os.makedirs(DEPLOY_DIR)

    # 4. 提取新增文件
    current_version_dir = os.path.join(VERSIONS_DIR, current_version)
    if not os.path.exists(current_version_dir):
        print(f"[ERROR] Version {current_version} not found")
        return False

    new_files = []

    for category in CATEGORIES:
        category_dir = os.path.join(current_version_dir, category)
        if os.path.exists(category_dir):
            for file in os.listdir(category_dir):
                if file.endswith('.md'):
                    # 检查是否为新文件
                    is_new = True
                    if previous_version:
                        previous_file = os.path.join(VERSIONS_DIR, previous_version, category, file)
                        is_new = not os.path.exists(previous_file)

                    if is_new:
                        src = os.path.join(category_dir, file)
                        dst = os.path.join(DEPLOY_DIR, category, file)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                        new_files.append(f"{category}/{file}")
                        print(f"  [+] {category}/{file}")

    if not new_files:
        print("[WARNING] No new files to deploy")
        return False

    # 5. 生成清单文件
    manifest_path = os.path.join(DEPLOY_DIR, 'manifest.txt')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(f"Deployment Package for {current_version}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if previous_version:
            f.write(f"Previous version: {previous_version}\n")
        f.write(f"\nTotal files: {len(new_files)}\n")
        f.write(f"\nFiles:\n")
        for file in sorted(new_files):
            f.write(f"  - {file}\n")

    # 6. 完成
    print(f"\n[OK] Deployment package prepared at {DEPLOY_DIR}/")
    print(f"[INFO] Total new files: {len(new_files)}")
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
