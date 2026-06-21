#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys


def ensure_git_hooks():
    """检测仓库级 Git hooks(.husky/)是否已启用,未启用时提示安装。

    本项目用 husky(hooksPath 指向仓库根 .husky/)管理 pre-commit / commit-msg / pre-push。
    两种安装方式等价:
    - 前端:``cd Frontend && npm install``(其 prepare 脚本会执行 ``husky install``);
    - 通用:``sh scripts/install-git-hooks.sh``(不依赖 npm,纯 git config)。

    默认仅"提示",不擅自修改 git 配置;将环境变量 ``HOOKS_AUTO_INSTALL`` 设为
    1/true/yes/on 时,才自动执行安装脚本。
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    git_dir = os.path.join(base_dir, ".git")
    if not os.path.isdir(git_dir):
        return  # 非 git 工作区(如容器内),无需处理

    # 读取当前 hooksPath;已指向 .husky 说明 hooks 已启用,直接返回。
    try:
        hooks_path = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=base_dir,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001 - git 不可用时静默跳过
        return

    if hooks_path == ".husky":
        return

    installer = os.path.join(base_dir, "scripts", "install-git-hooks.sh")
    if not os.path.exists(installer):
        return

    auto = os.environ.get("HOOKS_AUTO_INSTALL", "0").strip().lower() in ("1", "true", "yes", "on")
    if not auto:
        print(
            "ℹ️ 未启用仓库级 Git hooks(.husky/)。"
            "如需启用,执行: sh scripts/install-git-hooks.sh "
            "(或 cd Frontend && npm install)。"
        )
        return

    print("🛠️ [自动配置] 正在安装仓库级 Git hooks...")
    try:
        subprocess.run(["sh", installer], cwd=base_dir, check=True)
        print("✅ Git hooks 安装成功!")
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️ Git hooks 自动安装失败,请手动执行 sh scripts/install-git-hooks.sh。错误: {exc}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings.dev")

    # 执行 Django 命令前,先检测仓库级 Git hooks 是否启用(默认仅提示)。
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


if __name__ == "__main__":
    main()
