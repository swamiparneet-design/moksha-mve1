"""
PAUSE INJECTION ENGINE - Natural Speech Rhythm
Adds strategic pauses for emotional impact and natural breathing
"""
from loguru import logger


class PauseInjector:
    """Professional pause injection for natural speech rhythm"""
    
    def __init__(self):
        self.logger = logger
        
        # Pause types with durations
        self.pause_types = {
            "MICRO_PAUSE": {
                "duration_ms": 300,
                "purpose": "natural_breath",
                "when_to_use": ["between_clauses", "after_commas", "before_conjunctions"]
            },
            "SHORT_PAUSE": {
                "duration_ms": 600,
                "purpose": "thinking_moment",
                "when_to_use": ["before_important_point", "after_question", "transition"]
            },
            "MEDIUM_PAUSE": {
                "duration_ms": 1200,
                "purpose": "emotional_weight",
                "when_to_use": ["before_revelation", "after_shocking_news", "emphasis"]
            },
            "LONG_PAUSE": {
                "duration_ms": 2000,
                "purpose": "dramatic_impact",
                "when_to_use": ["major_revelation", "life_changing_moment", "climax"]
            },
            "EXTREME_PAUSE": {
                "duration_ms": 4000,
                "purpose": "maximum_dramatic_silence",
                "when_to_use": ["most_powerful_moment", "unbearable_emotion", "final_words"]
            }
        }
        
        # Emotion-based pause preferences
        self.emotion_pause_map = {
            "neutral": ["MICRO_PAUSE", "SHORT_PAUSE"],
            "joy": ["MICRO_PAUSE", "SHORT_PAUSE", "MEDIUM_PAUSE"],
            "sadness": ["MEDIUM_PAUSE", "LONG_PAUSE", "EXTREME_PAUSE"],
            "anger": ["SHORT_PAUSE", "MEDIUM_PAUSE"],
            "fear": ["MEDIUM_PAUSE", "LONG_PAUSE", "MICRO_PAUSE"],
            "surprise": ["LONG_PAUSE", "MEDIUM_PAUSE"],
            "love": ["MEDIUM_PAUSE", "LONG_PAUSE"],
            "pride": ["SHORT_PAUSE", "MEDIUM_PAUSE"],
            "gratitude": ["MEDIUM_PAUSE", "LONG_PAUSE"],
            "hope": ["SHORT_PAUSE", "MEDIUM_PAUSE"],
            "determination": ["SHORT_PAUSE", "MEDIUM_PAUSE"],
            "nostalgia": ["LONG_PAUSE", "MEDIUM_PAUSE", "EXTREME_PAUSE"],
            "sangharsh": ["MEDIUM_PAUSE", "LONG_PAUSE"],
            "tyaag": ["LONG_PAUSE", "EXTREME_PAUSE"],
            "karuna": ["EXTREME_PAUSE", "LONG_PAUSE"]
        }
        
        # Linguistic pause triggers (Hindi/Haryanvi)
        self.pause_triggers_hi = {
            "comma": {"pause": "MICRO_PAUSE", "markers": [",", "और", "लेकिन", "पर"]},
            "question": {"pause": "SHORT_PAUSE", "markers": ["?", "क्या", "क्यों", "कैसे"]},
            "emphasis": {"pause": "MEDIUM_PAUSE", "markers": ["बिल्कुल", "सच में", "वाकई"]},
            "revelation": {"pause": "LONG_PAUSE", "markers": ["असली सच", "पता चला", "जान गया"]},
            "emotional_peak": {"pause": "EXTREME_PAUSE", "markers": ["मर गया", "प्यार", "त्याग"]}
        }
    
    def inject_pauses(self, text: str, emotion: str = "neutral", language: str = "hindi") -> str:
        """
        Inject pause markers into text for natural speech rhythm
        
        Args:
            text: Original dialogue text
            emotion: Scene emotion
            language: hindi/haryanvi/bhojpuri
            
        Returns:
            Text with embedded pause markers
        """
        self.logger.debug(f"💨 Injecting pauses for emotion: {emotion}")
        
        # Get appropriate pause types for this emotion
        preferred_pauses = self.emotion_pause_map.get(emotion, self.emotion_pause_map["neutral"])
        
        # Analyze text structure
        sentences = self._split_into_sentences(text)
        
        processed_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Add pause after each sentence based on position and emotion
            processed_sentence = self._process_sentence(sentence, preferred_pauses, i, len(sentences))
            processed_sentences.append(processed_sentence)
        
        result = " ".join(processed_sentences)
        
        self.logger.debug(f"✅ Pauses injected: {result[:100]}...")
        return result
    
    def _split_into_sentences(self, text: str) -> list:
        """Split text into sentences considering Hindi punctuation"""
        
        # Common Hindi sentence enders
        enders = ["।", ".", "?", "!"]
        
        sentences = []
        current = ""
        
        for char in text:
            current += char
            if char in enders:
                sentences.append(current.strip())
                current = ""
        
        if current:
            sentences.append(current.strip())
        
        return sentences
    
    def _process_sentence(self, sentence: str, preferred_pauses: list, index: int, total: int) -> str:
        """Add pauses to a single sentence"""
        
        # Determine pause type based on position
        if index == total - 1:
            # Last sentence - use longest pause
            pause_type = preferred_pauses[-1] if len(preferred_pauses) > 1 else preferred_pauses[0]
        elif index == 0:
            # First sentence - medium pause
            pause_type = preferred_pauses[0]
        else:
            # Middle - vary the pauses
            pause_type = preferred_pauses[index % len(preferred_pauses)]
        
        # Get pause duration
        pause_data = self.pause_types.get(pause_type, self.pause_types["MICRO_PAUSE"])
        pause_ms = pause_data["duration_ms"]
        
        # Add pause marker
        paused_sentence = f"{sentence} [PAUSE: {pause_ms}ms]"
        
        # Also add micro-pauses within sentence at commas/conjunctions
        paused_sentence = self._add_internal_pauses(paused_sentence)
        
        return paused_sentence
    
    def _add_internal_pauses(self, sentence: str) -> str:
        """Add micro-pauses within sentence at natural break points"""
        
        # Replace common pause points
        replacements = [
            (", ", ", [PAUSE: 300ms] "),
            ("और ", "और [PAUSE: 300ms] "),
            ("लेकिन ", "लेकिन [PAUSE: 300ms] "),
            ("पर ", "पर [PAUSE: 300ms] "),
            ("कि ", "कि [PAUSE: 300ms] ")
        ]
        
        result = sentence
        for old, new in replacements:
            result = result.replace(old, new)
        
        return result
    
    def create_breath_markers(self, text: str, speaking_rate: float = 1.0) -> str:
        """
        Add subtle breath sound markers for ultra-realism
        
        Args:
            text: Dialogue text
            speaking_rate: 0.5-2.0 (1.0 = normal)
            
        Returns:
            Text with breath markers
        """
        
        # Calculate breath frequency based on speaking rate
        breath_interval_seconds = max(3, int(5 / speaking_rate))
        
        words = text.split()
        result_words = []
        
        for i, word in enumerate(words):
            result_words.append(word)
            
            # Add breath marker every N words
            if (i + 1) % breath_interval_seconds == 0:
                result_words.append("[BREATH: inhale_light]")
        
        return " ".join(result_words)
    
    def generate_rhythm_score(self, text: str, emotion: str) -> dict:
        """
        Generate comprehensive rhythm score showing all pauses and breaths
        
        Returns:
            Dictionary with timing information
        """
        
        # Process text with pauses
        text_with_pauses = self.inject_pauses(text, emotion)
        
        # Calculate total duration
        base_duration = len(text.split()) * 0.4  # ~400ms per word average
        pause_duration = text_with_pauses.count("[PAUSE:") * 0.8  # Average 800ms per pause
        
        total_duration = base_duration + pause_duration
        
        # Create rhythm map
        rhythm_map = []
        current_time = 0
        
        # Simple parsing of pause markers
        segments = text_with_pauses.split("[PAUSE:")
        
        for segment in segments:
            if "]" in segment:
                parts = segment.split("]")
                text_part = parts[0].strip()
                pause_part = parts[1].split("ms")[0].strip() if len(parts) > 1 else "300"
                
                if text_part:
                    rhythm_map.append({
                        "type": "speech",
                        "start_time": current_time,
                        "content": text_part[:50]
                    })
                    current_time += len(text_part.split()) * 0.4
                
                if pause_part.isdigit():
                    pause_ms = int(pause_part)
                    rhythm_map.append({
                        "type": "pause",
                        "start_time": current_time,
                        "duration_ms": pause_ms
                    })
                    current_time += pause_ms / 1000.0
        
        return {
            "total_duration_sec": total_duration,
            "pause_count": text_with_pauses.count("[PAUSE:"),
            "rhythm_map": rhythm_map,
            "text_with_markers": text_with_pauses
        }


# Test function
def test_pause_injector():
    """Test pause injection engine"""
    injector = PauseInjector()
    
    test_cases = [
        ("यह एक महत्वपूर्ण विषय है। हमें इस पर ध्यान देना चाहिए।", "neutral"),
        ("मुझे तुमसे प्यार है। लेकिन हम कभी मिल नहीं सकते।", "sadness"),
        ("तुमने ऐसा क्यों किया? मैं बहुत दुखी हूं।", "anger"),
        ("आज का दिन बहुत खास है। हम जीत गए!", "joy"),
        ("उसने सब कुछ त्याग दिया। सिर्फ मेरे लिए।", "tyaag")
    ]
    
    print("\n💨 Testing Pause Injector")
    print("="*70)
    
    for text, emotion in test_cases:
        print(f"\nEmotion: {emotion.upper()}")
        print(f"Original: {text}")
        
        result = injector.inject_pauses(text, emotion)
        print(f"With Pauses: {result}")
        
        # Get rhythm score
        rhythm = injector.generate_rhythm_score(text, emotion)
        print(f"Duration: {rhythm['total_duration_sec']:.1f}s, Pauses: {rhythm['pause_count']}")
    
    print("\n✅ Pause Injector test complete!")


if __name__ == "__main__":
    test_pause_injector()
