from agents.goal.goal import Goal
from agents.goal.milestones.software_dev.software_dev_milestones import UMLMilestone, UsageExampleMilestone, UnitTestMilestone, OracleTestMilestone, ConvergenceMilestone

class SoftwareDevelopmentGoal(Goal):
    def __init__(self, description, milestones, goal_file=None):
        description = "Complete software development process according to PRD"
        milestones = [
            UMLMilestone(),
            UsageExampleMilestone(),
            UnitTestMilestone(),
            OracleTestMilestone(),
            ConvergenceMilestone()
        ]
        super().__init__(description, milestones, goal_file)
