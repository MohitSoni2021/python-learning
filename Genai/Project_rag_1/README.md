# Project RAG 1 - LangGraph Weather Assistant

A CLI-based AI assistant built with **LangGraph** and an OpenAI-compatible chat API (served locally via Ollama endpoint) that can:

- reason over user input,
- decide whether a tool is needed,
- call a weather tool (`wttr.in`),
- handle user/input errors, and
- return a final natural-language response.

---

## What this project does

This project runs an interactive terminal chatbot:

1. Takes a user query.
2. Uses a reasoning model to produce structured output.
3. Decides whether to call a tool (currently weather lookup).
4. Routes based on tool result:
   - ask user again for corrected input,
   - continue to final response,
   - or return temporary tool-unavailable message.

---

## Project structure

```text
main.py                         # Entry point + LangGraph workflow definition
config/openAI_Client.py         # OpenAI-compatible client wrapper
prompts/system_prompt.py        # System instructions for reasoning model
output_struct/output_struct.py  # Pydantic structured response schema
tools/weather_tool.py           # Standalone weather tool helper (currently not wired into graph)
tools/tools_provider.py         # Tool registry (currently not wired into graph)
langgraph_flow/woker.py         # Placeholder (empty)
requirement.txt                 # Python dependencies
```

---

## Agent workflow (designed flow)

The graph is defined in `main.py`.

### State fields

- `user_query`
- `tool_name`
- `tool_input`
- `tool_output`
- `final_answer`
- `is_tool_required`
- `error_type`

### Nodes

- **reasoning**: Calls model with `SYSTEM_PROMPT` and parses `StructuredOutput`.
- **tool_node**: Executes weather API call when tool is `get_weather`.
- **after_tool_router**: Chooses next step using `error_type`.
- **ask_user_node**: Prompts user for corrected city input.
- **final_node**: Creates user-facing final answer.
- **tool_unavailable_node**: Returns fallback error message.

### Routing logic

```text
START
  -> reasoning
     -> should_use_tool
        -> ask_user_node         (if reasoning marks user_error)
        -> tool_node             (if weather/tool required)
        -> final_node            (if no tool needed)

tool_node
  -> after_tool_router
     -> ask_user_node            (user_error)
     -> tool_unavailable_node    (system_error)
     -> final_node               (success)

ask_user_node -> reasoning       (retry loop with corrected input)
final_node -> END
tool_unavailable_node -> END
```

---

## Tools used in this project

### 1) LLM / Inference

- **Ollama-compatible OpenAI API endpoint** via `openai` Python client
- Configured in `config/openAI_Client.py` with:
  - `base_url = http://localhost:11434/v1`
  - model currently used in graph: `qwen2.5:7b`

### 2) Orchestration

- **LangGraph** for node-based control flow and routing.

### 3) Schema / structured parsing

- **Pydantic** (`StructuredOutput`) to force parseable model output.

### 4) External tool API

- **wttr.in** weather endpoint via `requests`.

### 5) CLI display

- **rich** for markdown-formatted terminal output.

---

## Setup

## 1) Clone and enter project

```bash
git clone <your-repo-url>
cd Project_rag_1
```

## 2) Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies

```bash
pip install -r requirement.txt
```

## 4) Make sure local model server is running

This project expects an OpenAI-compatible endpoint at:

```text
http://localhost:11434/v1
```

If using Ollama, ensure the model is available (for example `qwen2.5:7b`) and the server is running.

## 5) Configure API client

Current code uses a hardcoded API key in `config/openAI_Client.py`.
For production/GitHub-safe usage, replace it with environment variables.

---

## Run

```bash
python main.py
```

Then type your query at the prompt:

```text
👉️ : tell me about the weather in Delhi
```

---

## Current notes / limitations

- `tools/weather_tool.py` and `tools/tools_provider.py` exist but graph logic in `main.py` currently calls weather API directly instead of using the tool registry.
- `langgraph_flow/woker.py` is currently empty.
- On Python 3.14+, some LangChain compatibility warnings may appear (Pydantic V1 deprecation warning path).

---

## Suggested next improvements

1. Move API key to environment variable and remove hardcoded secret from code.(currently using the local llm to run this agent)
2. Use `tools_provider` in the graph for centralized tool execution.
3. Add unit tests for routing (`should_use_tool`, `after_tool_router`).
4. Add retries/timeouts and better error normalization for tool calls.
5. Split graph logic out of `main.py` into `langgraph_flow/` module.
