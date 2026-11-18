from datasets import Dataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import Faithfulness, AnswerRelevancy
from langchain_ollama import ChatOllama, OllamaEmbeddings

def run_evaluation():
    print("Initializing Ragas v1.0 with Langchain wrappers for local Ollama...")

    # 1. Τυλίγουμε τα τοπικά Ollama models με τα επίσημα Ragas wrappers
    eval_llm = LangchainLLMWrapper(ChatOllama(model="qwen2.5:7b", temperature=0))
    eval_embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text"))

    # 2. Αρχικοποίηση των μετρικών δίνοντάς τους τα wrapped models
    metrics = [
        Faithfulness(llm=eval_llm),
        AnswerRelevancy(llm=eval_llm, embeddings=eval_embeddings)
    ]

    # 3. Dataset αξιολόγησης (Standard Ragas v1.0 schema)
    data = {
        "user_input": ["Πόση συνολική παραγωγή ενέργειας (generation_mwh) είχαμε από Lignite;"],
        "response": ["Συνολική παραγωγή ενέργειας από lignite ήταν 4200.5 MWh."],
        "retrieved_contexts": [[
            "plant_id: PLT-01, plant_name: Ptolemaida V, fuel_type: Lignite, generation_mwh: 4200.5"
        ]],
        "reference": ["4200.5 MWh"]
    }

    dataset = Dataset.from_dict(data)

    print("Running evaluation metrics...")

    # 4. Εκτέλεση evaluation
    results = evaluate(
        dataset=dataset,
        metrics=metrics
    )

    print("\n--- RAGAS EVALUATION RESULTS ---")
    print(results)
    
    df = results.to_pandas()
    print("\nDetailed DataFrame View:")
    print(df)

if __name__ == "__main__":
    run_evaluation()