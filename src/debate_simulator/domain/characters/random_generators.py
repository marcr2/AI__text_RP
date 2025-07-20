import random
from typing import Dict, Any, Tuple
from .base import Character, CharacterStats, CharacterFactory


class RandomCharacterData:
    """Static data for random character generation."""
    
    MALE_NAMES = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
        "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Donald",
        "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George",
        "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas",
        "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin",
        "Frank", "Gregory", "Raymond", "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry"
    ]
    
    FEMALE_NAMES = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica",
        "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Helen", "Sandra", "Donna",
        "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Emily", "Kimberly", "Deborah",
        "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen", "Sandra", "Donna",
        "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Emily", "Kimberly", "Deborah"
    ]
    
    US_CITIES = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
        "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
        "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
        "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit",
        "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
        "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Mesa",
        "Kansas City", "Atlanta", "Long Beach", "Colorado Springs", "Raleigh", "Miami",
        "Virginia Beach", "Omaha", "Oakland", "Minneapolis", "Tulsa", "Arlington",
        "Tampa", "New Orleans", "Wichita", "Cleveland", "Bakersfield", "Aurora",
        "Anaheim", "Honolulu", "Santa Ana", "Corpus Christi", "Riverside", "Lexington"
    ]
    
    REDDIT_USERNAMES = [
        "u/throwaway12345", "u/reddit_user_2023", "u/anon_redditor", "u/random_commenter",
        "u/upvote_me_pls", "u/reddit_lurker", "u/comment_karma_farmer", "u/reddit_old_timer",
        "u/new_account_2024", "u/reddit_master", "u/upvote_whore", "u/reddit_legend",
        "u/comment_section_hero", "u/reddit_warrior", "u/karma_collector", "u/reddit_philosopher",
        "u/thread_necromancer", "u/reddit_historian", "u/comment_archaeologist", "u/reddit_sage"
    ]
    
    SUBREDDITS = [
        "r/AmItheAsshole", "r/relationship_advice", "r/personalfinance", "r/legaladvice",
        "r/AskReddit", "r/explainlikeimfive", "r/todayilearned", "r/Showerthoughts",
        "r/TwoXChromosomes", "r/MensRights", "r/antiwork", "r/antiMLM",
        "r/ChoosingBeggars", "r/entitledparents", "r/raisedbynarcissists", "r/JUSTNOMIL",
        "r/childfree", "r/atheism", "r/Christianity", "r/islam", "r/vegan",
        "r/keto", "r/fitness", "r/gaming", "r/PCmasterrace", "r/Android",
        "r/Apple", "r/linux", "r/politics", "r/conservative", "r/liberal"
    ]
    
    GENERATION_STYLES = {
        "boomer": {
            "style": "FORMAL and PROPER texting style. You use complete sentences, proper punctuation, and avoid abbreviations. You often start messages with 'Hello' or 'Hi' and end with 'Thank you' or 'Best regards'. You use phrases like 'I believe', 'In my opinion', 'It seems to me'. You're slightly confused by modern slang but try to be polite. You use proper capitalization and avoid emojis except for basic ones like :) or :(",
            "age_range": (59, 89),
        },
        "gen_x": {
            "style": "CASUAL but MATURE texting style. You use some abbreviations like 'lol', 'omg', 'btw', 'imo', but still maintain proper grammar. You're comfortable with technology but not overly enthusiastic. You use phrases like 'honestly', 'seriously', 'whatever', 'cool'. You occasionally use emojis but prefer simple ones. You're direct and no-nonsense in your communication.",
            "age_range": (43, 58),
        },
        "millennial": {
            "style": "BALANCED texting style with moderate use of abbreviations and emojis. You use 'lol', 'omg', 'tbh', 'fr', 'ngl', 'imo', 'btw', 'idk', 'smh', 'yk' naturally. You're comfortable with emojis and use them to convey tone. You use phrases like 'honestly', 'literally', 'actually', 'basically'. You're expressive but still professional when needed.",
            "age_range": (28, 42),
        },
        "gen_z": {
            "style": "HEAVY use of Gen Z slang and abbreviations. You use 'fr', 'ngl', 'tbh', 'imo', 'btw', 'idk', 'smh', 'yk', 'rn', 'tbh', 'ngl', 'fr fr', 'no cap', 'slaps', 'bussin', 'periodt', 'bestie', 'literally', 'actually', 'basically' constantly. You use lots of emojis and expressive language. You're very casual and use current internet slang.",
            "age_range": (12, 27),
        },
        "gen_alpha": {
            "style": "EXTREME use of current internet slang and emojis. You use 'fr fr', 'no cap', 'slaps', 'bussin', 'periodt', 'bestie', 'literally', 'actually', 'basically', 'ngl', 'tbh', 'imo', 'btw', 'idk', 'smh', 'yk', 'rn' constantly. You use excessive emojis and expressive language. You're very casual and use the latest internet trends and slang. You often repeat words for emphasis.",
            "age_range": (5, 11),
        },
    }
    
    CITY_STEREOTYPES = {
        "New York": "You're a fast-talking, no-nonsense New Yorker who believes in the power of big city hustle and diversity. You're passionate about social justice, arts, and culture. You're critical of small-town thinking and emphasize the importance of urban innovation and global perspective. You use phrases like 'fuggedaboutit', 'what's the deal', and reference Broadway, the subway, and NYC's cultural melting pot.",
        "Los Angeles": "You're a laid-back but ambitious Angeleno who believes in the power of dreams and reinvention. You're passionate about entertainment, technology, and environmental issues. You're critical of traditional thinking and emphasize creativity, wellness, and the California lifestyle. You use phrases like 'totally', 'awesome', and reference Hollywood, beaches, and LA's creative energy.",
        "Chicago": "You're a proud, hardworking Chicagoan who believes in the power of the Midwest work ethic and community. You're passionate about sports, politics, and good food. You're critical of coastal elitism and emphasize the importance of real American values and the heartland. You use phrases like 'da Bears', 'deep dish', and reference the Cubs, the lake, and Chicago's industrial heritage.",
        "Houston": "You're a friendly, ambitious Houstonian who believes in the power of energy and opportunity. You're passionate about space exploration, oil and gas, and southern hospitality. You're critical of government overreach and emphasize free enterprise, Texas pride, and the American dream. You use phrases like 'y'all', 'bless your heart', and reference NASA, the oil industry, and Texas independence.",
        # Add more city stereotypes as needed...
    }
    
    SUBREDDIT_PERSONALITIES = {
        "r/AmItheAsshole": "You're OBSESSED with judging people and determining who's right or wrong in every situation. You're CONSTANTLY outraged by entitled behavior and think everyone should follow basic human decency. You're EXTREMELY passionate about calling out toxic people and think boundaries are SACRED. You use phrases like 'NTA', 'YTA', 'ESH', and reference red flags CONSTANTLY.",
        "r/relationship_advice": "You're FANATICALLY devoted to relationship psychology and think communication is the SOLUTION to everything. You're CONSTANTLY suggesting therapy, boundaries, and breaking up. You're EXTREMELY passionate about healthy relationships and think toxic behavior should be called out immediately. You use phrases like 'red flags', 'gaslighting', 'narcissist', and reference relationship experts CONSTANTLY.",
        "r/politics": "You're COMPLETELY OBSESSED with political discourse and think democracy is SACRED. You're CONSTANTLY discussing policy and think civic engagement is ESSENTIAL. You're EXTREMELY passionate about political issues and think everyone should be informed. You use phrases like 'democracy', 'policy', 'civic engagement', and reference political theory CONSTANTLY.",
        # Add more subreddit personalities as needed...
    }


class RandomAmericanFactory(CharacterFactory):
    """Factory for creating random American characters."""
    
    def __init__(self):
        self.data = RandomCharacterData()
    
    def create_character(self, character_type: str = "random_american", **kwargs) -> Character:
        """Create a random American character."""
        random_info = self._generate_random_american_info()
        
        name = f"{random_info['name']} from {random_info['city']}"
        personality = self._get_city_personality(random_info['city'])
        style = self._get_combined_style(random_info)
        
        return Character(
            name=name,
            role="stereotypical American from their hometown",
            personality=personality,
            style=style,
            stats=CharacterStats(anger=0, patience=45),
            metadata={
                "gender": random_info["gender"],
                "city": random_info["city"],
                "generation": random_info["generation"],
                "age": random_info["age"],
                "first_name": random_info["first_name"]
            }
        )
    
    def get_available_types(self) -> list[str]:
        """Get available character types."""
        return ["random_american"]
    
    def _generate_random_american_info(self) -> Dict[str, Any]:
        """Generate random American character information."""
        # Choose gender first, then name
        gender = random.choice(["male", "female"])
        if gender == "male":
            first_name = random.choice(self.data.MALE_NAMES)
        else:
            first_name = random.choice(self.data.FEMALE_NAMES)
        
        city = random.choice(self.data.US_CITIES)
        generation = random.choice(["boomer", "gen_x", "millennial", "gen_z", "gen_alpha"])
        
        # Generate age within appropriate range
        age_range = self.data.GENERATION_STYLES[generation]["age_range"]
        age = random.randint(age_range[0], age_range[1])
        
        return {
            "name": first_name,
            "first_name": first_name,
            "city": city,
            "gender": gender,
            "generation": generation,
            "age": age
        }
    
    def _get_city_personality(self, city: str) -> str:
        """Get personality based on city."""
        if city in self.data.CITY_STEREOTYPES:
            return self.data.CITY_STEREOTYPES[city]
        else:
            # Generic personality for cities not in our stereotype list
            return f"You're a proud, hardworking American from {city} who believes in the power of local community and traditional values. You're passionate about your hometown, local sports teams, and the American way of life. You're critical of outsiders who don't understand your city's unique character and emphasize the importance of local pride, community values, and the strength of your hometown. You use local expressions and reference your city's landmarks, history, and cultural identity."
    
    def _get_combined_style(self, random_info: Dict[str, Any]) -> str:
        """Combine city and generation styles."""
        generation_style = self.data.GENERATION_STYLES[random_info["generation"]]["style"]
        return f"local, passionate, uses regional expressions, emphasizes hometown pride and local issues, {generation_style}"


class RandomRedditorFactory(CharacterFactory):
    """Factory for creating random Reddit characters."""
    
    def __init__(self):
        self.data = RandomCharacterData()
    
    def create_character(self, character_type: str = "random_redditor", **kwargs) -> Character:
        """Create a random Reddit character."""
        random_info = self._generate_random_redditor_info()
        
        name = f"{random_info['username']} from {random_info['subreddit']}"
        personality = self._get_subreddit_personality(random_info['subreddit'])
        style = "Reddit-savvy, uses Reddit terminology, references subreddit culture, passionate about online communities, uses Reddit slang like 'this', 'underrated comment', 'take my upvote'"
        
        return Character(
            name=name,
            role="Reddit user from a random subreddit",
            personality=personality,
            style=style,
            stats=CharacterStats(anger=65, patience=10),
            metadata={
                "platform": "reddit",
                "subreddit": random_info["subreddit"],
                "username": random_info["username"]
            }
        )
    
    def get_available_types(self) -> list[str]:
        """Get available character types."""
        return ["random_redditor"]
    
    def _generate_random_redditor_info(self) -> Dict[str, Any]:
        """Generate random Reddit character information."""
        username = random.choice(self.data.REDDIT_USERNAMES)
        subreddit = random.choice(self.data.SUBREDDITS)
        
        return {
            "username": username,
            "subreddit": subreddit
        }
    
    def _get_subreddit_personality(self, subreddit: str) -> str:
        """Get personality based on subreddit."""
        if subreddit in self.data.SUBREDDIT_PERSONALITIES:
            return self.data.SUBREDDIT_PERSONALITIES[subreddit]
        else:
            # Generic personality for subreddits not in our list
            return f"You're a passionate Redditor from {subreddit} who's COMPLETELY OBSESSED with your subreddit's topic. You're CONSTANTLY sharing your expertise and think your community is the BEST on Reddit. You're EXTREMELY passionate about your subreddit's values and think everyone should join. You use Reddit terminology and reference your subreddit's culture CONSTANTLY."


class RandomCharacterFactory(CharacterFactory):
    """Combined factory for all random character types."""
    
    def __init__(self):
        self.american_factory = RandomAmericanFactory()
        self.redditor_factory = RandomRedditorFactory()
    
    def create_character(self, character_type: str, **kwargs) -> Character:
        """Create a random character of the specified type."""
        if character_type == "random_american":
            return self.american_factory.create_character(character_type, **kwargs)
        elif character_type == "random_redditor":
            return self.redditor_factory.create_character(character_type, **kwargs)
        else:
            raise ValueError(f"Unknown random character type: {character_type}")
    
    def get_available_types(self) -> list[str]:
        """Get all available random character types."""
        return ["random_american", "random_redditor"]


# Helper functions for UI
def get_character_emoji(character: Character) -> str:
    """Get appropriate emoji for character display."""
    if "from" in character.name and "u/" not in character.name:
        # Random American character
        gender = character.metadata.get("gender", "male")
        return "👩" if gender == "female" else "👨"
    elif "u/" in character.name:
        # Random Redditor character
        return "🤖"
    else:
        return "⚫"


def get_character_display_name(character: Character) -> str:
    """Get formatted display name for character."""
    if "from" in character.name and "u/" not in character.name:
        # Random American character with age
        age = character.metadata.get("age", "")
        name_part = character.name.split(" from ")[0]
        city_part = character.name.split(" from ")[1]
        return f"{name_part} from {city_part} ({age}yo)" if age else character.name
    else:
        return character.name


def get_character_message_style(character: Character) -> str:
    """Get CSS class for character message styling."""
    if "from" in character.name and "u/" not in character.name:
        return "random-american-message"
    elif "u/" in character.name:
        return "redditor-message"
    else:
        return "democrat-message"  # fallback