from model_plan import Step, create_plan, MAX_STEPS
from order_steps import order_steps

def validate(plan: list[Step], start: set[str], goal: set[str]) -> list[str]:
    """Validate a plan without executing its steps."""

    if len(plan) > MAX_STEPS:
        raise ValueError("Plan exceeds maximum step limit")

    if not all(isinstance(step, Step) for step in plan):
        raise ValueError("Plan must contain Step objects")

    if not all(isinstance(fact, str) for fact in start | goal):
        raise ValueError("Start and goal facts must be strings")

    facts = set(start)
    problems = []

    for step in plan:
        missing = step.needs - facts

        if missing:
            problems.append(f"{step.name}: missing {sorted(missing)}")

        if not missing:
            facts.update(step.gives)

    # Check whether the goal can be reached.
    missing_goals = goal - facts

    if missing_goals:
        problems.append(f"goal not reached: {sorted(missing_goals)}")

    return problems

if __name__ == "__main__":
    steps = create_plan()

    start = set()
    goal = {"deployment_verified"}

    # Case 1: Valid ordered plan
    ordered = order_steps(steps, start)

    print("Case 1: Valid Plan")
    print("Plan:", [step.name for step in ordered])
    print("Problems:", validate(ordered, start, goal))

    # Case 2: Incorrect order
    bad_plan = [
        steps[3],  # deploy_app
        steps[4],  # verify_deployment
        steps[1],  # run_tests
        steps[2],  # build_image
        steps[0]   # prepare_code
    ]

    print("\nCase 2: Incorrect Order")
    print("Plan:", [step.name for step in bad_plan])
    print("Problems:", validate(bad_plan, start, goal))

    # Case 3: Unreachable goal
    print("\nCase 3: Unreachable Goal")
    print("Problems:", validate(ordered, start, {"payment_completed"}))
