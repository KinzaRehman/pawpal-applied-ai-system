# PawPal AI — Reliable Pet-Care Scheduling Agent

PawPal AI extends my **CodePath Module 2 PawPal+ project** into an end-to-end
applied AI system. The original project used object-oriented classes such as
`Owner`, `Pet`, `Task`, and `Scheduler` to organize pet-care responsibilities
by priority and time. This version adds a specialized multi-step planning agent,
input guardrails, self-critique, automatic revision, confidence scoring,
decision logs, tests, and an evaluation harness.

## Why this project matters

Pet-care scheduling is not only a sorting problem. A schedule can appear neat
while putting a low-priority medication after a less safety-sensitive task.
PawPal AI makes its planning process inspectable and flags situations that
require human review.

## Features

- Agentic workflow: plan → analyze → act → test → critique → revise → reflect
- PawPal-specific behavior that elevates medication priority
- Input validation and duplicate-task warnings
- Capacity and due-time checks
- Human-readable confidence score
- Persistent agent traces in `logs/`
- Automated `pytest` tests
- Multi-case evaluation script with pass/fail summary
- Mermaid architecture source file

## Project structure

```text
pawpal-applied-ai-system/
├── main.py
├── evaluate.py
├── requirements.txt
├── README.md
├── model_card.md
├── ai_interactions.md
├── pawpal_ai/
│   ├── agent.py
│   ├── guardrails.py
│   ├── io_utils.py
│   └── models.py
├── data/
│   ├── sample_day.json
│   ├── invalid_pet.json
│   └── overloaded_day.json
├── diagrams/
│   └── architecture.mmd
├── logs/
└── tests/
    └── test_agent.py
```

## Architecture

The Mermaid source is stored at `diagrams/architecture.mmd`.

The system loads a JSON scenario, validates it, specializes and ranks tasks,
constructs a draft schedule, critiques the draft, revises unsafe ordering,
calculates confidence, and returns a schedule with warnings. A human reviews the
result. The test harness exercises the same validation, planning, and scoring
components.

## Setup

### Windows PowerShell

```powershell
git clone YOUR_NEW_REPOSITORY_URL
cd pawpal-applied-ai-system

py -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run the end-to-end system

```powershell
python main.py --input data/sample_day.json
```

### Example 1 — valid day

```text
============================================================
PAWPAL AI SCHEDULE
============================================================
Status: SUCCESS
Confidence: 0.91

Recommended schedule:
- 8:00 AM–8:10 AM: Morning medicine for Milo [high/medication]
- 8:20 AM–8:35 AM: Breakfast for Milo [high/feeding]
- 8:45 AM–9:15 AM: Morning walk for Luna [high/walk]
- 9:25 AM–9:45 AM: Clean litter box for Milo [medium/cleaning]
- 9:55 AM–10:20 AM: Play session for Luna [low/play]

Decision trace:
- PLAN: Validate inputs, specialize task priorities, rank tasks, construct a schedule, critique it, and revise if needed.
- ANALYZE: Accepted 2 pet(s) and 5 task(s).
- SPECIALIZE: Elevated medication task 'Morning medicine' from medium to high.
- ACT: Ranked tasks by safety category, priority, due time, and duration.
- TEST: Checked capacity, due times, and medication placement.
- CRITIQUE: Medication safety ordering passed.
- REVISE: No revision was necessary.
- REFLECT: Final status=success; confidence=0.91; scheduled=5/5.
```

### Example 2 — invalid pet reference guardrail

```powershell
python main.py --input data/invalid_pet.json
```

```text
============================================================
PAWPAL AI SCHEDULE
============================================================
Status: BLOCKED
Confidence: 0.00

No tasks were scheduled.

Human-review warnings:
- Task 'Walk' references unknown pet 'Luna'.

Decision trace:
- PLAN: Validate inputs, specialize task priorities, rank tasks, construct a schedule, critique it, and revise if needed.
- GUARDRAIL: Blocked invalid input — Task 'Walk' references unknown pet 'Luna'.
```

### Example 3 — overloaded day

```powershell
python main.py --input data/overloaded_day.json
```

```text
============================================================
PAWPAL AI SCHEDULE
============================================================
Status: PARTIAL
Confidence: 0.75

Recommended schedule:
- 8:00 AM–8:30 AM: Medicine for Milo [high/medication]

Unscheduled tasks:
- Deep grooming
- Play session
```

The system does not silently discard overflow. It returns a partial status,
lists the unscheduled tasks, and lowers confidence.

## Run the reliability evaluation

```powershell
python evaluate.py
```

```text
PawPal AI Evaluation Harness
============================================================
[PASS] Medication specialization
[PASS] Unknown pet guardrail
[PASS] Capacity handling
[PASS] Duplicate warning
------------------------------------------------------------
Summary: 4/4 tests passed (100%)
```

## Run unit tests

```powershell
pytest -q
```

```text
3 passed
```

## Reliability and guardrail behavior

| Test input | Expected behavior | Result |
|---|---|---|
| Medication marked medium | Elevate it to high and schedule it first | Pass |
| Task references unknown pet | Block schedule safely | Pass |
| Tasks exceed availability | Return partial result and list overflow | Pass |
| Duplicate task | Warn the user | Pass |

The evaluation harness reports **4/4 passing cases**. The unit-test suite reports
**3 passing tests**. Confidence decreases when tasks are unscheduled or warnings
are present.

## Design decisions and trade-offs

I used a local deterministic planning agent instead of requiring a generative
model API. This makes the project reproducible, free to run, transparent, and
easy for a grader to test. The trade-off is that it cannot interpret unrestricted
natural language or understand medical nuance.

The trace records high-level system decisions rather than hidden chain-of-thought.
This provides useful audit evidence without pretending that internal reasoning is
always correct.

## Stretch features completed

- **Agentic Workflow Enhancement (+2):** Multi-step planning and critique with
  saved traces in `logs/agent_trace.md` and documentation in `ai_interactions.md`.
- **Fine-Tuning or Specialization Behavior (+2):** PawPal-specific constrained
  rules and a baseline comparison in `model_card.md`.
- **Test Harness or Evaluation Script (+2):** `evaluate.py` runs four predefined
  scenarios and prints a pass/fail summary.

## Testing summary

The system performs consistently on valid, invalid, duplicate, and capacity-
limited scenarios. It struggles with real-world details that are not represented
in the input, such as travel time, veterinarian instructions, medication
intervals, and changing household availability.

## What this project says about me as an AI engineer

This project shows that I approach AI as a system-design and reliability problem,
not only as a prompt. I built a transparent workflow that validates inputs,
makes decisions, checks its work, communicates uncertainty, and keeps a human in
the loop.
