def update_memory(db, decision, result):
    """
    Convierte experiencia → aprendizaje
    """

    action = decision.get("action")
    strategy = decision.get("strategy")

    success = result.get("success", False)
    impact = result.get("impact", 0)

    record = {
        "action": action,
        "strategy": strategy,
        "success": success,
        "impact": impact
    }

    db.append(record)

    return db


def get_success_rate(memory):
    if not memory:
        return 0.5

    successes = [m for m in memory if m["success"]]
    return len(successes) / len(memory)
