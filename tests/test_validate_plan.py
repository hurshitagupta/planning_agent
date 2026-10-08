import pytest
from model_plan import Step, create_plan, MAX_STEPS
from order_steps import order_steps
from validate_plan import validate

def test_valid_plan():
    steps = create_plan()
    ordered = order_steps(steps, start=set())

    problems = validate( ordered, start=set(), goal={"deployment_verified"})

    assert problems == []

def test_missing_precondition():
    steps = [Step("deploy", frozenset({"image_ready"}), frozenset({"app_deployed"}))]

    problems = validate(steps, start=set(), goal={"app_deployed"})

    assert any("image_ready" in p for p in problems)
    assert any("goal not reached" in p for p in problems)

def test_unmet_goal():
    steps = create_plan()
    ordered = order_steps(steps, start=set())

    problems = validate(ordered, start=set(), goal={"payment_completed"})

    assert problems == ["goal not reached: ['payment_completed']"]

def test_multiple_missing_preconditions():
    steps = [Step("deploy", frozenset({"tests_passed", "image_ready"}), frozenset({"app_deployed"})),
             Step("verify", frozenset({"app_deployed"}), frozenset({"verified"}))]

    problems = validate(steps, start=set(), goal={"verified"})

    assert len(problems) == 3
    assert "tests_passed" in problems[0]
    assert "image_ready" in problems[0]
    assert "app_deployed" in problems[1]
    assert "goal not reached" in problems[2]

def test_empty_plan_with_unmet_goal():
    problems = validate( [], start=set(), goal={"deployment_verified"})
    
    assert problems == ["goal not reached: ['deployment_verified']"]

def test_goal_already_satisfied():
    problems = validate([], start={"deployment_verified"}, goal={"deployment_verified"})

    assert problems == []

def test_invalid_step_input():
    with pytest.raises(ValueError, match="Step objects"):
        validate(["invalid_step"], start=set(), goal={"done"})

def test_step_limit():
    steps = [Step(f"step_{i}", frozenset(), frozenset({f"fact_{i}"})) 
            for i in range(MAX_STEPS + 1)]

    with pytest.raises(ValueError, match="step limit"):
        validate(steps, start=set(), goal=set())

def test_failed_step_does_not_produce_effects():
    steps = [Step("deploy", frozenset({"tests_passed"}), frozenset({"app_deployed"})),
            Step("verify", frozenset({"app_deployed"}), frozenset({"verified"}))]

    problems = validate(steps, start=set(), goal={"verified"})

    assert len(problems) == 3
    assert "tests_passed" in problems[0]
    assert "app_deployed" in problems[1]
    assert "goal not reached" in problems[2]
