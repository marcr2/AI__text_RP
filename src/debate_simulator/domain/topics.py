from typing import List
import random


class DebateTopics:
    """Manages available debate topics."""
    
    DEFAULT_TOPICS = [
        "Healthcare reform and the role of government in healthcare",
        "Climate change and environmental policy",
        "Tax policy and economic inequality",
        "Immigration reform and border security",
        "Gun control and Second Amendment rights",
        "Education policy and school choice",
        "Foreign policy and international relations",
        "Social media regulation and free speech",
        "Criminal justice reform",
        "Infrastructure spending and government investment",
    ]
    
    def __init__(self, custom_topics: List[str] = None):
        """Initialize with default and optional custom topics."""
        self._topics = self.DEFAULT_TOPICS.copy()
        if custom_topics:
            self._topics.extend(custom_topics)
    
    def get_all_topics(self) -> List[str]:
        """Get all available topics."""
        return self._topics.copy()
    
    def get_random_topic(self) -> str:
        """Get a random topic."""
        return random.choice(self._topics)
    
    def add_topic(self, topic: str) -> None:
        """Add a new topic."""
        if topic and topic not in self._topics:
            self._topics.append(topic)
    
    def remove_topic(self, topic: str) -> None:
        """Remove a topic."""
        if topic in self._topics:
            self._topics.remove(topic)
    
    def search_topics(self, keyword: str) -> List[str]:
        """Search topics by keyword."""
        keyword_lower = keyword.lower()
        return [topic for topic in self._topics if keyword_lower in topic.lower()]
    
    def validate_topic(self, topic: str) -> bool:
        """Validate if a topic is suitable for debate."""
        if not topic or not topic.strip():
            return False
        
        # Basic validation - topic should be substantial
        if len(topic.strip()) < 10:
            return False
        
        return True


# Topic categories for better organization
class TopicCategories:
    """Categorizes topics for better organization."""
    
    CATEGORIES = {
        "Economic Policy": [
            "Tax policy and economic inequality",
            "Infrastructure spending and government investment",
            "Healthcare reform and the role of government in healthcare",
        ],
        "Social Issues": [
            "Gun control and Second Amendment rights",
            "Criminal justice reform",
            "Immigration reform and border security",
        ],
        "Environment & Science": [
            "Climate change and environmental policy",
        ],
        "Technology & Media": [
            "Social media regulation and free speech",
        ],
        "Education & Culture": [
            "Education policy and school choice",
        ],
        "Foreign Affairs": [
            "Foreign policy and international relations",
        ]
    }
    
    @classmethod
    def get_category_topics(cls, category: str) -> List[str]:
        """Get topics for a specific category."""
        return cls.CATEGORIES.get(category, [])
    
    @classmethod
    def get_all_categories(cls) -> List[str]:
        """Get all available categories."""
        return list(cls.CATEGORIES.keys())
    
    @classmethod
    def get_topic_category(cls, topic: str) -> str:
        """Find which category a topic belongs to."""
        for category, topics in cls.CATEGORIES.items():
            if topic in topics:
                return category
        return "Other"


def get_default_topics() -> List[str]:
    """Convenience function to get default topics."""
    return DebateTopics.DEFAULT_TOPICS.copy()


def create_topic_prompt(topic: str) -> str:
    """Create an initial prompt for starting a debate on the given topic."""
    return f"Let's discuss {topic}. What are your thoughts on this issue?"