#!/usr/bin/env sh
#
# 仓库级 Git hooks 安装器。
#
# 作用:把 Git 的 hooksPath 指向仓库根的 .husky/,并为其中的 hook 脚本补上可执行权限。
# 与 husky 解耦:不依赖 npm / node,Backend 开发者(无前端环境)也能直接运行本脚本启用钩子。
#
# 用法:
#   sh scripts/install-git-hooks.sh
#
# 说明:
#   Frontend 安装依赖时 `npm run prepare` 会调用 `husky install`,效果等价(同样设置 core.hooksPath=.husky)。
#   两条路径任选其一即可;本脚本是不经过 npm 的等价入口。

set -eu

# 解析仓库根目录(本脚本位于 scripts/ 下,上一级即仓库根)。
ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

cd "$ROOT_DIR"

# 必须在 git 工作区内。
git rev-parse --is-inside-work-tree >/dev/null 2>&1

# 指向仓库根的 .husky 目录。
git config core.hooksPath .husky

# 为所有 hook 脚本补可执行权限(排除 _/.gitignore)。
find .husky -type f ! -name '.gitignore' -exec chmod +x {} +

printf 'Git hooks 已安装:core.hooksPath = .husky\n'
