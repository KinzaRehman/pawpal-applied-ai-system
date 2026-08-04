# PawPal AI – Agent Interaction Log

This document explains how the PawPal AI planning agent makes scheduling decisions.

Rather than producing a schedule in a single step, the system follows a multi-stage workflow. Each stage performs a specific responsibility and records a high-level trace of its actions.

The trace is saved to:

```
logs/agent_trace.md
```

This project intentionally records **high-level planning steps** rather than hidden chain-of-thought. The goal is to make the workflow understandable, reproducible, and easy to debug while protecting internal reasoning.

---

# Agent Workflow

The planning agent follows this sequence:

```
PLAN
↓
VALIDATE
↓
RETRIEVE
↓
ANALYZE
↓
SPECIALIZE
↓
ACT
↓
TEST
↓
CRITIQUE
↓
REVISE
↓
REFLECT
```

Each stage has a specific purpose.

---

# Step 1 – PLAN

Purpose

Determine the overall workflow before scheduling begins.

Responsibilities

- Receive user input
- Define planning stages
- Initialize the scheduling process

Example Trace

```text
PLAN

Validate inputs,
retrieve pet-care guidance,
rank tasks,
construct a schedule,
critique the result,
revise if necessary.
```

---

# Step 2 – VALIDATE

Purpose

Verify that the submitted information is safe to process.

Validation includes

- valid pet names
- valid priorities
- valid durations
- valid scheduling window
- duplicate task detection

If validation fails, planning immediately stops.

Example

```text
VALIDATE

Accepted 2 pets
Accepted 5 tasks
```

---

# Step 3 – RETRIEVE (RAG)

Purpose

Retrieve pet-care guidance from the custom knowledge base.

Knowledge Base

```
knowledge/

cat_care.md

dog_care.md
```

The retriever

- determines pet species
- identifies task categories
- loads matching Markdown files
- extracts relevant sections
- passes retrieved guidance to the planning agent

Example Trace

```text
RETRIEVE

Loaded 4 guidance sections
for cat and dog.
```

This step demonstrates Retrieval-Augmented Generation because planning incorporates information retrieved from external documents.

---

# Step 4 – ANALYZE

Purpose

Review all submitted tasks before ranking.

Responsibilities

- examine task types
- determine task urgency
- identify due times
- prepare scheduling inputs

Example

```text
ANALYZE

Accepted
2 pets
5 tasks
```

---

# Step 5 – SPECIALIZE

Purpose

Apply PawPal-specific scheduling rules.

Examples

Medication

```
Medium Priority
```

becomes

```
High Priority
```

Example Trace

```text
SPECIALIZE

Elevated medication task
Morning Medicine
from Medium
to High.
```

---

# Step 6 – ACT

Purpose

Construct the initial schedule.

Responsibilities

- rank tasks
- assign times
- generate explanations
- attach retrieved guidance

Example

```text
ACT

Ranked tasks
by

category

priority

due time

duration
```

---

# Step 7 – TEST

Purpose

Evaluate the generated schedule before returning it.

Checks include

- scheduling capacity
- medication ordering
- due times
- overflow
- warnings

Example

```text
TEST

Checked capacity

Checked due times

Checked medication placement
```

---

# Step 8 – CRITIQUE

Purpose

Review the schedule for potential problems.

Examples

- medication appears after play
- scheduling overflow
- duplicate warnings
- unsafe ordering

Example

```text
CRITIQUE

Medication safety ordering passed.
```

---

# Step 9 – REVISE

Purpose

Repair the schedule if critique identifies problems.

Possible revisions include

- moving medication earlier
- adjusting task ordering
- preserving safety priorities

Example

```text
REVISE

No revision necessary.
```

or

```text
REVISE

Moved medication
ahead of play session.
```

---

# Step 10 – REFLECT

Purpose

Summarize the completed planning process.

Outputs

- scheduling status
- confidence
- scheduled tasks
- warnings
- unscheduled tasks

Example

```text
REFLECT

Status

SUCCESS

Confidence

0.91

Scheduled

5 / 5 tasks
```

---

# Example End-to-End Trace

```text
PLAN

Validate inputs

↓

VALIDATE

Accepted 2 pets

↓

RETRIEVE

Loaded guidance
for cat and dog

↓

ANALYZE

Accepted 5 tasks

↓

SPECIALIZE

Elevated medication priority

↓

ACT

Ranked tasks

↓

TEST

Checked scheduling capacity

↓

CRITIQUE

Medication ordering passed

↓

REVISE

No revision required

↓

REFLECT

Status SUCCESS

Confidence 0.91
```

---

# Why This Matters

The planning agent intentionally separates scheduling into multiple stages instead of relying on a single algorithm.

This design provides several advantages:

- easier debugging
- reproducible behavior
- transparent planning
- modular components
- improved testing
- easier future expansion

---

# Future Agent Improvements

Future versions could include

- calendar integration
- veterinarian-approved retrieval sources
- recurring medication scheduling
- natural language scheduling
- voice commands
- multiple pet owners
- mobile notifications
- cloud synchronization
- larger retrieval knowledge bases

---

# Summary

PawPal AI demonstrates an Applied AI workflow that combines:

- Retrieval-Augmented Generation
- Agentic planning
- Specialized scheduling behavior
- Reliability guardrails
- Self-critique
- Confidence scoring
- Automated evaluation

The saved interaction traces document the complete planning workflow and provide evidence that the AI system follows a transparent, repeatable decision process.