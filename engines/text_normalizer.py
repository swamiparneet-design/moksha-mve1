"""
TEXT NORMALIZATION ENGINE
Converts written dialect to spoken phonetic form for natural TTS
"""
import json
from pathlib import Path
from loguru import logger


class TextNormalizer:
    """Normalize local dialect text for natural TTS pronunciation"""
    
    def __init__(self, language: str = "hindi"):
        self.logger = logger
        self.language = language
        
        # Load dictionary from languages folder
        self.dictionary_path = Path(f"languages/{language}/dictionary.json")
        self.learned_corrections = self._load_learned_dictionary()
        
        # Haryanvi hardcoded corrections (will merge with learned)
        self.haryanvi_corrections = {
            # Agriculture terms
            'hala chukta': 'hal uthaata',
            'hala': 'hal',
            'hal chal': 'hal chal',
            'khet mein': 'khet me',
            'kheti': 'kheti baadi',
            'fasal': 'fasal',
            'kisan': 'kisaan',
            
            # Pronouns
            'mhara': 'hamara',
            'thara': 'tumhara',
            'mara': 'mera',
            'tara': 'tera',
            'mhari': 'hamari',
            'thari': 'tumhari',
            
            # Common words
            'ke': 'ki',
            'che': 'hai',
            'tha': 'tha',
            'thi': 'thi',
            'the': 'the',
            'ho': 'hu',
            'ha': 'hu',
            
            # Verbs
            'chala jaata': 'jaata tha',
            'chal': 'ja',
            'aaya': 'aaya',
            'gayo': 'gaya',
            'kariyo': 'kiya',
            'dhariyo': 'dhara',
            'uthayo': 'uthaya',
            'baitho': 'baitha',
            'sovo': 'soya',
            'jago': 'jaga',
            'khaavo': 'khaya',
            'piyo': 'piya',
            
            # Adjectives
            'badi': 'bahut',
            'choto': 'chhota',
            'baro': 'bada',
            'saro': 'sara',
            'thodo': 'thoda',
            'niko': 'achha',
            'nado': 'bura',
            
            # Time expressions
            'subah': 'savere',
            'shaam': 'saanjh',
            'raat': 'raat',
            'din': 'din',
            'roz': 'roj',
            'kal': 'kal',
            'aaj': 'aaj',
            
            # Location
            'gaon mein': 'gaon me',
            'ghar mein': 'ghar pe',
            'khet mein': 'khet me',
            'paas mein': 'lage',
            'upar': 'upar',
            'niche': 'neeche',
            'aage': 'aage',
            'piche': 'peeche',
            
            # Relationships
            'bhai': 'bhai',
            'beera': 'bhai',
            'ma': 'maa',
            'ba': 'baap',
            'dada': 'dada',
            'dadi': 'dadi',
            'nana': 'nana',
            'nani': 'nani',
            
            # Common phrases
            'kya haal': 'kya haal chaal',
            'kaise ho': 'kya haal',
            'kahan ja rahe': 'katte ja riya',
            'kab aaye': 'kab aaya',
            'bahut achha': 'bahut niko',
            'bahut bura': 'bahut nado',
            
            # Auxiliary verbs
            'rah': 'riya',
            'raha': 'riya',
            'rahi': 'riya',
            'sakta': 'sakta',
            'sakti': 'sakti',
            'chahiye': 'chiye',
            
            # Numbers
            'ek': 'ek',
            'do': 'do',
            'teen': 'teen',
            'chaar': 'chaar',
            'paanch': 'paanch',
        }
        
        # Merge corrections based on language
        if language == "haryanvi":
            self.corrections = {**self.haryanvi_corrections, **self.learned_corrections}
        else:
            self.corrections = self.learned_corrections
        
        # Hindi common corrections (for standard Hindi content)
        self.hindi_corrections = {
            'mein': 'me',
            'hai': 'he',
            'tha': 'tha',
            'thi': 'thi',
            'the': 'the',
            'kar': 'kar',
            'karke': 'karke',
            'karte': 'karte',
            'karti': 'karti',
            'karta': 'karta',
            'dekho': 'dekh',
            'sunno': 'sun',
            'jao': 'ja',
            'aao': 'aa',
            'lo': 'le',
            'do': 'de',
        }
        
        # Natural pause markers for breathing
        self.pause_markers = ['...', ',', '.', 'aur', 'par', 'lekin', 'toh', 'fir', 'phir']
        
        # Emotion-based speed adjustments
        self.emotion_speed = {
            'excited': '1.05',
            'sad': '0.85',
            'angry': '1.1',
            'happy': '1.0',
            'curious': '0.95',
            'serious': '0.9',
            'storytelling': '0.92',
            'neutral': '1.0'
        }
    
    def _load_learned_dictionary(self) -> dict:
        """Load learned corrections from language dictionary file"""
        if self.dictionary_path.exists():
            try:
                with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('word_corrections', {})
            except Exception as e:
                self.logger.error(f"Error loading dictionary: {e}")
                return {}
        return {}
        
    def normalize(self, text: str, language: str = "hindi") -> tuple:
        """
        Convert written text to spoken phonetic form
        
        Args:
            text: Input text
            language: hindi/haryanvi/bhojpuri
            
        Returns:
            (display_text, tts_text, pause_points)
        """
        display_text = text.strip()
        tts_text = text.strip()
        
        # Apply corrections based on language
        if language == "haryanvi":
            corrections = self.haryanvi_corrections
        elif language == "bhojpuri":
            # TODO: Add Bhojpuri corrections
            corrections = {**self.haryanvi_corrections, **self.hindi_corrections}
        else:  # Hindi
            corrections = self.hindi_corrections
        
        # Apply pronunciation corrections
        for wrong, correct in corrections.items():
            tts_text = tts_text.replace(wrong, correct)
        
        # Add natural pauses
        pause_points = []
        words = tts_text.split()
        
        # Add pause after every 6-8 words for natural breathing
        normalized_words = []
        for i, word in enumerate(words):
            normalized_words.append(word)
            if (i + 1) % 7 == 0 and i < len(words) - 1:
                normalized_words.append('...')
                pause_points.append(f"breath_after_word_{i}")
        
        tts_text = ' '.join(normalized_words)
        
        # Add slight pause before/after conjunctions
        for marker in self.pause_markers:
            if marker == '...':
                continue
            tts_text = tts_text.replace(f' {marker} ', f' ...{marker}... ')
        
        self.logger.info(f"📝 [{language.upper()}] Normalized: '{display_text}' → '{tts_text}'")
        
        return display_text, tts_text, pause_points
    
    def add_emotion_markers(self, text: str, emotion: str) -> str:
        """Add emotion-specific markers for TTS"""
        
        emotion_speed = {
            'excited': '1.05',
            'sad': '0.85',
            'angry': '1.1',
            'happy': '1.0',
            'curious': '0.95',
            'serious': '0.9',
            'storytelling': '0.92',
            'neutral': '1.0'
        }
        
        speed = emotion_speed.get(emotion, '1.0')
        
        # Add speed marker
        marked_text = f"[speed:{speed}] {text}"
        
        return marked_text
