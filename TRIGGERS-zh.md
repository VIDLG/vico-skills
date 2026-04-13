# 触发示例矩阵

这是一份面向使用者的 `vico-skills` 路由示例矩阵。
它不是第二份行为真相源；真正的 owner 契约仍然是 `CONTRACTS-zh.md`、各个 `<skill>/SKILL.md` 和 `README-zh.md`。

## 路由顺序

1. 先按意图簇路由。
2. 再检查 route 前置条件。
3. 再用自然语言短语提升召回。
4. 如果仍有歧义，就问一句短确认。
5. 如果任务明显只是局部、小范围，就优先直接回答或直接执行。

## 意图簇

| 意图簇 | 默认 route | 核心前置条件 | 例子 |
| --- | --- | --- | --- |
| 仓库摸底、架构扫描、澄清、pressure-test、handoff | `vico-ground` | 用户目标是整个对象或整体决策面 | `scan the repo`、`inspect the codebase`、`scan the architecture`、`clarify 一下这个目标`、`stress-test 这个方案`、`把这个 resolve 成 handoff`、`扫一下这个项目`、`摸个底`、`盘一下这个代码库`、`看下架构` |
| tracked work 控制、规划、verify、replan | `vico-plan` | tracked work 已经在上下文里，或应该进入 tracked work | `make a plan`、`verify this plan`、`做个计划`、`对一下 plan`、`verify 一下`、`replan 这个 slug` |
| 持续推进实现 | `vico-exec` | 已经存在 active plan | `keep going`、`continue until complete`、`继续做`、`别停`、`接着跑`、`一直做到完成` |
| 反馈 `vico-skills` 自身 | `vico-feedback` | 抱怨或建议的目标是 workflow / skill 行为本身 | `file an issue`、`I have feedback about vico-skills`、`提个 issue`、`记个反馈`、`这个触发不太对`、`帮我整理成 issue` |
| repo-local 维护、生命周期操作与 truth extraction | `vico-ops` | tracked artifact 或 `.vico` 状态已经在上下文里 | `bootstrap 一个新 slug`、`sync 当前 active docs`、`close 这个 tracked work`、`cancel 这个 slug`、`抽取 architecture truth`、`校验 vico workspace` |

## 路由示例

| 用户表达 | Route | 原因 |
| --- | --- | --- |
| `扫一下 spoon 项目看看架构方面的问题` | `vico-ground` | 明显是在做整体摸底和架构审视 |
| `我们是不是把目标理解错了，clarify 一下` | `vico-ground` | 当前目标或解释框架需要先澄清 |
| `把我们现在的 operating brief 导出到 AGENTS.md` | 仓库级 utility | 把当前 workflow 规则导出成项目内说明文件 |
| `看下这个函数为什么 panic` | `direct_execute` 或直接回答 | 单点、局部的排障请求 |
| `做个计划把这个需求落成 tracked work` | `vico-plan` | 明确是在做 tracked planning |
| `verify 一下这个 active plan 能不能 close` | `vico-plan` | verify 属于 planning，cleanup 在后续 ops |
| `close 这个 tracked work` | `vico-ops` | 生命周期清理属于 repo-local operations |
| `sync 一下当前 .vico 状态` | `vico-ops` | 状态对齐属于维护动作，不属于 planning |
| 已有 active plan 时说 `继续做，别停，直到完成` | `vico-exec` | 持续执行意图明确，且前置条件满足 |
| 没有 active plan 时说 `继续做这个需求` | 一句短确认或 `vico-plan` | 有执行意图，但 `vico-exec` 前置条件不成立 |
| `这个 vico-ground 的触发不太对，帮我提个 issue` | `vico-feedback` | 反馈对象明确是 `vico-skills` 自己 |

## 短确认模板

- 仓库摸底 vs 单点回答
  - `你是想让我先走 vico-ground 做整体摸底，还是只是快速回答这个点？`
- tracked planning vs 持续执行
  - `你是想先更新/核对计划，还是要我按现有 active plan 持续执行到完成？`
- workflow feedback vs 普通仓库 bug
  - `这是在反馈 vico-skills 本身的触发/工作流，还是在报当前仓库里的业务问题？`

## 反模式

- 不要因为用户说了 `看一下` 就把单文件问题误路由到 `vico-ground`。
- 不要因为用户说了 `继续` 就在没有 active plan 的情况下误路由到 `vico-exec`。
- 不要把与 `vico-skills` 无关的普通仓库 bug 自动路由到 `vico-feedback`。
- 不要把明显一次性的直接问答或直接改动请求硬套进 Vico route。
