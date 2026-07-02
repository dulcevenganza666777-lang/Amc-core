def make_decision(state, memory=None):
    trends = state.get("trends", [])
    confidence = state.get("confidence", 0.5)

    if memory is None:
        memory = []

    success_rate = sum(1 for m in memory if m["success"]) / len(memory) if memory else 0.5

    # CEO empresarial (no técnico)
    if confidence > 0.8 and success_rate > 0.6:
        return {
            "action": "scale_content",
            "strategy": trends[:1],
            "risk": "low"
        }

    if confidence > 0.5:
        return {
            "action": "test_content",
            "strategy": trends[:2],
            "risk": "medium"
        }

    return {
        "action": "observe_market",
        "strategy": None,
        "risk": "high_wait"
    }
