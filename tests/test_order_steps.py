import random
import pytest
from model_plan import Step, create_plan, MAX_STEPS
from order_steps import order_steps

def test_correct_dependency_order():
    steps = create_plan()

    ordered = order_steps(steps, start=set())
    names = [step.name for step in ordered]

    assert names.index("prepare_code") < names.index("run_tests")
    assert names.index("prepare_code") < names.index("build_image")
    assert names.index("run_tests") < names.index("deploy_app")
    assert names.index("build_image") < names.index("deploy_app")
    assert names.index("deploy_app") < names.index("verify_deployment")

def test_shuffled_inputs_produce_valid_plans():
    original = create_plan()

    for seed in range(10):
        steps = original.copy()
        random.Random(seed).shuffle(steps)

        ordered = order_steps(steps, start=set())
        available = set()

        for step in ordered:
            assert step.needs <= available
            available.update(step.gives)

        assert "deployment_verified" in available

def test_all_steps_are_preserved():
    steps = create_plan()
    ordered = order_steps(steps, start=set())

    assert len(ordered) == len(steps)
    assert {s.name for s in ordered} == {s.name for s in steps}

def test_step_limit():
    steps = [Step(f"step_{i}", frozenset(), frozenset({f"fact_{i}"}))
        for i in range(MAX_STEPS + 1)]

    with pytest.raises(ValueError, match="step limit"):
        order_steps(steps, start=set())

def test_duplicate_names():
    steps = [Step("duplicate", frozenset(), frozenset({"a"})),
        Step("duplicate", frozenset(), frozenset({"b"}))]

    with pytest.raises(ValueError, match="unique"):
        order_steps(steps, start=set())

def test_missing_producer():
    steps = [Step("deploy", frozenset({"unknown_fact"}), frozenset({"live"}))]

    with pytest.raises(ValueError, match="no producer"):
        order_steps(steps, start=set())

def test_circular_dependencies():
    steps = [Step("step_a", frozenset({"b"}), frozenset({"a"})),
            Step("step_b", frozenset({"a"}), frozenset({"b"}))]

    with pytest.raises(ValueError, match="Circular plan"):
        order_steps(steps, start=set())

def test_empty_plan():
    assert order_steps([], start=set()) == []

def test_initial_fact_satisfies_dependency():
    steps = [Step("deploy", frozenset({"image_ready"}), frozenset({"live"}))]
    ordered = order_steps(steps, start={"image_ready"})
    assert [step.name for step in ordered] == ["deploy"]
