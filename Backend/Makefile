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
