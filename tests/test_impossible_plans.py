import pytest
from model_plan import Step
from order_steps import order_steps
from impossible_plans import create_circular_plan, create_missing_producer_plan, check_plan

def test_circular_plan_is_rejected():
    steps = create_circular_plan()

    with pytest.raises(ValueError, match="Circular plan"):
        order_steps(steps, start=set())

def test_cycle_error_names_steps():
    steps = create_circular_plan()

    with pytest.raises(ValueError) as error:
        order_steps(steps, start=set())

    message = str(error.value)

    assert "build_image" in message
    assert "run_tests" in message

def test_missing_producer_is_rejected():
    steps = create_missing_producer_plan()

    with pytest.raises(ValueError, match="no producer"):
        order_steps(steps, start=set())

def test_missing_fact_is_named():
    steps = create_missing_producer_plan()

    with pytest.raises(ValueError) as error:
        order_steps(steps, start=set())

    assert "security_approved" in str(error.value)

def test_starting_fact_allows_plan():
    steps = create_missing_producer_plan()
    ordered = order_steps(steps, start={"security_approved"})

    assert [step.name for step in ordered] == ["deploy_app"]

def test_self_dependency_is_rejected():
    steps = [Step("self_dependent", frozenset({"done"}), frozenset({"done"}))]

    with pytest.raises(ValueError, match="Circular plan"):
        order_steps(steps, start=set())

def test_duplicate_producers_are_rejected():
    steps = [Step("step_a", frozenset(), frozenset({"ready"})),
             Step("step_b", frozenset(), frozenset({"ready"}))]

    with pytest.raises(ValueError, match="Multiple producers"):
        order_steps(steps, start=set())

def test_check_plan_prints_rejection(capsys):
    steps = create_circular_plan()

    check_plan("Circular Plan", steps)

    output = capsys.readouterr().out

    assert "Status: Rejected" in output
    assert "Circular plan" in output

def test_valid_plan_is_accepted():
    steps = [
        Step("prepare", frozenset(), frozenset({"ready"})),
        Step("deploy", frozenset({"ready"}), frozenset({"live"}))
        ]

    ordered = order_steps(steps, start=set())

    assert [step.name for step in ordered] == ["prepare", "deploy"]
