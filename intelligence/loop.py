import time
from intelligence.cycle_manager import run
from intelligence.ceo import make_decision
from intelligence.evaluator import evaluate
from intelligence.learning_memory import update_memory
from intelligence.logger import get_logger

log = get_logger()

memory = []

def start_loop(interval=5, max_cycles=None):
    global memory

    log.info("SYSTEM → LEARNING MODE ACTIVATED")

    cycle = 0

    while True:
        cycle += 1

        state = run()

        decision = make_decision(state, memory)

        result = evaluate(decision)

        memory = update_memory(memory, decision, result)

        log.info(f"CYCLE {cycle}")
        log.info(f"DECISION: {decision['action']}")
        log.info(f"RESULT: {result}")
        log.info(f"SUCCESS RATE: {len([m for m in memory if m['success']])}/{len(memory)}")

        if max_cycles and cycle >= max_cycles:
            break

        time.sleep(interval)
