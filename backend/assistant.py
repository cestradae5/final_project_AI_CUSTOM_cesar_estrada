from backend.cag import apply_context
from backend.context_store import ContextStore
from backend.knowledge import retrieve_snippets

context_store = ContextStore()


def answer_question(user_id, question):
    snippets = retrieve_snippets(question)

    if not snippets:
        return {
            "user_id": user_id,
            "answer": "No encontre informacion suficiente en la base de conocimiento del curso.",
            "sources": [],
            "context_used": [],
        }

    source_text = " ".join(item["content"] for item in snippets)
    base_answer = f"Segun la base de conocimiento del curso: {source_text}"

    context_items = context_store.list_for_user(user_id)
    final_answer = apply_context(user_id, question, base_answer, context_items)
    context_used = [item["key"] for item in context_items]

    return {
        "user_id": user_id,
        "answer": final_answer,
        "sources": [item["id"] for item in snippets],
        "context_used": context_used,
    }
