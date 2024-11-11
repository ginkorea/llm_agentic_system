# goal.py


class Goal:
    def __init__(self, description, milestones, goal_file=None):
        self.description = description
        self.milestones = milestones
        self.current_milestone_index = 0
        self.goal_file = goal_file

    def current_milestone(self):
        return self.milestones[self.current_milestone_index] if self.current_milestone_index < len(self.milestones) else None

    def update_progress(self, agent):
        if self.current_milestone() and self.current_milestone().is_achieved(agent):
            self.current_milestone_index += 1

    def fallback(self):
        fallback_index = self.current_milestone().fallback
        self.current_milestone_index += fallback_index

    def is_complete(self):
        return self.current_milestone_index >= len(self.milestones)

    def set_unique_goal(self):
        pass
