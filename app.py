import streamlit as st
import json
import random
from datetime import datetime, timedelta
import base64
from io import BytesIO
import requests
import time
import hashlib

# ==========================================
# CONFIGURATION & INITIALIZATION
# ==========================================

# Page config
st.set_page_config(
    page_title="LinguaFlow - AI German Tutor",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_level = None
    st.session_state.xp = 0
    st.session_state.streak = 0
    st.session_state.current_day = 1
    st.session_state.daily_tasks_completed = []
    st.session_state.chat_history = []
    st.session_state.api_keys = {
        'openrouter': '',
        'huggingface': '',
        'mymemory_email': ''
    }
    st.session_state.placement_completed = False
    st.session_state.todays_lesson = None
    st.session_state.achievements = []
    st.session_state.user_name = ""
    st.session_state.lesson_cache = {}

# ==========================================
# STYLING
# ==========================================

st.markdown("""
<style>
    /* Main styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Card styling */
    .lesson-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Achievement badges */
    .achievement-badge {
        display: inline-block;
        padding: 5px 15px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
    }
    
    /* XP Bar */
    .xp-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .xp-fill {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Chat bubbles */
    .user-message {
        background: #E3F2FD;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 70%;
        margin-left: auto;
    }
    
    .ai-message {
        background: #F5F5F5;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 70%;
    }
    
    /* Level indicator */
    .level-indicator {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        padding: 10px;
        background: white;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Lesson content box */
    .content-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
    
    /* Translation result */
    .translation-result {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONTENT GENERATION SYSTEM
# ==========================================

class ContentGenerator:
    """Generate dynamic German learning content based on level"""
    
    @staticmethod
    def generate_vocabulary(level, topic=None):
        """Generate vocabulary based on level"""
        vocab_pools = {
            'A1': {
                'greetings': ['Hallo', 'Guten Tag', 'Tschüss', 'Auf Wiedersehen', 'Danke'],
                'numbers': ['eins', 'zwei', 'drei', 'vier', 'fünf'],
                'colors': ['rot', 'blau', 'grün', 'gelb', 'schwarz'],
                'family': ['Mutter', 'Vater', 'Bruder', 'Schwester', 'Kind'],
                'food': ['Brot', 'Wasser', 'Milch', 'Apfel', 'Käse']
            },
            'A2': {
                'daily': ['aufstehen', 'frühstücken', 'arbeiten', 'einkaufen', 'schlafen'],
                'transport': ['Bus', 'Zug', 'Auto', 'Fahrrad', 'U-Bahn'],
                'shopping': ['Supermarkt', 'Bäckerei', 'Apotheke', 'Kleidung', 'Preis'],
                'weather': ['sonnig', 'regnerisch', 'kalt', 'warm', 'windig'],
                'hobbies': ['lesen', 'schwimmen', 'kochen', 'tanzen', 'wandern']
            },
            'B1': {
                'emotions': ['glücklich', 'traurig', 'aufgeregt', 'nervös', 'entspannt'],
                'work': ['Büro', 'Kollege', 'Besprechung', 'Projekt', 'Deadline'],
                'health': ['Gesundheit', 'Krankheit', 'Arzt', 'Medikament', 'Termin'],
                'travel': ['Reise', 'Flughafen', 'Hotel', 'Sehenswürdigkeit', 'Gepäck'],
                'education': ['Universität', 'Prüfung', 'Semester', 'Vorlesung', 'Abschluss']
            },
            'B2': {
                'abstract': ['Meinung', 'Argument', 'Perspektive', 'Konzept', 'Theorie'],
                'environment': ['Umweltschutz', 'Klimawandel', 'Nachhaltigkeit', 'Energie', 'Recycling'],
                'technology': ['Digitalisierung', 'Innovation', 'Künstliche Intelligenz', 'Datenschutz', 'Software'],
                'society': ['Gesellschaft', 'Integration', 'Demokratie', 'Gleichberechtigung', 'Vielfalt'],
                'economy': ['Wirtschaft', 'Globalisierung', 'Arbeitsmarkt', 'Inflation', 'Investition']
            }
        }
        
        level_vocab = vocab_pools.get(level, vocab_pools['A1'])
        topics = list(level_vocab.keys())
        selected_topic = topic or random.choice(topics)
        words = level_vocab[selected_topic]
        
        return selected_topic, random.sample(words, min(3, len(words)))
    
    @staticmethod
    def generate_sentence_patterns(level):
        """Generate sentence patterns based on level"""
        patterns = {
            'A1': [
                "Ich bin [Name].",
                "Das ist [ein/eine] [Noun].",
                "Ich habe [ein/eine] [Noun].",
                "Ich komme aus [Place].",
                "Ich mag [Noun/Verb]."
            ],
            'A2': [
                "Ich gehe [Time] [Place].",
                "Kannst du mir bitte [Verb]?",
                "Gestern habe ich [Past Participle].",
                "Ich möchte gerne [Infinitive].",
                "Wenn es regnet, [Verb] ich [Object]."
            ],
            'B1': [
                "Ich denke, dass [Subordinate Clause].",
                "Obwohl [Condition], [Main Clause].",
                "Es ist wichtig, [zu + Infinitive].",
                "Nachdem ich [Past Perfect], [Past].",
                "Je mehr [Comparative], desto [Result]."
            ],
            'B2': [
                "Meiner Meinung nach [Complex Statement].",
                "Es lässt sich nicht leugnen, dass [Argument].",
                "Einerseits [Point], andererseits [Counterpoint].",
                "Vorausgesetzt, dass [Condition], [Consequence].",
                "Im Hinblick auf [Topic], [Analysis]."
            ]
        }
        
        return patterns.get(level, patterns['A1'])
    
    @staticmethod
    def generate_grammar_topic(level):
        """Generate grammar topics based on level"""
        grammar_topics = {
            'A1': [
                ('Articles', 'der, die, das - Definite articles', 
                 'Der Mann (the man), Die Frau (the woman), Das Kind (the child)'),
                ('Present Tense', 'Regular verb conjugation',
                 'ich mache, du machst, er/sie/es macht, wir machen, ihr macht, sie machen'),
                ('Basic Word Order', 'Subject-Verb-Object',
                 'Ich esse einen Apfel. (I eat an apple.)')
            ],
            'A2': [
                ('Perfect Tense', 'haben/sein + past participle',
                 'Ich habe gegessen. (I have eaten.) Ich bin gegangen. (I have gone.)'),
                ('Modal Verbs', 'können, müssen, wollen, sollen, dürfen',
                 'Ich kann schwimmen. (I can swim.) Du musst lernen. (You must learn.)'),
                ('Dative Case', 'Indirect object case',
                 'Ich gebe dem Mann das Buch. (I give the book to the man.)')
            ],
            'B1': [
                ('Subjunctive II', 'Konjunktiv II for hypothetical situations',
                 'Wenn ich reich wäre, würde ich reisen. (If I were rich, I would travel.)'),
                ('Relative Clauses', 'der/die/das as relative pronouns',
                 'Das ist der Mann, der mir geholfen hat. (That\'s the man who helped me.)'),
                ('Passive Voice', 'werden + past participle',
                 'Das Haus wird gebaut. (The house is being built.)')
            ],
            'B2': [
                ('Subjunctive I', 'Indirect speech',
                 'Er sagte, er habe keine Zeit. (He said he had no time.)'),
                ('Nominalization', 'Converting verbs/adjectives to nouns',
                 'Das Lesen von Büchern (The reading of books)'),
                ('Advanced Conjunctions', 'Complex sentence connectors',
                 'Insofern als... (Insofar as...), Zumal... (Especially since...)')
            ]
        }
        
        topics = grammar_topics.get(level, grammar_topics['A1'])
        return random.choice(topics)

# ==========================================
# DYNAMIC LESSON GENERATOR
# ==========================================

def generate_dynamic_lesson(level, skill):
    """Generate personalized lesson content based on level and skill"""
    
    generator = ContentGenerator()
    
    # Generate unique content based on skill type
    if skill == 'speaking':
        topic, vocab = generator.generate_vocabulary(level)
        patterns = generator.generate_sentence_patterns(level)
        
        lesson = {
            'title': f'Speaking Practice: {topic.title()}',
            'vocabulary': vocab,
            'content': f"""
            ### Today's Focus: {topic.title()} Vocabulary
            
            **New Words to Practice:**
            {' | '.join([f'• **{word}**' for word in vocab])}
            
            **Practice Patterns:**
            1. {patterns[0]}
            2. {patterns[1] if len(patterns) > 1 else 'Practice the pattern above'}
            
            **Speaking Exercise:**
            Use the vocabulary above to create 3 sentences. Record yourself saying them!
            """,
            'exercise': f"Create sentences using: {', '.join(vocab[:2])}",
            'tip': "Focus on pronunciation. Say each word slowly first, then speed up."
        }
        
    elif skill == 'writing':
        topic, vocab = generator.generate_vocabulary(level)
        patterns = generator.generate_sentence_patterns(level)
        
        lesson = {
            'title': f'Writing Practice: {topic.title()}',
            'vocabulary': vocab,
            'content': f"""
            ### Writing Theme: {topic.title()}
            
            **Key Vocabulary:**
            {' | '.join([f'• **{word}**' for word in vocab])}
            
            **Sentence Structures to Use:**
            {' | '.join([f'{i+1}. {p}' for i, p in enumerate(patterns[:3])])}
            """,
            'exercise': f"Write a short paragraph (3-5 sentences) about {topic} using at least 2 of these words: {', '.join(vocab)}",
            'tip': "Remember word order and use correct articles (der/die/das)."
        }
        
    elif skill == 'listening':
        topic, vocab = generator.generate_vocabulary(level)
        
        # Generate listening content
        sample_dialogue = {
            'A1': f"Anna: Guten Tag! Wie heißt du?\nBen: Ich heiße Ben. Und du?\nAnna: Ich bin Anna. Woher kommst du?\nBen: Ich komme aus Berlin.",
            'A2': f"Lisa: Was machst du am Wochenende?\nTom: Ich gehe ins Kino. Möchtest du mitkommen?\nLisa: Ja, gerne! Um wie viel Uhr?\nTom: Um 19 Uhr.",
            'B1': f"Marie: Ich überlege, ob ich den Job wechseln sollte.\nPaul: Was sind denn die Vor- und Nachteile?\nMarie: Naja, das Gehalt wäre besser, aber ich müsste umziehen.\nPaul: Das ist wirklich eine schwierige Entscheidung.",
            'B2': f"Prof: Die Digitalisierung verändert unsere Gesellschaft fundamental.\nStudent: Inwiefern beeinflusst das den Arbeitsmarkt?\nProf: Einerseits entstehen neue Berufe, andererseits werden traditionelle Tätigkeiten automatisiert.\nStudent: Das wirft natürlich Fragen zur Weiterbildung auf."
        }
        
        lesson = {
            'title': f'Listening Comprehension: {topic.title()}',
            'vocabulary': vocab,
            'content': f"""
            ### Listening Focus: {topic.title()} Dialogue
            
            **Pre-listening Vocabulary:**
            {' | '.join([f'• **{word}**' for word in vocab])}
            
            **Dialogue to Practice:**
            {sample_dialogue.get(level, sample_dialogue['A1'])}
            
            **Listen for:**
            - Key words from the vocabulary
            - Question words (Was, Wie, Wo, Wann)
            - Time expressions if mentioned
            """,
            'exercise': "Read the dialogue aloud 3 times, then answer: What is the main topic of the conversation?",
            'tip': "First, read through once for general understanding. Then focus on specific details."
        }
        
    elif skill == 'reading':
        topic, vocab = generator.generate_vocabulary(level)
        
        # Generate reading texts based on level
        reading_texts = {
            'A1': f"""
            **Meine Familie**
            Ich heiße Max. Ich habe eine kleine Familie. Mein Vater heißt Peter und meine Mutter heißt Anna. 
            Ich habe eine Schwester. Sie heißt Lisa. Wir wohnen in Berlin. 
            Unsere Wohnung ist groß und schön. Ich liebe meine Familie.
            """,
            'A2': f"""
            **Ein Tag im Supermarkt**
            Gestern bin ich zum Supermarkt gegangen. Ich musste Lebensmittel für die Woche kaufen. 
            Zuerst habe ich Obst und Gemüse gekauft: Äpfel, Bananen und Tomaten. 
            Dann habe ich Brot von der Bäckerei geholt. Es war sehr frisch und hat gut gerochen.
            An der Kasse musste ich lange warten, aber das macht nichts. 
            Insgesamt habe ich 45 Euro ausgegeben.
            """,
            'B1': f"""
            **Die Bedeutung von Fremdsprachen**
            In unserer globalisierten Welt werden Fremdsprachenkenntnisse immer wichtiger. 
            Nicht nur für die berufliche Karriere, sondern auch für die persönliche Entwicklung sind sie von großer Bedeutung.
            Wer mehrere Sprachen spricht, kann leichter mit Menschen aus verschiedenen Kulturen kommunizieren.
            Außerdem zeigen Studien, dass das Erlernen von Sprachen die kognitiven Fähigkeiten verbessert.
            Obwohl es manchmal schwierig ist, lohnt sich die Mühe definitiv.
            """,
            'B2': f"""
            **Digitalisierung im Bildungswesen**
            Die fortschreitende Digitalisierung hat das Bildungswesen grundlegend verändert. 
            Einerseits ermöglichen digitale Medien einen flexibleren und individuelleren Zugang zu Bildungsinhalten.
            Lernplattformen und Apps erlauben es, jederzeit und überall zu lernen, was besonders für Berufstätige von Vorteil ist.
            Andererseits stellt die Digitalisierung Lehrkräfte vor neue Herausforderungen.
            Sie müssen nicht nur fachlich kompetent sein, sondern auch digitale Kompetenzen entwickeln.
            Kritiker warnen zudem vor einer zunehmenden sozialen Ungleichheit, da nicht alle Schüler gleichen Zugang zu digitalen Endgeräten haben.
            """
        }
        
        lesson = {
            'title': f'Reading Comprehension: {topic.title()}',
            'vocabulary': vocab,
            'content': f"""
            ### Reading Text
            
            **Key Vocabulary:**
            {' | '.join([f'• **{word}**' for word in vocab])}
            
            {reading_texts.get(level, reading_texts['A1'])}
            
            **Comprehension Questions:**
            1. What is the main topic of the text?
            2. Identify 3 key facts mentioned.
            3. Find one sentence you find challenging and analyze its structure.
            """,
            'exercise': "Summarize the text in 2-3 sentences in your own words.",
            'tip': "Underline words you don't know, but try to understand them from context first."
        }
        
    else:  # grammar
        grammar_topic = generator.generate_grammar_topic(level)
        
        lesson = {
            'title': f'Grammar: {grammar_topic[0]}',
            'vocabulary': [],
            'content': f"""
            ### Grammar Focus: {grammar_topic[0]}
            
            **Concept:**
            {grammar_topic[1]}
            
            **Examples:**
            {grammar_topic[2]}
            
            **Practice Patterns:**
            Try creating your own sentences using this grammar structure.
            
            **Remember:**
            German grammar has rules, but also many exceptions. Practice makes perfect!
            """,
            'exercise': f"Create 3 sentences using {grammar_topic[0]}",
            'tip': "Write down the rule and keep examples handy for reference."
        }
    
    return lesson

# ==========================================
# TRANSLATION FUNCTIONS
# ==========================================

def translate_text(text, source_lang, target_lang):
    """Translate text using MyMemory API (free tier)"""
    
    # Check if we have API email for better limits
    email = st.session_state.api_keys.get('mymemory_email', '')
    
    try:
        # Use MyMemory Translation API (free, 1000 words/day)
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'{source_lang}|{target_lang}'
        }
        
        if email:
            params['de'] = email  # Add email for better limits
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                translation = data['responseData']['translatedText']
                
                # Get match percentage
                match = data['responseData'].get('match', 0)
                
                # Get alternative translations if available
                alternatives = []
                if 'matches' in data:
                    for match_item in data['matches'][:3]:
                        if match_item['translation'] != translation:
                            alternatives.append(match_item['translation'])
                
                return {
                    'success': True,
                    'translation': translation,
                    'confidence': match,
                    'alternatives': alternatives
                }
        
        # Fallback to simple dictionary for common phrases
        return use_fallback_translation(text, source_lang, target_lang)
        
    except Exception as e:
        return use_fallback_translation(text, source_lang, target_lang)

def use_fallback_translation(text, source_lang, target_lang):
    """Simple fallback translation for common phrases"""
    
    # Basic dictionary for common phrases
    translations = {
        'en-de': {
            'hello': 'hallo',
            'goodbye': 'auf wiedersehen',
            'thank you': 'danke',
            'please': 'bitte',
            'yes': 'ja',
            'no': 'nein',
            'good morning': 'guten morgen',
            'good evening': 'guten abend',
            'how are you': 'wie geht es dir',
            'i love you': 'ich liebe dich',
            'my name is': 'mein name ist',
            'what is your name': 'wie heißt du',
        },
        'de-en': {
            'hallo': 'hello',
            'auf wiedersehen': 'goodbye',
            'danke': 'thank you',
            'bitte': 'please',
            'ja': 'yes',
            'nein': 'no',
            'guten morgen': 'good morning',
            'guten abend': 'good evening',
            'wie geht es dir': 'how are you',
            'ich liebe dich': 'i love you',
            'mein name ist': 'my name is',
            'wie heißt du': 'what is your name',
        }
    }
    
    # Try to find translation
    lang_pair = f'{source_lang}-{target_lang}'
    text_lower = text.lower().strip()
    
    if lang_pair in translations and text_lower in translations[lang_pair]:
        return {
            'success': True,
            'translation': translations[lang_pair][text_lower],
            'confidence': 100,
            'alternatives': [],
            'note': 'Basic translation - for better results, add MyMemory email in Settings'
        }
    
    return {
        'success': False,
        'translation': f'[Translation pending: {text}]',
        'confidence': 0,
        'alternatives': [],
        'note': 'Translation service temporarily unavailable. Add API key in Settings for full functionality.'
    }

def get_example_sentences(word, language='de'):
    """Generate example sentences for a word"""
    
    examples = {
        'de': {
            'haus': [
                "Das Haus ist groß. (The house is big.)",
                "Ich gehe nach Hause. (I'm going home.)",
                "Unser Haus hat einen Garten. (Our house has a garden.)"
            ],
            'arbeiten': [
                "Ich arbeite in einem Büro. (I work in an office.)",
                "Sie arbeitet sehr fleißig. (She works very diligently.)",
                "Wir arbeiten zusammen. (We work together.)"
            ],
            'schön': [
                "Das Wetter ist schön. (The weather is nice.)",
                "Sie hat ein schönes Kleid. (She has a beautiful dress.)",
                "Vielen Dank, das ist sehr schön! (Thank you, that's very nice!)"
            ]
        }
    }
    
    word_lower = word.lower()
    
    # Return examples if available
    if language in examples and word_lower in examples[language]:
        return examples[language][word_lower]
    
    # Generate generic examples based on word type
    generic_examples = [
        f"Das ist ein/eine {word}. (This is a {word}.)",
        f"Ich mag {word}. (I like {word}.)",
        f"Der/Die/Das {word} ist gut. (The {word} is good.)"
    ]
    
    return generic_examples

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_level_title(xp):
    """Get user title based on XP"""
    titles = [
        (0, "Anfänger (Beginner) 🌱"),
        (100, "Entdecker (Explorer) 🔍"),
        (300, "Lerner (Learner) 📚"),
        (600, "Fortgeschritten (Advanced) 🎯"),
        (1000, "Sprachkenner (Language Expert) 🏆"),
        (1500, "Meister (Master) 👑"),
        (2000, "Guru 🧙‍♂️")
    ]
    
    for i in range(len(titles)-1, -1, -1):
        if xp >= titles[i][0]:
            return titles[i][1]
    return titles[0][1]

def add_xp(amount):
    """Add XP and check for achievements"""
    st.session_state.xp += amount
    check_achievements()

def check_achievements():
    """Check and award achievements"""
    achievements = []
    
    if st.session_state.xp >= 100 and "First Century" not in st.session_state.achievements:
        achievements.append("First Century")
        st.balloons()
    
    if st.session_state.streak >= 7 and "Week Warrior" not in st.session_state.achievements:
        achievements.append("Week Warrior")
    
    if st.session_state.current_day >= 30 and "Monthly Master" not in st.session_state.achievements:
        achievements.append("Monthly Master")
    
    for achievement in achievements:
        st.session_state.achievements.append(achievement)
        st.success(f"🏆 Achievement Unlocked: {achievement}!")

def display_xp_bar():
    """Display XP progress bar"""
    max_xp = ((st.session_state.xp // 100) + 1) * 100
    current_progress = (st.session_state.xp % 100)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"<div class='level-indicator'>{get_level_title(st.session_state.xp)}</div>", unsafe_allow_html=True)
        st.progress(current_progress / 100)
        st.caption(f"XP: {st.session_state.xp} | Next level: {max_xp} XP")

# ==========================================
# API FUNCTIONS
# ==========================================

def test_api_connection():
    """Test if API keys are configured"""
    if st.session_state.api_keys['openrouter']:
        return True, "OpenRouter API configured ✅"
    elif st.session_state.api_keys['huggingface']:
        return True, "HuggingFace API configured ✅"
    else:
        return False, "⚠️ No API keys configured. Add keys in Settings for AI features."

# ==========================================
# MAIN PAGES
# ==========================================

def page_dashboard():
    """Main dashboard page"""
    st.title("🇩🇪 LinguaFlow - Your AI German Tutor")
    
    # Welcome message
    if st.session_state.user_name:
        st.header(f"Willkommen, {st.session_state.user_name}! 👋")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            name = st.text_input("What's your name?", key="name_input")
        with col2:
            if st.button("Save", type="primary"):
                if name:
                    st.session_state.user_name = name
                    st.rerun()
    
    # Display XP and progress
    display_xp_bar()
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Level", st.session_state.user_level or "Not Set", 
                  help="Take the placement test to determine your level")
    
    with col2:
        st.metric("Day", f"{st.session_state.current_day}/180",
                  help="Your journey to B2")
    
    with col3:
        st.metric("Streak", f"{st.session_state.streak} 🔥",
                  help="Days in a row")
    
    with col4:
        st.metric("Achievements", len(st.session_state.achievements),
                  help="Unlock more by learning!")
    
    # Daily tasks overview
    st.markdown("### 📝 Today's Learning Path")
    
    if not st.session_state.placement_completed:
        st.warning("👉 Start with the Placement Test to unlock your personalized learning path!")
        if st.button("Take Placement Test", type="primary", use_container_width=True):
            st.session_state.selected_page = "📊 Placement Test"  # Fixed: Use correct key
            st.rerun()
    else:
        # Show today's tasks
        skills = ['Speaking 🗣️', 'Writing ✍️', 'Listening 👂', 'Reading 📖', 'Grammar 📐']
        
        cols = st.columns(5)
        for i, skill in enumerate(skills):
            with cols[i]:
                completed = skill in st.session_state.daily_tasks_completed
                if completed:
                    st.success(f"✅ {skill}")
                else:
                    if st.button(f"📚 {skill}", key=f"skill_{skill}", use_container_width=True):
                        st.session_state.selected_skill = skill
                        st.session_state.selected_page = "📚 Today's Lesson"
                        st.rerun()
        
        # Progress for today
        progress = len(st.session_state.daily_tasks_completed) / 5
        st.progress(progress)
        st.caption(f"Daily Progress: {len(st.session_state.daily_tasks_completed)}/5 tasks completed")
        
        if progress == 1.0:
            st.success("🎉 Congratulations! You've completed today's lessons! +50 XP")
            if "daily_complete" not in st.session_state:
                add_xp(50)
                st.session_state.daily_complete = True

def page_placement_test():
    """Placement test page"""
    st.title("📊 Placement Test")
    st.markdown("### Determine Your German Level (A1 → B2)")
    
    if st.session_state.placement_completed:
        st.info(f"You've already taken the placement test. Your level: **{st.session_state.user_level}**")
        if st.button("Retake Test"):
            st.session_state.placement_completed = False
            st.session_state.user_level = None
            st.rerun()
        return
    
    with st.form("placement_test"):
        st.markdown("#### Part 1: Multiple Choice")
        
        q1 = st.radio(
            "1. Wie ____ du?",
            ["heißen", "heißt", "heiße", "heißst"],
            index=None
        )
        
        q2 = st.radio(
            "2. Ich komme ____ Deutschland.",
            ["aus", "von", "in", "zu"],
            index=None
        )
        
        st.markdown("#### Part 2: Fill in the Blanks")
        
        q3 = st.text_input("3. Complete: Ich _____ (to have) einen Hund.")
        
        q4 = st.text_input("4. Complete: Er _____ (to go) zur Schule.")
        
        st.markdown("#### Part 3: Translation")
        
        q5 = st.text_area("5. Translate to German: 'I would like a coffee, please.'")
        
        st.markdown("#### Part 4: Word Order")
        
        q6 = st.text_input("6. Arrange: morgen / ich / gehe / Arbeit / zur")
        
        submitted = st.form_submit_button("Submit Test", type="primary", use_container_width=True)
        
        if submitted:
            # Simple scoring logic
            score = 0
            
            if q1 == "heißt": score += 1
            if q2 == "aus": score += 1
            if q3 and "habe" in q3.lower(): score += 1
            if q4 and "geht" in q4.lower(): score += 1
            if q5 and any(word in q5.lower() for word in ["möchte", "kaffee", "bitte"]): score += 2
            if q6 and "morgen gehe ich zur arbeit" in q6.lower(): score += 2
            
            # Determine level
            if score <= 2:
                level = "A1"
            elif score <= 4:
                level = "A2"
            elif score <= 6:
                level = "B1"
            else:
                level = "B2"
            
            st.session_state.user_level = level
            st.session_state.placement_completed = True
            
            st.balloons()
            st.success(f"Test Complete! Your level is: **{level}**")
            st.info("Your personalized 180-day learning plan has been created!")
            add_xp(25)
            
            time.sleep(2)
            st.rerun()

def page_todays_lesson():
    """Today's lesson page with dynamic content"""
    st.title("📚 Today's Lesson")
    
    if not st.session_state.placement_completed:
        st.warning("Please complete the placement test first!")
        if st.button("Go to Placement Test"):
            st.session_state.selected_page = "📊 Placement Test"
            st.rerun()
        return
    
    st.markdown(f"### Day {st.session_state.current_day} - Level {st.session_state.user_level}")
    
    # Skill selector
    skill = st.selectbox(
        "Choose a skill to practice:",
        ["speaking", "writing", "listening", "reading", "grammar"]
    )
    
    # Generate dynamic lesson
    lesson = generate_dynamic_lesson(st.session_state.user_level, skill)
    
    # Display lesson in a nice card format
    st.markdown(f"<div class='lesson-card'>", unsafe_allow_html=True)
    st.markdown(f"## {lesson['title']}")
    st.markdown(lesson['content'])
    
    # Show tip
    st.info(f"💡 **Tip:** {lesson['tip']}")
    
    # Exercise section
    st.markdown("### 📝 Exercise")
    st.markdown(lesson['exercise'])
    
    # Exercise interaction based on skill type
    if skill == "writing":
        answer = st.text_area("Your answer:", height=150, key="writing_answer")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if answer:
                    st.success("Great job! Your writing has been submitted.")
                    st.markdown("**Sample Feedback:** Good structure! Remember to capitalize nouns in German.")
                    add_xp(10)
                    if "Writing ✍️" not in st.session_state.daily_tasks_completed:
                        st.session_state.daily_tasks_completed.append("Writing ✍️")
    
    elif skill == "speaking":
        st.info("🎤 Practice saying the sentences above. Focus on clear pronunciation!")
        if st.button("I completed the speaking exercise", type="primary"):
            st.success("Excellent pronunciation practice! Keep speaking daily.")
            add_xp(10)
            if "Speaking 🗣️" not in st.session_state.daily_tasks_completed:
                st.session_state.daily_tasks_completed.append("Speaking 🗣️")
    
    elif skill == "grammar":
        answer = st.text_input("Your answer:", key="grammar_answer")
        if st.button("Check Answer", type="primary"):
            if answer:
                st.info("Answer submitted! Review the grammar rules above to check your work.")
                add_xp(10)
                if "Grammar 📐" not in st.session_state.daily_tasks_completed:
                    st.session_state.daily_tasks_completed.append("Grammar 📐")
    
    elif skill == "listening":
        st.markdown("**Practice:** Read the dialogue aloud 3 times, focusing on pronunciation.")
        if st.button("Complete Listening Exercise", type="primary"):
            st.success("Well done! Listening skills improved.")
            add_xp(10)
            if "Listening 👂" not in st.session_state.daily_tasks_completed:
                st.session_state.daily_tasks_completed.append("Listening 👂")
    
    elif skill == "reading":
        answer = st.text_area("Write your summary:", height=100, key="reading_answer")
        if st.button("Submit Summary", type="primary"):
            if answer:
                st.success("Good comprehension! Keep reading daily.")
                add_xp(10)
                if "Reading 📖" not in st.session_state.daily_tasks_completed:
                    st.session_state.daily_tasks_completed.append("Reading 📖")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Regenerate lesson button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 New Lesson", use_container_width=True):
            # Clear cache for this skill to generate new content
            st.session_state.lesson_cache = {}
            st.rerun()
    
    with col2:
        if st.button("📚 Resources", use_container_width=True):
            st.info("Additional resources and explanations will be available in Phase 2!")

def page_ai_guru():
    """AI Guru chat interface"""
    st.title("🧙‍♂️ AI Guru - Your Personal German Teacher")
    
    # Check API status
    api_status, message = test_api_connection()
    if not api_status:
        st.warning(message)
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📖 Explain Grammar", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you explain German grammar basics?"
            })
    
    with col2:
        if st.button("🗣️ Practice Speaking", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Let's practice speaking German!"
            })
    
    with col3:
        if st.button("✍️ Check My Writing", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you check my German writing?"
            })
    
    with col4:
        if st.button("❓ Ask a Question", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "I have a question about German."
            })
    
    # Chat interface
    st.markdown("### Chat with AI Guru")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class='ai-message'>
            👋 Guten Tag! I'm your AI German Guru. I'm here to help you learn German effectively!
            
            I can:
            - Explain grammar concepts
            - Help you practice speaking
            - Check your writing
            - Answer any questions about German
            - Give you personalized exercises
            
            What would you like to work on today?
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"<div class='user-message'>You: {message['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='ai-message'>AI Guru: {message['content']}</div>", unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", key="chat_input")
        col1, col2 = st.columns([1, 5])
        with col1:
            submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        if submitted and user_input:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Generate contextual response (enhanced placeholder for now)
            if "grammar" in user_input.lower():
                response = "German grammar has 4 cases: Nominative (subject), Accusative (direct object), Dative (indirect object), and Genitive (possession). Would you like me to explain any specific case?"
            elif "practice" in user_input.lower():
                response = f"Let's practice! Based on your {st.session_state.user_level} level, try this: 'Ich gehe heute ins Kino.' Can you tell me what this means and identify the verb?"
            elif "translate" in user_input.lower():
                response = "I can help with translation! Please share the sentence you'd like to translate, and I'll explain the grammar structure too."
            else:
                response = f"Great question about '{user_input}'! In Phase 2, I'll provide detailed, AI-powered responses. For now, keep practicing your {st.session_state.user_level} level materials!"
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()

def page_translator():
    """Enhanced smart translator page"""
    st.title("🔄 Smart Translator")
    st.markdown("### English ↔ German Translation with Context")
    
    # Translation direction selector
    direction = st.radio("Translation Direction:", 
                        ["English → German", "German → English"], 
                        horizontal=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if direction == "English → German":
            st.markdown("#### English Input")
            source_text = st.text_area("Enter English text:", height=150, key="source_input")
            source_lang = "en"
            target_lang = "de"
        else:
            st.markdown("#### German Input")
            source_text = st.text_area("Enter German text:", height=150, key="source_input")
            source_lang = "de"
            target_lang = "en"
    
    with col2:
        st.markdown("#### Translation Result")
        
        if st.button("🔄 Translate", type="primary", use_container_width=True):
            if source_text:
                with st.spinner("Translating..."):
                    result = translate_text(source_text, source_lang, target_lang)
                    
                    if result['success']:
                        st.markdown(f"<div class='translation-result'>", unsafe_allow_html=True)
                        st.markdown(f"**Translation:** {result['translation']}")
                        
                        if result.get('confidence'):
                            st.progress(result['confidence'] / 100)
                            st.caption(f"Confidence: {result['confidence']}%")
                        
                        if result.get('alternatives'):
                            st.markdown("**Alternative translations:**")
                            for alt in result['alternatives']:
                                st.caption(f"• {alt}")
                        
                        if result.get('note'):
                            st.info(result['note'])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.warning(result.get('note', 'Translation service temporarily unavailable'))
            else:
                st.warning("Please enter text to translate")
    
    # Word analysis section
    st.markdown("---")
    st.markdown("### 📝 Word Analysis & Examples")
    
    word_to_analyze = st.text_input("Enter a German word to see examples:")
    
    if word_to_analyze:
        examples = get_example_sentences(word_to_analyze, 'de')
        st.markdown("**Example sentences:**")
        for example in examples:
            st.markdown(f"• {example}")
    
    # Common phrases section
    with st.expander("📚 Common Phrases"):
        st.markdown("""
        **Greetings:**
        - Guten Morgen = Good morning
        - Guten Tag = Good day/Hello
        - Guten Abend = Good evening
        - Auf Wiedersehen = Goodbye
        
        **Polite Expressions:**
        - Bitte = Please
        - Danke = Thank you
        - Entschuldigung = Excuse me
        - Es tut mir leid = I'm sorry
        
        **Questions:**
        - Wie geht es Ihnen? = How are you? (formal)
        - Wie heißen Sie? = What's your name? (formal)
        - Wo ist...? = Where is...?
        - Wie viel kostet das? = How much does it cost?
        """)

def page_progress():
    """Progress tracking page"""
    st.title("📈 Your Progress")
    
    # Overall stats
    st.markdown("### Learning Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total XP", st.session_state.xp)
        st.metric("Current Title", get_level_title(st.session_state.xp).split()[0])
    
    with col2:
        st.metric("Days Completed", st.session_state.current_day)
        st.metric("Current Streak", f"{st.session_state.streak} days")
    
    with col3:
        st.metric("Level", st.session_state.user_level or "Not Set")
        completion = (st.session_state.current_day / 180) * 100
        st.metric("Journey Progress", f"{completion:.1f}%")
    
    # Progress chart
    st.markdown("### 180-Day Journey Progress")
    progress_bar = st.progress(st.session_state.current_day / 180)
    st.caption(f"Day {st.session_state.current_day} of 180 - {180 - st.session_state.current_day} days to B2!")
    
    # Skills breakdown
    st.markdown("### Skills Breakdown")
    
    # Calculate skill progress based on completed tasks
    skills_progress = {
        "Speaking 🗣️": 0,
        "Writing ✍️": 0,
        "Listening 👂": 0,
        "Reading 📖": 0,
        "Grammar 📐": 0
    }
    
    for skill in st.session_state.daily_tasks_completed:
        if skill in skills_progress:
            skills_progress[skill] = min(skills_progress[skill] + 20, 100)
    
    for skill, progress in skills_progress.items():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(skill)
        with col2:
            st.progress(progress/100)
            st.caption(f"{progress}% completed today")
    
    # Milestones
    st.markdown("### 🎯 Upcoming Milestones")
    milestones = [
        ("Week 1", 7, st.session_state.current_day >= 7),
        ("Month 1", 30, st.session_state.current_day >= 30),
        ("Quarter", 45, st.session_state.current_day >= 45),
        ("Midway", 90, st.session_state.current_day >= 90),
        ("Final Sprint", 150, st.session_state.current_day >= 150),
        ("B2 Achievement", 180, st.session_state.current_day >= 180)
    ]
    
    cols = st.columns(6)
    for i, (name, day, achieved) in enumerate(milestones):
        with cols[i]:
            if achieved:
                st.success(f"✅ {name}")
            else:
                st.info(f"🎯 {name}\nDay {day}")

def page_achievements():
    """Achievements page"""
    st.title("🏆 Achievements")
    
    st.markdown("### Unlocked Achievements")
    
    if st.session_state.achievements:
        cols = st.columns(3)
        for i, achievement in enumerate(st.session_state.achievements):
            with cols[i % 3]:
                st.markdown(f"<div class='achievement-badge'>🏆 {achievement}</div>", unsafe_allow_html=True)
    else:
        st.info("No achievements yet. Keep learning to unlock rewards!")
    
    st.markdown("### Available Achievements")
    
    all_achievements = [
        ("First Century", "Earn 100 XP", st.session_state.xp >= 100),
        ("Week Warrior", "7-day streak", st.session_state.streak >= 7),
        ("Monthly Master", "Complete 30 days", st.session_state.current_day >= 30),
        ("Grammar Guru", "Complete 20 grammar lessons", False),
        ("Conversation Champion", "Complete 50 speaking exercises", False),
        ("Writing Wizard", "Submit 30 writing exercises", False),
        ("Listening Legend", "Complete 40 listening exercises", False),
        ("Reading Rockstar", "Read 100 texts", False),
        ("Halfway Hero", "Reach day 90", st.session_state.current_day >= 90),
        ("B2 Boss", "Complete the 180-day journey", st.session_state.current_day >= 180)
    ]
    
    for name, description, unlocked in all_achievements:
        col1, col2, col3 = st.columns([3, 4, 1])
        with col1:
            st.write(f"**{name}**")
        with col2:
            st.caption(description)
        with col3:
            if unlocked:
                st.success("✅")
            else:
                st.write("🔒")

def page_settings():
    """Settings page"""
    st.title("⚙️ Settings")
    
    st.markdown("### API Configuration")
    st.info("Add your API keys here for enhanced AI features. Leave blank to use limited free features.")
    
    with st.form("api_settings"):
        openrouter_key = st.text_input(
            "OpenRouter API Key (Recommended)",
            value=st.session_state.api_keys.get('openrouter', ''),
            type="password",
            help="Get your key from openrouter.ai"
        )
        
        huggingface_key = st.text_input(
            "HuggingFace API Key (Alternative)",
            value=st.session_state.api_keys.get('huggingface', ''),
            type="password",
            help="Get your key from huggingface.co"
        )
        
        mymemory_email = st.text_input(
            "MyMemory Email (For better translation)",
            value=st.session_state.api_keys.get('mymemory_email', ''),
            help="Optional: Provides higher translation limits (10,000 words/day vs 1,000)"
        )
        
        if st.form_submit_button("Save Settings", type="primary"):
            st.session_state.api_keys['openrouter'] = openrouter_key
            st.session_state.api_keys['huggingface'] = huggingface_key
            st.session_state.api_keys['mymemory_email'] = mymemory_email
            st.success("Settings saved successfully!")
    
    # Test connection
    if st.button("Test API Connection"):
        status, message = test_api_connection()
        if status:
            st.success(message)
        else:
            st.error(message)
    
    st.markdown("### Learning Preferences")
    
    daily_goal = st.slider("Daily learning goal (minutes)", 5, 60, 15)
    notification = st.checkbox("Enable reminder notifications", value=False)
    
    st.markdown("### About LinguaFlow")
    st.info("""
    **LinguaFlow** - Your Free AI German Tutor
    
    Version: 1.0.1 (Phase 1 - Enhanced)
    
    Created with ❤️ to make German learning accessible to everyone.
    
    Features:
    - 🤖 AI-powered personalized lessons
    - 📚 Dynamic content generation for each skill
    - 🎮 Gamified progress tracking
    - 🔄 Smart translation with examples
    - 🧙‍♂️ Interactive AI tutor
    - 📊 Adaptive learning path based on your level
    
    No subscription required. Ever. 🎉
    """)

# ==========================================
# MAIN APP NAVIGATION
# ==========================================

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("# 🇩🇪 LinguaFlow")
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Dashboard": page_dashboard,
            "📊 Placement Test": page_placement_test,
            "📚 Today's Lesson": page_todays_lesson,
            "🧙‍♂️ AI Guru": page_ai_guru,
            "🔄 Translator": page_translator,
            "📈 Progress": page_progress,
            "🏆 Achievements": page_achievements,
            "⚙️ Settings": page_settings
        }
        
        # Initialize selected page
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "🏠 Dashboard"
        
        # Create navigation buttons
        for page_name in pages.keys():
            if st.button(page_name, use_container_width=True, 
                        type="primary" if st.session_state.selected_page == page_name else "secondary"):
                st.session_state.selected_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats in sidebar
        if st.session_state.user_level:
            st.markdown(f"**Level:** {st.session_state.user_level}")
            st.markdown(f"**XP:** {st.session_state.xp}")
            st.markdown(f"**Streak:** {st.session_state.streak} 🔥")
    
    # Display selected page
    pages[st.session_state.selected_page]()

if __name__ == "__main__":
    main()