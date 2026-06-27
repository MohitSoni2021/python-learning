# GenAI Notebook Learning Journey

This repository captures a structured, notebook-first learning path for building **LLM-powered applications** from fundamentals to multi-agent orchestration patterns.

The progression is practical: each notebook introduces one concept, then builds toward richer workflows such as routing, parallelization, and orchestrator-worker systems.

---

## What This Project Is

This is a personal learning project focused on:

- Core model connectivity and message handling
- Typed state management with Pydantic
- Prompt engineering and chain composition
- Tool calling and ReAct-style reasoning
- Advanced control-flow patterns for agentic systems

The project is implemented as a sequence of Jupyter notebooks plus a lightweight Python project setup.

---

## Learning Roadmap (Committed Notebooks)

### 1) `1_basic_connection.ipynb`
**Goal:** Establish a clean baseline connection to the LLM stack.

You start by validating the environment, model access, and request/response cycle. This notebook sets the technical foundation used by all later exercises.

### 2) `2_pydantic_State.ipynb`
**Goal:** Introduce typed state for reliability.

You learn to model workflow state using Pydantic, which improves validation, readability, and maintainability when agent logic gets more complex.

### 3) `3_messages.ipynb`
**Goal:** Work with structured chat/message abstractions.

This notebook focuses on message roles and conversation structure, which is critical for controlling behavior in chat-based LLM systems.

### 4) `4_Prompts&Chains.ipynb`
**Goal:** Build reusable prompt and chain patterns.

You practice composing prompts and chaining operations so outputs from one step can reliably feed the next.

### 5) `5_Tools&Binding.ipynb`
**Goal:** Add tools to your model workflow.

You explore tool definitions, binding tools to the model, and using function/tool calls to connect LLM reasoning with external capabilities.

### 6) `6_ReAct.ipynb`
**Goal:** Implement ReAct-style reasoning.

You learn a think-act-observe loop that improves multi-step problem solving, especially when tool usage and intermediate reasoning are required.

### 7) `7_Parralelization.ipynb`
**Goal:** Execute independent steps in parallel.

You move from linear chains to concurrent execution patterns, improving responsiveness and throughput for compound tasks.

### 8) `8_Router.ipynb`
**Goal:** Route tasks to specialized paths.

This notebook introduces dynamic decision logic to send requests to the most suitable prompt/tool/subflow.

### 9) `9_Orchestrator_Worker.ipynb`
**Goal:** Coordinate multi-agent-style execution.

You implement orchestrator-worker design, where a controller decomposes work and worker units solve subtasks.

### 10) `10_Generator_Evaluator.ipynb`
**Goal:** Add iterative quality loops.

You explore generator-evaluator workflows, where one component drafts output and another critiques/refines it for better final quality.

---

## Supporting Files (Committed)

- `main.py` – script entry point for quick experiments outside notebooks
- `pyproject.toml` – project metadata and dependency configuration
- `uv.lock` – resolved dependency lockfile for reproducible environments

---

## Skills Gained Through This Project

By the end of this sequence, you practice:

1. Building LLM workflows from scratch
2. Managing typed state across steps
3. Designing robust prompt and chain structures
4. Integrating tools with model calls
5. Implementing ReAct and orchestration patterns
6. Creating evaluation-driven generation loops

This represents a strong progression from **single-call prompting** to **agentic workflow design**.

---

## How To Run

### Option A: Notebook workflow (recommended)
Open notebooks in order from `1_basic_connection.ipynb` to `10_Generator_Evaluator.ipynb`.

### Option B: Python script workflow
Use `main.py` for script-based runs and quick iteration outside notebooks.

---

## Suggested Next Learning Steps

After this committed learning path, good next steps are:

- Add long-term memory patterns
- Add human-in-the-loop review checkpoints
- Add tracing, evaluation metrics, and regression tests
- Package common utilities into reusable modules

---

## Notes

This README intentionally documents only committed project artifacts and committed notebook progression.
