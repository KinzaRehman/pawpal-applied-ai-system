# 🐾 PawPal AI – Intelligent Pet Care Planning Assistant

**Author:** Kinza Rehman  
**Course:** CodePath AI Engineering – Applied AI System (Project 4)

---

# Project Overview

PawPal AI extends my **CodePath Module 2 PawPal+** project into a complete Applied AI system.

The original PawPal+ project was an object-oriented pet scheduling application that allowed users to organize pet-care tasks using classes such as **Owner**, **Pet**, **Task**, and **Scheduler**. It supported priority-based scheduling, recurring tasks, and conflict management.

For Project 4, I transformed PawPal into an intelligent AI planning assistant by adding Retrieval-Augmented Generation (RAG), a multi-step planning agent, reliability guardrails, confidence scoring, automated evaluation, and decision trace logging.

Instead of simply sorting tasks, PawPal AI now reasons through the scheduling process, retrieves pet-care guidance from an external knowledge base, validates inputs, critiques its own schedule, and returns a confidence score alongside every recommendation.

---

# Original Project

### Base Project

**PawPal+ (CodePath Module 2)**

### Original Goal

The original PawPal+ project was designed to help pet owners organize daily pet-care responsibilities.

The application used object-oriented programming concepts to represent:

- Owners
- Pets
- Tasks
- Scheduler

Users could create tasks, assign priorities, estimate task duration, and generate a schedule.

While useful, the original scheduler relied entirely on deterministic scheduling rules.

---

# Applied AI Enhancements

This project transforms PawPal into an AI-assisted scheduling system by adding four major capabilities.

## 1. Retrieval-Augmented Generation (RAG)

Instead of relying only on hard-coded scheduling rules, PawPal retrieves relevant information from a local knowledge base before creating the schedule.

Current knowledge sources include:

```
knowledge/
│
├── cat_care.md
└── dog_care.md
```

The retriever

- identifies pet species
- determines task categories
- searches the appropriate knowledge document
- retrieves relevant care guidance
- provides that guidance to the planning agent

The retrieved information becomes part of the final recommendation rather than being displayed separately.

---

## 2. Agentic Planning Workflow

Rather than performing one scheduling step, PawPal completes multiple planning stages.

```
PLAN
↓
Validate Inputs
↓
Retrieve Pet Knowledge
↓
Analyze Tasks
↓
Apply PawPal Rules
↓
Rank Tasks
↓
Construct Draft Schedule
↓
Self Critique
↓
Revise Schedule
↓
Confidence Score
↓
Final Recommendation
```

Each stage performs a different responsibility.

This makes the scheduling process easier to inspect, debug, and evaluate.

---

## 3. Reliability Features

The project includes multiple reliability mechanisms.

### Guardrails

- Invalid pets are rejected.
- Invalid priorities are blocked.
- Invalid durations are rejected.
- Invalid scheduling windows are rejected.
- Duplicate tasks generate warnings.

### Self Critique

After constructing the schedule, the planner verifies:

- medication ordering
- scheduling conflicts
- due times
- capacity overflow
- warning generation

If necessary, the planner revises the schedule before returning it.

### Confidence Scoring

Each recommendation includes a confidence score based on:

- percentage of scheduled tasks
- number of warnings
- number of unscheduled tasks

Confidence is not intended to represent medical certainty. It reflects scheduling quality.

---

# Key Features

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Agentic multi-step planning
- ✅ Custom pet-care knowledge base
- ✅ Medication prioritization
- ✅ Self-critique and schedule revision
- ✅ Confidence scoring
- ✅ Input validation guardrails
- ✅ Automated evaluation harness
- ✅ Unit testing with pytest
- ✅ Mermaid architecture diagram
- ✅ Decision trace logging

---

# Project Structure

```text
pawpal-applied-ai-system/

├── main.py
├── evaluate.py
├── README.md
├── model_card.md
├── ai_interactions.md
├── requirements.txt

├── knowledge/
│   ├── cat_care.md
│   └── dog_care.md

├── pawpal_ai/
│   ├── agent.py
│   ├── retriever.py
│   ├── guardrails.py
│   ├── io_utils.py
│   └── models.py

├── data/
│   ├── sample_day.json
│   ├── invalid_pet.json
│   └── overloaded_day.json

├── diagrams/
│   └── architecture.mmd

├── tests/
│   └── test_agent.py

└── logs/
```

---

# System Architecture

The Mermaid architecture diagram is located in:

```
diagrams/architecture.mmd
```

The system processes information using the following workflow.

```
User Input
      │
      ▼
Input Validation
      │
      ▼
Knowledge Retrieval (RAG)
      │
      ▼
Planning Agent
      │
      ▼
Self Critique
      │
      ▼
Schedule Revision
      │
      ▼
Confidence Scoring
      │
      ▼
Final Schedule
```

The evaluation harness and unit tests exercise the same planning pipeline to verify reliability.

---

# Installation

## Clone the repository

```powershell
git clone https://github.com/KinzaRehman/pawpal-applied-ai-system.git

cd pawpal-applied-ai-system
```

## Create a virtual environment

```powershell
python -m venv .venv
```

## Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

## Install requirements

```powershell
python -m pip install -r requirements.txt
```

---

# Running PawPal AI

Run the main scheduling system:

```powershell
python main.py --input data/sample_day.json
```
---

# Example 1 – Successful Schedule

Run:

```powershell
python main.py --input data/sample_day.json
```

Example Output

```text
============================================================
PAWPAL AI SCHEDULE
============================================================

Status: SUCCESS

Confidence: 0.91

Recommended Schedule

8:00 AM – 8:10 AM
Morning Medicine (Milo)

8:20 AM – 8:35 AM
Breakfast (Milo)

8:45 AM – 9:15 AM
Morning Walk (Luna)

9:25 AM – 9:45 AM
Clean Litter Box (Milo)

9:55 AM – 10:20 AM
Play Session (Luna)

Decision Trace

PLAN
ANALYZE
RETRIEVE
SPECIALIZE
ACT
TEST
CRITIQUE
REVISE
REFLECT
```

---

# Example 2 – Guardrail

Run

```powershell
python main.py --input data/invalid_pet.json
```

Output

```text
Status: BLOCKED

Confidence: 0.00

Task "Walk"
references unknown pet "Luna".

Schedule generation stopped.
```

This demonstrates that invalid input is safely rejected before planning begins.

---

# Example 3 – Capacity Overflow

Run

```powershell
python main.py --input data/overloaded_day.json
```

Output

```text
Status: PARTIAL

Confidence: 0.75

Scheduled

Medicine

Unscheduled

Deep Grooming

Play Session
```

Instead of silently removing tasks, PawPal reports every unscheduled task so the owner can decide how to proceed.

---

# Retrieval-Augmented Generation (RAG)

The planning agent retrieves pet-care guidance before constructing a schedule.

Knowledge Base

```
knowledge/

cat_care.md

dog_care.md
```

## Before Retrieval

```
Morning Medicine

Reason

Medication task.
```

## After Retrieval

```
Morning Medicine

Reason

Medication task.

Retrieved guidance

Medication instructions from a veterinarian always take priority.

Medication tasks should be completed before lower-priority activities.
```

Because retrieval occurs before planning, recommendations contain information from external documents instead of relying only on hard-coded priorities.

The planning trace records retrieval:

```text
RETRIEVE

Loaded relevant guidance sections for cat and dog.
```

---

# Evaluation

Run

```powershell
python evaluate.py
```

Example Output

```text
PawPal AI Evaluation Harness

PASS
Medication prioritization

PASS
Unknown pet guardrail

PASS
Capacity handling

PASS
Duplicate warning

Summary

4 / 4 tests passed
```

---

# Unit Testing

Run

```powershell
python -m pytest -q
```

Output

```text
3 passed
```

---

# Reliability Summary

| Test | Expected Result | Outcome |
|------|-----------------|---------|
| Medication priority | Elevated to High | ✅ Pass |
| Unknown pet | Block schedule | ✅ Pass |
| Overflow schedule | Partial schedule returned | ✅ Pass |
| Duplicate task | Warning generated | ✅ Pass |

The evaluation harness demonstrates consistent behavior across multiple predefined scenarios.

---

# Design Decisions

Several design choices were intentionally made while extending PawPal.

### Local AI instead of Cloud APIs

The planning agent runs entirely on the local machine.

Advantages

- No API keys
- No internet connection required
- Fully reproducible
- Deterministic outputs
- Easy for graders to run

Tradeoff

The system cannot understand unrestricted natural language like a large language model.

---

### Why Retrieval Instead of Hard Coding?

Instead of embedding all pet-care rules directly into Python, the system retrieves guidance from Markdown knowledge files.

Benefits

- Easier to expand
- Easier to update
- Demonstrates Retrieval-Augmented Generation
- Better separation of knowledge and planning

---

### Human in the Loop

PawPal AI is designed as a decision-support tool.

It never replaces veterinarian advice.

Medication tasks remain visible for human review.

Warnings are never hidden.

Confidence scores communicate scheduling quality rather than certainty.

---

# Stretch Features Completed

## ✅ RAG Enhancement (+2)

- Custom Markdown knowledge base
- Species-specific retrieval
- Retrieved guidance integrated into schedule explanations
- Before/after comparison documented

---

## ✅ Agentic Workflow (+2)

The planner performs multiple reasoning stages.

```
PLAN

↓

RETRIEVE

↓

ANALYZE

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

Each run is recorded inside

```
logs/agent_trace.md
```

---

## ✅ Specialized Behavior (+2)

The scheduler contains PawPal-specific scheduling rules.

Examples

- Medication automatically elevated to High Priority.
- Safety-related tasks ranked ahead of optional enrichment.
- Species-specific care guidance retrieved before scheduling.

---

## ✅ Evaluation Harness (+2)

The project contains

```
evaluate.py
```

which automatically evaluates multiple predefined scenarios and reports pass/fail results.

---

# What I Learned

Coming from a data analytics background rather than a traditional software engineering background, this project helped me understand that AI systems involve much more than prompting a language model.

Reliable AI systems require:

- validation
- retrieval
- planning
- evaluation
- testing
- transparency
- human oversight

Designing PawPal AI taught me how these components work together to create an AI assistant that is more reliable, explainable, and reproducible.

---

# Future Improvements

Potential future enhancements include

- veterinarian-approved knowledge sources
- recurring medication schedules
- calendar integration
- Streamlit web application
- mobile interface
- multiple pet owners
- appointment synchronization
- cloud database
- larger retrieval knowledge base
- natural language task creation

---

# Portfolio Statement

This project demonstrates my ability to design an end-to-end Applied AI system rather than simply integrating a language model.

It combines object-oriented programming, retrieval, planning, reliability engineering, automated testing, documentation, and human-centered AI design into a single reproducible application.

The project reflects how I approach AI engineering: building transparent systems that can be tested, evaluated, and improved while keeping humans involved in important decisions.