"""
SOUL EXTRACTOR ENGINE - Emotional Core of Video
Extracts the deeper meaning, emotion, and message behind any topic
"""
import json
from pathlib import Path
from loguru import logger
from config import Config


class SoulExtractor:
    """Extract emotional and thematic core of video content"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.api_key = self.config.DEEPSEEK_API_KEY
        self.cache_dir = self.config.CACHE_PATH / "soul_extractions"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Emotion taxonomy for Indian context
        self.emotion_taxonomy = {
            "primary": [
                "joy", "sadness", "anger", "fear", "surprise", "disgust",
                "love", "pride", "gratitude", "hope", "determination", "nostalgia"
            ],
            "secondary": [
                "frustration", "worry", "excitement", "contentment",
                "disappointment", "relief", "confusion", "clarity",
                "inspiration", "motivation", "empathy", "compassion"
            ],
            "cultural_specific": [
                "vatsalya_bhavna",  # parental love
                "shraddha",         # respect/reverence
                "tyaag",           # sacrifice
                "sangharsh",       # struggle
                "jeet",            # victory
                "haar",            # defeat
                "samadhan",        # contentment/peace
                "krodh",           # righteous anger
                "karuna",          # compassion
                "bhakti",          # devotion
                "desh_bhakti",     # patriotism
                "parivaar_prem"    # family love
            ]
        }
        
        # Viewer feeling targets
        self.feeling_targets = {
            "inspirational": "viewer feels motivated to take action",
            "emotional": "viewer connects deeply, may cry or feel moved",
            "educational": "viewer understands clearly, feels informed",
            "entertaining": "viewer enjoys, laughs, forgets worries",
            "awareness": "viewer becomes conscious of issue, thinks deeply",
            "nostalgic": "viewer remembers past, feels warm/sad",
            "uplifting": "viewer feels happy, hopeful, positive"
        }
    
    async def extract_soul(self, topic: str, language: str = "hindi", style: str = "educational") -> dict:
        """
        Extract the soul/emotional core of the video
        
        Args:
            topic: Video topic/title
            language: hindi/haryanvi/bhojpuri
            style: educational/story/news/vlog
            
        Returns:
            Dictionary containing:
            - core_emotion: Primary emotional driver
            - viewer_feeling_target: What viewer should feel
            - powerful_moment: Most impactful scene idea
            - real_life_connection: How it relates to audience
            - underlying_message: Deeper meaning
        """
        self.logger.info(f"🔮 Extracting soul for: {topic}")
        
        # Check cache
        cache_key = f"{topic}_{language}_{style}"
        cache_hash = self._generate_cache_hash(cache_key)
        cached_result = self._load_from_cache(cache_hash)
        
        if cached_result:
            self.logger.info(f"💾 Soul loaded from cache: {cache_hash[:8]}")
            return cached_result
        
        # Use AI to extract soul
        try:
            soul_data = await self._call_deepseek_for_soul(topic, language, style)
            
            # Validate and enhance
            soul_data = self._validate_and_enhance(soul_data, topic, language)
            
            # Save to cache
            self._save_to_cache(cache_hash, soul_data)
            
            self.logger.success(f"✅ Soul extracted: {soul_data.get('core_emotion', 'unknown')}")
            return soul_data
            
        except Exception as e:
            self.logger.error(f"❌ Soul extraction failed: {e}")
            # Return fallback soul
            return self._create_fallback_soul(topic, language, style)
    
    async def _call_deepseek_for_soul(self, topic: str, language: str, style: str) -> dict:
        """Call DeepSeek API to extract emotional core"""
        
        prompt = f"""
You are a Master Storyteller and Emotional Intelligence Expert specializing in Indian content.

TOPIC: "{topic}"
LANGUAGE: {language}
STYLE: {style}

TASK: Extract the SOUL of this video by answering these questions deeply:

1. CORE EMOTION (What is the primary emotional driver?)
   - Choose from: joy, sadness, anger, fear, surprise, love, pride, gratitude, hope, determination, nostalgia
   - Add cultural emotions if relevant: vatsalya_bhavna (parental love), shraddha (respect), tyaag (sacrifice), sangharsh (struggle), jeet (victory), haar (defeat), samadhan (contentment), karuna (compassion), bhakti (devotion), desh_bhakti (patriotism), parivaar_prem (family love)
   - Explain WHY this emotion is central

2. VIEWER FEELING TARGET (After watching, what should the viewer FEEL?)
   - Be specific: "Inspired to protect environment" not just "inspired"
   - Include both intellectual and emotional takeaway
   - Example: "Viewer feels proud of Indian heritage AND worried about climate change"

3. MOST POWERFUL MOMENT (Which single moment will have maximum emotional impact?)
   - Describe the exact scene
   - What happens?
   - What is said/shown?
   - Why is it powerful?
   - Example: "When papa silently hands beti the old photo album, his hands trembling slightly"

4. REAL-LIFE CONNECTION (How does this connect to average Indian viewer's life?)
   - Specific situations they face
   - Emotions they've felt
   - Relationships that mirror this
   - Example: "Every Indian daughter has seen her father sacrifice for her education"

5. UNDERLYING MESSAGE (What is the deeper meaning beyond surface topic?)
   - Life lesson
   - Universal truth
   - Cultural value being transmitted
   - Example: "Love isn't spoken, it's shown through daily sacrifices"

6. SILENT SUBTEXT (What is NOT being said but everyone understands?)
   - Unspoken family dynamics
   - Cultural assumptions
   - Shared experiences
   - Example: "Indian parents show love through service, not words"

Respond in JSON format:
{{
  "core_emotion": {{
    "primary": "emotion_name",
    "secondary": "supporting_emotion",
    "intensity": 0.8,
    "explanation": "why this emotion drives the video"
  }},
  "viewer_feeling_target": "detailed description",
  "powerful_moment": {{
    "description": "scene description",
    "timestamp_estimate": "when it might occur (early/middle/late)",
    "impact_reason": "why it hits hard"
  }},
  "real_life_connection": {{
    "situation": "specific scenario",
    "emotion": "what they've felt",
    "relationship": "which relationships mirror this"
  }},
  "underlying_message": "deep meaning",
  "silent_subtext": "unspoken understanding"
}}
"""
        
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are an expert Indian content creator and emotional storyteller."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        soul_text = data["choices"][0]["message"]["content"]
                        
                        # Parse JSON
                        try:
                            # Extract JSON from response
                            soul_json = self._extract_json_from_response(soul_text)
                            return soul_json
                        except Exception as parse_error:
                            self.logger.warning(f"JSON parse error: {parse_error}")
                            # Return structured fallback
                            return self._create_structured_fallback(soul_text, topic)
                    else:
                        error_text = await response.text()
                        raise Exception(f"DeepSeek API error: {response.status} - {error_text}")
                        
        except Exception as e:
            self.logger.error(f"API call failed: {e}")
            raise
    
    def _extract_json_from_response(self, text: str) -> dict:
        """Extract JSON from AI response text"""
        import re
        import json
        
        # Try to find JSON block
        json_pattern = r'\{[\s\S]*\}'
        match = re.search(json_pattern, text)
        
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except:
                pass
        
        # Fallback: create structured data from text
        return {
            "core_emotion": {
                "primary": "determination",
                "secondary": "hope",
                "intensity": 0.7,
                "explanation": text[:200]
            },
            "viewer_feeling_target": "Viewer understands the topic deeply and feels motivated",
            "powerful_moment": {
                "description": "Key revelation or emotional moment",
                "timestamp_estimate": "middle",
                "impact_reason": "Connects personal story to universal truth"
            },
            "real_life_connection": {
                "situation": "Common experience in Indian context",
                "emotion": "Relatable emotion",
                "relationship": "Family or social connection"
            },
            "underlying_message": text[:200],
            "silent_subtext": "Cultural understanding shared by Indian audience"
        }
    
    def _validate_and_enhance(self, soul_data: dict, topic: str, language: str) -> dict:
        """Validate extracted soul and enhance for Indian context"""
        
        # Ensure all required fields exist
        required_fields = [
            "core_emotion", "viewer_feeling_target", "powerful_moment",
            "real_life_connection", "underlying_message", "silent_subtext"
        ]
        
        for field in required_fields:
            if field not in soul_data:
                self.logger.warning(f"Missing field: {field}, adding fallback")
                soul_data[field] = self._get_fallback_for_field(field)
        
        # Validate core emotion
        if "core_emotion" in soul_data:
            emotion = soul_data["core_emotion"]
            if isinstance(emotion, dict):
                if "primary" not in emotion:
                    emotion["primary"] = "neutral"
                if "intensity" not in emotion:
                    emotion["intensity"] = 0.7
            else:
                soul_data["core_emotion"] = {
                    "primary": str(emotion),
                    "secondary": "neutral",
                    "intensity": 0.7,
                    "explanation": "Auto-generated from topic"
                }
        
        # Enhance for Indian context
        soul_data = self._add_indian_context(soul_data, topic, language)
        
        return soul_data
    
    def _add_indian_context(self, soul_data: dict, topic: str, language: str) -> dict:
        """Add Indian cultural context to soul extraction"""
        
        topic_lower = topic.lower()
        
        # Detect cultural themes
        cultural_themes = []
        
        if any(word in topic_lower for word in ["papa", "father", "pitaji", "beti", "daughter"]):
            cultural_themes.append("parent_child_relationship")
            cultural_themes.append("indian_family_dynamics")
        
        if any(word in topic_lower for word in ["sacrifice", "tyaag", "kurbaani"]):
            cultural_themes.append("sacrifice_theme")
        
        if any(word in topic_lower for word in ["education", "padhai", "school", "college"]):
            cultural_themes.append("education_pressure")
            cultural_themes.append("indian_parent_expectations")
        
        if any(word in topic_lower for word in ["marriage", "shaadi", "wedding"]):
            cultural_themes.append("marriage_expectations")
            cultural_themes.append("indian_wedding_culture")
        
        if any(word in topic_lower for word in ["festival", "tyohar", "diwali", "holi", "eid"]):
            cultural_themes.append("festival_traditions")
            cultural_themes.append("indian_celebrations")
        
        # Add detected themes
        if cultural_themes:
            soul_data["cultural_themes"] = cultural_themes
            self.logger.debug(f"Detected cultural themes: {cultural_themes}")
        
        # Add language-specific nuances
        if language == "haryanvi":
            soul_data["cultural_nuances"] = {
                "directness": "high",
                "emotion_display": "open_hearted",
                "humor_style": "dry_witty",
                "values": ["family_honor", "hard_work", "simplicity"]
            }
        elif language == "bhojpuri":
            soul_data["cultural_nuances"] = {
                "expressiveness": "high",
                "music_integration": "natural",
                "community_focus": "strong",
                "values": ["celebration", "resilience", "togetherness"]
            }
        else:  # Hindi
            soul_data["cultural_nuances"] = {
                "formality": "medium",
                "metaphor_usage": "moderate",
                "values": ["balance", "wisdom", "inclusivity"]
            }
        
        return soul_data
    
    def _create_fallback_soul(self, topic: str, language: str, style: str) -> dict:
        """Create fallback soul when AI extraction fails"""
        
        # Topic-based emotion mapping
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["happy", "joy", "celebration", "utsav"]):
            core_emotion = "joy"
        elif any(word in topic_lower for word in ["sad", "loss", "death", "mourn"]):
            core_emotion = "sadness"
        elif any(word in topic_lower for word in ["angry", "fight", "protest", "injustice"]):
            core_emotion = "anger"
        elif any(word in topic_lower for word in ["scary", "horror", "danger", "threat"]):
            core_emotion = "fear"
        elif any(word in topic_lower for word in ["love", "romance", "relationship"]):
            core_emotion = "love"
        elif any(word in topic_lower for word in ["success", "achievement", "win", "jeet"]):
            core_emotion = "pride"
        elif any(word in topic_lower for word in ["thank", "grateful", "shukriya", "dhanyavaad"]):
            core_emotion = "gratitude"
        elif any(word in topic_lower for word in ["hope", "future", "better", "improve"]):
            core_emotion = "hope"
        elif any(word in topic_lower for word in ["struggle", "fight", "mehnat", "sangharsh"]):
            core_emotion = "determination"
        elif any(word in topic_lower for word in ["memory", "past", "nostalgia", "yaad"]):
            core_emotion = "nostalgia"
        else:
            core_emotion = "curiosity"
        
        return {
            "core_emotion": {
                "primary": core_emotion,
                "secondary": "curiosity",
                "intensity": 0.7,
                "explanation": "Derived from topic keywords"
            },
            "viewer_feeling_target": f"Viewer gains understanding of '{topic}' and feels engaged",
            "powerful_moment": {
                "description": "Key insight or revelation about the topic",
                "timestamp_estimate": "middle",
                "impact_reason": "Provides new perspective"
            },
            "real_life_connection": {
                "situation": "Topic relevance in daily life",
                "emotion": "Curiosity and interest",
                "relationship": "Personal or social impact"
            },
            "underlying_message": f"Understanding '{topic}' enriches life",
            "silent_subtext": "Shared human experience around this topic",
            "fallback_used": True
        }
    
    def _create_structured_fallback(self, ai_text: str, topic: str) -> dict:
        """Create structured soul data from unstructured AI text"""
        
        base_soul = self._create_fallback_soul(topic, "hindi", "educational")
        
        # Try to extract insights from AI text
        if len(ai_text) > 100:
            base_soul["underlying_message"] = ai_text[:300]
            base_soul["viewer_feeling_target"] = f"Viewer understands: {ai_text[:100]}"
        
        return base_soul
    
    def _get_fallback_for_field(self, field: str) -> any:
        """Get fallback value for missing field"""
        
        fallbacks = {
            "core_emotion": {
                "primary": "neutral",
                "secondary": "curiosity",
                "intensity": 0.5,
                "explanation": "Default emotional state"
            },
            "viewer_feeling_target": "Viewer feels informed and engaged",
            "powerful_moment": {
                "description": "Key moment of understanding",
                "timestamp_estimate": "middle",
                "impact_reason": "Central insight delivery"
            },
            "real_life_connection": {
                "situation": "Relatable scenario",
                "emotion": "Interest and curiosity",
                "relationship": "Personal relevance"
            },
            "underlying_message": "Knowledge empowers and transforms",
            "silent_subtext": "Universal human experience"
        }
        
        return fallbacks.get(field, None)
    
    def _generate_cache_hash(self, key: str) -> str:
        """Generate MD5 hash for caching"""
        import hashlib
        return hashlib.md5(key.encode()).hexdigest()
    
    def _load_from_cache(self, cache_hash: str) -> dict:
        """Load soul extraction from cache"""
        cache_file = self.cache_dir / f"{cache_hash}.json"
        
        if cache_file.exists():
            import json
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def _save_to_cache(self, cache_hash: str, soul_data: dict):
        """Save soul extraction to cache"""
        import json
        cache_file = self.cache_dir / f"{cache_hash}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(soul_data, f, indent=2, ensure_ascii=False)
        
        self.logger.debug(f"💾 Soul cached: {cache_hash[:8]}")
    
    async def get_emotion_intensity_curve(self, soul_data: dict, duration_minutes: int) -> list:
        """
        Generate emotion intensity curve over time
        
        Returns list of (timestamp, intensity) tuples showing how emotion should flow
        """
        
        base_intensity = soul_data.get("core_emotion", {}).get("intensity", 0.7)
        
        # Create dramatic arc
        curve = []
        total_seconds = duration_minutes * 60
        
        # Opening (0-10%): Establish baseline
        curve.append((0, base_intensity * 0.8))
        
        # Build-up (10-40%): Gradual increase
        curve.append((total_seconds * 0.1, base_intensity * 0.9))
        curve.append((total_seconds * 0.4, base_intensity))
        
        # Peak (40-60%): Maximum intensity at powerful moment
        peak_time = total_seconds * 0.5
        curve.append((peak_time, min(1.0, base_intensity * 1.2)))
        
        # Resolution (60-90%): Gradual decrease
        curve.append((total_seconds * 0.6, base_intensity))
        curve.append((total_seconds * 0.9, base_intensity * 0.7))
        
        # Ending (90-100%): Soft conclusion
        curve.append((total_seconds, base_intensity * 0.6))
        
        return curve


# Test function
async def test_soul_extractor():
    """Test the Soul Extractor"""
    extractor = SoulExtractor()
    
    test_topics = [
        ("Climate Change", "hindi", "educational"),
        ("Papa aur Beti ka Rishta", "hindi", "story"),
        ("Farmers of Haryana", "haryanvi", "documentary"),
        ("My First Job Interview", "hindi", "vlog")
    ]
    
    for topic, lang, style in test_topics:
        print(f"\n{'='*60}")
        print(f"Testing: {topic} ({lang}, {style})")
        print('='*60)
        
        soul = await extractor.extract_soul(topic, lang, style)
        
        print(f"Core Emotion: {soul['core_emotion']['primary']}")
        print(f"Intensity: {soul['core_emotion']['intensity']}")
        print(f"Viewer Should Feel: {soul['viewer_feeling_target'][:100]}...")
        print(f"Powerful Moment: {soul['powerful_moment']['description'][:80]}...")
    
    print("\n✅ Soul Extractor testing complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_soul_extractor())
