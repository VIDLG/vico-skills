# 共识模型

这份文档总结了“建立 shared ground / 达成共识”背后的主要理论线索，以及它们如何映射到 Vico 工作流。

它不是任何 skill 的第二份行为契约。
真正的 owner contract 仍然在各个 skill 自己的 `SKILL.md` 里。

## 为什么要有这份文档

Vico 不只是想检查仓库、写计划或执行任务。
它还想帮助用户和 AI 逐步建立一种可操作的共同理解，明确：

- 什么已经成立
- 什么只是暂时假设
- 什么仍然有分歧
- 什么 tradeoff 需要摊开
- 下一步到底该做什么

这件事背后其实有比较稳定的理论支撑。

## 主要理论族

### Common Ground

核心思想：
- 沟通成功，不只是传输了信息，而是建立了双方都知道、并且双方都知道对方知道的共享基础

它解释了什么：
- 为什么 `Accepted Facts` 和 `Accepted Decisions` 要显式记录
- 为什么隐藏假设和静默歧义会破坏协作

在 Vico 中最适合映射到：
- `Accepted Facts`
- `Accepted Decisions`
- `Active Assumptions`
- `Open Questions`
- `Ground Handoff`

### Conversational Grounding

核心思想：
- 对话是一个把信息逐步 grounding 到“足够可以继续行动”的过程

它解释了什么：
- 为什么不是每句话都同样“成立”
- 为什么 skill 应该区分 proposed、assumed、accepted、unresolved

在 Vico 中最适合映射到：
- clarification-first 行为
- 显式不确定性
- 不猜、先问短澄清

### Sensemaking

核心思想：
- 面对复杂情况，人不是先有完整模型再行动，而是边收集信号、边形成解释、边修正框架

它解释了什么：
- 为什么 `scan` 应该先建立问题图，而不是立刻进入执行
- 为什么 findings、issues、topic map 应该是演化中的，而不是一次成型

在 Vico 中最适合映射到：
- `Evidence Bank`
- `Findings`
- `Issue Bank`
- `Topic Map`
- 递进式窄化 `scan`

### Collaborative Problem Solving

核心思想：
- 对话不是单纯问答，而是围绕同一个问题做联合工作

它解释了什么：
- 为什么 `clarify`、`review`、`resolve` 应该被看作不同协作动作，而不只是不同输出样式

在 Vico 中最适合映射到：
- controller 式路由
- 基于“下一步协作需要什么”来选 move

### Deliberation / Argumentation

核心思想：
- 很多推进不是来自补信息，而是来自结构化挑战：claim、evidence、assumption、counterexample、rebuttal

它解释了什么：
- 为什么 `grill` 不能只是连续提问
- 为什么 tradeoff 和反例压测很重要

在 Vico 中最适合映射到：
- `grill`
- `tradeoff`
- `challenge`
- `counterexample`
- recommendation vs. open branch

### Negotiation / Preference Reconciliation

核心思想：
- 不是所有分歧都是事实分歧，很多分歧其实是偏好、优先级或约束排序不同

它解释了什么：
- 为什么光有 evidence 也不一定能定 plan 形状、文档负担、推进顺序
- 为什么系统有时需要协调 preference，而不只是继续找证据

在 Vico 中最适合映射到：
- `tradeoff`
- hard / soft constraints
- preference ranking
- execution-risk negotiation

### Vocabulary / Ontology Alignment

核心思想：
- 很多看起来像分歧的问题，其实只是双方对同一个词用法不同

它解释了什么：
- 为什么 `done`、`verify`、`tracked`、`architecture`、`simple` 这类词需要显式对齐

在 Vico 中最适合映射到：
- `align`
- term freeze
- boundary naming
- restatement / glossary

### Decision-Making Under Uncertainty

核心思想：
- 很多 workflow 决策都是在不完整信息下做的，所以更重要的是管理风险，而不是假装绝对确定

它解释了什么：
- 为什么系统要考虑 reversibility、downside、ambiguity、verification strength

在 Vico 中最适合映射到：
- recommendation shortcut
- execution readiness
- close-out verification
- continue / stale-plan / needs-user 路由

### Double-Loop Learning

核心思想：
- 强系统不只修正动作，还会反过来检查导致该动作的假设、目标和流程

它解释了什么：
- 为什么 process review 和 mode shift 也是达成共识的一部分
- 为什么 workflow 有时需要反过来质疑自己的 framing

在 Vico 中最适合映射到：
- process review
- route shift
- reframe
- assumption audit

## 可用的共识动作

从上面的理论往下压，最实用的一组 move 是：

- `clarify`
  对齐目标、术语、边界、成功标准
- `scan`
  建立 evidence、findings、issues、topic map
- `align`
  显式统一概念含义和边界
- `tradeoff`
  对比方案、优先级、不可逆性
- `grill`
  压测假设和结论
- `map`
  把当前问题结构外显出来
- `review`
  checkpoint 当前 shared ground，不继续扩张
- `resolve`
  把当前 shared ground 压缩成决定或 handoff

## 理论到 Move 的映射表

| 理论族 | 主要解决的失败模式 | 最适合的 Vico move | 典型产物 |
| --- | --- | --- | --- |
| Common Ground | 双方以为对齐了，其实没对齐 | `clarify`、`review`、`resolve` | accepted facts / accepted decisions |
| Conversational Grounding | 模糊表述被误当成已成立内容 | `clarify`、`align` | epistemic status 分层 |
| Sensemaking | 在结构还没看清时就急着行动 | `scan`、`map`、`reframe` | findings / topic map |
| Deliberation / Argumentation | 方案从未被真正压测就被接受 | `grill`、`challenge` | tradeoffs / rebuttals |
| Preference Reconciliation | 事实已对齐，但价值排序仍冲突 | `tradeoff` | priorities / constraints |
| Ontology Alignment | 同一个词在双方脑中不是一个意思 | `align` | accepted vocabulary / boundaries |
| Decision Under Uncertainty | 过早假装确定、低估风险 | `tradeoff`、`review`、`resolve` | assumptions / commitments / risks |
| Double-Loop Learning | 错的不是答案，而是看问题的框架 | `reframe`、`review` | replacement frame / updated objective |

## 失败模式

- 隐含假设被当成事实
- 偏好被说成客观真相
- findings 被误当成完整 issue 集
- 分歧被误标成“只是缺证据”
- 该 reframe 的时候却直接去 pressure-test
- shared ground 还不够稳时就急着进入 planning

## 反模式

- 不检查 shared intent，就直接顺着表层提问回答
- 把所有不确定性都压成一个泛泛的 `open question`
- 把每个 finding 都硬塞成 issue
- 真正需要 `tradeoff` 或 `align` 时却误用 `grill`
- 把 `challenge` 用成攻击语气，而不是结构化 review move
- 在当前 ground 还不稳时就导出 operating rules

## 建议的 shared-ground 状态

如果以后 Vico 要进一步往“共识系统”演化，最有用的一组状态桶会是：

- `Objective`
- `Target`
- `Accepted Facts`
- `Accepted Decisions`
- `Active Assumptions`
- `Disagreements`
- `Tradeoffs`
- `Open Questions`
- `Evidence Bank`
- `Findings`
- `Issue Bank`
- `Topic Map`
- `Ground Handoff`

## 对 Vico 设计的启发

最重要的启发其实是：

- `Findings` 不等于 `Issues`
- `Facts` 不等于 `Assumptions`
- `Disagreement` 不总等于 `missing evidence`
- `Consensus` 不等于 `full certainty`

也正因为如此，Vico 更适合用：

- 多个不同 move
- 多个不同状态桶
- 显式 handoff 契约

而不是一个泛泛的“analyze”步骤来处理所有问题。
