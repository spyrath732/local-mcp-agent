# Local-First Agentic MCP & Ragas Evaluation Pipeline

A production-grade, zero-cost, local-first enterprise architecture pattern combining **Ollama**, **DuckDB**, **FastMCP**, **LangGraph ReAct Agents**, and **Ragas v1.0 Evaluation** without external cloud dependencies.

---

## 🏗️ Architecture Overview

This repository implements a secure, local analytical agent framework designed for powertech / enterprise data workloads:
* **Local LLM & Embeddings:** Powered by Ollama (`qwen2.5:7b` & `nomic-embed-text`).
* **Analytical Storage:** Local analytical database via `DuckDB`.
* **Secure Tooling:** Custom FastMCP Server enforcing strict read-only SQL guardrails and explicit docstrings.
* **Orchestration:** LangGraph `StateGraph` ReAct Agent communicating over `stdio`.
* **Evaluation:** Local evaluation pipeline leveraging Ragas v1.0 and reference-free metrics.

---

## 🛠️ 1. Environment Setup & Installation

### A. Model Installation (Ollama)
Ensure Ollama is running locally, then pull the required models:
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### B. Virtual Environment & Dependencies
Navigate to your project folder and run:
```bash
python -m venv .venv
.venv\Scripts\activate

# Install stable pinned versions
pip install "mcp<2" duckdb langgraph langchain-ollama ragas langchain-mcp-adapters datasets pandas
```

---

## 🗄️ 2. Database Initialization (`setup_db.py`)
This script initializes a local **DuckDB** database populated with structured energy production and operational datasets.

* **Run:**
```bash
python setup_db.py
```

---

## 🔌 3. Custom MCP Server (`mcp_server.py`)
Exposes the local database securely via the **Model Context Protocol (MCP)**, enforcing strict read-only SQL execution guardrails and semantic docstrings tailored for tool-calling LLMs.

---

## 🤖 4. LangGraph ReAct Agent (`agent.py`)
Implements a clean **StateGraph ReAct Agent** that connects to the custom MCP server via `stdio` and coordinates reasoning loops using local Ollama (`qwen2.5:7b`).

* **Run:**
```bash
python agent.py
```

---

## 📊 5. Local Ragas Evaluation & Production Patterns (`evaluate_rag.py`)

Evaluating agentic workflows in real-world environments presents challenges when expected ground truths are unknown beforehand. This pipeline handles evaluations using production patterns:

### Production Evaluation Strategies:
1. **Reference-Free Metrics (Live Monitoring):** Metrics like **Faithfulness** and **Answer Relevancy** require no `ground_truth`. They evaluate live traffic using only `user_input`, `response`, and `retrieved_contexts`.
2. **Synthetic Dataset Generation:** Use Ragas's built-in `TestsetGenerator` to feed raw documents and automatically synthesize test triplets (`[Question, Context, Ground Truth]`) for regression testing.
3. **Golden Datasets (Human-in-the-Loop):** Curate production logs periodically with domain experts to build robust CI/CD evaluation gates.

* **Run Evaluation Script:**
```bash
python evaluate_rag.py
```