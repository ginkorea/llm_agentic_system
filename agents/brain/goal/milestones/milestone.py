# milestone.py

from abc import ABC, abstractmethod

class Milestone(ABC):
    def __init__(self, description, milestone_id=None, fallback=-1):
        self.description = description
        self.achieved = False
        self.m_id = milestone_id
        self.fallback = fallback

    @abstractmethod
    def is_achieved(self, brain, input_data):
        """Check if the milestone has been achieved. This should be overridden in each subclass."""
        return True