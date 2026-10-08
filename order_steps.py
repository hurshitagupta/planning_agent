import random
from graphlib import TopologicalSorter, CycleError
from model_plan import Step, create_plan, MAX_STEPS

def order_steps(steps: list[Step], start: set[str]) -> list[Step]:
    """Arrange steps so their dependencies are satisfied."""

    if len(steps) > MAX_STEPS:
        raise ValueError("Plan exceeds maximum step limit")

    if len({step.name for step in steps}) != len(steps):
        raise ValueError("Step names must be unique")

    producers = {}

    for step in steps:
        for fact in step.gives:
            if fact in producers:
                raise ValueError(f"Multiple producers for fact: {fact}")
            producers[fact] = step.name

    graph = {}

    for step in steps:
        dependencies = set()

        for fact in step.needs:
            if fact in start:
                continue

            if fact not in producers:
                raise ValueError(f"{step.name}: no producer for '{fact}'")

            dependencies.add(producers[fact])

        graph[step.name] = dependencies

    try:
        ordered_names = list(TopologicalSorter(graph).static_order())
    except CycleError as error:
        raise ValueError(f"Circular plan detected: {error.args[1]}") from None

    step_lookup = {step.name: step for step in steps}
    return [step_lookup[name] for name in ordered_names]

if __name__ == "__main__":
    steps = create_plan()

    random.Random(42).shuffle(steps)

    print("Shuffled Plan:")
    print([step.name for step in steps])

    ordered_plan = order_steps(steps, start=set())

    print("\nOrdered Plan:")
    print([step.name for step in ordered_plan])

    print("\nExecution Trace:")
    available_facts = set()

    for step in ordered_plan:
        missing = step.needs - available_facts

        if missing:
            print(f"BLOCKED: {step.name}, missing {sorted(missing)}")
            break

        print(f"READY: {step.name} | needs={sorted(step.needs)} | gives={sorted(step.gives)}")
        available_facts.update(step.gives)

    print("\nGoal reached:",
          "deployment_verified" in available_facts)
