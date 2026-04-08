# wilco-skills

面向仓库内 `.wilco/` 工作流的 Wilco 技能集合，用于任务初始化、规划、执行、对账、归档和文档治理。

English version: [README.md](README.md)

## 技能列表

- `wilco-init`
  新任务第一次进入 `.wilco` 时使用，创建最小有效 artifact 集合。
- `wilco-plan`
  默认跟踪工作流，用来创建或更新执行计划。
- `wilco-prd`
  只有在 `plan-only` 不够时才创建或更新 PRD。
- `wilco-resume`
  对账 `.wilco`、代码和测试，判断真实当前状态。
- `wilco-execute`
  按 active plan 持续执行，直到完成或遇到真实阻塞。
- `wilco-cleanup`
  对已完成或已废弃的 slug 做收尾、归档和临时状态清理。
- `wilco-docs`
  管理 `.wilco` 与 `docs/` 的边界、生命周期和归档规则。
- `wilco-grill`
  对当前 PRD、plan 或设计做压力测试式追问。

`wilco-grill` 的输出示例见 [wilco-grill/references/output-format.md](wilco-grill/references/output-format.md)。

## 默认模型

- `wilco-skills` 是强意见、强路由的工作流，不是松散工具箱
- 新的 tracked work 必须先经 `wilco-init`
- `plan-only` 是默认的 tracked workflow
- `PRD` 是升级路径，不是默认要求
- `resume` 是临时交接/恢复快照
- 每个 tracked slug 都应有 `.wilco/index/<slug>.json`
- `index` 是派生出来的 linkage metadata，不是主文档

## 什么时候用哪个 Skill

- 新的 tracked work，还没有 slug：`wilco-init`
- 已有 slug，需要补或修执行计划：`wilco-plan`
- 已有 slug，但 scope / acceptance 变了：`wilco-prd` + `wilco-plan`
- `.wilco` 看起来过期或不同步：先 `wilco-resume`
- 基于 active plan 继续实现：`wilco-execute`
- 工作已经基本完成，需要归档收尾：`wilco-cleanup`
- 需要判断文档放哪、怎么归档、怎么做架构沉淀：`wilco-docs`

不要从 `wilco-plan` 或 `wilco-prd` 直接为新 tracked work 开新入口。它们可以直接更新已有 slug，但新的 tracked work 应先通过 `wilco-init` 进入工作流。

## 自动化脚本

- `wilco-init/scripts/bootstrap_wilco_slug.py`
  为新 slug 创建初始 plan / PRD / architecture 骨架。
- `wilco-docs/scripts/sync_wilco_headers.py`
  同步 plan / PRD 的 header 和交叉引用。
- `wilco-docs/scripts/sync_wilco_index.py`
  从当前 artifact 重新生成最小化 `.wilco/index/*.json`。
- `wilco-docs/scripts/close_wilco_slug.py`
  归档已完成 slug，并清理临时 resume / index 状态。
- `wilco-docs/scripts/validate_wilco_workspace.py`
  按 Wilco schema 校验当前 `.wilco` 工作区。
- `scripts/validate_wilco_skills.py`
  校验整个 Wilco skill 仓库、辅助脚本和测试。

## 常见流程

### 新任务进入 Wilco

```text
wilco-init -> wilco-plan
```

或者：

```text
wilco-init -> wilco-prd -> wilco-plan
```

### `.wilco` 不同步 / 失真

```text
wilco-resume -> wilco-plan
wilco-resume -> wilco-prd -> wilco-plan
wilco-resume -> wilco-docs
```

### 执行并收尾

```text
wilco-execute -> wilco-cleanup
```

即使用户表达的是“做到真正完成”，skill 边界仍然保持分离：

- `wilco-execute` 负责完成实现并同步 plan
- `wilco-cleanup` 负责 `close-archive`
- agent 可以在执行结束后自动路由到 `wilco-cleanup`，不要求用户手动记住第二步

## 开发说明

- `wilco-skills/` 是单一事实来源。
- 开发时优先让项目内 `.codex/skills/` 和 `.claude/skills/` 指向这些目录，而不是复制内容。
- Claude Code 相关 hook 脚本在 `wilco-execute/scripts/`，项目级 hook 配置在 `.claude/settings*.json`。

## 校验

运行：

```text
python3 wilco-skills/scripts/validate_wilco_skills.py
```

它会执行：

- 所有 skill 的 `quick_validate`
- 辅助 Python 脚本的 `py_compile`
- 基于 fixture 的自动化测试
- 轻量 workflow invariant 校验
- placeholder 和 `__pycache__` 清理校验
