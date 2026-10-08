import pytest
from model_plan import Step, create_plan

def test_plan_has_five_steps():
    plan = create_plan()
    assert len(plan) == 5

def test_step_has_correct_dependencies():
    plan = create_plan()

    deploy = next(step for step in plan if step.name == "deploy_app")
    assert deploy.needs == frozenset({"tests_passed", "image_ready"})
    assert deploy.gives == frozenset({"app_deployed"})

def test_step_is_immutable():
    step = Step("prepare_code", frozenset(), frozenset({"code_ready"}))

    with pytest.raises(AttributeError):
        step.name = "modified"

def test_plan_step_names_are_unique():
    plan = create_plan()
    names = [step.name for step in plan]

    assert len(names) == len(set(names))
