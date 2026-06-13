"""Rule-based context augmentation for CAG (Context-Augmented Generation)."""


def apply_context(user_id, question, base_answer, context_items):
    """
    Apply user context items to modify the base answer.

    Known rules:
    - "audience": append "(adaptado para {value})"
    - "include_examples" == "si": append "(con ejemplos incluidos)"
    - "language": append "(en {value})"
    - Unknown keys: silently ignored

    Returns base_answer unchanged when context_items is None or empty.
    """
    if not context_items:
        return base_answer

    answer = base_answer

    for item in context_items:
        key = item.get("key", "")
        value = item.get("value", "")

        if key == "audience":
            answer = f"{answer} (adaptado para {value})"
        elif key == "include_examples" and value == "si":
            answer = f"{answer} (con ejemplos incluidos)"
        elif key == "language":
            answer = f"{answer} (en {value})"
        # Unknown keys: silently ignored

    return answer
