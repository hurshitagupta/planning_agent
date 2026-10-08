from dataclasses import dataclass

@dataclass(frozen=True)
class Step:
    name: str
    needs: frozenset[str]
    gives: frozenset[str]

MAX_STEPS = 10

def create_plan() -> list[Step]:
    steps = [
        Step("prepare_code", frozenset(), frozenset({"code_ready"})),
        Step("run_tests", frozenset({"code_ready"}), frozenset({"tests_passed"})),
        Step("build_image", frozenset({"code_ready"}), frozenset({"image_ready"})),
        Step("deploy_app", frozenset({"tests_passed", "image_ready"}), frozenset({"app_deployed"})),
        Step("verify_deployment", frozenset({"app_deployed"}), frozenset({"deployment_verified"}))]

    if len(steps) > MAX_STEPS:
        raise ValueError("Plan exceeds the maximum step limit")

    if len({step.name for step in steps}) != len(steps):
        raise ValueError("Step names must be unique")

    for step in steps:
        if not step.name.strip():
            raise ValueError("Step name cannot be empty")

        if not step.gives:
            raise ValueError(f"{step.name}: effects cannot be empty")

    return steps

if __name__ == "__main__":
    plan = create_plan()

    print("Deployment Plan:")
    for step in plan:
        print(f"{step.name}: needs={sorted(step.needs)}, gives={sorted(step.gives)}")
