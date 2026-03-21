"""
REAL HARYANVI ACCENT LEARNER
Uses DeepSeek AI to analyze and replicate authentic Haryanvi accent
"""
import asyncio
import aiohttp
import json
from pathlib import Path
from loguru import logger


class HaryanviAccentLearner:
    """Learn real Haryanvi accent from native content"""
    
    def __init__(self):
        self.logger = logger
        self.accent_patterns = {}
        
        # Load existing dictionary
        dict_path = Path("languages/haryanvi/dictionary.json")
        if dict_path.exists():
            with open(dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.accent_patterns = data.get('accent_variations', {})
    
    async def analyze_native_speech(self, sample_text: str, audio_reference: str = None):
        """
        Analyze native Haryanvi speech patterns using DeepSeek
        
        Args:
            sample_text: Text in Haryanvi
            audio_reference: Optional YouTube URL or file path
        """
        prompt = f"""
You are a Haryanvi language expert analyzing authentic dialect patterns.

Analyze this Haryanvi text for accent features:
"{sample_text}"

Provide detailed analysis:
1. Vowel modifications (e.g., 'aa' → 'aaa' for emphasis)
2. Consonant shifts (e.g., 's' → 'h' in some words)
3. Stress patterns (which syllables get emphasis)
4. Speech rhythm (fast/slow, pauses)
5. Regional markers (Jat/Ahir/Gujar accent indicators)
6. Emotional tone (pride/celebration/aggression)

Format as JSON with practical pronunciation guide.
"""
        
        # Call DeepSeek API
        api_key = "sk-59383c9f9495450086cfe1ecd9a08315"
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a Haryanvi linguistics expert specializing in dialect analysis and phonetic transcription."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200:
                        analysis = result['choices'][0]['message']['content']
                        self.logger.success(f"✅ Accent analyzed by DeepSeek")
                        return json.loads(analysis) if analysis.startswith('{') else {"analysis": analysis}
                    else:
                        self.logger.error(f"DeepSeek error: {result}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return None
    
    async def learn_from_song_lyrics(self, song_title: str, lyrics: str):
        """Learn accent patterns from complete song"""
        
        prompt = f"""
Analyze this Haryanvi song "{song_title}" for authentic accent patterns:

LYRICS:
{lyrics}

Extract and teach me:
1. **Signature Haryanvi words** with correct pronunciation
2. **Accent rules** (vowel shifts, consonant changes)
3. **Rhythm pattern** (meter, rhyme scheme)
4. **Emotional delivery** (where to add power, where soft)
5. **Regional markers** (is this Jat style? Ahir style?)
6. **Performance tips** for natural sound

Create a comprehensive accent training guide that I can use to train TTS or voice actors.

Output as structured JSON with examples.
"""
        
        api_key = "sk-59383c9f9495450086cfe1ecd9a08315"
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a professional Haryanvi music director and dialect coach."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200:
                        guide = result['choices'][0]['message']['content']
                        self.logger.success(f"✅ Learned accent from '{song_title}'")
                        
                        # Save accent guide
                        guide_path = Path(f"languages/haryanvi/accent_guides/{song_title.replace(' ', '_')}.json")
                        guide_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(guide_path, 'w', encoding='utf-8') as f:
                            f.write(guide)
                        
                        return guide
                    else:
                        self.logger.error(f"Learning failed: {result}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None
    
    async def generate_pronunciation_guide(self, text_lines: list):
        """Generate phonetic pronunciation for each line"""
        
        all_guides = []
        
        for i, line in enumerate(text_lines):
            prompt = f"""
Convert this Haryanvi line to phonetic pronunciation guide:

Haryanvi: {line}

Provide:
1. IPA transcription (International Phonetic Alphabet)
2. Simple English approximation (how an English speaker would read it)
3. Stress markers (which syllables to emphasize)
4. Tone indicators (rising/falling pitch)

Example format:
- Original: Mhari jaan Haryana
- IPA: /mʱɑːriː dʒɑːn hɑːrjɑːnɑː/
- Pronounced: mum-HAAR-ee JAAN HAAR-yaa-naa
- Stress: 2nd syllable of each word
- Tone: Proud, chest-out delivery
"""
            
            api_key = "sk-59383c9f9495450086cfe1ecd9a08315"
            
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5,
                    "max_tokens": 500
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://api.deepseek.com/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        result = await response.json()
                        
                        if response.status == 200:
                            guide = result['choices'][0]['message']['content']
                            all_guides.append({
                                "line": line,
                                "guide": guide
                            })
                            print(f"✅ Line {i+1} transcribed")
                            
            except Exception as e:
                print(f"❌ Line {i+1} failed: {e}")
        
        return all_guides


async def main():
    """Test accent learning with Mhari Jaan Haryana song"""
    
    learner = HaryanviAccentLearner()
    
    print("\n🎵 Loading song: Mhari Jaan Haryana")
    print("=" * 60)
    
    # Load song lyrics
    song_path = Path("languages/haryanvi/songs/mhari_jaan_haryana.json")
    with open(song_path, 'r', encoding='utf-8') as f:
        song_data = json.load(f)
    
    # Combine all lyrics
    all_lyrics = []
    for section_name, lines in song_data['lyrics'].items():
        all_lyrics.extend(lines)
    
    full_lyrics = '\n'.join(all_lyrics)
    
    # Learn accent from song
    print("\n🧠 Teaching DeepSeek about Haryanvi accent...")
    guide = await learner.learn_from_song_lyrics(
        song_data['title'],
        full_lyrics
    )
    
    if guide:
        print("\n" + "=" * 60)
        print("✅ ACCENT GUIDE GENERATED!")
        print("=" * 60)
        print(guide[:500] + "...")  # Show preview
    
    # Generate pronunciation guides for each line
    print("\n\n📝 Generating phonetic transcriptions...")
    pronunciations = await learner.generate_pronunciation_guide(all_lyrics[:5])  # First 5 lines
    
    print("\n" + "=" * 60)
    print("🗣️ PRONUNCIATION GUIDES:")
    print("=" * 60)
    
    for item in pronunciations:
        print(f"\n🎵 {item['line']}")
        print(f"   {item['guide'][:200]}")


if __name__ == "__main__":
    asyncio.run(main())
