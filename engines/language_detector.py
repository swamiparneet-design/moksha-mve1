"""
DYNAMIC LANGUAGE DETECTOR
Automatically detects Indian language and dialect from text/speech
Activates appropriate language learner agent
"""
import json
from pathlib import Path
from loguru import logger


class LanguageDetector:
    """Detect and activate language-specific learning agent"""
    
    def __init__(self):
        self.logger = logger
        self.supported_languages = {
            'haryanvi': {
                'keywords': ['mhara', 'thara', 'ke', 'che', 'haryanvi', 'hariyana'],
                'region': 'Haryana',
                'script': 'Devanagari',
                'agent': 'language_learner'
            },
            'bhojpuri': {
                'keywords': ['hamar', 'tohar', 'ba', 'bani', 'bhojpuri', 'bihar'],
                'region': 'Bihar/Jharkhand/UP',
                'script': 'Devanagari',
                'agent': 'language_learner'
            },
            'rajasthani': {
                'keywords': ['mara', 'tara', 'padharo', 'mharo', 'rajasthan'],
                'region': 'Rajasthan',
                'script': 'Devanagari',
                'agent': 'language_learner'
            },
            'punjabi': {
                'keywords': ['mera', 'tera', 'ji', 'sat Sri', 'akal', 'punjab'],
                'region': 'Punjab',
                'script': 'Gurmukhi',
                'agent': 'language_learner'
            },
            'marathi': {
                'keywords': ['majha', 'tujha', 'ahe', 'maharashtra', 'namaskar'],
                'region': 'Maharashtra',
                'script': 'Devanagari',
                'agent': 'language_learner'
            },
            'gujarati': {
                'keywords': ['maru', 'tamaru', 'chhe', 'gujarat', 'kem cho'],
                'region': 'Gujarat',
                'script': 'Gujarati',
                'agent': 'language_learner'
            },
            'tamil': {
                'keywords': ['en', 'un', 'vanakkam', 'tamil', 'nadu'],
                'region': 'Tamil Nadu',
                'script': 'Tamil',
                'agent': 'language_learner'
            },
            'telugu': {
                'keywords': ['na', 'nee', 'namaskaram', 'telugu', 'desam'],
                'region': 'Andhra/Telangana',
                'script': 'Telugu',
                'agent': 'language_learner'
            },
            'kannada': {
                'keywords': ['nan', 'nin', 'namaskara', 'kannada', 'nadu'],
                'region': 'Karnataka',
                'script': 'Kannada',
                'agent': 'language_learner'
            },
            'malayalam': {
                'keywords': ['ente', 'ningal', 'namaskaram', 'kerala'],
                'region': 'Kerala',
                'script': 'Malayalam',
                'agent': 'language_learner'
            },
            'odia': {
                'keywords': ['mora', 'tora', 'namaskara', 'odia', 'isha'],
                'region': 'Odisha',
                'script': 'Odia',
                'agent': 'language_learner'
            },
            'bengali': {
                'keywords': ['amar', 'tomar', 'nomoshkar', 'bangla', 'ami'],
                'region': 'West Bengal/Bangladesh',
                'script': 'Bengali',
                'agent': 'language_learner'
            },
            'assamese': {
                'keywords': ['mor', 'tor', 'nomoskar', 'axomiya', 'moi'],
                'region': 'Assam',
                'script': 'Assamese',
                'agent': 'language_learner'
            },
            'hindi': {
                'keywords': ['mera', 'tera', 'hai', 'hind', 'namaste'],
                'region': 'Pan-India',
                'script': 'Devanagari',
                'agent': 'language_learner'
            }
        }
        
        # Accent variations within languages
        self.accent_profiles = {
            'haryanvi': {
                'jat': {'features': ['hard_consonants', 'strong_h'], 'regions': ['Rohtak', 'Hisar']},
                'ahir': {'features': ['softened_t', 'melodic'], 'regions': ['Rewari', 'Gurgaon']},
                'gujar': {'features': ['nasal_sounds', 'drawl'], 'regions': ['Sirsa', 'Fatehabad']},
                'urban': {'features': ['hindi_mix', 'softer'], 'regions': ['Faridabad', 'Panipat']}
            },
            'bhojpuri': {
                'western': {'features': ['hard_k', 'strong_t'], 'regions': ['Varanasi', 'Ballia']},
                'central': {'features': ['balanced', 'standard'], 'regions': ['Patna', 'Gaya']},
                'eastern': {'features': ['softened_p', 'bengali_influence'], 'regions': ['Purnia', 'Katihar']}
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language from text sample"""
        text_lower = text.lower()
        scores = {}
        
        for lang, data in self.supported_languages.items():
            score = 0
            for keyword in data['keywords']:
                if keyword in text_lower:
                    score += 1
            scores[lang] = score
        
        # Get highest scoring language
        if max(scores.values()) == 0:
            return 'hindi'  # Default fallback
        
        detected_lang = max(scores, key=scores.get)
        confidence = scores[detected_lang] / len(self.supported_languages[detected_lang]['keywords'])
        
        self.logger.info(f"🔍 Detected: {detected_lang} (confidence: {confidence:.2f})")
        
        return detected_lang
    
    def detect_accent(self, text: str, language: str) -> str:
        """Detect accent/sub-dialect from text"""
        if language not in self.accent_profiles:
            return 'standard'
        
        profiles = self.accent_profiles[language]
        text_lower = text.lower()
        
        for accent, features in profiles.items():
            # Check for region-specific words
            for region in features.get('regions', []):
                if region.lower() in text_lower:
                    return accent
            
            # Check for phonetic features
            if 'hard_consonants' in features.get('features', []):
                if any(c in text_lower for c in ['kh', 'gh', 'th']):
                    return accent
        
        return 'standard'
    
    def activate_agent(self, language: str, accent: str = 'standard'):
        """Activate language learning agent with specific configuration"""
        self.logger.info(f"🚀 Activating {language} ({accent}) learning agent...")
        
        # Create language directory if not exists
        lang_dir = Path(f"languages/{language}")
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize dictionary if not exists
        dict_path = lang_dir / "dictionary.json"
        if not dict_path.exists():
            self._create_initial_dictionary(language, accent)
        
        # Load language learner
        from engines.language_learner import LanguageLearner
        learner = LanguageLearner(language)
        
        self.logger.success(f"✅ {language.capitalize()} agent activated!")
        return learner
    
    def _create_initial_dictionary(self, language: str, accent: str):
        """Create base dictionary for new language"""
        template = {
            "language": language,
            "accent": accent,
            "phonetic_rules": {},
            "word_corrections": {},
            "common_phrases": {},
            "pronunciation_guide": {
                "vowel_sounds": {},
                "consonant_shifts": {},
                "stress_patterns": {}
            },
            "learning_sources": [],
            "usage_examples": [],
            "metadata": {
                "created": "auto_generated",
                "version": "1.0",
                "last_updated": "auto"
            }
        }
        
        dict_path = Path(f"languages/{language}/dictionary.json")
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
    
    def learn_from_media(self, language: str, media_type: str, source_data: dict):
        """
        Learn language from various media sources
        
        Args:
            language: Target language
            media_type: 'film' | 'ragni' | 'song' | 'podcast'
            source_data: Dictionary with media details
        """
        self.logger.info(f"📚 Learning {language} from {media_type}: {source_data.get('title', 'Unknown')}")
        
        learner = self.activate_agent(language)
        
        if media_type == 'film':
            # Process film dialogue/transcript
            if 'dialogues' in source_data:
                learner.learn_from_corpus(source_data['dialogues'])
            
            if 'youtube_url' in source_data:
                audio_path = learner.download_youtube_audio(
                    source_data['youtube_url'],
                    f"{language}_film_{source_data.get('year', 'unknown')}"
                )
                if audio_path:
                    transcript = learner.transcribe_audio(audio_path)
                    learner.analyze_pronunciation(transcript, audio_path)
        
        elif media_type == 'ragni':
            # Process traditional Haryanvi Ragni
            if 'lyrics' in source_data:
                learner.learn_from_corpus(source_data['lyrics'])
            
            if 'audio_url' in source_data:
                # Download and analyze
                pass
        
        elif media_type == 'song':
            # Process modern/traditional songs
            if 'lyrics' in source_data:
                learner.learn_from_corpus(source_data['lyrics'])
        
        # Save updated dictionary
        learner.save_dictionary()
        
        self.logger.success(f"✅ Learned from {media_type}!")


# Example usage
if __name__ == "__main__":
    detector = LanguageDetector()
    
    # Test detection
    test_texts = [
        "Bhai sun, mhare gaon mein ek kisan tha",  # Haryanvi
        "Hamra gaon me ek kisan rahaa",  # Bhojpuri
        "Mhane ek story sangaychi",  # Marathi
        "Enakku oru kadhai theriyum"  # Tamil
    ]
    
    for text in test_texts:
        lang = detector.detect_language(text)
        accent = detector.detect_accent(text, lang)
        print(f"\nText: {text}")
        print(f"Language: {lang} | Accent: {accent}")
