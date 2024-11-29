from agents.brain.goal.milestones.software_dev.test_milestone import TestMilestone


class AcceptanceTestMilestone(TestMilestone):
    def __init__(self):
        super().__init__(
            name="Run and Validate Acceptance Tests",
            test_type="Acceptance",
            knowledge_key="acceptance_tests",
            test_dir_suffix="acceptance",
            predefined_dependencies=["pytest"],
        )
