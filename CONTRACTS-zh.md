# Wilco 契约映射

这是一份治理映射文档，不会反过来成为新的 workflow、skill 或 template 真相源。

## 分发前提

- 运行时应对单个 skill 的安装和使用安全。
- 运行时不能依赖仓库根 `README.md`。
- 运行时不能依赖 `../wilco-docs/...` 这类跨 skill 路径。
- 共享运行时需求应通过 owner 源加 skill 本地闭包来满足。

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
| 共享脚本 | owner 脚本文件，目前在 `wilco-docs/scripts/` | `<skill>/scripts/` 下的本地包装入口 | 检查 owner 源存在、需要的本地入口存在、运行时引用不再跨 skill |
| 共享状态与决策规则 | owner reference 文件，如 `wilco-docs/references/status-vocabulary.md`、`decision-tree.md` | 需要运行时可见的 skill 本地完整副本 | 检查 owner 文件存在、所需本地副本存在、并把副本视为派生产物 |
| 强结构模板 | owner template 文件，如 `plan-template.md`、`prd-template.md`、`resume-output-template.md` | 满足运行时闭包所需的本地可见副本或本地引用 | 检查 owner 模板存在、所需本地闭包存在、关键结构保持稳定 |
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

- 这份文档负责映射 owner 和同步关系，不替代 owner 文件本身。
- 当契约变更时，应先改 owner 源，再刷新派生层，最后补 validator 覆盖。
