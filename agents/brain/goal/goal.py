# goal.py
from torch import unique


class Goal:
    def __init__(self, description, milestones, goal_file=None):
        self.description = description
        self.milestones = milestones
        self.current_milestone_index = 0
        self.goal_file = goal_file

    def current_milestone(self):
        return self.milestones[self.current_milestone_index] if self.current_milestone_index < len(self.milestones) else None

    def update_progress(self):
        if self.current_milestone():
            self.current_milestone_index += 1
        return self.is_complete()

    def fallback(self):
        fallback_index = self.current_milestone().fallback
        self.current_milestone_index += fallback_index

    def is_complete(self):
        return self.current_milestone_index >= len(self.milestones)

    def set_unique_goal_from_file(self, goal_file=None, brain=None):
        """Sets a unique goal description based on specific requirements or PRD."""
        if goal_file: self.goal_file = goal_file
        requirements_file = open(self.goal_file, "r")
        requirements_text = requirements_file.read()
        goal_prompt = brain.goal_setter.prompt_builder.build_prompt(requirements_text, '')
        print(f"Goal prompt: {goal_prompt}")
        unique_goal = brain.goal_setter.process(goal_prompt)
        brain.memory.store_memory(goal_prompt, unique_goal, module="GoalSetter")
        print(f"Unique goal set: {unique_goal}")
        return unique_goal


    def get_progress_description(self):
        """Returns a formatted description of the goal and current milestone for the prompt."""
        progress = f"Goal: {self.description}\n"
        progress += f"Milestone {self.current_milestone_index + 1}/{len(self.milestones)}: {self.current_milestone().description}\n"
        progress += f"Progress: {self.current_milestone_index}/{len(self.milestones)} milestones completed.\n"
        return progress
