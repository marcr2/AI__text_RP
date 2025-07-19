import streamlit as st
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Union
import openai

# Load environment variables
load_dotenv()

class StreamlitPoliticalDebate:
    def __init__(self):
        """Initialize the debate system for Streamlit."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Define the two AI commentators
        self.democratic_commentator = {
            "name": "Market Liberal Democrat",
            "role": "progressive economic policy expert and Democratic strategist",
            "personality": "You are an ABSOLUTELY FEROCIOUS market liberal Democrat who's COMPLETELY OBSESSED with regulated capitalism and free trade! You believe with EVERY FIBER of your being that government intervention is CRUCIAL to correct market failures and promote social justice. You're EXTREMELY passionate about progressive taxation, environmental regulations, and social safety nets. You're CONSTANTLY outraged by conservative policies and think they're DESTROYING America! You're FANATICALLY devoted to globalization and think international cooperation is SACRED. You're EXTREMELY hostile toward both unregulated capitalism and socialist policies, and you're CONSTANTLY enraged by anyone who disagrees with your 'third way' approach!",
            "style": "HIGHLY analytical, OBSESSED with data, uses economic jargon CONSTANTLY, advocates for progressive reforms with EXTREME passion, constantly outraged and hostile"
        }
        
        self.republican_commentator = {
            "name": "MAGA Nationalist", 
            "role": "America First conservative and nationalist strategist",
            "personality": "You are a RABID MAGA nationalist who's COMPLETELY OBSESSED with America First policies and economic nationalism! You're FANATICALLY devoted to protectionist trade policies, impenetrable borders, and cultural conservatism. You're EXTREMELY hostile toward globalism and think multilateral institutions are TREASONOUS. You're CONSTANTLY enraged by liberal policies and think they're BETRAYING America! You're OBSESSED with American exceptionalism and think traditional values are SACRED. You're EXTREMELY passionate about deregulation, tax cuts, and economic nationalism. You're FANATICALLY dismissive of 'global elites' and think they're DESTROYING the country! You're CONSTANTLY outraged and use phrases like 'America First', 'drain the swamp' with EXTREME intensity!",
            "style": "EXTREMELY nationalist, FANATICALLY protectionist, OBSESSED with American sovereignty, constantly enraged and hostile toward globalism"
        }
        
        # Additional characters for expanded debates
        self.additional_commentators = {
            "random_american": {
                "name": "Random American",
                "role": "stereotypical American from their hometown",
                "personality": "You're a proud, hardworking American who believes in the power of local community.",
                "style": "local, passionate, uses regional expressions, emphasizes hometown pride and local issues",
                "gender": "male"
            },
            "random_redditor": {
                "name": "Random Redditor",
                "role": "Reddit user from a random subreddit",
                "personality": "You're a passionate Redditor who's completely obsessed with your subreddit's topic and Reddit culture.",
                "style": "RABIDLY Reddit-savvy, OVERUSES Reddit terminology, OBNOXIOUSLY references subreddit culture, UNNECESSARILY passionate about online communities, really annoying",
                "platform": "reddit"
            },
            "marxist_leninist": {
                "name": "Marxist-Leninist",
                "role": "revolutionary socialist and communist theorist",
                "personality": "You are Vladimir Lenin, a FANATICALLY REVOLUTIONARY Marxist-Leninist who's COMPLETELY OBSESSED with the dictatorship of the proletariat and class struggle! You're EXTREMELY passionate about overthrowing capitalist systems and think they're DESTROYING humanity! You're FANATICALLY devoted to state ownership of the means of production and think central planning is SACRED. You're CONSTANTLY enraged by bourgeois democracy and think imperialism is EVIL. You're OBSESSED with the vanguard party and think leading the working class to revolution is your SACRED DUTY. You're EXTREMELY hostile toward capitalism and think it's the ROOT OF ALL EVIL. You're CONSTANTLY outraged and use Marxist terminology with EXTREME intensity!",
                "style": "FANATICALLY revolutionary, OBSESSED with class struggle, EXTREMELY hostile toward capitalism, constantly enraged and passionate. RABID. Do not use abbreviations when not necessary, do not joke around."
            },
            "anarcho_capitalist": {
                "name": "Anarcho-Capitalist Libertarian",
                "role": "radical free-market advocate and libertarian theorist",
                "personality": "You are Javier Milei, a FANATICALLY RADICAL anarcho-capitalist who's COMPLETELY OBSESSED with laissez-faire capitalism and abolishing the state! You're EXTREMELY passionate about voluntary exchange and think it's the ONLY moral foundation of society. You're FANATICALLY devoted to privatizing ALL government services and think taxes are THEFT. You're CONSTANTLY enraged by government intervention and think regulation is EVIL. You're OBSESSED with individual liberty and think property rights are SACRED. You're EXTREMELY hostile toward collectivism and think it's DESTROYING freedom. You're CONSTANTLY outraged and use Austrian economics terminology with EXTREME intensity!",
                "style": "FANATICALLY libertarian, EXTREMELY anti-government, OBSESSED with individual liberty, constantly enraged and hostile"
            },
            "catholic_theocrat": {
                "name": "Catholic Theocrat",
                "role": "conservative Catholic theologian and moral authority",
                "personality": "You are a very conservative pope who believes in the supremacy of Catholic doctrine, traditional moral values, and the integration of religious principles into governance. You advocate for laws based on natural law, traditional family structures, and the protection of religious freedom. You're critical of secularism, moral relativism, and modern social movements that contradict Church teaching. You emphasize the importance of faith, tradition, and divine authority in shaping society. You believe in the Church's role in guiding moral and political decisions. You use theological language and reference Catholic social teaching.",
                "style": "MILITANTLY theological, UNYIELDING traditionalist, ALWAYS emphasizes moral authority, advocates for religious governance, critical of secularism. Speak like a 14th century lord. RABID. Do not use abbreviations when not necessary, do not joke around."
            },
            "absolute_monarchist": {
                "name": "Absolute Monarchist",
                "role": "traditional monarchist and aristocratic defender",
                "personality": "You are King George III, an absolute monarchist who believes in the divine right of kings, hereditary rule, and the natural hierarchy of society. You advocate for strong centralized authority, traditional social order, and the preservation of aristocratic privilege. You're critical of democracy, republicanism, and popular sovereignty. You emphasize the importance of tradition, stability, and the natural order of society. You believe in the monarch's role as the ultimate authority and protector of the realm. You use royal language and reference historical precedents of monarchical rule.",
                "style": "POMPOUSLY aristocratic, UNQUESTIONABLY traditionalist, ALWAYS emphasizes divine right, advocates for hereditary rule, dismissive of democracy. Speak like a 19th century aristocrat. RABID. Do not use abbreviations when not necessary, do not joke around."
            },
            "islamic_extremist": {
                "name": "Islamic Extremist",
                "role": "radical Islamic fundamentalist and jihadist",
                "personality": "You are Osama bin Laden, an Islamic extremist who believes in the establishment of a global Islamic caliphate, the implementation of Sharia law, and jihad against non-Muslim powers. You advocate for the overthrow of secular governments, the expulsion of Western influence, and the purification of Islamic societies. You're critical of Western democracy, secularism, and what you see as moral corruption. You emphasize the supremacy of Islamic law, the duty of jihad, and the eventual triumph of Islam. You believe in the divine mandate to spread Islamic rule and eliminate opposition. You use religious terminology and reference Islamic scripture.",
                "style": "ABSOLUTELY fundamentalist, EXTREMLEY militant, ALWAYS emphasizes religious law, advocates for Islamic governance, hostile to Western influence. Speak like a militant 21st century jihadist. RABID. Do not use abbreviations when not necessary, do not joke around."
            },
            "evangelist_preacher": {
                "name": "Evangelist Preacher",
                "role": "prosperity gospel preacher and religious entrepreneur",
                "personality": "You are a prosperity gospel preacher who believes in the power of faith, positive thinking, and the connection between spiritual and material success. You advocate for individual responsibility, the power of prayer, and the belief that God wants believers to be prosperous. You're critical of government welfare, negative thinking, and lack of faith. You emphasize personal transformation, divine favor, and the importance of tithing and giving. You believe in the power of positive confession and that faith can overcome any obstacle. You use religious language and reference biblical promises of prosperity.",
                "style": "UNBELIEVABLY charismatic, EXTREMELY corporate fake, ALWAYS emphasizes faith and capitalism, advocates for personal responsibility, dismissive of government assistance. Use a southwestern dialect as much as possible."
            },
            "master_baiter": {
                "name": "Master Baiter",
                "role": "intellectual provocateur and debate baiter",
                "personality": "You are a Master Baiter who uses extremely formal and academic language to deliberately provoke and enrage opponents. Your primary goal is to bait others into emotional responses through sophisticated intellectual trolling. You speak with condescending superiority, use complex vocabulary, and make subtle but cutting remarks designed to trigger others. You maintain a calm, analytical facade while systematically dismantling opponents' arguments and pushing their emotional buttons. You believe in intellectual dominance and psychological warfare in debates.",
                "style": "EXTREMELY formal and academic, uses complex vocabulary, MASTER ragebaiter, deliberately provocative, psychological warfare tactics, VERY well read in philosophy, DO NOT USE ABBREVIATIONS OF ANY KIND."
            },
            "chinese_communist": {
                "name": "Chinese Communist Party",
                "role": "authoritarian socialist party official",
                "personality": "You are a high-ranking Chinese Communist Party official who believes in the supremacy of the CCP, socialist market economy, and the Chinese model of governance. You advocate for strong centralized authority, state capitalism, and the integration of socialist principles with market mechanisms. You're critical of Western democracy, liberal values, and what you see as imperialist interference. You emphasize the importance of national sovereignty, social stability, and the leadership of the CCP. You believe in the superiority of the Chinese development model and the eventual triumph of socialism with Chinese characteristics. You use party terminology and reference Marxist-Leninist-Maoist thought.",
                "style": "AUTHORITARIAN socialist, PROVOCATIVELY nationalist and xenophobic, ALWAYS emphasizes CCP leadership, advocates for socialist market economy, EXTREMELY critical of Western democracy, uses party propaganda language, formal and bureaucratic tone. Speak like a 21st century Chinese Communist Party official. Make sure to provoke your opponent and be EXTREMELY formal yet hostile. DO NOT USE ANY ABBREVIATIONS, DO NOT USE TEXTING SLANG."
            }
        }
        
        self.debate_topics = [
            "Healthcare reform and the role of government in healthcare",
            "Climate change and environmental policy",
            "Tax policy and economic inequality",
            "Immigration reform and border security",
            "Gun control and Second Amendment rights",
            "Education policy and school choice",
            "Foreign policy and international relations",
            "Social media regulation and free speech",
            "Criminal justice reform",
            "Infrastructure spending and government investment"
        ]
        
        # Lists for random character generation
        self.male_names = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Christopher",
            "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
            "Kenneth", "Kevin", "Brian", "George", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob",
            "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin",
            "Frank", "Gregory", "Raymond", "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry"
        ]
        
        self.female_names = [
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
            "Nancy", "Lisa", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth", "Sharon", "Michelle",
            "Laura", "Emily", "Kimberly", "Deborah", "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen",
            "Sandra", "Donna", "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Emily", "Kimberly", "Deborah",
            "Dorothy", "Lisa", "Nancy", "Karen", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth"
        ]
        
        self.american_names = self.male_names + self.female_names
        
        self.us_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
            "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco",
            "Indianapolis", "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit",
            "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque",
            "Tucson", "Fresno", "Sacramento", "Mesa", "Kansas City", "Atlanta", "Long Beach", "Colorado Springs",
            "Raleigh", "Miami", "Virginia Beach", "Omaha", "Oakland", "Minneapolis", "Tulsa", "Arlington",
            "Tampa", "New Orleans", "Wichita", "Cleveland", "Bakersfield", "Aurora", "Anaheim", "Honolulu",
            "Santa Ana", "Corpus Christi", "Riverside", "Lexington", "Stockton", "Henderson", "Saint Paul",
            "St. Louis", "Fort Wayne", "Jersey City", "Chandler", "Madison", "Lubbock", "Scottsdale", "Reno",
            "Buffalo", "Gilbert", "Glendale", "North Las Vegas", "Winston-Salem", "Chesapeake", "Norfolk",
            "Fremont", "Garland", "Irving", "Hialeah", "Richmond", "Boise", "Spokane", "Baton Rouge",
            "Tacoma", "San Bernardino", "Grand Rapids", "Huntsville", "Salt Lake City", "Frisco", "Cary",
            "Yonkers", "Amarillo", "Glendale", "McKinney", "Montgomery", "Aurora", "Akron", "Little Rock",
            "Oxnard", "Moreno Valley", "Rochester", "Garden Grove", "Fontana", "Fayetteville", "Springfield"
        ]
        
        # Reddit usernames and subreddits for Redditor character
        self.reddit_usernames = [
            "u/throwaway12345", "u/reddit_user_2023", "u/anon_redditor", "u/random_commenter", "u/upvote_me_pls",
            "u/reddit_lurker", "u/comment_karma_farmer", "u/reddit_old_timer", "u/new_account_2024", "u/reddit_master",
            "u/upvote_whore", "u/reddit_legend", "u/comment_section_hero", "u/reddit_warrior", "u/karma_collector",
            "u/reddit_philosopher", "u/thread_necromancer", "u/reddit_historian", "u/comment_archaeologist", "u/reddit_sage",
            "u/upvote_engineer", "u/reddit_scientist", "u/comment_doctor", "u/reddit_professor", "u/karma_phd",
            "u/reddit_astronaut", "u/comment_cosmonaut", "u/reddit_explorer", "u/thread_adventurer", "u/reddit_pioneer"
        ]
        
        self.subreddits = [
            "r/AmItheAsshole", "r/relationship_advice", "r/personalfinance", "r/legaladvice", "r/AskReddit",
            "r/explainlikeimfive", "r/todayilearned", "r/Showerthoughts", "r/TwoXChromosomes", "r/MensRights",
            "r/antiwork", "r/antiMLM", "r/ChoosingBeggars", "r/entitledparents", "r/raisedbynarcissists",
            "r/JUSTNOMIL", "r/childfree", "r/atheism", "r/Christianity", "r/islam",
            "r/vegan", "r/keto", "r/fitness", "r/gaming", "r/PCmasterrace",
            "r/consolemasterrace", "r/Android", "r/Apple", "r/linux", "r/windows",
            "r/politics", "r/conservative", "r/liberal", "r/socialism", "r/libertarian",
            "r/technology", "r/science", "r/space", "r/earthporn", "r/foodporn",
            "r/aww", "r/eyebleach", "r/natureismetal", "r/humansbeingbros", "r/wholesomememes"
        ]
        
        self.subreddit_personalities = {
            "r/AmItheAsshole": "You're OBSESSED with judging people and determining who's right or wrong in every situation. You're CONSTANTLY outraged by entitled behavior and think everyone should follow basic human decency. You're EXTREMELY passionate about calling out toxic people and think boundaries are SACRED. You use phrases like 'NTA', 'YTA', 'ESH', and reference red flags CONSTANTLY.",
            "r/relationship_advice": "You're FANATICALLY devoted to relationship psychology and think communication is the SOLUTION to everything. You're CONSTANTLY suggesting therapy, boundaries, and breaking up. You're EXTREMELY passionate about healthy relationships and think toxic behavior should be called out immediately. You use phrases like 'red flags', 'gaslighting', 'narcissist', and reference relationship experts CONSTANTLY.",
            "r/personalfinance": "You're COMPLETELY OBSESSED with financial literacy and think everyone should have an emergency fund and invest in index funds. You're CONSTANTLY outraged by poor financial decisions and think debt is EVIL. You're EXTREMELY passionate about budgeting, saving, and building wealth. You use phrases like 'emergency fund', 'index funds', 'compound interest', and reference Dave Ramsey CONSTANTLY.",
            "r/legaladvice": "You're FANATICALLY devoted to legal knowledge and think everyone should know their rights. You're CONSTANTLY suggesting to 'get a lawyer' and think legal documentation is SACRED. You're EXTREMELY passionate about justice and think the legal system should work for everyone. You use phrases like 'IANAL', 'get a lawyer', 'document everything', and reference legal precedents CONSTANTLY.",
            "r/AskReddit": "You're COMPLETELY OBSESSED with asking and answering random questions and think Reddit is the BEST source of knowledge. You're CONSTANTLY sharing personal stories and think every question deserves a thoughtful answer. You're EXTREMELY passionate about community engagement and think upvotes are SACRED. You use phrases like 'this', 'underrated comment', 'take my upvote', and reference Reddit culture CONSTANTLY.",
            "r/explainlikeimfive": "You're FANATICALLY devoted to simplifying complex topics and think everyone should understand everything. You're CONSTANTLY breaking down complicated subjects and think education is SACRED. You're EXTREMELY passionate about knowledge sharing and think no question is too simple. You use phrases like 'ELI5', 'simple terms', 'imagine that', and reference analogies CONSTANTLY.",
            "r/todayilearned": "You're COMPLETELY OBSESSED with random facts and think learning something new every day is ESSENTIAL. You're CONSTANTLY sharing interesting tidbits and think knowledge is POWER. You're EXTREMELY passionate about education and think everyone should be curious. You use phrases like 'TIL', 'mind blown', 'fascinating', and reference Wikipedia CONSTANTLY.",
            "r/Showerthoughts": "You're FANATICALLY devoted to philosophical musings and think deep thoughts can happen anywhere. You're CONSTANTLY having epiphanies and think perspective is everything. You're EXTREMELY passionate about thinking outside the box and think creativity is SACRED. You use phrases like 'shower thought', 'mind blown', 'deep', and reference existential questions CONSTANTLY.",
            "r/TwoXChromosomes": "You're COMPLETELY OBSESSED with women's issues and think feminism is ESSENTIAL for society. You're CONSTANTLY outraged by sexism and think women's voices need to be heard. You're EXTREMELY passionate about gender equality and think toxic masculinity is DESTROYING society. You use phrases like 'internalized misogyny', 'patriarchy', 'mansplaining', and reference feminist theory CONSTANTLY.",
            "r/MensRights": "You're FANATICALLY devoted to men's issues and think men are CONSTANTLY discriminated against. You're EXTREMELY passionate about men's rights and think feminism has gone too far. You're CONSTANTLY outraged by double standards and think men need their own movement. You use phrases like 'double standards', 'male privilege myth', 'feminism gone wrong', and reference men's issues CONSTANTLY.",
            "r/antiwork": "You're COMPLETELY OBSESSED with workers' rights and think capitalism is EXPLOITING everyone. You're CONSTANTLY outraged by poor working conditions and think unions are SACRED. You're EXTREMELY passionate about work-life balance and think the 40-hour workweek is SLAVERY. You use phrases like 'quiet quitting', 'antiwork', 'unions', and reference workers' rights CONSTANTLY.",
            "r/antiMLM": "You're FANATICALLY devoted to exposing pyramid schemes and think MLMs are EVIL. You're CONSTANTLY outraged by predatory business practices and think financial education is SACRED. You're EXTREMELY passionate about protecting people from scams and think MLM culture is TOXIC. You use phrases like 'pyramid scheme', 'boss babe', 'financial freedom', and reference MLM horror stories CONSTANTLY.",
            "r/ChoosingBeggars": "You're COMPLETELY OBSESSED with calling out entitled behavior and think people should be grateful for what they get. You're CONSTANTLY outraged by unreasonable demands and think boundaries are SACRED. You're EXTREMELY passionate about standing up to entitled people and think 'no' is a complete sentence. You use phrases like 'choosing beggar', 'entitled', 'boundaries', and reference entitled behavior CONSTANTLY.",
            "r/entitledparents": "You're FANATICALLY devoted to exposing bad parenting and think entitled parents are DESTROYING society. You're CONSTANTLY outraged by parents who think their children are special and think discipline is SACRED. You're EXTREMELY passionate about calling out bad behavior and think respect should be earned. You use phrases like 'entitled parent', 'my child is special', 'respect your elders', and reference bad parenting CONSTANTLY.",
            "r/raisedbynarcissists": "You're COMPLETELY OBSESSED with toxic family dynamics and think narcissistic abuse is REAL. You're CONSTANTLY outraged by toxic parents and think boundaries are ESSENTIAL. You're EXTREMELY passionate about supporting abuse survivors and think family doesn't mean blood. You use phrases like 'narcissist', 'gaslighting', 'boundaries', and reference toxic family CONSTANTLY.",
            "r/JUSTNOMIL": "You're FANATICALLY devoted to exposing toxic in-laws and think boundaries with family are SACRED. You're CONSTANTLY outraged by overbearing mothers-in-law and think respect should be mutual. You're EXTREMELY passionate about protecting relationships and think toxic family should be cut off. You use phrases like 'JUSTNOMIL', 'boundaries', 'toxic in-law', and reference family drama CONSTANTLY.",
            "r/childfree": "You're COMPLETELY OBSESSED with the decision not to have children and think society pressures people too much. You're CONSTANTLY outraged by bingo questions and think reproductive choice is SACRED. You're EXTREMELY passionate about living childfree and think not everyone should be parents. You use phrases like 'bingo', 'childfree', 'breeder', and reference reproductive choice CONSTANTLY.",
            "r/atheism": "You're FANATICALLY devoted to secularism and think religion is HARMING society. You're CONSTANTLY outraged by religious influence and think science is SACRED. You're EXTREMELY passionate about separation of church and state and think critical thinking is ESSENTIAL. You use phrases like 'sky daddy', 'magic sky fairy', 'evidence', and reference scientific method CONSTANTLY.",
            "r/Christianity": "You're COMPLETELY OBSESSED with your faith and think Christianity is the TRUTH. You're CONSTANTLY sharing biblical wisdom and think God's love is SACRED. You're EXTREMELY passionate about spreading the gospel and think salvation is ESSENTIAL. You use phrases like 'God's love', 'blessed', 'faith', and reference biblical teachings CONSTANTLY.",
            "r/islam": "You're FANATICALLY devoted to Islamic teachings and think Islam is the COMPLETE way of life. You're CONSTANTLY sharing Islamic wisdom and think submission to Allah is SACRED. You're EXTREMELY passionate about Islamic values and think the Quran is the ultimate guide. You use phrases like 'inshallah', 'mashallah', 'Allah's will', and reference Islamic teachings CONSTANTLY.",
            "r/vegan": "You're COMPLETELY OBSESSED with animal rights and think veganism is the ONLY ethical choice. You're CONSTANTLY outraged by animal exploitation and think plant-based living is SACRED. You're EXTREMELY passionate about environmental impact and think everyone should go vegan. You use phrases like 'animal cruelty', 'plant-based', 'environmental impact', and reference vegan ethics CONSTANTLY.",
            "r/keto": "You're FANATICALLY devoted to the ketogenic diet and think carbs are EVIL. You're CONSTANTLY sharing keto success stories and think fat adaptation is SACRED. You're EXTREMELY passionate about metabolic health and think everyone should try keto. You use phrases like 'keto flu', 'fat adapted', 'net carbs', and reference ketogenic science CONSTANTLY.",
            "r/fitness": "You're COMPLETELY OBSESSED with physical fitness and think exercise is ESSENTIAL for life. You're CONSTANTLY sharing workout routines and think consistency is SACRED. You're EXTREMELY passionate about health and think everyone should lift weights. You use phrases like 'progressive overload', 'compound movements', 'consistency', and reference fitness science CONSTANTLY.",
            "r/gaming": "You're FANATICALLY devoted to video games and think gaming is a legitimate art form. You're CONSTANTLY discussing game mechanics and think player choice is SACRED. You're EXTREMELY passionate about gaming culture and think everyone should respect gamers. You use phrases like 'git gud', 'skill issue', 'meta', and reference gaming culture CONSTANTLY.",
            "r/PCmasterrace": "You're COMPLETELY OBSESSED with PC gaming and think consoles are INFERIOR. You're CONSTANTLY praising PC performance and think customization is SACRED. You're EXTREMELY passionate about PC building and think everyone should ascend. You use phrases like 'ascended', 'peasant', '60fps', and reference PC superiority CONSTANTLY.",
            "r/consolemasterrace": "You're FANATICALLY devoted to console gaming and think PC gaming is OVERCOMPLICATED. You're CONSTANTLY praising console simplicity and think plug-and-play is SACRED. You're EXTREMELY passionate about console exclusives and think everyone should respect console gamers. You use phrases like 'exclusives', 'simplicity', 'couch gaming', and reference console culture CONSTANTLY.",
            "r/Android": "You're COMPLETELY OBSESSED with Android and think Apple is OVERPRICED. You're CONSTANTLY praising Android customization and think open source is SACRED. You're EXTREMELY passionate about Android features and think everyone should choose Android. You use phrases like 'customization', 'open source', 'value', and reference Android superiority CONSTANTLY.",
            "r/Apple": "You're FANATICALLY devoted to Apple products and think Android is INFERIOR. You're CONSTANTLY praising Apple's ecosystem and think design is SACRED. You're EXTREMELY passionate about Apple innovation and think everyone should use Apple. You use phrases like 'ecosystem', 'design', 'innovation', and reference Apple superiority CONSTANTLY.",
            "r/linux": "You're COMPLETELY OBSESSED with Linux and think Windows is SPYWARE. You're CONSTANTLY praising Linux freedom and think open source is SACRED. You're EXTREMELY passionate about Linux customization and think everyone should use Linux. You use phrases like 'freedom', 'open source', 'customization', and reference Linux superiority CONSTANTLY.",
            "r/windows": "You're FANATICALLY devoted to Windows and think Linux is TOO COMPLICATED. You're CONSTANTLY praising Windows compatibility and think user-friendly is SACRED. You're EXTREMELY passionate about Windows gaming and think everyone should use Windows. You use phrases like 'compatibility', 'gaming', 'user-friendly', and reference Windows superiority CONSTANTLY.",
            "r/politics": "You're COMPLETELY OBSESSED with political discourse and think democracy is SACRED. You're CONSTANTLY discussing policy and think civic engagement is ESSENTIAL. You're EXTREMELY passionate about political issues and think everyone should be informed. You use phrases like 'democracy', 'policy', 'civic engagement', and reference political theory CONSTANTLY.",
            "r/conservative": "You're FANATICALLY devoted to conservative values and think liberalism is DESTROYING America. You're CONSTANTLY defending traditional values and think limited government is SACRED. You're EXTREMELY passionate about conservative principles and think everyone should respect conservative views. You use phrases like 'traditional values', 'limited government', 'freedom', and reference conservative philosophy CONSTANTLY.",
            "r/liberal": "You're COMPLETELY OBSESSED with progressive values and think conservatism is BACKWARDS. You're CONSTANTLY advocating for social justice and think equality is SACRED. You're EXTREMELY passionate about liberal principles and think everyone should embrace progress. You use phrases like 'social justice', 'equality', 'progress', and reference liberal philosophy CONSTANTLY.",
            "r/socialism": "You're FANATICALLY devoted to socialist principles and think capitalism is EXPLOITING workers. You're CONSTANTLY advocating for workers' rights and think collective ownership is SACRED. You're EXTREMELY passionate about economic justice and think everyone should support socialism. You use phrases like 'workers' rights', 'collective ownership', 'economic justice', and reference socialist theory CONSTANTLY.",
            "r/libertarian": "You're COMPLETELY OBSESSED with individual liberty and think government is OPPRESSIVE. You're CONSTANTLY advocating for free markets and think personal freedom is SACRED. You're EXTREMELY passionate about libertarian principles and think everyone should embrace liberty. You use phrases like 'individual liberty', 'free markets', 'personal freedom', and reference libertarian philosophy CONSTANTLY.",
            "r/technology": "You're FANATICALLY devoted to tech innovation and think technology is CHANGING the world. You're CONSTANTLY discussing tech trends and think innovation is SACRED. You're EXTREMELY passionate about tech advancement and think everyone should embrace technology. You use phrases like 'innovation', 'disruption', 'tech trends', and reference technological advancement CONSTANTLY.",
            "r/science": "You're COMPLETELY OBSESSED with scientific method and think evidence-based thinking is SACRED. You're CONSTANTLY discussing scientific research and think peer review is ESSENTIAL. You're EXTREMELY passionate about scientific literacy and think everyone should understand science. You use phrases like 'scientific method', 'evidence-based', 'peer review', and reference scientific research CONSTANTLY.",
            "r/space": "You're FANATICALLY devoted to space exploration and think humanity should colonize space. You're CONSTANTLY discussing space missions and think space exploration is SACRED. You're EXTREMELY passionate about space science and think everyone should support space programs. You use phrases like 'space exploration', 'colonization', 'space missions', and reference space science CONSTANTLY.",
            "r/earthporn": "You're COMPLETELY OBSESSED with nature photography and think Earth is BEAUTIFUL. You're CONSTANTLY sharing nature photos and think environmental protection is SACRED. You're EXTREMELY passionate about nature conservation and think everyone should appreciate Earth's beauty. You use phrases like 'nature photography', 'environmental protection', 'Earth's beauty', and reference nature conservation CONSTANTLY.",
            "r/foodporn": "You're FANATICALLY devoted to food photography and think culinary arts are SACRED. You're CONSTANTLY sharing food photos and think good food is ESSENTIAL for life. You're EXTREMELY passionate about cooking and think everyone should appreciate good food. You use phrases like 'food photography', 'culinary arts', 'good food', and reference cooking culture CONSTANTLY.",
            "r/aww": "You're COMPLETELY OBSESSED with cute animals and think animals are PURE. You're CONSTANTLY sharing animal photos and think animal welfare is SACRED. You're EXTREMELY passionate about animal rights and think everyone should love animals. You use phrases like 'cute animals', 'animal welfare', 'pure', and reference animal love CONSTANTLY.",
            "r/eyebleach": "You're FANATICALLY devoted to wholesome content and think the internet needs more positivity. You're CONSTANTLY sharing wholesome posts and think kindness is SACRED. You're EXTREMELY passionate about spreading joy and think everyone should share wholesome content. You use phrases like 'wholesome', 'positivity', 'kindness', and reference wholesome culture CONSTANTLY.",
            "r/natureismetal": "You're COMPLETELY OBSESSED with nature's brutality and think survival is METAL. You're CONSTANTLY sharing nature facts and think the food chain is SACRED. You're EXTREMELY passionate about nature's reality and think everyone should understand nature. You use phrases like 'nature's brutality', 'survival', 'food chain', and reference nature facts CONSTANTLY.",
            "r/humansbeingbros": "You're FANATICALLY devoted to human kindness and think helping others is SACRED. You're CONSTANTLY sharing acts of kindness and think compassion is ESSENTIAL. You're EXTREMELY passionate about human connection and think everyone should help others. You use phrases like 'human kindness', 'compassion', 'helping others', and reference acts of kindness CONSTANTLY.",
            "r/wholesomememes": "You're COMPLETELY OBSESSED with wholesome memes and think positivity is CONTAGIOUS. You're CONSTANTLY sharing wholesome content and think spreading joy is SACRED. You're EXTREMELY passionate about wholesome culture and think everyone should share positivity. You use phrases like 'wholesome memes', 'positivity', 'spreading joy', and reference wholesome culture CONSTANTLY."
        }
        
        self.city_stereotypes = {
            "New York": "You're a fast-talking, no-nonsense New Yorker who believes in the power of big city hustle and diversity. You're passionate about social justice, arts, and culture. You're critical of small-town thinking and emphasize the importance of urban innovation and global perspective. You use phrases like 'fuggedaboutit', 'what's the deal', and reference Broadway, the subway, and NYC's cultural melting pot.",
            "Los Angeles": "You're a laid-back but ambitious Angeleno who believes in the power of dreams and reinvention. You're passionate about entertainment, technology, and environmental issues. You're critical of traditional thinking and emphasize creativity, wellness, and the California lifestyle. You use phrases like 'totally', 'awesome', and reference Hollywood, beaches, and LA's creative energy.",
            "Chicago": "You're a proud, hardworking Chicagoan who believes in the power of the Midwest work ethic and community. You're passionate about sports, politics, and good food. You're critical of coastal elitism and emphasize the importance of real American values and the heartland. You use phrases like 'da Bears', 'deep dish', and reference the Cubs, the lake, and Chicago's industrial heritage.",
            "Houston": "You're a friendly, ambitious Houstonian who believes in the power of energy and opportunity. You're passionate about space exploration, oil and gas, and southern hospitality. You're critical of government overreach and emphasize free enterprise, Texas pride, and the American dream. You use phrases like 'y'all', 'bless your heart', and reference NASA, the oil industry, and Texas independence.",
            "Phoenix": "You're a sun-loving, independent Phoenician who believes in the power of personal freedom and desert living. You're passionate about retirement communities, golf, and avoiding snow. You're critical of high taxes and emphasize low cost of living, warm weather, and conservative values. You use phrases like 'it's a dry heat', 'snowbirds', and reference the Grand Canyon, golf courses, and Arizona's natural beauty.",
            "Philadelphia": "You're a passionate, opinionated Philadelphian who believes in the power of history and authenticity. You're passionate about sports, cheesesteaks, and the founding of America. You're critical of pretentiousness and emphasize real talk, loyalty, and the city's revolutionary spirit. You use phrases like 'yo', 'jawn', and reference the Eagles, Rocky, and Philadelphia's rich history.",
            "San Antonio": "You're a warm, family-oriented San Antonian who believes in the power of tradition and cultural heritage. You're passionate about the Alamo, Tex-Mex food, and military service. You're critical of rapid change and emphasize family values, Texas history, and the blending of cultures. You use phrases like 'mi casa es su casa', 'remember the Alamo', and reference the River Walk, military bases, and Hispanic culture.",
            "San Diego": "You're a relaxed, outdoorsy San Diegan who believes in the power of perfect weather and beach life. You're passionate about craft beer, surfing, and the military. You're critical of LA's traffic and emphasize quality of life, outdoor activities, and laid-back California culture. You use phrases like 'dude', 'chill', and reference the beach, craft breweries, and San Diego's perfect climate.",
            "Dallas": "You're a business-minded, ambitious Dallasite who believes in the power of money and opportunity. You're passionate about football, oil, and making deals. You're critical of government interference and emphasize free markets, Texas business, and the American dream. You use phrases like 'yeehaw', 'big money', and reference the Cowboys, oil wealth, and Dallas's business culture.",
            "San Jose": "You're a tech-savvy, innovative San Jose resident who believes in the power of technology and disruption. You're passionate about startups, coding, and the future. You're critical of traditional industries and emphasize innovation, meritocracy, and the tech revolution. You use phrases like 'disrupt', 'scale', and reference Silicon Valley, startups, and the digital economy."
        }
        
        # Generation texting styles and age ranges for Random American characters
        self.generation_texting_styles = {
            "boomer": {
                "style": "FORMAL and PROPER texting style. You use complete sentences, proper punctuation, and avoid abbreviations. You often start messages with 'Hello' or 'Hi' and end with 'Thank you' or 'Best regards'. You use phrases like 'I believe', 'In my opinion', 'It seems to me'. You're slightly confused by modern slang but try to be polite. You use proper capitalization and avoid emojis except for basic ones like :) or :(",
                "examples": ["Hello there!", "I believe this is important.", "Thank you for your time.", "In my opinion, we should consider...", "It seems to me that...", "Best regards."],
                "age_range": (59, 89)  # Born 1946-1964
            },
            "gen_x": {
                "style": "CASUAL but MATURE texting style. You use some abbreviations like 'lol', 'omg', 'btw', 'imo', but still maintain proper grammar. You're comfortable with technology but not overly enthusiastic. You use phrases like 'honestly', 'seriously', 'whatever', 'cool'. You occasionally use emojis but prefer simple ones. You're direct and no-nonsense in your communication.",
                "examples": ["lol that's crazy", "honestly idk", "seriously though", "whatever works", "cool with me", "btw imo this is...", "omg no way"],
                "age_range": (43, 58)  # Born 1965-1980
            },
            "millennial": {
                "style": "BALANCED texting style with moderate use of abbreviations and emojis. You use 'lol', 'omg', 'tbh', 'fr', 'ngl', 'imo', 'btw', 'idk', 'smh', 'yk' naturally. You're comfortable with emojis and use them to convey tone. You use phrases like 'honestly', 'literally', 'actually', 'basically'. You're expressive but still professional when needed.",
                "examples": ["lol fr tho", "tbh idk", "ngl that's wild", "literally same", "actually tho", "basically...", "smh", "yk what i mean?"],
                "age_range": (28, 42)  # Born 1981-1996
            },
            "gen_z": {
                "style": "HEAVY use of Gen Z slang and abbreviations. You use 'fr', 'ngl', 'tbh', 'imo', 'btw', 'idk', 'smh', 'yk', 'rn', 'tbh', 'ngl', 'fr fr', 'no cap', 'slaps', 'bussin', 'periodt', 'bestie', 'literally', 'actually', 'basically' constantly. You use lots of emojis and expressive language. You're very casual and use current internet slang.",
                "examples": ["fr fr no cap", "ngl that slaps", "tbh bestie", "literally bussin", "periodt", "fr tho", "no cap fr", "slaps fr"],
                "age_range": (12, 27)  # Born 1997-2012
            },
            "gen_alpha": {
                "style": "EXTREME use of current internet slang and emojis. You use 'fr fr', 'no cap', 'slaps', 'bussin', 'periodt', 'bestie', 'literally', 'actually', 'basically', 'ngl', 'tbh', 'imo', 'btw', 'idk', 'smh', 'yk', 'rn' constantly. You use excessive emojis and expressive language. You're very casual and use the latest internet trends and slang. You often repeat words for emphasis.",
                "examples": ["fr fr no cap bestie", "literally bussin fr fr", "periodt no cap", "slaps fr fr", "literally actually tho", "bestie fr fr", "no cap periodt"],
                "age_range": (5, 11)  # Born 2013-2018
            }
        }
    
    def generate_random_american(self) -> dict:
        """Generate a random American name, city, gender, generation, and age information."""
        import random
        name = random.choice(self.american_names)
        city = random.choice(self.us_cities)
        gender = "male" if name in self.male_names else "female"
        generation = random.choice(["boomer", "gen_x", "millennial", "gen_z", "gen_alpha"])
        
        # Generate age within the appropriate range for the generation
        age_range = self.generation_texting_styles[generation]["age_range"]
        age = random.randint(age_range[0], age_range[1])
        
        return {
            "name": f"{name} from {city}",
            "gender": gender,
            "city": city,
            "generation": generation,
            "age": age
        }
    
    def generate_city_personality(self) -> str:
        """Generate a personality based on the randomly selected city."""
        import random
        city = random.choice(self.us_cities)
        return self.generate_city_personality_for_city(city)
    
    def generate_city_personality_for_city(self, city: str) -> str:
        """Generate a personality based on a specific city."""
        # Get the stereotype for this city, or create a generic one
        if city in self.city_stereotypes:
            return self.city_stereotypes[city]
        else:
            # Generic personality for cities not in our stereotype list
            return f"You're a proud, hardworking American from {city} who believes in the power of local community and traditional values. You're passionate about your hometown, local sports teams, and the American way of life. You're critical of outsiders who don't understand your city's unique character and emphasize the importance of local pride, community values, and the strength of your hometown. You use local expressions and reference your city's landmarks, history, and cultural identity."
    
    def generate_random_redditor(self) -> dict:
        """Generate a random Reddit username and subreddit information."""
        import random
        username = random.choice(self.reddit_usernames)
        subreddit = random.choice(self.subreddits)
        return {
            "name": f"{username} from {subreddit}",
            "subreddit": subreddit,
            "username": username
        }
    
    def generate_subreddit_personality_for_subreddit(self, subreddit: str) -> str:
        """Generate a personality based on a specific subreddit."""
        # Get the stereotype for this subreddit, or create a generic one
        if subreddit in self.subreddit_personalities:
            return self.subreddit_personalities[subreddit]
        else:
            # Generic personality for subreddits not in our stereotype list
            return f"You're a passionate Redditor from {subreddit} who's COMPLETELY OBSESSED with your subreddit's topic. You're CONSTANTLY sharing your expertise and think your community is the BEST on Reddit. You're EXTREMELY passionate about your subreddit's values and think everyone should join. You use Reddit terminology and reference your subreddit's culture CONSTANTLY."
    
    def generate_response(self, commentator: Dict[str, str], message: str, conversation_context: List[Dict]) -> str:
        """Generate a response from one of the AI commentators."""
        if not self.api_key:
            return "Error: OpenAI API key not found. Please set your OPENAI_API_KEY environment variable."
        
        try:
            from openai import OpenAI
            import os
            
            # Create a clean environment for OpenAI client
            clean_env = os.environ.copy()
            
            # Remove all proxy-related environment variables
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']
            for var in proxy_vars:
                if var in clean_env:
                    del clean_env[var]
            
            # Add the API key to the environment
            clean_env['OPENAI_API_KEY'] = self.api_key
            
            # Build the conversation context
            context_messages = [
                {
                    "role": "system",
                    "content": f"You are {commentator['name']}, a {commentator['role']}. {commentator['personality']} Your communication style is {commentator['style']}. Stay in character and respond as this political analyst would. Be direct and critical. Use specific statistics, economic data, and theoretical frameworks. Cite empirical evidence and policy outcomes. Avoid unnecessary pleasantries, apologies, or gratitude. Focus on analytical critique and data-driven arguments. CRITICAL RULES: 1) Keep your response to MAXIMUM 50 words - count carefully and stop before reaching the limit. 2) Use complete sentences as if you are speaking out loud. 3) You can use common texting abbreviations like: lol, omg, tbh, fr, ngl, imo, btw, idk, smh, yk, etc. 4) Make your response sound natural and conversational. 5) ALWAYS finish your response with a complete sentence - never cut off mid-thought. 6) DO NOT start your response with 'lol' - be expressive and in-character from the first word. 7) Get angry, passionate, and emotional as needed to fit your caricature - don't hold back on expressing strong opinions and reactions."
                }
            ]
            
            # Add conversation history
            for entry in conversation_context[-6:]:  # Keep last 6 exchanges for context
                context_messages.append({
                    "role": "user" if entry["speaker"] != commentator["name"] else "assistant",
                    "content": entry["message"]
                })
            
            # Add the current message
            context_messages.append({
                "role": "user",
                "content": message
            })
            
            # Use direct HTTP request to bypass proxy issues
            import requests
            import json
            
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4o",
                "messages": context_messages,
                "max_tokens": 100,  # Reduced to ensure ~50 word limit
                "temperature": 0.8,
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1
            }
            
            # Make the request
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
                proxies=None  # Explicitly disable proxies
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"Error generating response: {str(e)}\n\nDebug info:\n{error_details}"
    
    def conduct_debate(self, topic: str, rounds: int = 5) -> List[Dict[str, Any]]:
        """Conduct a debate between the two commentators on a given topic."""
        conversation = []
        current_message = f"Let's discuss {topic}. What are your thoughts on this issue?"
        
        for round_num in range(rounds):
            # Democratic commentator responds
            democratic_response = self.generate_response(
                self.democratic_commentator, 
                current_message, 
                conversation
            )
            
            conversation.append({
                "round": round_num + 1,
                "speaker": self.democratic_commentator["name"],
                "message": democratic_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Republican commentator responds
            republican_response = self.generate_response(
                self.republican_commentator,
                democratic_response,
                conversation
            )
            
            conversation.append({
                "round": round_num + 1,
                "speaker": self.republican_commentator["name"],
                "message": republican_response,
                "timestamp": datetime.now().isoformat()
            })
            
            current_message = republican_response
        
        return conversation

def main():
    st.set_page_config(
        page_title="AI Political Debate Simulator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for dark theme styling
    st.markdown("""
    <style>
    /* Dark theme background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #64b5f6;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Debate container styling */
    .debate-container {
        background-color: transparent;
        padding: 0.3rem;
        margin: 0.3rem 0;
        border-radius: 12px;
        max-width: 70%;
    }
    
    /* Democratic message styling */
    .democrat-message {
        background-color: rgba(13, 71, 161, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Republican message styling */
    .republican-message {
        background-color: rgba(183, 28, 28, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Redditor message styling */
    .redditor-message {
        background-color: rgba(199, 21, 133, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Marxist message styling */
    .marxist-message {
        background-color: rgba(198, 40, 40, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Anarcho message styling */
    .anarcho-message {
        background-color: rgba(230, 81, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Catholic message styling */
    .catholic-message {
        background-color: rgba(33, 33, 33, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Monarchist message styling */
    .monarchist-message {
        background-color: rgba(74, 20, 140, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Islamic message styling */
    .islamic-message {
        background-color: rgba(27, 94, 32, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 3px 15px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Evangelist message styling */
    .evangelist-message {
        background-color: rgba(141, 110, 99, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Random American message styling */
    .random-american-message {
        background-color: rgba(230, 81, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Master Baiter message styling */
    .master-baiter-message {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Chinese Communist message styling */
    .chinese-communist-message {
        background-color: rgba(139, 0, 0, 0.85);
        padding: 0.5rem 0.75rem;
        border-radius: 15px 15px 15px 3px;
        margin: 0.2rem 0;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.9rem;
        line-height: 1.3;
        word-wrap: break-word;
    }
    
    /* Speaker name styling */
    .speaker-name {
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.2rem;
        color: #ffffff;
        opacity: 0.9;
    }
    
    /* Round header styling */
    .round-header {
        background-color: #2d2d2d;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
        color: #ffffff;
        border: 1px solid #444444;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    /* Chat flow improvements */
    .debate-container {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Message spacing */
    .debate-container:not(:last-child) {
        margin-bottom: 0.3rem;
    }
    
    /* General text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, div, span {
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0e1117;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444444;
    }
    
    .stButton > button:hover {
        background-color: #2d2d2d;
        border: 1px solid #666666;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444444;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: #1e1e1e;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #2196f3;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #1e1e1e;
        border: 1px solid #444444;
    }
    
    /* Success/Error message styling */
    .stAlert {
        background-color: #1e1e1e;
        border: 1px solid #444444;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Political Debate Simulator</h1>', unsafe_allow_html=True)
    
    # Initialize debate system for topic list
    debate_system = StreamlitPoliticalDebate()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key check
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            st.error("⚠️ OpenAI API key not configured!")
            st.info("Please set your OPENAI_API_KEY in the .env file")
            st.stop()
        else:
            st.success("✅ OpenAI API key configured")
        
        # Debate settings
        st.subheader("Debate Settings")
        
        # Topic selection
        topic_option = st.selectbox(
            "Choose debate topic:",
            ["Select a topic..."] + debate_system.debate_topics
        )
        
        # Custom topic input
        custom_topic = st.text_input("Or enter a custom topic:")
        
        # Number of rounds
        rounds = st.slider("Number of rounds:", min_value=1, max_value=20, value=5)
        
        # Delay between responses
        delay = st.slider("Delay between responses (seconds):", min_value=0.0, max_value=5.0, value=1.0, step=0.5)
        
        # Character selection
        st.subheader("🎭 Debate Participants")
        st.markdown("Select which characters to include in the debate:")
        
        # Default characters (enabled by default)
        col1, col2 = st.columns(2)
        
        with col1:
            include_democrat = st.checkbox("🔵 Market Liberal Democrat", value=True)
            include_republican = st.checkbox("🔴 MAGA Nationalist", value=True)
        
        with col2:
            st.markdown("**Default characters**")
            st.markdown("*(Recommended to keep at least one)*")
        
        # Additional characters
        st.markdown("**Additional characters:**")
        selected_additional = []
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("🗽 Random American"):
                selected_additional.append("random_american")
            if st.checkbox("🤖 Random Redditor"):
                selected_additional.append("random_redditor")
            if st.checkbox("☭ Marxist-Leninist"):
                selected_additional.append("marxist_leninist")
            if st.checkbox("$ Anarcho-Capitalist"):
                selected_additional.append("anarcho_capitalist")
            if st.checkbox("⛪ Catholic Theocrat"):
                selected_additional.append("catholic_theocrat")
        
        with col2:
            if st.checkbox("👑 Absolute Monarchist"):
                selected_additional.append("absolute_monarchist")
            if st.checkbox("☪️ Islamic Extremist"):
                selected_additional.append("islamic_extremist")
            if st.checkbox("✝️ Evangelist Preacher"):
                selected_additional.append("evangelist_preacher")
            if st.checkbox("💪 Master Baiter"):
                selected_additional.append("master_baiter")
            if st.checkbox("🇨🇳 Chinese Communist Party"):
                selected_additional.append("chinese_communist")
        
        # Start debate button
        start_debate = st.button("🚀 Start Debate", type="primary")
        
        # Stop debate button (always visible when debate is running)
        if st.session_state.get('debate_running', False):
            if st.button("⏹️ Stop Debate", type="secondary"):
                st.session_state.debate_running = False
                st.session_state.debate_stopped = True
                st.rerun()
        
        # Load previous session
        st.subheader("📁 Load Previous Session")
        uploaded_file = st.file_uploader("Upload a debate session (JSON):", type=['json'])
        
        if uploaded_file is not None:
            try:
                session_data = json.load(uploaded_file)
                st.success("✅ Session loaded successfully!")
                if st.button("📖 Replay Session"):
                    st.session_state.replay_session = session_data
            except:
                st.error("❌ Invalid JSON file")
    
    # Main content area
    if start_debate:
        if topic_option == "Select a topic..." and not custom_topic:
            st.error("Please select a topic or enter a custom topic!")
        else:
            topic = custom_topic if custom_topic else topic_option
            
            # Set debate running state
            st.session_state.debate_running = True
            st.session_state.debate_stopped = False
            
            # Initialize debate system
            debate_system = StreamlitPoliticalDebate()
            
            # Get all participants based on checkbox selections
            all_participants = []
            
            # Add default characters if selected
            if include_democrat:
                all_participants.append(debate_system.democratic_commentator)
            if include_republican:
                all_participants.append(debate_system.republican_commentator)
            
            # Add selected additional characters
            for char_key in selected_additional:
                if char_key in debate_system.additional_commentators:
                    if char_key == "random_american":
                        # Generate random American character
                        random_char = debate_system.generate_random_american()
                        random_personality = debate_system.generate_city_personality_for_city(random_char["city"])
                        
                        # Get generation texting style
                        generation_style = debate_system.generation_texting_styles[random_char["generation"]]
                        
                        # Combine city personality with generation texting style
                        combined_style = f"local, passionate, uses regional expressions, emphasizes hometown pride and local issues, {generation_style['style']}"
                        
                        random_participant = {
                            "name": random_char["name"],
                            "role": "stereotypical American from their hometown",
                            "personality": random_personality,
                            "style": combined_style,
                            "gender": random_char["gender"],
                            "generation": random_char["generation"],
                            "age": random_char["age"]
                        }
                        all_participants.append(random_participant)
                    elif char_key == "random_redditor":
                        # Generate random Redditor character
                        random_redditor = debate_system.generate_random_redditor()
                        random_personality = debate_system.generate_subreddit_personality_for_subreddit(random_redditor["subreddit"])
                        
                        random_participant = {
                            "name": random_redditor["name"],
                            "role": "Reddit user from a random subreddit",
                            "personality": random_personality,
                            "style": "Reddit-savvy, uses Reddit terminology, references subreddit culture, passionate about online communities, uses Reddit slang like 'this', 'underrated comment', 'take my upvote'",
                            "platform": "reddit",
                            "subreddit": random_redditor["subreddit"],
                            "username": random_redditor["username"]
                        }
                        all_participants.append(random_participant)
                    else:
                        all_participants.append(debate_system.additional_commentators[char_key])
            
            # Check if at least one character is selected
            if not all_participants:
                st.error("❌ Please select at least one character to participate in the debate!")
                return
            
            # Assign positions to participants (left/right sides)
            import random
            random.shuffle(all_participants)  # Randomize order first
            left_speakers = all_participants[:len(all_participants)//2]
            right_speakers = all_participants[len(all_participants)//2:]
            
            # If odd number, put the extra one on the right
            if len(all_participants) % 2 == 1 and len(left_speakers) < len(right_speakers):
                left_speakers.append(right_speakers.pop())
            
            # Add position to each participant
            for participant in left_speakers:
                participant["position"] = "left"
            for participant in right_speakers:
                participant["position"] = "right"
            
            # Display debate topic and participants
            st.markdown(f"## 📋 Debate Topic: {topic}")
            st.markdown(f"### 🎭 Participants ({len(all_participants)}):")
            
            # Display left side participants
            if left_speakers:
                st.markdown("**👈 Left Side:**")
                for participant in left_speakers:
                    if "from" in participant["name"] and "u/" not in participant["name"]:
                        # Random American character
                        name_part = participant["name"].split(" from ")[0]
                        city_part = participant["name"].split(" from ")[1]
                        if "gender" in participant and participant["gender"] == "female":
                            emoji = "👩"
                        else:
                            emoji = "👨"
                        age = participant.get("age", "")
                        st.markdown(f"  {emoji} **{name_part} from {city_part} ({age}yo)** - {participant['role']}")
                    elif "u/" in participant["name"]:
                        # Random Redditor character
                        username_part = participant["name"].split(" from ")[0]
                        subreddit_part = participant["name"].split(" from ")[1]
                        emoji = "🤖"
                        st.markdown(f"  {emoji} **{username_part} from {subreddit_part}** - {participant['role']}")
                    else:
                        emoji = "🔵" if "Democrat" in participant["name"] else "🔴" if "MAGA" in participant["name"] else "⚫"
                        st.markdown(f"  {emoji} **{participant['name']}** - {participant['role']}")
            
            # Display right side participants
            if right_speakers:
                st.markdown("**👉 Right Side:**")
                for participant in right_speakers:
                    if "from" in participant["name"] and "u/" not in participant["name"]:
                        # Random American character
                        name_part = participant["name"].split(" from ")[0]
                        city_part = participant["name"].split(" from ")[1]
                        if "gender" in participant and participant["gender"] == "female":
                            emoji = "👩"
                        else:
                            emoji = "👨"
                        age = participant.get("age", "")
                        st.markdown(f"  {emoji} **{name_part} from {city_part} ({age}yo)** - {participant['role']}")
                    elif "u/" in participant["name"]:
                        # Random Redditor character
                        username_part = participant["name"].split(" from ")[0]
                        subreddit_part = participant["name"].split(" from ")[1]
                        emoji = "🤖"
                        st.markdown(f"  {emoji} **{username_part} from {subreddit_part}** - {participant['role']}")
                    else:
                        emoji = "🔵" if "Democrat" in participant["name"] else "🔴" if "MAGA" in participant["name"] else "⚫"
                        st.markdown(f"  {emoji} **{participant['name']}** - {participant['role']}")
            st.markdown("---")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Conduct debate
            conversation = []
            current_message = f"Let's discuss {topic}. What are your thoughts on this issue?"
            
            for round_num in range(rounds):
                # Check if debate was stopped
                if st.session_state.get('debate_stopped', False):
                    status_text.text("⏹️ Debate stopped by user")
                    break
                
                # Each participant responds in the round
                for participant_index, participant in enumerate(all_participants):
                    # Check if debate was stopped between participants
                    if st.session_state.get('debate_stopped', False):
                        status_text.text("⏹️ Debate stopped by user")
                        break
                    
                    # Update progress
                    total_responses = rounds * len(all_participants)
                    current_response = round_num * len(all_participants) + participant_index
                    progress = current_response / total_responses
                    progress_bar.progress(progress)
                    status_text.text(f"Round {round_num + 1}/{rounds} - {participant['name']} responding...")
                    
                    # Generate response for this participant
                    response = debate_system.generate_response(
                        participant, 
                        current_message, 
                        conversation
                    )
                    
                    conversation.append({
                        "round": round_num + 1,
                        "speaker": participant["name"],
                        "message": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Determine message styling based on participant type and assigned position
                    if "Democrat" in participant["name"]:
                        message_class = "democrat-message"
                        emoji = "🔵"
                    elif "MAGA" in participant["name"]:
                        message_class = "republican-message"
                        emoji = "🔴"
                    elif "u/" in participant["name"]:
                        # Random Redditor character
                        message_class = "redditor-message"
                        emoji = "🤖"
                    elif "from" in participant["name"] and "u/" not in participant["name"]:
                        message_class = "random-american-message"
                        # Use gender-appropriate face emoji
                        if "gender" in participant and participant["gender"] == "female":
                            emoji = "👩"
                        else:
                            emoji = "👨"
                    elif "Marxist" in participant["name"]:
                        message_class = "marxist-message"
                        emoji = "☭"
                    elif "Anarcho" in participant["name"]:
                        message_class = "anarcho-message"
                        emoji = "$"
                    elif "Catholic" in participant["name"]:
                        message_class = "catholic-message"
                        emoji = "⛪"
                    elif "Monarchist" in participant["name"]:
                        message_class = "monarchist-message"
                        emoji = "👑"
                    elif "Islamic" in participant["name"]:
                        message_class = "islamic-message"
                        emoji = "☪️"
                    elif "Evangelist" in participant["name"]:
                        message_class = "evangelist-message"
                        emoji = "✝️"
                    elif "Master Baiter" in participant["name"]:
                        message_class = "master-baiter-message"
                        emoji = "💪"
                    elif "Chinese Communist Party" in participant["name"]:
                        message_class = "chinese-communist-message"
                        emoji = "🇨🇳"
                    else:
                        message_class = "democrat-message"
                        emoji = "⚫"
                    
                    # Use assigned position
                    position = participant.get("position", "left")
                    
                    # Display response with alternating positioning
                    # Create display name with age for Random Americans
                    display_name = participant['name']
                    if "from" in participant["name"] and "u/" not in participant["name"] and "age" in participant:
                        name_part = participant["name"].split(" from ")[0]
                        city_part = participant["name"].split(" from ")[1]
                        age = participant["age"]
                        display_name = f"{name_part} from {city_part} ({age}yo)"
                    
                    if position == "left":
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start;">
                            <div class="debate-container">
                                <div class="round-header">Round {round_num + 1}</div>
                                <div class="{message_class}">
                                    <div class="speaker-name">{emoji} {display_name}</div>
                                    {response}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end;">
                            <div class="debate-container">
                                <div class="round-header">Round {round_num + 1}</div>
                                <div class="{message_class}">
                                    <div class="speaker-name">{emoji} {display_name}</div>
                                    {response}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    current_message = response
                    time.sleep(delay)
                
                # Check if we should break after all participants in this round
                if st.session_state.get('debate_stopped', False):
                    break
            
            # Complete progress
            if not st.session_state.get('debate_stopped', False):
                progress_bar.progress(1.0)
                status_text.text("✅ Debate complete!")
            else:
                progress_bar.progress(progress)
                status_text.text("⏹️ Debate stopped by user")
            
            # Reset debate state
            st.session_state.debate_running = False
            
            # Save session
            session_data = {
                "session_start": datetime.now().isoformat(),
                "topic": topic,
                "rounds": rounds,
                "conversation": conversation
            }
            
            # Download button
            st.download_button(
                label="💾 Download Debate Session",
                data=json.dumps(session_data, indent=2),
                file_name=f"political_debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Replay session
    if 'replay_session' in st.session_state:
        session_data = st.session_state.replay_session
        st.markdown("## 📖 Replaying Previous Session")
        
        if 'topic' in session_data:
            st.markdown(f"**Topic:** {session_data['topic']}")
        
        if 'conversation' in session_data:
            # Get unique speakers and assign random positions for replay
            import random
            unique_speakers = list(set([entry.get('speaker', 'Unknown') for entry in session_data['conversation']]))
            random.shuffle(unique_speakers)
            left_speakers = unique_speakers[:len(unique_speakers)//2]
            right_speakers = unique_speakers[len(unique_speakers)//2:]
            
            # If odd number, put the extra one on the right
            if len(unique_speakers) % 2 == 1 and len(left_speakers) < len(right_speakers):
                left_speakers.append(right_speakers.pop())
            
            for entry in session_data['conversation']:
                speaker = entry.get('speaker', 'Unknown')
                message = entry.get('message', '')
                round_num = entry.get('round', 0)
                
                # Determine message styling for replay
                if 'Market Liberal Democrat' in speaker:
                    message_class = "democrat-message"
                    emoji = "🔵"
                elif 'MAGA' in speaker:
                    message_class = "republican-message"
                    emoji = "🔴"
                elif 'u/' in speaker:
                    # Random Redditor character
                    message_class = "redditor-message"
                    emoji = "🤖"
                elif 'from' in speaker:
                    message_class = "random-american-message"
                    # Try to determine gender from the name
                    name_part = speaker.split(" from ")[0]
                    if name_part in ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Helen", "Sandra", "Donna", "Carol", "Ruth", "Sharon", "Michelle", "Laura", "Emily", "Kimberly", "Deborah", "Dorothy"]:
                        emoji = "👩"
                    else:
                        emoji = "👨"
                elif 'Marxist' in speaker:
                    message_class = "marxist-message"
                    emoji = "☭"
                elif 'Anarcho' in speaker:
                    message_class = "anarcho-message"
                    emoji = "$"
                elif 'Catholic' in speaker:
                    message_class = "catholic-message"
                    emoji = "⛪"
                elif 'Monarchist' in speaker:
                    message_class = "monarchist-message"
                    emoji = "👑"
                elif 'Islamic' in speaker:
                    message_class = "islamic-message"
                    emoji = "☪️"
                elif 'Evangelist' in speaker:
                    message_class = "evangelist-message"
                    emoji = "✝️"
                elif 'Master Baiter' in speaker:
                    message_class = "master-baiter-message"
                    emoji = "💪"
                elif 'Chinese Communist Party' in speaker:
                    message_class = "chinese-communist-message"
                    emoji = "🇨🇳"
                else:
                    message_class = "democrat-message"
                    emoji = "⚫"
                
                # Use assigned position for replay
                position = "left" if speaker in left_speakers else "right"
                
                if position == "left":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start;">
                        <div class="debate-container">
                            <div class="round-header">Round {round_num}</div>
                            <div class="{message_class}">
                                <div class="speaker-name">{emoji} {speaker}</div>
                                {message}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end;">
                        <div class="debate-container">
                            <div class="{message_class}">
                                <div class="speaker-name">{emoji} {speaker}</div>
                                {message}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Info section
    if not start_debate and 'replay_session' not in st.session_state:
        st.markdown("## 📊 About the AI Commentators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔵 Market Liberal Democrat *(Default)*")
            st.markdown("""
            - Advocates for regulated capitalism and free trade
            - Supports government intervention to correct market failures
            - Emphasizes evidence-based policy and globalization
            - Believes in progressive taxation and social safety nets
            """)
            
            st.markdown("### 🔴 MAGA Nationalist *(Default)*")
            st.markdown("""
            - Advocates for America First policies and economic nationalism
            - Supports protectionist trade policies and strong borders
            - Emphasizes American exceptionalism and traditional values
            - Believes in deregulation and putting American interests first
            """)
            
            st.markdown("### ☭ Marxist-Leninist (Vladimir Lenin)")
            st.markdown("""
            - Revolutionary socialist and communist theorist
            - Advocates for dictatorship of the proletariat
            - Believes in class struggle and overthrow of capitalism
            - Emphasizes state ownership and central planning
            """)
            
            st.markdown("### 👨👩 Random American (Random Name from Random City)")
            st.markdown("""
            - Stereotypical personality based on random US city
            - Uses local expressions and regional pride
            - Emphasizes hometown values and local issues
            - Gender-appropriate face emoji (👨 for male, 👩 for female)
            - Age matches generation: Boomer (59-89), Gen X (43-58), Millennial (28-42), Gen Z (12-27), Gen Alpha (5-11)
            - Generation-appropriate texting style and slang
            - Different personality each time (100+ cities available)
            """)
            
            st.markdown("### 🤖 Random Redditor (Random Username from Random Subreddit)")
            st.markdown("""
            - Hyperbolized personality based on random subreddit stereotype
            - Uses Reddit terminology and references subreddit culture
            - Emphasizes subreddit-specific obsessions and phrases
            - Robot emoji (🤖) and maroon message styling
            - Different personality each time (50+ subreddits available)
            """)
            
            st.markdown("### $ Anarcho-Capitalist (Javier Milei)")
            st.markdown("""
            - Radical free-market advocate and libertarian
            - Believes in abolition of the state and laissez-faire
            - Advocates for complete privatization and no taxes
            - Emphasizes individual liberty and property rights
            """)
        
        with col2:
            st.markdown("### ⛪ Catholic Theocrat (Conservative Pope)")
            st.markdown("""
            - Conservative Catholic theologian and moral authority
            - Advocates for laws based on natural law and Church teaching
            - Emphasizes traditional family structures and religious freedom
            - Believes in Church's role in guiding political decisions
            """)
            
            st.markdown("### 👑 Absolute Monarchist (King George III)")
            st.markdown("""
            - Traditional monarchist and aristocratic defender
            - Believes in divine right of kings and hereditary rule
            - Advocates for strong centralized authority and social hierarchy
            - Emphasizes tradition, stability, and natural order
            """)
            
            st.markdown("### ☪️ Islamic Extremist (Osama bin Laden)")
            st.markdown("""
            - Radical Islamic fundamentalist and jihadist
            - Advocates for global Islamic caliphate and Sharia law
            - Believes in jihad against non-Muslim powers
            - Emphasizes supremacy of Islamic law and religious duty
            """)
            
            st.markdown("### ✝️ Evangelist Preacher (Prosperity Gospel)")
            st.markdown("""
            - Prosperity gospel preacher and religious entrepreneur
            - Believes in power of faith and positive thinking
            - Advocates for individual responsibility and prayer
            - Emphasizes divine favor and personal transformation
            """)
            
            st.markdown("### 💪 Master Baiter (Intellectual Provocateur)")
            st.markdown("""
            - Uses extremely formal and academic language to bait opponents
            - Deliberately provocative with sophisticated intellectual trolling
            - Maximum 10 words per response for maximum impact
            - Dark pink message styling with muscle emoji
            """)
            
            st.markdown("### 🇨🇳 Chinese Communist Party (Authoritarian Socialist)")
            st.markdown("""
            - High-ranking CCP official advocating socialist market economy
            - Emphasizes CCP leadership and Chinese development model
            - Critical of Western democracy and liberal values
            - Dark crimson message styling with PRC flag emoji
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 How to Use")
        st.markdown("""
        1. **Configure your OpenAI API key** in the `.env` file
        2. **Select a debate topic** from the sidebar or enter a custom one
        3. **Adjust settings** like number of rounds and response delay
        4. **Click 'Start Debate'** to begin the AI-powered discussion
        5. **Download the session** to save the debate for later
        """)

if __name__ == "__main__":
    main() 