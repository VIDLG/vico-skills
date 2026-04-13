# Trigger Examples

This document is a practical routing matrix for `vico-skills`.
It is not a second source of truth for skill behavior; the owner contracts remain `CONTRACTS.md`, each `<skill>/SKILL.md`, and `README.md`.

## Routing Order

1. Route by intent cluster first.
2. Check route preconditions.
3. Use natural-language phrases as recall hints.
4. If ambiguity remains, ask one short clarification question.
5. If the task is clearly narrow and local, prefer direct answer or direct execution.

## Intent Clusters

| Intent cluster | Default route | Core precondition | Examples |
| --- | --- | --- | --- |
| Repo orientation, architecture scan, clarification, pressure-test, handoff | `vico-ground` | user is working on the whole target or overall decision surface | `scan the repo`, `inspect the codebase`, `scan the architecture`, `clarify this`, `stress-test this`, `resolve this into a handoff`, `扫一下这个项目`, `摸个底`, `盘一下这个代码库`, `看下架构` |
| Tracked-work control, planning, verify, sync, replan, close | `vico-plan` | tracked work is in scope or should become tracked | `make a plan`, `verify this plan`, `做个计划`, `对一下 plan`, `verify 一下`, `收个口`, `close 这个 plan` |
| Persistent implementation continuation | `vico-exec` | an active plan already exists | `keep going`, `continue until complete`, `继续做`, `别停`, `接着跑`, `一直做到完成` |
| Feedback about `vico-skills` itself | `vico-feedback` | the complaint or suggestion targets the workflow or skill behavior | `file an issue`, `I have feedback about vico-skills`, `提个 issue`, `记个反馈`, `这个触发不太对`, `帮我整理成 issue` |

## Example Decisions

| User request | Route | Why |
| --- | --- | --- |
| `扫一下 spoon 项目看看架构方面的问题` | `vico-ground` | whole-repo orientation and architecture review |
| `我们其实是不是把问题看错了，clarify 一下` | `vico-ground` | the current interpretation or scope needs clarification before action |
| `把我们现在的 operating brief 导出到 AGENTS.md` | repo utility | export current workflow rules into a project-local instruction file |
| `看下这个函数为什么 panic` | `direct_execute` or direct answer | narrow local debugging request |
| `做个计划把这个需求落成 tracked work` | `vico-plan` | explicit tracked planning intent |
| `verify 一下这个 active plan 能不能 close` | `vico-plan` | verification and close-out control belong to plan |
| `继续做，别停，直到完成` with active plan present | `vico-exec` | persistent execution intent plus active-plan precondition satisfied |
| `继续做这个需求` with no active plan | short clarification or `vico-plan` | execution intent exists but `vico-exec` precondition is missing |
| `这个 vico-ground 的触发不太对，帮我提个 issue` | `vico-feedback` | workflow feedback targeted at `vico-skills` |

## Short Clarification Patterns

- ambiguous repo scan vs direct answer
  - `你是想让我先走 vico-ground 做整体摸底，还是只是快速回答这个点？`
- ambiguous tracked planning vs persistent execution
  - `你是想先更新/核对计划，还是要我按现有 active plan 持续执行到完成？`
- ambiguous workflow feedback vs ordinary repo bug
  - `这是在反馈 vico-skills 本身的触发/工作流，还是在报当前仓库里的业务问题？`

## Anti-Patterns

- Do not route to `vico-ground` just because the user said `看一下` when the target is one file.
- Do not route to `vico-exec` just because the user said `继续` when no active plan exists.
- Do not route to `vico-feedback` for general repository bugs unrelated to `vico-skills`.
- Do not force a Vico route when the request is obviously a one-off direct answer or direct implementation task.
