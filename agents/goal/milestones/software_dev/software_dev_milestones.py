from agents.goal.milestones.milestone import Milestone

class UMLMilestone(Milestone):
    def __init__(self):
        super().__init__("Complete UML Design")

    def is_achieved(self, agent):
        return agent.brain.check_uml_design()


class UsageExampleMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Usage Examples")

    def is_achieved(self, agent):
        return agent.brain.check_usage_examples()


class UnitTestMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Unit Tests")

    def is_achieved(self, agent):
        return agent.brain.check_unit_testing()


class OracleTestMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Oracle Tests")

    def is_achieved(self, agent):
        return agent.brain.check_oracle_test()


class ConvergenceMilestone(Milestone):
    def __init__(self):
        super().__init__("Achieve Model Convergence")

    def is_achieved(self, agent):
        return agent.brain.check_convergence()