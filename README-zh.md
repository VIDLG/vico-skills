# wilco-skills

面向仓库内 `.wilco/` 工作流的 Wilco 技能集合，用于规划与执行。

English version: [README.md](README.md)
契约映射: [CONTRACTS-zh.md](CONTRACTS-zh.md)

## 技能列表

- `wilco-plan`
  唯一默认入口；负责判断 `no-doc / plan_only / prd_backed`、轻量对账、创建或更新 active plan，并吸收 probe handoff。
- `wilco-exec`
  按 active plan 持续执行，直到完成或遇到真实阻塞。
- `wilco-probe`
  检查当前 plan、设计或代码库；先扫描问题，再按需追问，并产出可被 `wilco-plan` 消费的 handoff block。

`wilco-probe` 的输出示例见 [wilco-probe/references/output-format.md](wilco-probe/references/output-format.md)。

## 默认模型

- `wilco-skills` 是强意见、强路由的工作流，不是松散工具箱
- `wilco-plan` 是唯一默认入口
- `wilco-plan` 内部负责 bootstrap、轻量 reconcile、PRD 升级和 active slug 替换
- `wilco-plan` 还应暴露显式模式，例如 `help`、`review`、`sync`、`prd`、`replace`、`close`、`cancel`
- `plan_only` 是默认的 tracked workflow
- `PRD` 是内部升级路径，不是默认入口
- slug 一旦升级到 `prd_backed`，就不再原地降级
- 临时 reconcile 状态仍然可能存在，但 `resume` 不再是主要用户入口
- 每个 tracked slug 都应有 `.wilco/index/<slug>.json`
- `index` 是派生出来的 linkage metadata，不是主文档

## 设计原则

`默认从轻，按需升级。`

- `wilco-skills` 的目标是在低复杂度下保持 vibe-friendly，只在工作真正需要时才升级到更正式的流程
- probing 和 execution 是两条独立的升级轴，不是单条强制的重流程
- probing 可以从直接澄清逐步升级到 `wilco-probe`、`scan`、`grill`
- execution 可以从直接 vibe 式执行逐步升级到 `wilco-plan`、`prd_backed`、`wilco-exec`
- 更重的模式是为了降低歧义和协作成本，不是为了给每个任务预先加流程

owner map、派生层、同步边界、分发前提和 validator 责任见 [CONTRACTS-zh.md](CONTRACTS-zh.md)。

## 落盘原则

- `wilco-probe`：默认把 probe state 保持在会话内；只有用户明确要求写回时才落盘
- `wilco-plan`：只要在塑造 tracked work，就默认写入或更新 active plan、可选 PRD 和派生 index
- `wilco-exec`：当连续执行依赖准确状态，或用户希望文档保持最新时，落盘 plan、index 或临时 reconcile 更新

## 最常用路径

- 直接 vibe 式执行：不需要 tracked workflow 时，直接对话并立即实现
- 先检查再规划：`wilco-probe -> wilco-plan`
- 继续细化现有 plan：`wilco-probe grill plan -> wilco-plan`
- 只做 tracked planning：`wilco-plan`
- 端到端 tracked execution：`wilco-plan -> wilco-exec -> wilco-plan close`

## 升级提示

- 当任务局部、低风险、且不需要跨轮 tracked 协调时，停留在直接 vibe 式执行
- 当对象不清晰、有争议，或明显适合先做 evidence-first 追问时，使用 `wilco-probe`
- 当工作应升级为 `.wilco/` 下的 tracked execution contract 时，使用 `wilco-plan`
- 只有在 active plan 已经存在、且用户希望持续推进直到真正完成或遇到真实阻塞时，才进入 `wilco-exec`

## 自然触发词

- `wilco-probe`：`scan 仓库`、`inspect codebase`、`grill 这个 plan`、`继续细化这个 plan`、`wilco-probe 如何使用`
- `wilco-plan`：`做个计划`、`建个 tracked plan`、`整理成执行步骤`、`对账当前 plan`、`verify一下`、`verify this plan`、`verify close`、`verify sync`、`verify replan`、`wilco-plan 如何使用`
- `wilco-exec`：`继续做`、`一直做到完成`、`执行 active plan`、`除非阻塞否则继续`、`wilco-exec 如何使用`

如果一条自然语言请求同时可能落到多个 route 上，优先用一句简短确认来消歧，不要直接猜。

## 路由可见性

- 一旦选中了某个 Wilco skill，第一条可见 update 应显式展示当前 skill 和路由原因。
- 推荐形状：
  - `Skill route: wilco-probe`
  - `Route reason: natural trigger "scan the repo"`
- 如果是显式 skill 调用，也应说明这是显式 skill 请求，而不是自然触发命中。

## 什么时候用哪个 Skill

- 需要开始、更新、对账或重建 tracked work：`wilco-plan`
- 需要在 close-out 前根据真实代码库核实 plan 是否真的完成：`wilco-plan verify`
- 基于 active plan 继续实现：`wilco-exec`
- 需要对 tracked work 做 close-out 或 cancel 并删除 active docs：`wilco-plan`
- 需要判断怎么做架构沉淀：`wilco-plan`
- 需要先对 plan、设计或代码库做深入检查：`wilco-probe`

## 自动化脚本

- `wilco-plan/scripts/bootstrap_wilco_slug.py`
  当 `wilco-plan` 判断需要新 slug 时，为其创建最小骨架。
- `wilco-plan/scripts/sync_wilco_headers.py`
  同步 plan / PRD 的 header 和交叉引用。
- `wilco-plan/scripts/sync_wilco_index.py`
  从当前 artifact 重新生成最小化 `.wilco/index/*.json`。
- `wilco-plan/scripts/close_wilco_slug.py`
  删除已完成 slug 的 active docs，并清理临时 resume / index 状态。
- `wilco-plan/scripts/validate_wilco_workspace.py`
  按 Wilco schema 校验当前 `.wilco` 工作区。
- `scripts/validate_wilco_skills.py`
  校验整个 Wilco skill 仓库、辅助脚本和测试。

## 安装与卸载

推荐安装方式：使用 `npx skills@latest`。

### 用 `npx skills@latest` 安装

为指定 agent 安装单个 skill：

```bash
npx skills@latest add VIDLG/wilco-skills --skill wilco-probe --agent codex
npx skills@latest add VIDLG/wilco-skills --skill wilco-plan --agent codex
npx skills@latest add VIDLG/wilco-skills --skill wilco-exec --agent codex
```

为所有受支持的 agents 安装全部 Wilco skills：

```bash
npx skills@latest add VIDLG/wilco-skills --all
```

只列出可安装的 skills，不实际安装：

```bash
npx skills@latest add VIDLG/wilco-skills --list
```

`skills` CLI 也支持直接接 GitHub URL。
如果是 Claude Code，把命令里的 `--agent codex` 改成 `--agent claude-code` 即可。

### 开发期 Link

本地开发时，推荐把 skill 目录 link 到目标 agent 的 skills 目录，而不是复制内容。

- Codex：link 到 `.codex/skills/`
- Claude Code：link 到 `.claude/skills/`
- Unix-like 系统：使用 `ln -s`
- Windows：使用 symbolic link 或 junction

### 卸载

用 `npx skills@latest` 卸载单个 skill：

```bash
npx skills@latest remove wilco-probe
npx skills@latest remove wilco-plan
npx skills@latest remove wilco-exec
```

如果你走的是开发期 link，直接删除对应 agent skills 目录里的 link 即可。

## 常见流程

### 开始或对账工作

```text
wilco-plan
```

### 查看当前状态

```text
wilco-plan review
```

### Close-Out 前先 Verify

```text
wilco-plan verify
```

### Verify 通过后直接 Close

```text
wilco-plan verify close
```

### Verify 后直接 Sync

```text
wilco-plan verify sync
```

### Verify 后直接 Replan

```text
wilco-plan verify replan
```

### 查看可用模式

```text
wilco-plan help
```

### 先 Probe 再 Plan

```text
wilco-probe -> wilco-plan
```

### 查看可用模式

```text
wilco-exec help
wilco-probe help
```

## Probe 工作流

- `wilco-probe`
  - 默认入口；先做轻量 scan，再根据 issue state 决定是直接建议、发一问、进入 `review`，还是直接收口
- `wilco-probe scan`
  - 只做深度检查；建立 evidence、issues 和 topic map，不进入长追问
- `wilco-probe grill`
  - 强制进入持续性的高强度追问模式，围绕最重要的未决问题连续发问
- `wilco-probe grill plan`
  - 把当前 active plan 当作被 grill 的对象；当低风险澄清可以立即落地时，直接 refine plan 文本
- `wilco-probe review`
  - 查看当前已接受结论、未决问题和推荐下一步
- `wilco-probe resolve`
  - 停止追问，输出 final summary 或给 `wilco-plan` 的 `Probe Handoff`
- `wilco-probe help`
  - 查看模式和推荐使用方式

### 执行并完成

```text
wilco-exec -> wilco-plan close
```

即使用户表达的是“做到真正完成”，生命周期仍然保持简单：

- `wilco-exec` 负责完成实现并同步 plan
- `wilco-plan close` 负责 close-out 删除
- agent 可以在执行结束后自动路由到 `wilco-plan close`，不要求用户手动记住第二步

## 开发说明

- `wilco-skills/` 是单一事实来源。
- 开发时优先让项目内 `.codex/skills/` 和 `.claude/skills/` 指向这些目录，而不是复制内容。
- Claude Code 相关 hook 脚本在 `wilco-exec/scripts/`，项目级 hook 配置在 `.claude/settings*.json`。

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
