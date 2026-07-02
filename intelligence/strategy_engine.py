def calculate_confidence(trends):
    return len(trends) * 0.33


def generate_state(trends):
    return {
        "trends": trends,
        "confidence": calculate_confidence(trends)
    }
