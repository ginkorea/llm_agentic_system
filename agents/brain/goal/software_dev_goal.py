from agents.brain.goal.goal import Goal
from agents.brain.goal.milestones.software_dev import (SoftwareDesignMilestone, EnvSetupMilestone, ImplementationMilestone,
                                                       AcceptanceTestMilestone, UnitTestMilestone)

class SoftwareDevelopmentGoal(Goal):
    def __init__(self, goal_file=None):
        description = "Complete the software development process according to PRD"
        milestones = [
            SoftwareDesignMilestone(),
            EnvSetupMilestone(),
            ImplementationMilestone(),
            AcceptanceTestMilestone(),
            UnitTestMilestone()
        ]
        super().__init__(description, milestones, goal_file)
        self.milestone_module_map = [1, 3, 4, 5, 6]

