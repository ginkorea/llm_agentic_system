from agents.brain.goal.milestones.milestone import Milestone

class SoftwareDesignMilestone(Milestone):
    def __init__(self):
        super().__init__("Complete UML and Architecture Design")

    def is_achieved(self, brain, input_data):
        print("Checking if UML is achieved...")
        return True


class UsageExampleMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Usage Examples")

    def is_achieved(self, brain, input_data):
        print("Checking if Usage Examples are achieved...")
        return True

class UnitTestMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Unit Tests")

    def is_achieved(self, brain, input_data):
        print("Checking if Unit Tests are achieved...")
        return True


class OracleTestMilestone(Milestone):
    def __init__(self):
        super().__init__("Pass Oracle Tests")

    def is_achieved(self, brain, input_data):
        print("Checking if Oracle Tests are achieved...")
        return True


class ConvergenceMilestone(Milestone):
    def __init__(self):
        super().__init__("Achieve Model Convergence")

    def is_achieved(self, brain, input_data):
        print("Checking if Model Convergence is achieved...")
        return True