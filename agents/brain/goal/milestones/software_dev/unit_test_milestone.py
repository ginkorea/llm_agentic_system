from agents.brain.goal.milestones.software_dev.test_milestone import TestMilestone

class UnitTestMilestone(TestMilestone):
    def __init__(self):
        super().__init__(
            name="Run and Validate Unit Tests",
            test_type="Unit",
            knowledge_key="unit_tests",
            test_dir_suffix="unit",
            predefined_dependencies=["pytest"],
        )
