# ---测试环境---
build_test:
	TAG=test docker-compose -f docker-compose-test.yml build

push_test:
	TAG=test docker-compose -f docker-compose-test.yml push

pull_test:
	TAG=test docker-compose -f docker-compose-test.yml pull

up_test:
	TAG=test docker-compose --compatibility -f docker-compose-test.yml up -d --remove-orphans

down_test:
	TAG=test docker-compose -f docker-compose-test.yml down --remove-orphans

restart_test:
	TAG=test docker-compose -f docker-compose-test.yml down --remove-orphans
	TAG=test docker-compose --compatibility -f docker-compose-test.yml up -d --remove-orphans

# 生产环境
build_prod:
	TAG=prod docker-compose -f docker-compose-prod.yml build

push_prod:
	TAG=prod docker-compose -f docker-compose-prod.yml push

pull_prod:
	TAG=prod docker-compose -f docker-compose-prod.yml pull

up_prod:
	TAG=prod docker-compose --compatibility -f docker-compose-prod.yml up -d --remove-orphans

down_prod:
	TAG=prod docker-compose -f docker-compose-prod.yml down --remove-orphans

restart_prod:
	TAG=prod docker-compose -f docker-compose-prod.yml down --remove-orphans
	TAG=prod docker-compose --compatibility -f docker-compose-prod.yml up -d --remove-orphans

# ─── 代码质量(被 .husky/ 的 git hooks 调用,也可手动执行) ───
# ruff 配置见 pyproject.toml

# 全量静态检查(pre-push 调用)
lint:
	ruff check .

# 全量静态检查并自动修复
lint-fix:
	ruff check --fix .

# 全量格式化
format:
	ruff format .

# 仅检查格式是否合规(不改文件,适合 CI)
format-check:
	ruff format --check .

# Django 单元测试:固定用 unittest settings(内存 SQLite + 本地内存缓存,不碰 MySQL/Redis)
# 指向 Backend/apps 目录做 discovery:覆盖该目录下所有 app 的 tests,新增 app 无需改命令。
test:
	DJANGO_SETTINGS_MODULE=Backend.settings.unittest python manage.py test Backend/apps

.PHONY: lint lint-fix format format-check test

