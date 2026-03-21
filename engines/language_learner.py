"""
LANGUAGE LEARNING AGENT
Learns Indian dialects from YouTube/audio sources
Builds pronunciation dictionary automatically
"""
import json
from pathlib import Path
from loguru import logger
import subprocess


class LanguageLearner:
    """Learn language from audio/video sources"""
    
    def __init__(self, language: str = "haryanvi"):
        self.language = language
        self.logger = logger
        self.dictionary_path = Path(f"languages/{language}/dictionary.json")
        self.audio_samples_path = Path(f"languages/{language}/audio_samples")
        self.transcripts_path = Path(f"languages/{language}/transcripts")
        
        # Create directories
        self.dictionary_path.parent.mkdir(parents=True, exist_ok=True)
        self.audio_samples_path.mkdir(parents=True, exist_ok=True)
        self.transcripts_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing dictionary
        self.dictionary = self._load_dictionary()
        
    def _load_dictionary(self) -> dict:
        """Load or create language dictionary"""
        if self.dictionary_path.exists():
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Initialize with basic structure
            dictionary = {
                "language": self.language,
                "phonetic_rules": {},
                "word_corrections": {},
                "common_phrases": {},
                "pronunciation_guide": {}
            }
            return dictionary
    
    def download_youtube_audio(self, youtube_url: str, output_name: str) -> str:
        """Download audio from YouTube video"""
        try:
            output_path = self.audio_samples_path / f"{output_name}.mp3"
            
            # Use yt-dlp to download audio only
            cmd = [
                "yt-dlp",
                "-x",  # Extract audio
                "--audio-format", "mp3",
                "-o", str(output_path),
                youtube_url
            ]
            
            self.logger.info(f"📥 Downloading {self.language} audio from YouTube...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and output_path.exists():
                self.logger.success(f"✅ Audio downloaded: {output_path.name}")
                return str(output_path)
            else:
                self.logger.error(f"Download failed: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error downloading audio: {e}")
            return None
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using Whisper (free, offline)"""
        try:
            self.logger.info(f"🎤 Transcribing {Path(audio_path).name}...")
            
            # Use whisper for transcription
            cmd = [
                "whisper",
                audio_path,
                "--model", "base",
                "--language", "hi",  # Hindi script for Haryanvi
                "--output_dir", str(self.transcripts_path),
                "--output_format", "txt"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                transcript_path = self.transcripts_path / f"{Path(audio_path).stem}.txt"
                if transcript_path.exists():
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        transcript = f.read()
                    self.logger.success(f"✅ Transcribed: {len(transcript)} characters")
                    return transcript
            else:
                self.logger.error(f"Transcription failed: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error transcribing: {e}")
            return None
    
    def analyze_pronunciation(self, transcript: str, audio_path: str):
        """Analyze pronunciation patterns from transcript"""
        words = transcript.lower().split()
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word = word.strip('.,!?;:')
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add to dictionary
        for word, freq in word_freq.items():
            if freq >= 2:  # Only common words
                if word not in self.dictionary["word_corrections"]:
                    self.dictionary["word_corrections"][word] = {
                        "written_form": word,
                        "spoken_form": word,  # Will be refined later
                        "frequency": freq,
                        "context": "learned_from_audio"
                    }
        
        self.logger.info(f"📊 Analyzed {len(word_freq)} unique words")
    
    def save_dictionary(self):
        """Save learned dictionary to file"""
        with open(self.dictionary_path, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, indent=2, ensure_ascii=False)
        
        self.logger.success(f"💾 Dictionary saved: {self.dictionary_path}")
    
    def learn_from_corpus(self, corpus_text: str):
        """Learn from existing text corpus (films, ragni, songs)"""
        lines = corpus_text.split('\n')
        
        for line in lines:
            if len(line.strip()) > 10:
                # Extract phrases and patterns
                words = line.split()
                
                # Learn common phrases (3-5 words)
                for i in range(len(words) - 2):
                    phrase = ' '.join(words[i:i+3])
                    if len(phrase) > 10:
                        self.dictionary["common_phrases"][phrase] = {
                            "usage_count": self.dictionary["common_phrases"].get(phrase, {}).get("usage_count", 0) + 1,
                            "category": "learned_from_corpus"
                        }
                
                # Learn individual words
                for word in words:
                    word_clean = word.strip('.,!?;:"\'').lower()
                    if len(word_clean) > 2:
                        if word_clean not in self.dictionary["word_corrections"]:
                            self.dictionary["word_corrections"][word_clean] = {
                                "written_form": word_clean,
                                "spoken_form": word_clean,  # Will be refined with audio
                                "frequency": 0,
                                "context": "corpus_learning",
                                "source": "text"
                            }
                        else:
                            # Increment frequency
                            if isinstance(self.dictionary["word_corrections"][word_clean], dict):
                                self.dictionary["word_corrections"][word_clean]["frequency"] = \
                                    self.dictionary["word_corrections"][word_clean].get("frequency", 0) + 1
        
        self.logger.info(f"📚 Learned {len(lines)} lines from corpus")
    
    def get_correction(self, written_text: str) -> str:
        """Get corrected pronunciation for written text"""
        corrected = written_text
        
        # Apply word corrections
        for wrong, correct in self.dictionary["word_corrections"].items():
            if isinstance(correct, dict):
                correct = correct.get("spoken_form", wrong)
            corrected = corrected.replace(wrong, correct)
        
        return corrected
    
    def export_for_tts(self) -> dict:
        """Export dictionary in TTS-compatible format"""
        tts_format = {
            "language": self.language,
            "corrections": {}
        }
        
        for word, data in self.dictionary["word_corrections"].items():
            if isinstance(data, dict):
                spoken = data.get("spoken_form", word)
                tts_format["corrections"][word] = spoken
            else:
                tts_format["corrections"][word] = data
        
        return tts_format


# Example usage
if __name__ == "__main__":
    # Create Haryanvi learner
    learner = LanguageLearner("haryanvi")
    
    # Sample corpus (can be loaded from files)
    haryanvi_corpus = """
    Bhai sun, mhare gaon mein ek kisan tha
    Wo subah savere uthta aur khet me jaata
    Hal uthaata, bailo ko jotta
    Din bhar mehnat karta
    Shaam ko ghar aake aaram karta
    """
    
    # Learn from corpus
    learner.learn_from_corpus(haryanvi_corpus)
    
    # Save dictionary
    learner.save_dictionary()
    
    # Test correction
    test_text = "mhara bhai khet mein kaam karta"
    corrected = learner.get_correction(test_text)
    print(f"\nOriginal: {test_text}")
    print(f"Corrected: {corrected}")
