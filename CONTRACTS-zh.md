# Wilco 契约映射

这是一份 owner / derived / validator 边界治理文档。
它不是用户工作流说明，也不是第二份 skill 行为真相源。

## 分发前提

- 运行时应对单个 skill 的安装和使用安全。
- 运行时不能依赖仓库根 `README.md`。
- 运行时不能依赖跨 skill 路径。
- 共享运行时需求应通过 owner 源加 skill 本地闭包来满足。

## 落盘原则

- `wilco-probe` 的状态默认仅存在于会话中，只有用户明确要求时才应写回。
- `wilco-plan` 负责 active plan、可选 PRD 以及派生 index 的 tracked-doc 写入。
- `wilco-exec` 只在连续执行依赖准确持久化状态时，才写入 plan、index 或临时 reconcile 状态。

## 面向用户 vs 内部状态

- 面向用户的输出应优先呈现让用户继续推进所需的最小结论、决策和下一步。
- 只要额外细节主要服务于路由、连续性或校验，内部状态可以比面向用户的输出更丰富。
- 不要把完整的内部调度图、issue bank 或执行启发式默认直接摊给用户，除非用户明确要求这些细节，或这些细节会实质影响下一步决策。
- 即使外围文案为了用户可读性做了优化，机器消费字段也应保持稳定。
- 一旦选中了某个 Wilco skill，应在第一条可见 update 中显式展示当前 skill 路由和路由原因，让用户能区分 skill 路由行为与普通模型行为。
- 当输出的是面向用户的 checkpoint、summary、verification result 或 handoff 时，如果下一步动作并不显而易见，优先给出 `Recommended action`。
- `Recommended action` 的标准取值统一为：
  - `direct_execute`
  - `wilco-plan`
  - `wilco-plan -> wilco-exec`

## 核验权威性

- `Status`、checklist 完成情况、以及 index linkage 只是 operational planning signals，不是最终完成证明。
- 最终是否允许 close-out，应由 `wilco-plan verify` 基于当前代码库证据来 gate。

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
| Skill 行为契约 | 每个 `<skill>/SKILL.md` | `<skill>/agents/openai.yaml`、skill 本地 references、examples | 检查 skill body 存在、引用资源存在、agent 摘要没有长成第二份完整契约 |
| 共享脚本 | owner 脚本文件，目前在 `wilco-plan/scripts/` | 仍然需要时放在 `<skill>/scripts/` 下的本地包装入口 | 检查 owner 源存在、需要的本地入口存在、运行时引用不再跨 skill |
| 共享状态与决策规则 | owner reference 文件，目前在 `wilco-plan/references/` | 需要运行时可见的 skill 本地完整副本 | 检查 owner 文件存在、所需本地副本存在、并把副本视为派生产物 |
| 强结构模板 | owner template 文件，如 `plan-template.md`、`prd-template.md`、`reconcile-output-template.md` | 满足运行时闭包所需的本地可见副本或本地引用 | 检查 owner 模板存在、所需本地闭包存在、关键结构保持稳定 |
| feedback / issue 模板 | `wilco-feedback/references/` 下的 owner 模板 | `wilco-feedback` 中的 issue draft 与发 issue 流程 | 检查草稿模板存在、保持简洁、并明确确认边界 |
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
