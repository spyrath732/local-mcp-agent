# Ragas Evaluation Best Practices: Handling Unknown Ground Truths in Production

## Question
In our local POC, the answer was straightforward so we hardcoded the `ground_truth`. What happens in real-world production scenarios where the expected answer is unknown beforehand? What are the standard architectural practices?

---

## Architectural Answer & Production Practices

In production RAG and Agentic architectures, the expected answer is rarely known in advance, making hardcoded `ground_truth` values impractical for live traffic. To evaluate systems reliably at scale, AI Architects rely on three core strategies:

### 1. Reference-Free Metrics (No Ground Truth Required)
The most critical realization for production monitoring is that core Ragas metrics—specifically **Faithfulness** (whether the answer is derived strictly from the retrieved context without hallucinations) and **Answer Relevancy** (how well the response addresses the user's prompt)—**do not require a `ground_truth`**.
* **Required Inputs:** Only the user's query (`user_input`), the generated output (`response`), and the data fetched by the agent/retriever (`retrieved_contexts`).
* **Architectural Benefit:** You can run automated, real-time or asynchronous evaluations on 100% of live production queries without needing pre-defined answers.

### 2. Synthetic Test Dataset Generation
When conducting regression testing *before* deploying a new version (e.g., changing prompts, chunking strategies, or swapping LLMs), writing test cases manually does not scale.
* **How it works:** Frameworks like Ragas include a built-in **`TestsetGenerator`**. You feed your raw knowledge base (documents, database schemas, manuals) into the generator, and a strong LLM automatically synthesizes hundreds of diverse `[Question, Retrieved Context, Ground Truth]` triplets.
* **Architectural Benefit:** Allows you to build a comprehensive, multi-hop evaluation dataset in minutes to benchmark architectural changes.

### 3. Building a "Golden Dataset" via Human-in-the-Loop (HITL)
Once the system is live in production, evaluation shifts toward continuous improvement:
1. **Telemetry & Logging:** Log live user queries, retrieved contexts, tool calls, and final agent responses (e.g., via MLflow, Phoenix, or LangSmith).
2. **Domain Expert Review:** QA engineers or subject matter experts periodically sample production logs (especially edge cases or negative user feedback) and curate the ideal expected outputs (`ground_truth`).
3. **CI/CD Integration:** These curated records form a **"Golden Dataset"**, which is integrated into your CI/CD pipelines (e.g., GitHub Actions) to run automated regression gates before any new model or code change reaches production.

---

## Summary Blueprint
* **Live Production Monitoring:** Use **reference-free metrics** (`Faithfulness`, `AnswerRelevancy`) on live logs without ground truth.
* **Pre-Deployment & CI/CD Gates:** Use **Synthetic Datasets** and **Human-Curated Golden Datasets** to validate system accuracy before releasing updates.