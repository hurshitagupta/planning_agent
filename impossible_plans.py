from model_plan import Step
from order_steps import order_steps

def create_circular_plan() -> list[Step]:
    """Create a plan with circular dependencies."""

    return [
        Step("build_image", frozenset({"tests_passed"}), frozenset({"image_ready"})),
        Step("run_tests", frozenset({"image_ready"}), frozenset({"tests_passed"}))
        ]

def create_missing_producer_plan() -> list[Step]:
    """Create a plan requiring a fact nobody produces."""

    return [Step("deploy_app", frozenset({"security_approved"}), frozenset({"app_deployed"}))]

def check_plan(name: str, steps: list[Step]) -> None:
    """Attempt to order a plan and report any errors."""

    print(f"\nChecking: {name}")

    try:
        ordered = order_steps(steps, start=set())

        print("Status: Valid")
        print("Ordered steps:", [s.name for s in ordered])

    except ValueError as error:
        print("Status: Rejected")
        print("Reason:", error)

if __name__ == "__main__":

    # Case 1: Circular dependencies
    circular_plan = create_circular_plan()
    check_plan("Circular Plan", circular_plan)

    # Case 2: Missing producer
    missing_plan = create_missing_producer_plan()
    check_plan("Missing Producer Plan", missing_plan)
