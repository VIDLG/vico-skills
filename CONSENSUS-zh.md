# 共识模型

这份文档总结了建立 shared ground 背后的主要理论线索，并把它们映射到更轻量的 `vico-ground` v2 模型。

它不是任何 skill 的第二份行为契约。
真正的 owner contract 仍然在各个 skill 自己的 `SKILL.md` 里。

## 为什么要有这份文档

Vico 不只是想检查仓库、写计划或执行任务。
它也想帮助用户和 AI 建立一种足够可行动的共同理解，明确：

- 哪些内容已经足够成立，可以据此行动
- 哪些仍然只是暂时假设
- 哪些 tension 还值得处理
- 下一步应该走哪条路径

这些事情背后有稳定的理论支撑，但 `vico-ground` 已不再把这些理论直接展开成一大组公开 move。

## 主要理论族

### Common Ground

核心思想：
- 只有当双方都知道某些内容已经成立，并能据此行动时，协作才真正稳定

在 Vico 中最适合映射到：
- `Facts`
- `Assumptions`
- `handoff`

### Conversational Grounding

核心思想：
- 对话是在把信息逐步 grounding 到“足够继续行动”的过程

在 Vico 中最适合映射到：
- `clarify`
- 显式不确定性
- 不猜、先问短澄清

### Sensemaking

核心思想：
- 理解是通过证据、解释和必要时的重构逐步形成的

在 Vico 中最适合映射到：
- `scan`
- `scan` 里的可选结构化 mapping
- 递进式、窄化式的取证

### Collaborative Problem Solving

核心思想：
- 对话不是单纯问答，而是围绕同一个问题做联合工作

在 Vico 中最适合映射到：
- controller 式路由
- 选择最小但足够的下一步 move
- 一旦下一步路径清楚就停止 grounding

### Deliberation / Argumentation

核心思想：
- 很多推进来自结构化 pressure：claim、evidence、counterexample、rebuttal

在 Vico 中最适合映射到：
- `stress`
- 内部 `check` / `tradeoff` / `challenge` 子模式

### Negotiation / Preference Reconciliation

核心思想：
- 很多分歧不是事实分歧，而是偏好、优先级或约束排序不同

在 Vico 中最适合映射到：
- tradeoff 形态的 `stress`
- 影响路由决策的 priorities / constraints

### Vocabulary / Ontology Alignment

核心思想：
- 看起来像分歧的问题，很多其实只是同一个词在双方脑中不是一个意思

在 Vico 中最适合映射到：
- `clarify`
- 术语和边界的重述与对齐

### Decision-Making Under Uncertainty

核心思想：
- 好的 workflow 决策要管理 downside 和 reversibility，而不是假装绝对确定

在 Vico 中最适合映射到：
- `handoff`
- 不确定条件下的路径选择
- 下游 workflow 里的 close-out verification

### Double-Loop Learning

核心思想：
- 强系统不只修正动作，也会回头检查产生当前动作的假设和 framing

在 Vico 中最适合映射到：
- `clarify`
- `scan`
- 当当前 framing 不再适配时做 route shift

## 可用的共识动作

对 `vico-ground` v2 来说，公开界面刻意保持很小：

- `scan`
  - 获取足够证据来决定下一步路径
- `clarify`
  - 对齐目标、范围、术语、约束或 framing
- `stress`
  - 对方案、假设、选项集或 plan 做 pressure-test
- `handoff`
  - 停止 grounding，并明确给出下一步路径

内部子模式仍然存在，但不再需要作为主要公开界面暴露出来。

## 理论到 Move 的映射表

| 理论族 | 主要解决的失败模式 | 最适合的 Vico move | 典型产物 |
| --- | --- | --- | --- |
| Common Ground | 双方以为对齐了，其实没对齐 | `clarify`、`handoff` | facts / 瘦 handoff |
| Conversational Grounding | 模糊表述被误当成已成立内容 | `clarify` | 显式不确定性 |
| Sensemaking | 在理解还不够时就急着行动 | `scan` | evidence / 压缩结论 |
| Deliberation / Argumentation | 方案从未被真正压测就被接受 | `stress` | tradeoff 或 challenge 记录 |
| Preference Reconciliation | 事实已对齐，但价值排序仍冲突 | `stress` | priorities / constraints |
| Ontology Alignment | 同一个词在双方脑中不是一个意思 | `clarify` | 对齐后的术语 / 边界 |
| Decision Under Uncertainty | 过早假装确定、低估风险 | `handoff` | route choice / next action |
| Double-Loop Learning | 错的不是答案，而是 framing 本身 | `clarify`、`scan` | 重新 framing 的目标 |

## 失败模式

- 隐含假设被当成事实
- 偏好被说成客观真相
- facts 还不够稳就直接开始 pressure-test
- 下一步路径已经清楚了，却还在继续 grounding
- shared ground 还不够稳时就急着进入 planning

## 反模式

- 不检查 shared intent，就直接顺着表层提问回答
- 明明只需要决定路径，却把问题过度建模
- 把每个 tension 都包装成一个独立公开 move
- 用 pressure 风格代替清楚的 route 判断
- 在当前 ground 还不稳时就导出 operating rules

## 建议的 shared-ground 状态

对更轻量的 v2 模型来说，最有用的公开状态桶是：

- `Facts`
- `Assumptions`
- `Tensions`
- `Next route`

更丰富的状态仍然可以内部存在，但 `vico-ground` 不应该默认把它们摊进面向用户的输出。

## 对 Vico 设计的启发

最重要的启发是：

- `Facts` 不等于 `Assumptions`
- `Tension` 不总等于 `missing evidence`
- `Consensus` 不等于 `full certainty`
- “下一步安全路径”比“把当前分析空间榨干”更重要

也正因为如此，`vico-ground` v2 更适合：

- 小而清楚的公开 move 集
- 瘦 handoff
- 明确的 stop rule

而不是一整套暴露在外的大型 grounding taxonomy。
