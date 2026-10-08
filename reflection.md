# Task 5 — Reflection on Planning Concepts

## Understanding Planning Concepts

In our deployment planning project, we implemented a system that represents deployment activities as steps, automatically orders them based on dependencies, and checks whether the plan can achieve its goal.

**Goal:** A goal is the final result we want to achieve. In our project, the goal is `deployment_verified`, which means the application has been deployed and its deployment has been verified according to the plan.

**Step:** A step represents an individual activity required to achieve the goal. Our deployment plan contains five steps: `prepare_code`, `run_tests`, `build_image`, `deploy_app`, and `verify_deployment`. Each step has its own requirements and expected outcomes.

**Precondition:** A precondition is something that must already be true before a step can take place. In our project, `deploy_app` requires both `tests_passed` and `image_ready`. If either fact is missing, the deployment step cannot proceed.

**Effect:** An effect represents the outcome of completing a step successfully. For example, the `build_image` step produces `image_ready`, which becomes available for later steps. Similarly, `deploy_app` produces `app_deployed`.

These four concepts work together to create a structured plan. We use `order_steps()` to arrange activities according to their dependencies and `validate()` to check whether their declared preconditions and effects can lead to the goal. The validation is performed without executing real deployment commands.

Our implementation also detects impossible plans, including circular dependencies and missing fact producers. This prevents us from accepting a plan that cannot be completed.

## Suggested Improvement to Step

One improvement I would make to the `Step` dataclass is to add an **estimated duration** field.

For example:

`Step(name="run_tests", needs=..., gives=..., estimated_minutes=5)`

This would help us estimate the total time required to complete the deployment plan. In future, we could also use these estimates to compare different valid plans and select one that takes less time.
