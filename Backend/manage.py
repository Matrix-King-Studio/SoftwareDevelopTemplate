#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def ensure_git_hooks():
    """检测并自动安装 pre-commit 钩子"""
    # 往上找两级，找到 .git 隐藏目录和 hook 的目标路径
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    git_dir = os.path.join(base_dir, '.git')
    hook_path = os.path.join(git_dir, 'hooks', 'pre-commit')
    
    # 如果是 Git 仓库，且 pre-commit 钩子还没安装
    if os.path.exists(git_dir) and not os.path.exists(hook_path):
        print("🛠️ [自动配置] 未检测到 Git 提交拦截钩子，正在为您自动安装...")
        try:
            # 自动帮用户执行 pre-commit install
            subprocess.run(["pre-commit", "install"], cwd=base_dir, check=True)
            print("✅ 拦截钩子自动安装成功！")
        except Exception as e:
            print(f"⚠️ 自动安装失败，请确保已通过 pip install pre-commit 安装依赖。错误: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings.dev')
    
    # 👇 在执行任何 Django 命令前，先偷偷执行我们的检测函数
    ensure_git_hooks()
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
