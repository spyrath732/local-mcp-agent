1. Προετοιμασία Περιβάλλοντος & Εγκατάσταση
Α. Εγκατάσταση Μοντέλων (Ollama)
Βεβαιώσου ότι τρέχει το Ollama στον υπολογιστή σου και κατέβασε τα απαραίτητα μοντέλα:
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

Β. Δημιουργία Virtual Environment & Πακέτων
Στον φάκελο του project σου:
python -m venv .venv
.venv\Scripts\activate

# Εγκατάσταση σταθερών εκδόσεων
pip install "mcp<2" duckdb langgraph langchain-ollama ragas langchain-mcp-adapters datasets pandas

🗄️ 2. Δημιουργία Τοπικής Βάσης Δεδομένων (setup_db.py)
Αυτό το script δημιουργεί μια τοπική βάση DuckDB με δομημένα δεδομένα ενεργειακής παραγωγής.

Εκτέλεση: python setup_db.py

🔌 3. Κατασκευή Custom MCP Server (mcp_server.py)
Εκθέτει τη βάση μέσω του Model Context Protocol (MCP) με strict read-only SQL guardrails και επεξηγηματικά docstrings για το LLM.

🤖 4. Οργάνωση LangGraph Agent (agent.py)
Υλοποιεί έναν καθαρό StateGraph ReAct Agent που συνδέεται στον MCP server μέσω stdio και καλεί το τοπικό Ollama (qwen2.5:7b).

Εκτέλεση: python agent.py

📊 5. Τοπικό Ragas Evaluation (evaluate_rag.py)
Αξιολογεί την ποιότητα της απάντησης χρησιμοποιώντας τα επίσημα LangChain wrappers του Ragas v1.0 με τοπικό Ollama.

Εκτέλεση: python evaluate_rag.py