from intelligence.trend_hunter import search_trends
from intelligence.strategy_engine import generate_state


def run():
    trends = search_trends()
    state = generate_state(trends)
    print("[CYCLE STATE]", state)
    return state
