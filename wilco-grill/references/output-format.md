# Wilco Grill Output Format

Use this file for examples. The normative rules live in `../SKILL.md`.

## Minimal Question Template

```md
Context: repo > branch > current-topic

Question 7: Should this rule be enforced at the workflow layer?

Options
1. `Recommended` Yes, enforce it centrally.
2. No, keep it as guidance only.

Evidence
- The current README and skill body disagree about responsibility.

Why it matters
If this stays implicit, later skills will drift again.

Decision dependency
This depends on the earlier decision to keep the workflow strongly routed.

Write-back target
- README.md
- path/to/SKILL.md

Reply with a number or answer directly.
```

## Expanded Question Example

```md
Context: wilco-skills > wilco-grill > stop-conditions
Priority: critical

Question 12: Should grilling stop once only wording polish remains?

Options
1. `Recommended` Yes, transition directly to the final summary.
2. No, continue until wording is also fully optimized.

Evidence
- The current rules require rigor but do not define a stop condition.
- Long grilling chains degrade when they keep re-asking style-level questions.

Why it matters
Without an explicit stop rule, the grill either stops too early or drifts into low-value repetition.

Decision dependency
This builds on the earlier decision to prioritize critical and important branches before detail-level work.

Failure mode
If this is left undefined, the workflow turns into an endless review loop.

Counterargument
If the user explicitly wants line-level wording review, stopping here could feel premature.

Write-back target
- wilco-grill/SKILL.md

Reply with a number or answer directly.
```

## Final Summary Example

```md
Accepted decisions
- The grill uses `Question N: <question text>` on one line.
- `Options`, `Evidence`, `Why it matters`, `Decision dependency`, and `Write-back target` are core sections.

Unresolved decisions
- None.

Recommended resolutions
- None.

Suggested edits
- Update `wilco-grill/SKILL.md` with the new output contract.
- Add `wilco-grill/references/output-format.md` for long examples.

Edit priority
1. Update the skill contract.
2. Add the example reference.
3. Tighten the validator.

Not covered in this pass
- Concrete validator field names.
```
