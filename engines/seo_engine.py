"""
SEO ENGINE - Groq Llama 3.3 Integration
Generates titles, descriptions, tags, chapters
"""
import json
from pathlib import Path
from loguru import logger
from config import Config


class SEOEngine:
    """SEO optimization engine using Groq Llama 3.3"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.api_key = self.config.GROQ_API_KEY
    
    async def generate(
        self,
        topic: str,
        language: str = "hindi",
        style: str = "educational",
        duration_minutes: int = 5
    ) -> dict:
        """
        Generate complete SEO data
        
        Args:
            topic: Video topic
            language: Content language
            style: Video style
            duration_minutes: Duration in minutes
            
        Returns:
            Dictionary with title, description, tags, chapters
        """
        self.logger.info(f"📊 Generating SEO data...")
        
        try:
            if not self.api_key:
                self.logger.warning("⚠️  Groq API key missing - using demo data")
                return self._generate_demo_seo(topic, language)
            
            # Call Groq API
            return await self._call_groq_api(topic, language, style, duration_minutes)
            
        except Exception as e:
            self.logger.error(f"❌ SEO generation failed: {e}")
            return self._generate_demo_seo(topic, language)
    
    async def _call_groq_api(self, topic: str, language: str, style: str, duration: int) -> dict:
        """Call Groq Llama 3.3 API"""
        import aiohttp
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        prompt = f"""Generate YouTube SEO data for a {language} video about "{topic}".

Style: {style}
Duration: {duration} minutes

Return JSON format:
{{
  "title": "Catchy Hindi title with curiosity (max 60 chars)",
  "description": "Detailed description 300-500 words in {language}",
  "tags": ["tag1", "tag2", ...], // 15-20 relevant tags
  "hashtags": ["#hashtag1", "#hashtag2"], // 5-7 hashtags
  "chapters": [
    {{"time": "0:00", "title": "Intro"}},
    {{"time": "0:30", "title": "Main Point 1"}}
  ]
}}

Make it engaging and optimized for Indian audience."""
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a YouTube SEO expert for Indian content."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    # Parse JSON from response
                    try:
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        seo_data = json.loads(content.strip())
                        return seo_data
                    except:
                        return self._generate_demo_seo(topic, language)
                else:
                    self.logger.error(f"Groq API error: {response.status}")
                    return self._generate_demo_seo(topic, language)
    
    def _generate_demo_seo(self, topic: str, language: str) -> dict:
        """Generate demo SEO data"""
        
        titles = {
            "hindi": f"{topic} - पूरी जानकारी | Complete Guide",
            "haryanvi": f"{topic} - भाई सुन ये ज़रूरी बात है के!",
            "bhojpuri": f"{topic} - ई रहल अइसन महत्वपूर्ण बात"
        }
        
        return {
            "title": titles.get(language, titles["hindi"]),
            "description": f"यह वीडियो {topic} के बारे में विस्तृत जानकारी प्रदान करता है। इसमें हम सभी महत्वपूर्ण पहलुओं पर चर्चा करेंगे।\n\nवीडियो पसंद आए तो लाइक और सब्सक्राइब जरूर करें!",
            "tags": [topic, "hindi", "information", "guide", "tutorial", "india", "education"],
            "hashtags": [f"#{topic.replace(' ', '')}", "#hindi", "#information"],
            "chapters": [
                {"time": "0:00", "title": "Introduction"},
                {"time": "0:30", "title": "Main Topic"},
                {"time": "2:00", "title": "Key Points"},
                {"time": "4:00", "title": "Conclusion"}
            ]
        }
