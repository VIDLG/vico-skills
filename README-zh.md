# vico-skills

面向仓库内 `.vico/` 工作流的 Vico 技能集合，用于规划与执行。

English version: [README.md](README.md)
契约映射: [CONTRACTS-zh.md](CONTRACTS-zh.md)

## 为什么叫 Vico？

`Vico` 可以看作 `Wilco` 的一个变体。

- 它保留了 `Wilco` 里最有辨识度的 `-co` 发音骨架，所以名字虽然变了，但不会让人觉得完全断裂
- 它把更重、更硬的 `Wil` 感受换成了 `Vi`，让整体气质更靠近 vibe、轻量交互和低摩擦工作流
- 它想表达的是：内核仍然是靠谱执行，但外层更轻，更自然，默认从轻，按需升级，复杂度下降时也能再降级

当前仓库里的 skill 名称仍然沿用 `vico-*`。`vico-skills` 表示的是这整套工作流的项目品牌，而不是要求立刻改掉所有 skill 名称。

## 技能列表

- `vico-grill`
  面向任意主题的持续追问；在仓库证据还没成为主约束之前，用来拷问想法、决策和取舍。
- `vico-plan`
  唯一默认入口；负责判断 `no-doc / plan_only / prd_backed`、轻量对账、创建或更新 active plan，并吸收 probe handoff。
- `vico-exec`
  按 active plan 持续执行，直到完成或遇到真实阻塞。
- `vico-probe`
  检查当前 plan、设计或代码库；先扫描问题，再按需追问，并产出可被 `vico-plan` 消费的 handoff block。
- `vico-feedback`
  把针对 `vico-skills` 的反馈整理成 GitHub issue 草稿，并在用户明确确认后再发 issue。

`vico-probe` 的输出示例见 [vico-probe/references/output-format.md](vico-probe/references/output-format.md)。

## 默认模型

- `vico-skills` 是强意见、强路由的工作流，不是松散工具箱
- `vico-plan` 是唯一默认入口
- `vico-plan` 内部负责 bootstrap、轻量 reconcile、PRD 升级和 active slug 替换
- `vico-plan` 还应暴露显式模式，例如 `help`、`review`、`sync`、`prd`、`replace`、`close`、`cancel`
- `plan_only` 是默认的 tracked workflow
- `PRD` 是内部升级路径，不是默认入口
- slug 一旦升级到 `prd_backed`，就不再原地降级
- 临时 reconcile 状态仍然可能存在，但 `resume` 不再是主要用户入口
- 每个 tracked slug 都应有 `.vico/index/<slug>.json`
- `index` 是派生出来的 linkage metadata，不是主文档

## 设计原则

`默认从轻，按需升级。`

- `vico-skills` 的目标是在低复杂度下保持 vibe-friendly，只在工作真正需要时才升级到更正式的流程
- probing 和 execution 是两条独立的升级轴，不是单条强制的重流程
- freeform grilling 是最轻的追问通道
- 问题澄清强度和执行结构强度是两条独立的升级轴，不是单条强制的重流程
- freeform grilling 是最轻的问题澄清通道，`vico-probe` 是面向仓库对象的正式问题澄清通道
- freeform questioning 可以从 `vico-grill` 升级到 `vico-probe` 或 `vico-plan`，当下一个关键约束变成仓库现实或 tracked execution 时再升级
- probing 可以从直接澄清逐步升级到 `vico-probe`、`scan`、`grill`
- execution 可以从直接 vibe 式执行逐步升级到 `vico-plan`、`prd_backed`、`vico-exec`
- 更重的模式是为了降低歧义和协作成本，不是为了给每个任务预先加流程
- workflow re-entry 是一等能力：工作可以在 vibe execution 与 tracked workflow 之间往返，而不应被视为异常状态
- direct execution 可以发生在 tracked workflow 之前、之中或之后；当 workflow 恢复时，当前 Vico 路由应先根据仓库现实做 reconcile，再决定是否继续信任 `.vico` 状态

### 升级坐标图

```text
更高的执行结构强度
^
|                                      vico-exec
|                           vico-plan (plan_only / prd_backed)
|                  vico-probe -> vico-plan
|         vico-probe
|  vico-grill
+------------------------------------------------------------> 更高的问题澄清强度
  direct vibe execution
```

- 横轴：问题澄清强度
  在开始行动前，需要多少 discovery、clarification 和基于仓库现实的判断
- 纵轴：执行结构强度
  这项工作现在需要多少持久化计划、协作约束和可重复执行机制
- 当问题还不够清楚、仍有争议时，向右移动。
- 当执行需要更强的 contract、artifact 或持久状态时，向上移动。

owner map、派生层、同步边界、分发前提和 validator 责任见 [CONTRACTS-zh.md](CONTRACTS-zh.md)。

## 落盘原则

- `vico-grill`：默认把 freeform grill state 保持在会话内，不写 `.vico` artifact
- `vico-probe`：默认把 probe state 保持在会话内；只有用户明确要求写回时才落盘
- `vico-plan`：只要在塑造 tracked work，就默认写入或更新 active plan、可选 PRD 和派生 index
- `vico-exec`：当连续执行依赖准确状态，或用户希望文档保持最新时，落盘 plan、index 或临时 reconcile 更新

## 最常用路径

- 自由追问：`vico-grill`
- 自由追问后进入正式检查：`vico-grill -> vico-probe`
- 自由追问后直接立项：`vico-grill -> vico-plan`
- 直接 vibe 式执行：不需要 tracked workflow 时，直接对话并立即实现
- 先检查再规划：`vico-probe -> vico-plan`
- 继续细化现有 plan：`vico-probe grill plan -> vico-plan`
- 只做 tracked planning：`vico-plan`
- 跨 agent handoff：`Codex vico-plan -> Claude Code vico-exec`
- Claude runner 循环：`Codex vico-plan -> Claude runner -> vico-plan verify`
- 端到端 tracked execution：`vico-plan -> vico-exec -> vico-plan close`

## 升级提示

- 当你想围绕一个想法、决策或取舍做自由追问，而仓库证据还没成为核心约束时，使用 `vico-grill`
- 当任务局部、低风险、且不需要跨轮 tracked 协调时，停留在直接 vibe 式执行
- 当对象不清晰、有争议，或明显适合先做 evidence-first 追问时，使用 `vico-probe`
- 当工作应升级为 `.vico/` 下的 tracked execution contract 时，使用 `vico-plan`
- 只有在 active plan 已经存在、且用户希望持续推进直到真正完成或遇到真实阻塞时，才进入 `vico-exec`
- 如果 tracked work 又缩回到局部、低风险修改，优先降级回 `direct_execute`

## Route Shifts

- `vico-grill -> vico-probe`：当 freeform 追问已经碰到 repo plan、PRD、design、codebase，或下一个判断必须依赖仓库证据时升级
- `vico-grill -> vico-plan`：当追问结果已经足以定义 `.vico/` 下的 tracked work 时升级
- `direct_execute -> vico-plan`：当轻量执行演化成 tracked work 时，`vico-plan` 应自动做最小 reconcile / sync，重新锚定当前代码现实
- `vico-plan -> direct_execute`：当剩余工作已经足够小且低风险时，优先回到更轻的执行路径，而不是继续把用户留在重流程里
- `vico-probe -> direct_execute`：当 probe 已经确认下一步是局部实现时，直接路由去做，不要强行再过 planning
- 如果 tracked work 又缩回到局部、低风险修改，优先降级回 `direct_execute`

## 自然触发词

- `vico-grill`：`grill 这个想法`、`grill 我`、`拷问这个决策`、`deep interview 这个问题`、`discuss 这个取舍`、`vico-grill 如何使用`
- `vico-probe`：`scan 仓库`、`inspect codebase`、`grill 这个 plan`、`grill 这个 PRD`、`继续细化这个 plan`、`vico-probe 如何使用`
- `vico-plan`：`做个计划`、`建个 tracked plan`、`整理成执行步骤`、`对账当前 plan`、`verify一下`、`verify this plan`、`verify close`、`verify sync`、`verify replan`、`close 这个 plan`、`把这些规则导出到 AGENTS.md`、`把 operating brief 写到 CLAUDE.md`、`vico-plan 如何使用`
- `vico-exec`：`继续做`、`一直做到完成`、`执行 active plan`、`除非阻塞否则继续`、`vico-exec cc`、`用 cc 跑这个 plan`、`切到 cc`、`vico-exec 如何使用`
- `vico-feedback`：`提个 issue`、`报告 bug`、`我对 vico-skills 有反馈`、`整理成 GitHub issue`、`vico-feedback 如何使用`

如果一条自然语言请求同时可能落到多个 route 上，优先用一句简短确认来消歧，不要直接猜。
如果用户只说 `grill 这个`、`grill 这个问题`，且没有点名 repo object，优先走 `vico-grill`。
如果用户说的是 `grill 这个 plan`、`grill 这个 PRD`，或直接指向 `.vico` artifact，优先走 `vico-probe`。

## 路由可见性

- 一旦选中了某个 Vico skill，第一条可见 update 应显式展示当前 skill 和路由原因。
- 推荐形状：
  - `Skill route: <skill-name>`
  - `Route reason: <natural trigger | explicit skill request>`
- 如果是显式 skill 调用，也应说明这是显式 skill 请求，而不是自然触发命中。

## 什么时候用哪个 Skill

- 需要先围绕想法、决策或取舍做高强度自由追问：`vico-grill`
- 需要开始、更新、对账或重建 tracked work：`vico-plan`
- 需要在 close-out 前根据真实代码库核实 plan 是否真的完成：`vico-plan verify`
- 基于 active plan 继续实现：`vico-exec`
- 需要对 tracked work 做 close-out 或 cancel 并删除 active docs：`vico-plan`
- 需要判断怎么做架构沉淀：`vico-plan`
- 需要先对 plan、设计或代码库做深入检查：`vico-probe`
- 需要把反馈整理成 GitHub issue 草稿，或确认后直接发 issue：`vico-feedback`

`vico-feedback` 默认应根据用户表达和上下文自动归类为 `bug`、`ux_friction`、`contract_gap` 或 `feature_request`，只有类别确实不清楚时才反问用户。
如果存在明显重复的 issue，`vico-feedback` 应优先建议 `create`、`reopen` 或 `comment`，而不是默认新建。

## 反馈流程

如果你在 `vico-skills` 里遇到 bug、工作流不顺、命名别扭，或者发现 feature gap，就用 `vico-feedback`。

典型流程：

1. 用自然语言描述问题。
2. 让 `vico-feedback` 自动归类并生成 issue 草稿。
3. 先检查草稿内容和重复 issue 处理建议。
4. 只有当你真的想对 GitHub 执行动作时，再说 `create it`、`reopen it` 或 `comment there`。

示例输入：

- `我对 vico-skills 有反馈`
- `这个 workflow 有点别扭`
- `报告 vico-plan 的一个 bug`
- `把这个整理成 GitHub issue`

## 自动化脚本

- `vico-plan/scripts/bootstrap_vico_slug.py`
  当 `vico-plan` 判断需要新 slug 时，为其创建最小骨架。
- `vico-plan/scripts/sync_vico_headers.py`
  同步 plan / PRD 的 header 和交叉引用。
- `vico-plan/scripts/sync_vico_index.py`
  从当前 artifact 重新生成最小化 `.vico/index/*.json`。
- `vico-plan/scripts/close_vico_slug.py`
  删除已完成 slug 的 active docs，并清理临时 resume / index 状态。
- `vico-plan/scripts/validate_vico_workspace.py`
  按 Vico schema 校验当前 `.vico` 工作区。
- `scripts/validate_vico_skills.py`
  校验整个 Vico skill 仓库、辅助脚本和测试。

## 安装与卸载

推荐安装方式：使用 `npx skills@latest`。

### 用 `npx skills@latest` 安装

为指定 agent 安装单个 skill：

```bash
npx skills@latest add VIDLG/vico-skills --skill vico-grill --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-probe --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-plan --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-exec --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-feedback --agent codex
```

为所有受支持的 agents 安装全部 Vico skills：

```bash
npx skills@latest add VIDLG/vico-skills --all
```

只列出可安装的 skills，不实际安装：

```bash
npx skills@latest add VIDLG/vico-skills --list
```

`skills` CLI 也支持直接接 GitHub URL。
如果是 Claude Code，把命令里的 `--agent codex` 改成 `--agent claude-code` 即可。

参考链接：

- Vercel Skills 文档：https://vercel.com/docs/agent-resources/skills
- Vercel skills 使用指南：https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context

### 开发期 Link

本地开发时，推荐把 skill 目录 link 到目标 agent 的 skills 目录，而不是复制内容。

- Codex：link 到 `.codex/skills/`
- Claude Code：link 到 `.claude/skills/`
- Unix-like 系统：使用 `ln -s`
- Windows：使用 symbolic link 或 junction

### 卸载

用 `npx skills@latest` 卸载单个 skill：

```bash
npx skills@latest remove vico-grill
npx skills@latest remove vico-probe
npx skills@latest remove vico-plan
npx skills@latest remove vico-exec
npx skills@latest remove vico-feedback
```

如果你走的是开发期 link，直接删除对应 agent skills 目录里的 link 即可。

## 常见流程

### 开始或对账工作

```text
vico-plan
```

### 查看当前状态

```text
vico-plan review
```

### Close-Out 前先 Verify

```text
vico-plan verify
```

`verify` 的结果应同时给出：

- 面向用户的 `Recommended action`
- 面向 workflow 的 `Recommended Next Mode`

### Verify 通过后直接 Close

```text
vico-plan verify close
```

### Verify 后直接 Sync

```text
vico-plan verify sync
```

### Verify 后直接 Replan

```text
vico-plan verify replan
```

### 查看可用模式

```text
vico-plan help
```

### 先 Probe 再 Plan

```text
vico-probe -> vico-plan
```

### 导出仓库操作说明

```text
vico-plan export-md AGENTS.md
vico-plan export-md CLAUDE.md
```

当你希望把当前 Vico discipline 和 repo-local workflow 规则导出到项目里的说明文件时，用这个 mode。

### 查看可用模式

```text
vico-exec help
vico-probe help
```

## Probe 工作流

- `vico-probe`
  - 默认入口；先做轻量 scan，再根据 issue state 决定是直接建议、发一问、进入 `review`，还是直接收口
- `vico-probe scan`
  - 只做深度检查；建立 evidence、issues 和 topic map，不进入长追问
- `vico-probe grill`
  - 强制进入持续性的高强度追问模式，围绕最重要的未决问题连续发问
- `vico-probe grill plan`
  - 把当前 active plan 当作被 grill 的对象；当低风险澄清可以立即落地时，直接 refine plan 文本
- `vico-probe review`
  - 查看当前已接受结论、未决问题和推荐下一步
- `vico-probe resolve`
  - 停止追问，输出 final summary 或给 `vico-plan` 的 `Probe Handoff`
- `vico-probe help`
  - 查看模式和推荐使用方式

### 执行后手动 Close

```text
vico-exec -> 用户确认 -> vico-plan close
```

即使用户表达的是“做到真正完成”，生命周期仍然保持简单：

- `vico-exec` 负责完成实现并同步 plan
- `vico-plan close` 负责 close-out 删除
- agent 应在展示完成证据后停下，等待用户手动输入 close 命令

### Codex 做 Plan，Claude 执行

```text
Codex: vico-plan -> Claude Code: vico-exec
```

这是一条一等支持路径：

- Codex 可以先创建或细化 tracked plan
- Claude Code 可以接住 active plan 并执行
- handoff 通过 `.vico` artifact 完成，而不是依赖隐藏会话状态

### Claude Runner 循环

```bash
python3 vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon
```

当你希望 Claude Code 持续执行“实现 + verify + 判断是否继续”直到进入 `done`、`blocked`、`needs_user` 或 `stale_plan` 时，使用这个 runner。
自然入口可以直接说：`vico-exec cc`、`用 cc 跑这个 plan`、`切到 cc`。

## 外部参考

下面这些项目对 `vico-skills` 的形状有明显影响，但 Vico 仍然保持自己的 contract 和命名：

- [`forrestchang/andrej-karpathy-skills`](https://github.com/forrestchang/andrej-karpathy-skills)
  影响了我们对这几件事的强调：显式说出假设、持续施压简单性、外科式修改、以及目标驱动执行。这些思想和 Vico 里的 evidence-first probe、小范围改动、以及 verify 驱动的执行循环是高度一致的。
- [`mattpocock/skills` 的 `grill-me`](https://github.com/mattpocock/skills/tree/main/grill-me)
  影响了 `vico-grill` 这条 freeform grilling 通道，尤其是一问一答、持续拷问的风格。
- [`gsd-build/get-shit-done`](https://github.com/gsd-build/get-shit-done)
  影响了 repo-local planning artifact 和 context-engineered execution 这条思路。GSD 当前把规划状态放在 `.plans/` 下。
- [`Yeachan-Heo/oh-my-codex`](https://github.com/Yeachan-Heo/oh-my-codex)
  影响了“围绕 Codex 再包一层 workflow layer”的思路，包括 `.omx/` 下的持久状态，以及像 `$ralph` 这种 persistent completion loop。
- [`Yeachan-Heo/oh-my-claudecode`](https://github.com/Yeachan-Heo/oh-my-claudecode)
  影响了 Claude Code 这一侧的设计：team orchestration、分阶段执行流水线，以及 Codex/Claude 之间显式 handoff 的表面。

Vico 会刻意保持比这些系统更小、更 repo-native。这里是借鉴来源，不是兼容性目标。

## 开发说明

- `vico-skills/` 是单一事实来源。
- 开发时优先让项目内 `.codex/skills/` 和 `.claude/skills/` 指向这些目录，而不是复制内容。
- Claude Code 相关 hook 脚本在 `vico-exec/scripts/`，项目级 hook 配置在 `.claude/settings*.json`。
- Claude Code 更强的外层循环 runner 在 `vico-exec/scripts/claude_exec_runner.py`。

## 校验

运行：

```text
python3 vico-skills/scripts/validate_vico_skills.py
```

它会执行：

- 所有 skill 的 `quick_validate`
- 辅助 Python 脚本的 `py_compile`
- 基于 fixture 的自动化测试
- 轻量 workflow invariant 校验
- placeholder 和 `__pycache__` 清理校验
