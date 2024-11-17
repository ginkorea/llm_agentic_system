from agents.brain.goal.goal import Goal
from agents.brain.goal.milestones.software_dev import SoftwareDesignMilestone, EnvSetupMilestone, UnitTestMilestone, OracleTestMilestone, ConvergenceMilestone

class SoftwareDevelopmentGoal(Goal):
    def __init__(self, description, milestones, goal_file=None):
        description = "Complete software development process according to PRD"
        milestones = [
            SoftwareDesignMilestone(),
            EnvSetupMilestone(),
            UnitTestMilestone(),
            OracleTestMilestone(),
            ConvergenceMilestone()
        ]
        super().__init__(description, milestones, goal_file)

