# PawPal AI Model Card

**Project:** PawPal AI – Intelligent Pet Care Planning Assistant

**Author:** Kinza Rehman

**Course:** CodePath AI Engineering – Applied AI System (Project 4)

---

# 1. System Overview

## Model Name

PawPal AI Scheduling Assistant

## Base Project

CodePath Module 2 – PawPal+

## Purpose

PawPal AI helps pet owners organize daily pet-care responsibilities by creating a safe, prioritized schedule.

Unlike the original PawPal+ project, this version incorporates AI-inspired planning techniques including Retrieval-Augmented Generation (RAG), multi-step planning, reliability guardrails, confidence scoring, and automated evaluation.

The system is designed to assist with scheduling rather than replace veterinary advice or human decision-making.

---

# 2. Intended Users

Primary users include:

- Pet owners
- Students learning Applied AI
- Developers interested in AI planning systems

The application is intended for educational purposes and personal scheduling assistance.

It is **not** intended to provide veterinary or medical advice.

---

# 3. System Inputs

The planner accepts:

- Pet information
- Pet species
- Daily tasks
- Priority
- Duration
- Due time
- Available scheduling window

Example input

```text
Pet

Milo

Species

Cat

Task

Morning Medicine

Priority

Medium

Due Time

9:00 AM
```

---

# 4. System Outputs

The planner returns

- prioritized schedule
- scheduling explanation
- retrieved pet-care guidance
- warnings
- confidence score
- unscheduled tasks
- decision trace

Example

```text
Status

SUCCESS

Confidence

0.91

Morning Medicine

Retrieved guidance

Medication instructions from a veterinarian always take priority.
```

---

# 5. Specialized Behavior

PawPal AI does more than simply sort tasks.

It applies domain-specific scheduling rules.

Examples include

- Medication is automatically elevated to High Priority.
- Safety-related tasks are scheduled before optional enrichment.
- Pet-care guidance is retrieved before planning begins.
- The planner critiques its own schedule before returning results.

These behaviors make PawPal AI different from a generic scheduling algorithm.

---

# 6. Baseline vs Specialized Behavior

## Baseline Scheduler

```text
Priority

Play
Medicine
Breakfast

Output

Play
Medicine
Breakfast
```

The baseline scheduler simply follows task priority.

---

## PawPal AI

```text
Priority

Play
Medicine
Breakfast

Retrieved Knowledge

Medication instructions from a veterinarian always take priority.

Output

Medicine
Breakfast
Play
```

The specialized planner combines retrieval, domain knowledge, and planning rules to produce a safer schedule.

---

# 7. Retrieval-Augmented Generation

Instead of relying entirely on Python rules, PawPal retrieves information from external Markdown files.

Current knowledge base

```
knowledge/

cat_care.md

dog_care.md
```

The retriever

- detects pet species
- determines task categories
- retrieves matching sections
- provides those sections to the planning agent

The retrieved information becomes part of the scheduling explanation.
---

# 8. Reliability Mechanisms

PawPal AI includes several mechanisms designed to improve reliability and reduce unsafe scheduling recommendations.

## Input Validation

The system validates user input before scheduling begins.

Validation includes:

- Unknown pet detection
- Invalid priority detection
- Invalid duration detection
- Invalid scheduling window detection
- Duplicate task warnings

If validation fails, scheduling is safely stopped and a human-readable error message is returned.

---

## Retrieval Validation

Before planning begins, PawPal retrieves information from the local knowledge base.

If no matching knowledge document exists, the planner does not fail. Instead, it:

- warns the user
- continues scheduling
- lowers confidence if appropriate

This allows the application to remain usable even with incomplete knowledge.

---

## Self-Critique

After producing the first schedule, PawPal performs an internal review.

The planner checks:

- medication ordering
- task conflicts
- due times
- scheduling overflow
- warning generation

If problems are identified, the planner revises the schedule before presenting it to the user.

---

## Confidence Scoring

The confidence score reflects scheduling quality rather than certainty.

Confidence is influenced by:

- percentage of successfully scheduled tasks
- warnings
- unscheduled tasks
- scheduling conflicts

A higher confidence score indicates that the planner successfully created a schedule with fewer issues.

---

# 9. Evaluation Results

The project contains an automated evaluation harness (`evaluate.py`) that tests multiple scheduling scenarios.

Evaluation Results

| Scenario | Result |
|----------|--------|
| Medication prioritization | ✅ Pass |
| Unknown pet guardrail | ✅ Pass |
| Capacity overflow | ✅ Pass |
| Duplicate warning | ✅ Pass |

Overall Evaluation

```text
4 / 4 tests passed
```

The project also includes unit tests using pytest.

```text
3 passed
```

These automated tests improve confidence that future code changes do not break existing functionality.

---

# 10. Limitations

Although PawPal AI performs reliable scheduling, several limitations remain.

Current limitations include:

- no calendar integration
- no veterinarian-approved knowledge sources
- limited knowledge base
- no recurring medication scheduling
- no travel time estimation
- no real-time reminders
- no cloud synchronization

The planner is also unable to understand unrestricted natural language in the same way as a large language model.

---

# 11. Potential Biases

The planner reflects the assumptions encoded within its scheduling rules and knowledge documents.

Examples include:

- medication is always prioritized
- predefined task categories receive different weights
- recommendations depend on the completeness of the local knowledge base

As additional knowledge sources are added, the quality of recommendations should improve.

---

# 12. Misuse Prevention

PawPal AI is designed as a decision-support tool rather than an autonomous decision maker.

To reduce misuse:

- medication guidance remains visible
- veterinary advice is never replaced
- warnings are never hidden
- confidence scores communicate uncertainty
- invalid schedules are blocked before planning begins

Users are encouraged to review every recommendation before acting on it.

---

# 13. Collaboration with AI

Coming from a data analytics background rather than a traditional software engineering background, I used AI primarily as a design partner throughout this project.

AI helped me:

- brainstorm the overall architecture
- design the planning workflow
- debug scheduling logic
- improve reliability testing
- generate documentation
- identify edge cases for evaluation

Rather than accepting every suggestion automatically, I tested each recommendation before incorporating it into the project.

---

# 14. Helpful AI Suggestion

One particularly helpful suggestion was separating the application into multiple modules instead of placing all functionality into a single file.

Splitting the project into:

- retriever
- planning agent
- guardrails
- evaluation
- models

made the system easier to understand, test, and extend.

This also made it much easier to implement Retrieval-Augmented Generation without changing the entire scheduling system.

---

# 15. Flawed AI Suggestion

One suggestion that I decided not to follow was relying entirely on an external Large Language Model API for schedule generation.

Although this approach appeared powerful, it introduced several drawbacks:

- API key requirements
- internet dependency
- additional cost
- non-deterministic outputs
- more difficult testing

Instead, I chose to build a deterministic planning agent with Retrieval-Augmented Generation and explicit scheduling rules.

This approach produces reproducible results that are easier to evaluate and explain.

---

# 16. Ethical Considerations

Pet health and medication decisions should always involve human oversight.

For that reason, PawPal AI:

- never claims medical expertise
- keeps medication recommendations visible
- reports warnings
- communicates confidence
- encourages human review

The system is intended to assist pet owners rather than replace professional veterinary guidance.

---

# 17. Future Improvements

Future versions of PawPal AI could include:

- veterinarian-reviewed knowledge sources
- larger retrieval knowledge base
- calendar integration
- recurring task scheduling
- medication reminder notifications
- natural language task creation
- Streamlit web interface
- mobile application
- cloud synchronization
- multiple household support

These additions would improve usability while preserving the transparency and reliability principles used in this project.

---

# 18. Reflection

This project helped me better understand that building an AI system involves much more than prompting a language model.

Reliable AI systems require thoughtful system design, validation, retrieval, testing, and human oversight.

The biggest lesson I learned was that trustworthy AI comes from combining multiple components—planning, retrieval, evaluation, and guardrails—rather than relying on a single model to generate an answer.

As someone transitioning from data analytics into AI engineering, this project gave me hands-on experience building an end-to-end AI workflow that is modular, explainable, reproducible, and easy to evaluate.