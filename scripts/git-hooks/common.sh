#!/usr/bin/env sh
#
# Git Hook 公共工具函数库。
#
# 被 .husky/ 下的各 hook 通过 `. "$ROOT_DIR/scripts/git-hooks/common.sh"` 加载。
# 仅提供当前仓库用得到的最小集合:统一输出、命令探测、Python 解释器探测。
#
# 设计取舍(相对参考项目精简):
# - 当前仓库只有 Backend + Frontend 两个模块,无 Admin、无 elegant-router 自动生成文件;
# - 不引入「分支 -> Django settings 映射」「.git-hooks.config 加载」等重型配置,
#   pre-push 的测试固定使用 Backend.settings.unittest(内存库,不碰任何 MySQL/Redis)。
#

# ── 统一输出(带符号前缀,便于在 hook 输出中快速定位) ──

print_section() {
  printf '\n▶ %s\n' "$1"
}

print_skip() {
  printf '⊘ %s\n' "$1"
}

print_warn() {
  printf '⚠ %s\n' "$1"
}

print_error() {
  printf '✗ %s\n' "$1" >&2
}

# ── 命令存在性校验:缺失则报错退出,避免 hook 中途以晦涩错误失败 ──

ensure_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    print_error "缺少命令: $1"
    exit 1
  fi
}

# ── Python 解释器探测 ──
# 优先级:HOOKS_PYTHON 环境变量 > 已激活的 conda 环境 > PATH 中的 python/python3。
# 供 pre-push 执行 Django 单元测试时定位解释器(GUI Git / IDE 触发时 PATH 可能不含 conda)。
detect_python_command() {
  if [ -n "${HOOKS_PYTHON:-}" ] && [ -x "${HOOKS_PYTHON}" ]; then
    printf '%s\n' "$HOOKS_PYTHON"
    return 0
  fi

  if [ -n "${CONDA_PREFIX:-}" ] && [ -x "${CONDA_PREFIX}/bin/python" ]; then
    printf '%s\n' "${CONDA_PREFIX}/bin/python"
    return 0
  fi

  for candidate in python python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return 0
    fi
  done

  return 1
}

# 校验指定 Python 是否能 import 某模块(用于 pre-push 确认 django 已安装)。
python_has_module() {
  "$1" -c "import $2" >/dev/null 2>&1
}

# ── git 工具 ──

# 判断 oid 是否为全零(新分支首次推送时 remote_oid 为全零)。
is_zero_oid() {
  [ "$1" = "0000000000000000000000000000000000000000" ]
}

# ── Hook 开关配置 ──
#
# 读取顺序:环境变量 > .git-hooks.config.local > .git-hooks.config。
# 仅在变量"尚未设置"时才从配置文件载入,从而让环境变量与 .local 拥有更高优先级。

# 把字符串规整为真假:1/true/yes/on -> 真(返回 0),其余 -> 假(返回 1)。
is_truthy() {
  normalized="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')"
  case "$normalized" in
    1 | true | yes | on) return 0 ;;
  esac
  return 1
}

# 从一个配置文件载入 KEY=VALUE;仅当该变量当前未设置时才赋值(保证优先级)。
_load_hook_config_file() {
  config_path="$1"
  [ -f "$config_path" ] || return 0

  while IFS= read -r raw_line || [ -n "$raw_line" ]; do
    # 去首尾空白
    line="$(printf '%s' "$raw_line" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    # 跳过空行与注释
    case "$line" in
      '' | \#*) continue ;;
    esac
    # 必须是 KEY=VALUE
    case "$line" in
      *=*) ;;
      *) continue ;;
    esac

    key="$(printf '%s' "${line%%=*}" | sed 's/[[:space:]]*$//')"
    value="${line#*=}"
    # 去掉行内注释(" #" 之后),再去首尾空白
    value="$(printf '%s' "$value" | sed 's/[[:space:]]#.*$//; s/^[[:space:]]*//; s/[[:space:]]*$//')"

    # 仅接受合法变量名
    printf '%s' "$key" | grep -Eq '^[A-Za-z_][A-Za-z0-9_]*$' || continue

    # 已设置(环境变量或更高优先级文件已赋值)则不覆盖
    eval "already_set=\${$key+x}"
    [ -n "$already_set" ] && continue

    export "$key=$value"
  done < "$config_path"
}

# 载入仓库 hook 配置:.local 先于默认文件(先载入者优先,因为已设置不覆盖)。
load_hook_config() {
  root_dir="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  _load_hook_config_file "$root_dir/.git-hooks.config.local"
  _load_hook_config_file "$root_dir/.git-hooks.config"
}

# 判断某个 hook 是否启用:先看总开关 HOOKS_ENABLED,再看分项开关。
# 用法:is_hook_enabled HOOKS_PRE_COMMIT
# 未配置的开关默认视为"启用"(默认值 1)。
is_hook_enabled() {
  item_var="$1"
  load_hook_config

  # 总开关:显式设置且为假 -> 全部禁用
  if [ -n "${HOOKS_ENABLED+x}" ] && ! is_truthy "${HOOKS_ENABLED}"; then
    return 1
  fi

  # 分项开关:未设置默认启用;设置了则按真假判断
  eval "item_value=\${$item_var:-1}"
  is_truthy "$item_value"
}
