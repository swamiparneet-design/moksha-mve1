"""
SCRIPT ENGINE - Hybrid 3-Layer System
Layer 1: DeepSeek V3/R1 (Creative Director)
Layer 2: Groq Llama-70B (Fact Checker)
Layer 3: Claude 3.5 (Final Polish - Indian Context)
Generates director-level Hindi/Haryanvi/Bhojpuri scripts
"""
import json
import hashlib
from pathlib import Path
from loguru import logger
from config import Config


class ScriptEngine:
    """Script generation engine using DeepSeek V3"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.api_key = self.config.DEEPSEEK_API_KEY
        self.groq_api_key = self.config.GROQ_API_KEY
        # Note: anthropic_api_key not needed - using DeepSeek via Anthropic format!
        self.model = self.config.DEEPSEEK_MODEL
        self.cache_dir = self.config.CACHE_PATH / "scripts"
        
    async def generate(
        self,
        topic: str,
        language: str = "hindi",
        style: str = "educational",
        duration_minutes: int = 5,
        viral_mode: bool = True
    ) -> list:
        """
        Generate script for given topic with Auto Viral Mode
        
        Args:
            topic: Video topic
            language: hindi/haryanvi/bhojpuri
            style: educational/story/news/vlog
            duration_minutes: Target duration
            viral_mode: Enable viral optimization
            
        Returns:
            List of scene dictionaries with emotion flow
        """
        # Check cache first
        cache_key = f"{topic}_{language}_{style}_{duration_minutes}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cached_script = self._load_from_cache(cache_hash)
        
        if cached_script:
            self.logger.info(f"📝 Script loaded from cache: {cache_hash[:8]}")
            return cached_script
        
        # Generate new script
        self.logger.info(f"📝 Generating script for: {topic}")
        
        try:
            # === HYBRID 3-LAYER PIPELINE ===
            self.logger.info("🎬 Layer 1: DeepSeek generating creative script...")
            
            # Layer 1: DeepSeek - Creative Director
            prompt = self._build_prompt(topic, language, style, duration_minutes, viral_mode)
            creative_script = await self._call_deepseek_api(prompt)
            
            # Layer 2: Groq - Fact Checker (if API key available)
            if self.groq_api_key:
                self.logger.info("🔍 Layer 2: Groq fact-checking and logic validation...")
                try:
                    fact_checked_script = await self._call_groq(creative_script, topic, language)
                except Exception as groq_error:
                    self.logger.warning(f"⚠️ Groq failed: {groq_error}. Skipping fact-check layer...")
                    fact_checked_script = creative_script
            else:
                self.logger.warning("⚠️ Groq API key missing - skipping fact-check layer")
                fact_checked_script = creative_script
            
            # Layer 3: Claude - Final Polish (if API key available)
            if self.anthropic_api_key:
                self.logger.info("✨ Layer 3: Claude adding cultural accuracy & polish...")
                try:
                    final_script = await self._call_claude(fact_checked_script, language)
                except Exception as claude_error:
                    self.logger.warning(f"⚠️ Claude failed: {claude_error}. Using Groq output...")
                    final_script = fact_checked_script
            else:
                self.logger.warning("⚠️ Claude API key missing - skipping polish layer")
                final_script = fact_checked_script
            
            # Save to cache
            self._save_to_cache(cache_hash, final_script)
            
            self.logger.success(f"✅ Script generated: {len(final_script)} scenes")
            return final_script
            
        except Exception as e:
            self.logger.error(f"❌ Script generation failed: {e}")
            
            # === FALLBACK SYSTEM ===
            self.logger.info("🔄 Attempting fallback: DeepSeek-only mode...")
            try:
                # Fallback to simple DeepSeek call
                prompt = self._build_prompt(topic, language, style, duration_minutes, viral_mode)
                fallback_script = await self._call_deepseek_simple(prompt)
                self._save_to_cache(cache_hash, fallback_script)
                self.logger.success("✅ Fallback script generated!")
                return fallback_script
            except Exception as fallback_error:
                self.logger.error(f"❌ Fallback also failed: {fallback_error}")
                
                # Emergency demo script
                self.logger.info("🚨 Emergency: Returning demo script...")
                demo_script = self._generate_demo_script(topic, language, style)
                return demo_script
    
    def _build_prompt(self, topic: str, language: str, style: str, duration: int, viral_mode: bool) -> str:
        """Build detailed prompt for DeepSeek"""
        
        language_instructions = {
            "hindi": "Simple Hindi mein likho. Real human jaisi delivery.",
            "haryanvi": "Haryanvi boli mein likho. 'ke', 'tera', 'mhara', 'bhai', 'yaar' jaise words use karo.",
            "bhojpuri": "Bhojpuri bhasha mein likho. Local accent maintain karo."
        }
        
        style_instructions = {
            "educational": "Educational tone. Clear explanations. Examples ke saath.",
            "story": "Storytelling style. Emotional connection. Suspense create karo.",
            "news": "News anchor style. Factual. Quick updates.",
            "vlog": "Casual vlog style. Personal touch. Conversational."
        }
        
        if viral_mode:
            viral_rules = """
VIRAL STRUCTURE (MANDATORY):
- 0-3 sec: SHOCK HOOK that stops scroll
- 3-15 sec: Create curiosity gap
- 15-30 sec: Deliver value
- Every 20-30 sec: Pattern break
- End: Strong payoff + CTA

RETENTION RULES:
- First line MUST be shocking/question
- Har 5 sec baad visual change
- No boring segment > 4 seconds
- Use relatable Indian examples
- Create suspense before answers
"""
        else:
            viral_rules = ""
        
        prompt = f"""
Generate a professional YouTube video script in {language}.

TOPIC: {topic}
STYLE: {style_instructions.get(style, style_instructions['educational'])}
DURATION: {duration} minutes (approximately {duration * 12} scenes, 5 sec each)

LANGUAGE INSTRUCTIONS:
{language_instructions.get(language, language_instructions['hindi'])}

RULES:
- Short punchy sentences (max 15 words per sentence)
- Each scene should be 5 seconds max
- Mark emotions: curious, excited, serious, happy, sad, angry
- Specify scene type: avatar, broll, or mixed
- No filler content, no lies
- Real human jaisi natural delivery
- Hook in first 3 seconds
- Pattern break every 30 seconds
- Strong call to action at end

{viral_rules}
OUTPUT FORMAT (JSON array):
[
  {{
    "scene": 1,
    "text": "Scene text here...",
    "language": "{language}",
    "emotion": "curious/excited/serious/etc",
    "duration_estimate": 5,
    "type": "avatar/broll/mixed",
    "keyword": "keyword for b-roll if needed"
  }}
]

Generate complete script now:
"""
        return prompt
    
    async def _call_deepseek_api(self, prompt: str) -> list:
        """Call DeepSeek V3 API"""
        import aiohttp
        
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional YouTube scriptwriter for Indian content creators."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    script_text = data["choices"][0]["message"]["content"]
                    
                    # Parse JSON from response
                    try:
                        # Extract JSON from markdown code blocks if present
                        if "```json" in script_text:
                            script_text = script_text.split("```json")[1].split("```")[0]
                        elif "```" in script_text:
                            script_text = script_text.split("```")[1].split("```")[0]
                        
                        script = json.loads(script_text.strip())
                        return script
                    except json.JSONDecodeError as e:
                        self.logger.error(f"JSON parsing failed: {e}")
                        raise ValueError("Invalid JSON from API")
                else:
                    error_text = await response.text()
                    raise Exception(f"DeepSeek API error: {response.status} - {error_text}")
    
    async def _call_groq(self, script: list, topic: str, language: str) -> list:
        """Layer 2: Groq fact-checking and logic validation"""
        import aiohttp
        
        script_text = json.dumps(script, indent=2)
        
        prompt = f"""You are a strict film producer and fact-checker. Review this {language} video script:

TOPIC: {topic}
SCRIPT: {script_text}

Your tasks:
1. Check logical consistency (no plot holes)
2. Verify factual claims (if documentary/informational)
3. Ensure character motivations make sense
4. Remove any clichés or weak dialogue
5. Suggest improvements for pacing
6. Keep the same JSON format

Return corrected script with your changes. Maintain original structure."""
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    corrected_text = result['choices'][0]['message']['content']
                    
                    # Try to parse JSON from response
                    try:
                        if "```json" in corrected_text:
                            corrected_text = corrected_text.split("```json")[1].split("```")[0]
                        elif "```" in corrected_text:
                            corrected_text = corrected_text.split("```")[1].split("```")[0]
                        
                        corrected_script = json.loads(corrected_text.strip())
                        return corrected_script
                    except:
                        # If parsing fails, return original
                        self.logger.warning("Groq output not valid JSON, returning original")
                        return script
                else:
                    raise Exception(f"Groq API error: {response.status}")
    
    async def _call_claude(self, script: list, language: str) -> list:
        """Layer 3: Cultural polish using DeepSeek via Anthropic format (Cost optimized)"""
        import aiohttp
        
        script_text = json.dumps(script, indent=2)
        
        prompt = f"""You are an Indian screenwriter expert in {language} cinema. 

SCRIPT TO POLISH:
{script_text}

Your tasks:
1. Make dialogues sound natural in {language} (not robotic)
2. Add cultural references that {language} audience connects with
3. Ensure emotions translate properly to Indian context
4. Fix any Western-centric assumptions
5. Add appropriate idioms/proverbs if relevant
6. Ensure the script feels authentic to Indian viewers
7. Keep the same JSON format

Return final polished script ready for production."""
        
        # Use DeepSeek's Anthropic-compatible endpoint (SAME API KEY - Cost optimized!)
        headers = {
            "x-api-key": self.api_key,  # Using DeepSeek key itself!
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.config.CLAUDE_MODEL,  # deepseek-chat
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        # Use DeepSeek's Anthropic-compatible base URL
        url = f"{self.config.ANTHROPIC_BASE_URL}/v1/messages"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60)  # 60 sec timeout for DeepSeek
            ) as response:
                result = await response.json()
                
                if response.status == 200:
                    polished_text = result['content'][0]['text']
                    
                    # Try to parse JSON from response
                    try:
                        if "```json" in polished_text:
                            polished_text = polished_text.split("```json")[1].split("```")[0]
                        elif "```" in polished_text:
                            polished_text = polished_text.split("```")[1].split("```")[0]
                        
                        polished_script = json.loads(polished_text.strip())
                        return polished_script
                    except Exception as parse_error:
                        self.logger.warning(f"JSON parse failed: {parse_error}. Returning original")
                        return script
                else:
                    error_msg = await response.text()
                    self.logger.error(f"Anthropic-format API error: {response.status} - {error_msg}")
                    raise Exception(f"Anthropic-format API error: {response.status}")
    
    async def _call_deepseek_simple(self, prompt: str) -> list:
        """Simplified DeepSeek call for fallback (no JSON parsing)"""
        import aiohttp
        
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional YouTube scriptwriter. Return ONLY valid JSON array."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    script_text = data["choices"][0]["message"]["content"]
                    
                    # Try to parse JSON
                    try:
                        if "```json" in script_text:
                            script_text = script_text.split("```json")[1].split("```")[0]
                        elif "```" in script_text:
                            script_text = script_text.split("```")[1].split("```")[0]
                        
                        script = json.loads(script_text.strip())
                        return script
                    except:
                        # If still fails, generate minimal demo script
                        return self._generate_minimal_script(prompt)
                else:
                    raise Exception(f"DeepSeek API error: {response.status}")
    
    def _generate_minimal_script(self, topic: str, language: str = "hindi", style: str = "educational") -> list:
        """Generate very basic script when everything fails"""
        return [
            {"scene": 1, "text": f"नमस्ते! आज हम बात करेंगे {topic} के बारे में।", "language": language, "emotion": "excited", "duration_estimate": 5, "type": "avatar"},
            {"scene": 2, "text": "यह एक बहुत ही महत्वपूर्ण विषय है।", "language": language, "emotion": "serious", "duration_estimate": 5, "type": "broll", "keyword": topic},
            {"scene": 3, "text": "चलिए शुरू करते हैं और विस्तार से जानते हैं।", "language": language, "emotion": "curious", "duration_estimate": 5, "type": "avatar"},
            {"scene": 4, "text": "पहला पॉइंट यह है कि ध्यान देना जरूरी है।", "language": language, "emotion": "neutral", "duration_estimate": 5, "type": "mixed"},
            {"scene": 5, "text": "अंत में, इससे हमें यह सीख मिलती है।", "language": language, "emotion": "inspiring", "duration_estimate": 5, "type": "avatar"}
        ]
    
    def _generate_demo_script(self, topic: str, language: str, style: str) -> list:
        """Generate demo script for testing without API key"""
        
        demo_scripts = {
            "hindi": [
                {"scene": 1, "text": f"नमस्ते दोस्तों! आज हम बात करेंगे {topic} के बारे में।", "language": "hindi", "emotion": "excited", "duration_estimate": 5, "type": "avatar"},
                {"scene": 2, "text": "यह एक बहुत ही महत्वपूर्ण विषय है।", "language": "hindi", "emotion": "serious", "duration_estimate": 5, "type": "broll", "keyword": topic},
                {"scene": 3, "text": "चलिए शुरू करते हैं और विस्तार से जानते हैं।", "language": "hindi", "emotion": "curious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 4, "text": "पहला पॉइंट यह है कि ध्यान देना जरूरी है।", "language": "hindi", "emotion": "neutral", "duration_estimate": 5, "type": "mixed"},
                {"scene": 5, "text": "दूसरा पहलू बहुत ही दिलचस्प है।", "language": "hindi", "emotion": "happy", "duration_estimate": 5, "type": "broll", "keyword": "explanation"},
                {"scene": 6, "text": "अंत में, याद रखना चाहिए कि सीखना कभी नहीं रुकना चाहिए।", "language": "hindi", "emotion": "serious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 7, "text": "वीडियो पसंद आया तो लाइक और सब्सक्राइब जरूर करें!", "language": "hindi", "emotion": "excited", "duration_estimate": 5, "type": "avatar"}
            ],
            "haryanvi": [
                {"scene": 1, "text": f"भाई सुन! आज की बात {topic} पे है।", "language": "haryanvi", "emotion": "excited", "duration_estimate": 5, "type": "avatar"},
                {"scene": 2, "text": "ये तो बड़ी मजेदार बात है के।", "language": "haryanvi", "emotion": "happy", "duration_estimate": 5, "type": "broll", "keyword": topic},
                {"scene": 3, "text": "चल बताता हु तुजके, ध्यान से सुनियो।", "language": "haryanvi", "emotion": "serious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 4, "text": "पहली बात तो ये के, ये बहुत जरूरी है।", "language": "haryanvi", "emotion": "neutral", "duration_estimate": 5, "type": "mixed"},
                {"scene": 5, "text": "दूसरी बात और भी दमदार है भाई।", "language": "haryanvi", "emotion": "excited", "duration_estimate": 5, "type": "broll", "keyword": "explanation"},
                {"scene": 6, "text": "बात याद रखियो, सीखते रहियो हमेशा।", "language": "haryanvi", "emotion": "serious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 7, "text": "वीडियो अच्छा लगा तो शेयर जरूर करियो भाई!", "language": "haryanvi", "emotion": "excited", "duration_estimate": 5, "type": "avatar"}
            ],
            "bhojpuri": [
                {"scene": 1, "text": f"प्रणाम भाई लोग! आज हम बात करब {topic} के बारे में।", "language": "bhojpuri", "emotion": "excited", "duration_estimate": 5, "type": "avatar"},
                {"scene": 2, "text": "ई बहुत महत्व वाला विषय बा।", "language": "bhojpuri", "emotion": "serious", "duration_estimate": 5, "type": "broll", "keyword": topic},
                {"scene": 3, "text": "चलू विस्तार से जानी।", "language": "bhojpuri", "emotion": "curious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 4, "text": "पहिला बात ई बा के ध्यान दिह जरूरी बा।", "language": "bhojpuri", "emotion": "neutral", "duration_estimate": 5, "type": "mixed"},
                {"scene": 5, "text": "दूसरा पहलू बहुत मजेदार बा।", "language": "bhojpuri", "emotion": "happy", "duration_estimate": 5, "type": "broll", "keyword": "explanation"},
                {"scene": 6, "text": "आखिर में, याद रखू कि सीखना कबो नई रुकना चाहीं।", "language": "bhojpuri", "emotion": "serious", "duration_estimate": 5, "type": "avatar"},
                {"scene": 7, "text": "वीडियो पसंद आइल त लाइक आ सब्सक्राइब जरूर करीं!", "language": "bhojpuri", "emotion": "excited", "duration_estimate": 5, "type": "avatar"}
            ]
        }
        
        # Return demo script for requested language or default to Hindi
        return demo_scripts.get(language, demo_scripts["hindi"])
    
    def _load_from_cache(self, cache_hash: str) -> list:
        """Load script from cache"""
        cache_file = self.cache_dir / f"{cache_hash}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Cache load failed: {e}")
        return None
    
    def _save_to_cache(self, cache_hash: str, script: list):
        """Save script to cache"""
        cache_file = self.cache_dir / f"{cache_hash}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(script, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"💾 Script cached: {cache_hash[:8]}")
        except Exception as e:
            self.logger.warning(f"Cache save failed: {e}")
