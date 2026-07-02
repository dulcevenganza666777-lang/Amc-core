import random

def evaluate(decision):
    """
    Simula resultado real del mundo
    (luego lo conectas a YouTube real)
    """

    action = decision.get("action")

    if action == "execute_content":
        success = random.random() > 0.3
        impact = random.randint(50, 1000)

    elif action == "test_experiment":
        success = random.random() > 0.5
        impact = random.randint(10, 300)

    else:
        success = False
        impact = 0

    return {
        "success": success,
        "impact": impact
    }
