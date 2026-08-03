# PawPal AI Model Card

## 1. System Overview

**Name:** PawPal AI Scheduling Assistant  
**Base project:** PawPal+ from CodePath Module 2  
**Purpose:** Turn pet-care tasks and owner availability into a prioritized,
human-reviewable daily schedule.

The original PawPal+ project used object-oriented classes such as `Owner`,
`Pet`, `Task`, and `Scheduler` to store pet-care information and organize
tasks. It supported deterministic scheduling concepts such as task priority,
time, recurrence, and conflicts. This extension adds a specialized multi-step
planning agent, guardrails, self-critique, confidence scoring, trace logging,
and an automated evaluation harness.

## 2. Intended Use

PawPal AI is intended for students and pet owners who want help organizing
routine pet-care tasks. It is a planning aid, not a veterinarian, emergency
service, or medical dosing system. A person must review all medication,
health, and appointment decisions.

## 3. Specialized Behavior

The system applies PawPal-specific rules rather than generic sorting:

- Medication is automatically treated as at least high priority.
- Safety-related categories receive more ranking weight.
- Invalid pet references and unsafe durations are blocked.
- Capacity overflow is explicitly reported.
- A critique step checks medication placement.
- The system revises the schedule when safety ordering is incorrect.

### Baseline vs. specialized comparison

| Input | Baseline priority sort | PawPal specialized result |
|---|---|---|
| Urgent play task + low-priority medication | Play may appear first | Medication is elevated to high and scheduled first |
| Task references an unknown pet | May fail later or silently continue | Input is blocked with confidence 0.00 |
| More work than available time | Tasks may be dropped | Unscheduled tasks are explicitly listed |

## 4. Reliability Mechanisms

The project uses:

1. Input validation guardrails.
2. Duplicate-task and timing warnings.
3. Deterministic ranking.
4. Self-critique and revision.
5. Confidence scoring based on completion, warnings, and overflow.
6. Automated tests and an evaluation harness.
7. Persistent high-level decision traces.

Confidence is not a medical probability. It is an operational score indicating
how completely and cleanly the planner handled the submitted scenario.

## 5. Limitations and Biases

The planner uses fixed rules and therefore reflects the assumptions encoded by
the developer. It may over-prioritize one category, cannot understand a pet's
individual medical condition, and does not know travel time, household
routines, exact medication intervals, or veterinarian instructions unless
those constraints are added. Its confidence score measures scheduling quality,
not whether the care itself is medically correct.

## 6. Potential Misuse and Prevention

The system could be misused as a substitute for veterinary guidance or as an
automatic medication authority. To reduce that risk, the documentation clearly
states that it is a planning aid, medical tasks remain visible for human review,
invalid inputs are blocked, and warnings are never hidden. A future version
should require explicit owner confirmation for medication tasks.

## 7. Reliability Testing Surprise

The most surprising finding was that a schedule can look organized while still
being unsafe. A normal priority sort could place an urgent play task ahead of a
low-priority medication task. The specialization and critique stages corrected
this by elevating medication and checking its position.

## 8. Collaboration With AI

I used AI to help break the rubric into concrete files, design the architecture,
draft test cases, debug scheduling logic, and improve documentation. A helpful
AI suggestion was to separate validation, planning, evaluation, and logging
instead of placing everything in one script; this made the system easier to
test and explain.

One flawed suggestion was to rely on an external generative-AI API for every
schedule. That would have added cost, API-key setup, non-deterministic output,
and a greater risk of hallucinated care advice. I rejected that approach and
used a transparent specialized planning agent that runs locally.

## 9. Future Improvements

Future versions could add recurring-task support, exact medication intervals,
calendar integration, owner confirmation, veterinarian-approved rules, a
Streamlit interface, and retrieval from trusted pet-care documents. Any RAG
source should be curated and cited rather than treated as unquestioned truth.
