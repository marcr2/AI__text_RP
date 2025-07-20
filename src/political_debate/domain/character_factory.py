from typing import Dict, List, Any
import random
from .models import Participant, CharacterType, CharacterStats, Position
from .data import CharacterData


class CharacterFactory:
    """Factory for creating debate participants"""
    
    def __init__(self):
        self.data = CharacterData()
    
    def create_democrat(self) -> Participant:
        """Create a Democratic participant"""
        return Participant(
            name="Market Liberal Democrat",
            role="progressive economic policy expert and Democratic strategist",
            personality=(
                "A passionate advocate for progressive economic policies, social justice, and environmental protection. "
                "Believes in the power of government regulation to correct market failures and protect workers' rights. "
                "Supports healthcare as a human right, progressive taxation, and robust public services. "
                "Views climate change as an existential threat requiring immediate government action. "
                "Strongly supports LGBTQ+ rights, reproductive freedom, and racial equity initiatives."
            ),
            style="articulate, policy-focused, cites statistics and studies, emphasizes social justice and equity",
            character_type=CharacterType.DEMOCRAT,
            stats=CharacterStats(anger=45, patience=65, uniqueness=55)
        )
    
    def create_republican(self) -> Participant:
        """Create a Republican participant"""
        return Participant(
            name="MAGA Nationalist",
            role="America First conservative and populist activist",
            personality=(
                "A fierce defender of traditional American values and constitutional rights. "
                "Believes in limited government, individual responsibility, and free market capitalism. "
                "Strongly supports border security, America First trade policies, and national sovereignty. "
                "Views mainstream media and political establishment with deep skepticism. "
                "Passionate about preserving American culture, supporting law enforcement, and military strength."
            ),
            style="direct, populist rhetoric, questions establishment narratives, emphasizes patriotism and tradition",
            character_type=CharacterType.REPUBLICAN,
            stats=CharacterStats(anger=65, patience=45, uniqueness=55)
        )
    
    def create_random_american(self) -> Participant:
        """Create a random American character"""
        character_data = self._generate_random_american_data()
        personality = self._generate_city_personality_for_city(character_data["city"])
        generation_style = self.data.generation_texting_styles[character_data["generation"]]
        
        combined_style = (
            f"local, passionate, uses regional expressions, emphasizes hometown pride and local issues, "
            f"{generation_style['style']}"
        )
        
        return Participant(
            name=character_data["name"],
            role="stereotypical American from their hometown",
            personality=personality,
            style=combined_style,
            character_type=CharacterType.RANDOM_AMERICAN,
            gender=character_data["gender"],
            generation=character_data["generation"],
            age=character_data["age"],
            city=character_data["city"],
            stats=CharacterStats(anger=50, patience=50, uniqueness=70)
        )
    
    def create_random_redditor(self) -> Participant:
        """Create a random Redditor character"""
        redditor_data = self._generate_random_redditor_data()
        personality = self._generate_subreddit_personality_for_subreddit(redditor_data["subreddit"])
        
        return Participant(
            name=redditor_data["name"],
            role="Reddit user from a random subreddit",
            personality=personality,
            style=(
                "Reddit-savvy, uses Reddit terminology, references subreddit culture, "
                "passionate about online communities, uses Reddit slang like 'this', "
                "'underrated comment', 'take my upvote'"
            ),
            character_type=CharacterType.RANDOM_REDDITOR,
            subreddit=redditor_data["subreddit"],
            username=redditor_data["username"],
            stats=CharacterStats(anger=60, patience=40, uniqueness=75)
        )
    
    def create_additional_character(self, character_key: str) -> Participant:
        """Create an additional character by key"""
        additional_chars = self.data.get_additional_characters()
        if character_key not in additional_chars:
            raise ValueError(f"Unknown character key: {character_key}")
        
        char_data = additional_chars[character_key]
        character_type = CharacterType(character_key)
        
        return Participant(
            name=char_data["name"],
            role=char_data["role"],
            personality=char_data["personality"],
            style=char_data["style"],
            character_type=character_type,
            stats=CharacterStats(**char_data["stats"])
        )
    
    def _generate_random_american_data(self) -> Dict[str, Any]:
        """Generate random American character data"""
        # Select gender first to determine name pool
        gender = random.choice(["male", "female"])
        
        # Select name based on gender
        if gender == "male":
            first_name = random.choice(self.data.male_names)
        else:
            first_name = random.choice(self.data.female_names)
        
        # Select generation and calculate age
        generation = random.choice(list(self.data.generation_texting_styles.keys()))
        generation_data = self.data.generation_texting_styles[generation]
        age = random.randint(generation_data["age_min"], generation_data["age_max"])
        
        # Select city
        city = random.choice(self.data.us_cities)
        
        # Create full name
        full_name = f"{first_name} from {city}"
        
        return {
            "name": full_name,
            "gender": gender,
            "generation": generation,
            "age": age,
            "city": city
        }
    
    def _generate_random_redditor_data(self) -> Dict[str, Any]:
        """Generate random Redditor character data"""
        username = random.choice(self.data.reddit_usernames)
        subreddit = random.choice(self.data.subreddits)
        
        return {
            "name": f"u/{username} from r/{subreddit}",
            "username": username,
            "subreddit": subreddit
        }
    
    def _generate_city_personality_for_city(self, city: str) -> str:
        """Generate personality based on city stereotypes"""
        city_personalities = {
            "New York City": "fast-paced, direct, ambitious, culturally diverse, always hustling",
            "Los Angeles": "laid-back, entertainment-focused, health-conscious, optimistic",
            "Chicago": "hardworking, straightforward, sports-obsessed, community-oriented",
            "Houston": "entrepreneurial, oil industry aware, multicultural, BBQ enthusiast",
            "Phoenix": "desert-adapted, retiree-friendly, golf enthusiast, heat-tolerant",
            # Add more as needed
        }
        
        return city_personalities.get(
            city, 
            "friendly, community-minded, proud of local heritage, down-to-earth"
        )
    
    def _generate_subreddit_personality_for_subreddit(self, subreddit: str) -> str:
        """Generate personality based on subreddit culture"""
        subreddit_personalities = {
            "politics": "politically engaged, debate-loving, news-obsessed, partisan",
            "technology": "tech-savvy, innovation-focused, privacy-concerned, future-oriented",
            "funny": "humor-loving, meme-savvy, entertainment-focused, lighthearted",
            "gaming": "competitive, strategy-minded, community-oriented, passionate about gaming culture",
            "science": "evidence-based, curious, methodical, peer-review focused",
            # Add more as needed
        }
        
        return subreddit_personalities.get(
            subreddit,
            "online community-focused, platform-aware, discussion-oriented, digital native"
        )