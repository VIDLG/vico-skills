# Scan Template

Use this when you need a concrete `scan` output shape.
Keep the move contract in `SKILL.md` authoritative; this file is an expansion aid, not a replacement for the contract.

```md
Move: scan

Conclusion

- <1-3 grounded conclusions>

Evidence

- <1-3 evidence items>

Optional: Why this matters

- <why the conclusions change the route>

Next route

- `stay_in_ground` | `direct_execute` | `vico-plan`

Next action

- <exact command or action>
```

Minimum completion check:

- includes `Move: scan`
- includes `Conclusion`
- includes `Evidence`
- includes `Next route`
- includes `Next action`
- does not keep mapping the target once the next route is already clear
