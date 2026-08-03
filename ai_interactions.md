# PawPal AI Interaction Traces

The planning agent saves each run to `logs/agent_trace.md`. The trace records
high-level, inspectable decisions rather than hidden private model reasoning.

## Trace fields

1. **PLAN** — defines the workflow.
2. **ANALYZE** — reports accepted inputs.
3. **SPECIALIZE** — applies PawPal-specific priority rules.
4. **ACT** — ranks and schedules tasks.
5. **TEST** — checks capacity and timing.
6. **CRITIQUE** — checks safety ordering and warnings.
7. **REVISE** — changes the draft when needed.
8. **REFLECT** — reports status, completion, and confidence.

## Example trace

```text
PLAN: Validate inputs, specialize task priorities, rank tasks, construct a
schedule, critique it, and revise if needed.
ANALYZE: Accepted 2 pet(s) and 5 task(s).
SPECIALIZE: Elevated medication task 'Morning medicine' from medium to high.
ACT: Ranked tasks by safety category, priority, due time, and duration.
TEST: Checked capacity, due times, and medication placement.
CRITIQUE: Medication safety ordering passed.
REVISE: No revision was necessary.
REFLECT: Final status=success; confidence=0.95; scheduled=5/5.
```

This committed file plus the generated log demonstrates the multi-step agentic
workflow required for the stretch feature.
