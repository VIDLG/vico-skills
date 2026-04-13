# Vico 契约映射

这是一份 owner / derived / validator 边界治理文档。
它不是用户工作流说明，也不是第二份 skill 行为真相源。

## 分发前提

- `vico-skills` 按一整套 repo-local workflow set 设计。
- 运行时不能依赖仓库根 `README.md`。
- shared runtime、CLI、adapter 需求可以放在 `runtime/`、`adapters/` 这类 repo-level owner 层。
- 如果稳定的 skill-local wrapper 路径对使用者更友好，可以保留，但不得取代 owner source。

## 落盘原则

- `vico-ground` 的状态默认仅存在于会话中；除非用户明确要求 capture 或 export 结论，否则不应写入 `.vico` artifact。
- `vico-plan` 负责 active plan、可选 PRD 以及派生 index 的 tracked-doc 写入。
- `vico-exec` 只在连续执行依赖准确持久化状态时，才写入 plan、index 或临时 reconcile 状态。

## 面向用户 vs 内部状态

- 面向用户的输出应优先呈现让用户继续推进所需的最小结论、决策和下一步。
- 只要额外细节主要服务于路由、连续性或校验，内部状态可以比面向用户的输出更丰富。
- 不要把完整的内部调度图、issue bank 或执行启发式默认直接摊给用户，除非用户明确要求这些细节，或这些细节会实质影响下一步决策。
- 不要把 `vico-ground` 中仍然停留在假设层或未充分 grounding 的结论包装成基于仓库证据的发现，或包装成已经成立的 tracked-plan 承诺。
- 即使外围文案为了用户可读性做了优化，机器消费字段也应保持稳定。
- 一旦选中了某个 Vico skill，应在第一条可见 update 中显式展示当前 skill 路由和路由原因，让用户能区分 skill 路由行为与普通模型行为。
- 当输出的是面向用户的 checkpoint、summary、verification result 或 handoff 时，如果下一步动作并不显而易见，优先显式给出路由和下一步动作。
- 对 `vico-ground`，优先使用这一对字段：
  - `Next route`
  - `Recommended next action`
- 路由字面值应保持稳定，尤其是：
  - `direct_execute`
  - `vico-plan`
  - `stay_in_ground`
  - `vico-plan -> vico-exec`

## Trigger Model

- Vico skill 的路由应先看意图簇，而不是只看字面 trigger phrase。
- 自然语言例子是强提示，不是唯一合法入口。
- phrase 列表主要用于提升召回，尤其是短口语表达；但不能让字面匹配压过更清楚的用户意图。
- 在锁定 skill 前，先检查 route 前置条件：
  - `vico-ground`：用户是在做整体摸底、查看、对齐、建图、challenge、review，或建立 shared ground
  - `vico-plan`：用户是在创建、对账、verify、replan tracked work
  - `vico-exec`：用户要持续推进实现，而且已经存在 active plan
  - `vico-feedback`：用户是在反馈 `vico-skills` 自身行为，或要求整理 / 发 issue
  - `vico-ops`：用户是在做 bootstrap、sync、close、cancel、truth extraction 或 repo-local workspace 校验
- 当同一句话可以合理落到多个 route 时，优先用一句短确认消歧。
- 当请求明显是窄范围、局部、且不需要 Vico workflow 时，优先 direct execution 或直接回答。
- `scan`、`quick pass`、`orient me`、`扫一下`、`摸底`、`盘一下`、`过一遍整体` 这类仓库摸底式表达，如果目标是整个 repo、架构、边界或整体结构，应视为 `vico-ground` 强信号。
- `做个计划`、`对一下 plan`、`verify 一下`、`replan 一下` 这类 tracked-work 表达，在 tracked work 已经进入上下文时，应视为 `vico-plan` 强信号。
- `继续做`、`一直做完`、`别停`、`接着跑`、`继续直到完成` 这类持续执行表达，只有在 active plan 已存在时才应视为 `vico-exec` 强信号。
- `提个 issue`、`记个反馈`、`这个体验别扭`、`这个触发不对`、`帮我整理成 issue` 这类反馈表达，在目标明确是 `vico-skills` 本身时，应视为 `vico-feedback` 强信号。
- `收尾`、`收口删除`、`sync 一下`、`close 这个 tracked work`、`cancel 这个 slug`、`校验一下 .vico` 这类维护表达，在 repo-local tracked state 已进入上下文时，应视为 `vico-ops` 强信号。

## Workflow Re-entry 规则

- workflow re-entry 是一等支持路径，不是异常路径。
- direct execution 可以发生在 tracked workflow 之前、之中或之后。
- 当 tracked workflow 恢复时，当前 Vico 路由应先根据仓库现实做 reconcile，再决定是否继续信任已经变旧的 `.vico` 状态。

## Route Shift 策略

- 升级和降级都应是合法的 workflow move。
- 当工作超出安全的局部执行范围时，应按需要升级到 `vico-plan` 或 `vico-exec`。
- 当工作又缩回到局部、低风险修改时，应优先回到 `direct_execute`，而不是继续把用户困在更重的流程里。
- 当 direct execution 之后重新回到 tracked workflow 时，应自动执行最小 reconcile / sync，让 `.vico` 状态重新对齐当前代码现实。

## 前向契约原则

- 默认按前向设计处理，并假设不存在历史负担；只有用户明确说兼容性重要时，才进入兼容性思维。
- 不要默认保留旧命名、别名、模式、文件或结构。
- 优先一个清晰契约，而不是长期并存的过渡表面。
- 当旧表面已经在误导当前系统时，优先直接替换，而不是继续背兼容层。
- 先更新 owner source，再刷新派生层，最后移除过时表面。

## 核验权威性

- `Status`、checklist 完成情况、以及 index linkage 只是 operational planning signals，不是最终完成证明。
- 最终是否允许 close-out，应由 `vico-plan verify` 基于当前代码库证据来 gate。

## 公开模式名 vs 状态值

- 面向用户的 workflow 动作应使用稳定的 mode 名，例如 `close`、`cancel`、`verify`、`sync`、`replan`。
- `done`、`partial`、`not_started` 这类字面量继续作为状态/进度词汇，而不是公开 close-out 命令名。

## 外部副作用

- 创建、重开、评论、关闭 GitHub issue 这类外部副作用，默认都需要用户显式确认。
- issue 草稿生成和重复检查可以默认进行；真正修改外部系统不应默认发生。

## 契约层级

1. `全局 workflow 宪法`
   owner 源: [README.md](README.md)
2. `Skill 行为契约`
   owner 源: 每个 `<skill>/SKILL.md`
3. `共享结构契约`
   owner 源: 对应的 template、reference 或共享脚本源文件

## Owner 与派生层

| 契约类型 | Owner source | 派生层 | Validator 责任 |
| --- | --- | --- | --- |
| 全局 workflow 宪法 | `README.md` | skill 级引用、contract map 条目、workflow invariant checks | 检查 README 关键标记存在，并防止下游文档在核心不变量上漂移 |
| Skill 行为契约 | 每个 `<skill>/SKILL.md` | `<skill>/agents/openai.yaml`、skill 本地 references、examples | 检查 skill body 存在、引用资源存在、`Agent Summary` 块保持结构化、agent 摘要没有长成第二份完整契约 |
| 共享脚本 | owner 脚本文件，目前在 `runtime/vico_artifacts/` | 仍然需要时放在 `<skill>/scripts/` 下的本地包装入口 | 检查 owner 源存在、需要的本地入口存在、运行时引用不再跨 skill |
| 仓库本地 CLI owner | `runtime/cli/` 下的 owner CLI 文件 | 当仍需要稳定命令路径时，放在 `<skill>/scripts/` 下的本地 wrapper | 检查 owner CLI 存在、wrapper 保持轻薄、repo-local 自动化逻辑不再漂移到重复入口 |
| 平台适配层 | `adapters/` 下的 owner 适配器文件 | 仍然需要稳定 skill 本地路径时放在 `<skill>/scripts/` 下的包装入口 | 检查 owner 适配器存在、wrapper 保持轻薄、平台特有逻辑不再回流进 skill 契约 |
| 共享状态与决策规则 | owner reference 文件，目前在 `vico-plan/references/` | 需要运行时可见的 skill 本地完整副本 | 检查 owner 文件存在、所需本地副本存在、并把副本视为派生产物 |
| 强结构模板 | owner template 文件，如 `plan-template.md`、`prd-template.md`、`reconcile-output-template.md` | 满足运行时闭包所需的本地可见副本或本地引用 | 检查 owner 模板存在、所需本地闭包存在、关键结构保持稳定 |
| feedback / issue 模板 | `vico-feedback/references/` 下的 owner 模板 | `vico-feedback` 中的 issue draft 与发 issue 流程 | 检查草稿模板存在、保持简洁、并明确确认边界 |
| 契约映射 | `CONTRACTS.md` 与 `CONTRACTS-zh.md` | README 入口链接 | 检查映射文档存在，并让 owner/派生/validator 责任保持一致 |

## 同步策略

- 直接编辑 owner source。
- 派生层从 owner source 同步生成或刷新。
- 派生层默认只读。
- 如果某个派生文件需要 owner-specific 附加内容，必须把同步块和本地附加块显式隔离。
- 不要为了去重再引入新的顶层 shared source 目录。
- 只有高重复、结构稳定、跨多个 skill 的内容才值得进入同步体系。

### 第一批迁移顺序

1. 共享脚本
2. 状态与决策规则
3. 强结构模板

## Validator 责任

validator 的责任应显式分层，而不是笼统写成“一致性检查”。至少应覆盖：

- owner source existence
- derived-form presence
- sync-boundary enforcement
- read-only generated content rules

## 说明

- 这份文档负责治理边界，不替代 README、SKILL.md 或 owner 模板本身。
- 当契约变更时，应先改 owner 源，再刷新派生层，最后补 validator 覆盖。
