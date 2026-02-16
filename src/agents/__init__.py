from .orchestrator import build_parallel_orchestrator, run_parallel_query
from .router import route_query, classify_router_accuracy

# ARCHIVED: debate and self_correction modules produced negative results
# (Exp 07, F-009). Imports kept lazy for backward compatibility with
# experiment scripts but NOT part of the active pipeline.
def __getattr__(name):
    if name in ("run_debate", "save_debate_logs"):
        from .debate import run_debate, save_debate_logs
        return {"run_debate": run_debate, "save_debate_logs": save_debate_logs}[name]
    if name == "revise_answer":
        from .self_correction import revise_answer
        return revise_answer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
