import random
import json
import time
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class EnhancedUser:
    user_id: int
    preferences: Dict
    feedback: List[Dict]
    experience_level: str
    interaction_history: List[Dict]

class EnhancedSimulation(UserFeedbackSimulation):
    def __init__(self):
        super().__init__()
        self.metrics = {}
        self.start_time = None
        
    def initialize_simulation(self):
        self.start_time = time.time()
        experience_levels = ['beginner', 'intermediate', 'expert']
        
        for i in range(3):
            user = EnhancedUser(
                user_id=i,
                preferences={
                    'response_time': random.uniform(0, 1),
                    'accuracy': random.uniform(0, 1),
                    'detail_level': random.uniform(0, 1)
                },
                feedback=[],
                experience_level=random.choice(experience_levels),
                interaction_history=[]
            )
            self.users.append(user)

    def collect_metrics(self):
        self.metrics = {
            'duration': time.time() - self.start_time,
            'total_users': len(self.users),
            'feedback_count': sum(len(user.feedback) for user in self.users),
            'average_satisfaction': np.mean([
                feedback['satisfaction'] 
                for user in self.users 
                for feedback in user.feedback
            ])
        }

