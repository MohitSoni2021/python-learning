"""LangGraph edge and flow logic."""

def judge_decision(state):
    score = state.get("score", 5)

    print(f"\n[Judge Score]: {score}")
    
    print(f"\n[Judge Feedback]: {state.get('feedback', 'No feedback')}")

    if score >= 7:
        return "end"
    else:
        return "retry"