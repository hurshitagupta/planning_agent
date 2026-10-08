# Planning Concepts in Code

## Project Overview

This project demonstrates how planning concepts can be implemented in Python. It represents a software deployment plan using steps, preconditions, and effects, automatically orders steps based on dependencies, validates whether the plan can reach its goal, and detects impossible plans.

The implementation uses Python's built-in `graphlib` module and does not require an LLM or external API.

## Project Structure

```text
planning_concepts/
│
├── model_plan.py
├── order_steps.py
├── validate_plan.py
├── impossible_plans.py
├── reflection.md
├── requirements.txt
├── README.md
│
├── tests/
│   ├── test_model_plan.py
│   ├── test_order_steps.py
│   ├── test_validate_plan.py
│   └── test_impossible_plans.py
│
└── outputs/
    ├── model_plan_output.txt
    ├── order_steps_output.txt
    ├── validate_plan_output.txt
    ├── impossible_plans_output.txt
```

## Technologies Used

- Python 3.11+
- `dataclasses` — define immutable planning steps
- `graphlib` — order steps using topological sorting
- `random` — shuffle inputs reproducibly
- `pytest` — automated testing

## Implementation

### Task 1 — Model the Plan

Created an immutable `Step` dataclass with three fields:

- `name`: Name of the step
- `needs`: Preconditions required before the step
- `gives`: Facts produced by the step

The deployment scenario contains five steps:

| Step | Needs | Gives |
|---|---|---|
| prepare_code | None | code_ready |
| run_tests | code_ready | tests_passed |
| build_image | code_ready | image_ready |
| deploy_app | tests_passed, image_ready | app_deployed |
| verify_deployment | app_deployed | deployment_verified |

**File:** `model_plan.py`

### Task 2 — Order the Steps

Implemented `order_steps()` using `TopologicalSorter` to automatically arrange steps according to their dependencies.

The input is shuffled using a fixed random seed, and tests verify that the resulting plan respects all dependencies.

**File:** `order_steps.py`

### Task 3 — Validate a Plan

Implemented `validate()` to check whether a plan can achieve its goal.

The validator:

- Checks preconditions before each step.
- Tracks available facts.
- Simulates declared effects without executing deployment operations.
- Reports all missing preconditions and unmet goals.

**File:** `validate_plan.py`

### Task 4 — Handle Impossible Plans

Implemented examples demonstrating two impossible planning scenarios:

- **Circular dependencies:** Two steps depend on each other.
- **Missing producer:** A step requires a fact that is unavailable and cannot be produced.

Invalid plans are rejected with clear error messages.

**File:** `impossible_plans.py`

### Task 5 — Reflection

Explained the differences between goals, steps, preconditions, and effects using the deployment example.

Suggested adding an `estimated_minutes` field to the `Step` dataclass to support time estimation.

**File:** `reflection.md`

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

The only external dependency is pytest.

**requirements.txt**

```text
pytest>=8.0
```

Install it:

```bash
python -m pip install -r requirements.txt
```

## Execution Commands

Run each task from the project root:

```bash
python model_plan.py
python order_steps.py
python validate_plan.py
python impossible_plans.py
```

Task 5 is a written reflection and does not require execution.

## Running Tests

Run all automated tests:

```bash
python -m pytest tests/ -q
```

Run tests individually:

```bash
python -m pytest tests/test_model_plan.py -q
python -m pytest tests/test_order_steps.py -q
python -m pytest tests/test_validate_plan.py -q
python -m pytest tests/test_impossible_plans.py -q
```

The test suite covers valid planning, shuffled ordering, missing dependencies, unreachable goals, circular plans, duplicate step names, and step limits.


## Guardrails and Reliability

- **Step limits:** Plans are restricted to a maximum of 10 steps.
- **Validation:** Invalid inputs and missing dependencies are rejected.
- **Error handling:** Circular dependencies and unavailable facts produce clear errors.
- **Determinism:** Fixed random seeds ensure repeatable shuffle tests.
- **Safe execution:** Plans are inspected and validated without executing real deployment actions. No `eval()` or `exec()` is used.
- **Secret hygiene:** No hardcoded credentials or API keys are required.

## Expected Results

A valid plan reaches the goal `deployment_verified`, with no validation problems.

An incorrectly ordered plan produces a list of missing preconditions and unmet goals.

Circular plans and plans with missing fact producers are rejected with descriptive errors.

The test suite should complete successfully when all implementations and tests are correctly configured.
