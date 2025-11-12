import random
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class User:
    """Represents a user in the simulation"""
    user_id: int
    preferences: Dict
    feedback: List[Dict] = None

    def __post_init__(self):
        if self.feedback is None:
            self.feedback = []

class UserFeedbackSimulation:
    """Handles individual simulation logic"""
    def __init__(self):
        self.users = []
        self.current_phase = 0
        self.results = []

    def initialize_simulation(self):
        """Set up initial simulation state"""
        # Create some sample users with random preferences
        for i in range(3):  # Default 3 users
            user = User(
                user_id=i,
                preferences={
                    'response_time': random.uniform(0, 1),
                    'accuracy': random.uniform(0, 1),
                    'detail_level': random.uniform(0, 1)
                }
            )
            self.users.append(user)

    def run_simulation(self):
        """Execute the simulation"""
        # Simulate user feedback collection
        for user in self.users:
            feedback = self.generate_user_feedback(user)
            user.feedback.append(feedback)
            self.results.append({
                'user_id': user.user_id,
                'feedback': feedback
            })

    def generate_user_feedback(self, user: User) -> Dict:
        """Generate synthetic user feedback based on preferences"""
        return {
            'satisfaction': random.uniform(0, 1),
            'response_quality': random.uniform(0, 1),
            'would_recommend': random.choice([True, False]),
            'timestamp': '2023-01-01T00:00:00Z'  # Placeholder timestamp
        }

    def save_results(self, filename: str):
        """Save simulation results to file"""
        with open(filename, 'w') as f:
            json.dump({
                'users': len(self.users),
                'results': self.results
            }, f, indent=4)