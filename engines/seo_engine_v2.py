"""
SEO ENGINE V2 - Advanced Hindi/Haryanvi Optimization
YouTube algorithm dominance with Indian language psychology
Professional metadata generation for maximum reach
"""
import json
from pathlib import Path
from loguru import logger
from config import Config


class SEOEngineV2:
    """Advanced SEO optimization for Indian content creators"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # YouTube algorithm keywords for Indian content
        self.keyword_categories = {
            "educational": {
                "hindi_primary": ["शिक्षा", "ज्ञान", "सीखें", "जानकारी", "महत्वपूर्ण"],
                "hindi_secondary": ["नया ज्ञान", "अध्ययन", "पढ़ाई", "कोचिंग", "तैयारी"],
                "english_boost": ["education", "learning", "knowledge", "tutorial", "guide"],
                "trending_tags": ["#Education", "#Learning", "#Knowledge", "#Study", "#Tutorial"]
            },
            "story": {
                "hindi_primary": ["कहानी", "दास्तान", "सच्ची घटना", "जीवनी", "इतिहास"],
                "hindi_secondary": ["प्रेरणादायक", "भावुक", "रोमांचक", "रहस्यमयी", "डरावना"],
                "english_boost": ["story", "true story", "inspiring", "emotional", "biography"],
                "trending_tags": ["#Story", "#TrueStory", "#Inspiration", "#Emotional", "#Biography"]
            },
            "news": {
                "hindi_primary": ["समाचार", "खबर", "ब्रेकिंग न्यूज़", "ताज़ा खबर", "अपडेट"],
                "hindi_secondary": ["विश्लेषण", "राजनीति", "अर्थव्यवस्था", "क्राइम", "खेल"],
                "english_boost": ["news", "breaking", "latest", "update", "analysis"],
                "trending_tags": ["#News", "#Breaking", "#Latest", "#Update", "#Analysis"]
            },
            "vlog": {
                "hindi_primary": ["व्लॉग", "दैनिक जीवन", "यात्रा", "अनुभव", "लाइफस्टाइल"],
                "hindi_secondary": ["घूमना", "खाना", "शॉपिंग", "मस्ती", "दोस्त"],
                "english_boost": ["vlog", "daily life", "travel", "lifestyle", "experience"],
                "trending_tags": ["#Vlog", "#DailyLife", "#Travel", "#Lifestyle", "#Experience"]
            },
            "devotional": {
                "hindi_primary": ["भक्ति", "आध्यात्म", "पूजा", "पाठ", "कीर्तन"],
                "hindi_secondary": ["मंदिर", "देवी", "देवता", "मंत्र", "श्लोक"],
                "english_boost": ["devotional", "spiritual", "prayer", "temple", "god"],
                "trending_tags": ["#Devotional", "#Spiritual", "#Bhakti", "#Temple", "#Prayer"]
            }
        }
        
        # Title formulas that work in India
        self.title_formulas = {
            "question_based": {
                "formula": "{question_word} {topic} {shocking_element}",
                "examples": [
                    "क्या है {topic} का असली सच?",
                    "क्यों हुआ {topic} में ये बड़ा बदलाव?",
                    "कौन सी वजह है {topic} की असफलता की?"
                ],
                "ctr_boost": 0.35
            },
            "listicle": {
                "formula": "{number} {topic} {benefit}",
                "examples": [
                    "{topic} के 5 रहस्य जो कोई नहीं बताता",
                    "{topic} पर 7 जरूरी बातें",
                    "10 गलतियां जो {topic} में सब करते हैं"
                ],
                "ctr_boost": 0.40
            },
            "emotional_hook": {
                "formula": "{emotion_word} {topic} {outcome}",
                "examples": [
                    "रुला देने वाला {topic} का सच",
                    "झटका देने वाली {topic} की हकीकत",
                    "खुशी से झूम उठेंगे जब जानेंगे {topic}"
                ],
                "ctr_boost": 0.45
            },
            "controversial": {
                "formula": "{topic} {controversy_word} {reveal}",
                "examples": [
                    "{topic} विवाद: आखिर क्या है मामला?",
                    "{topic} का छुपा हुआ सच सामने",
                    "{topic} पर बड़ी गड़बड़ी पकड़ी गई"
                ],
                "ctr_boost": 0.50
            },
            "how_to_guide": {
                "formula": "कैसे {achieve_something} {topic} में",
                "examples": [
                    "कैसे पाएं {topic} में सफलता",
                    "कैसे बचें {topic} की गलतियों से",
                    "कैसे करें {topic} की शुरुआत"
                ],
                "ctr_boost": 0.30
            }
        }
        
        # Description structure for YouTube algorithm
        self.description_template = {
            "hook_first_2_lines": {
                "purpose": "appear_in_search_preview",
                "max_length": 150,
                "must_include": ["primary_keyword", "benefit_or_curiosity"]
            },
            "detailed_summary": {
                "purpose": "youtube_algorithm_understanding",
                "length": "200-400 words",
                "elements": ["topic_explanation", "key_points", "viewer_benefit"]
            },
            "timestamps_chapters": {
                "purpose": "user_engagement_retention",
                "format": "MM:SS Chapter Title",
                "seo_boost": True
            },
            "call_to_action": {
                "purpose": "engagement_signals",
                "elements": ["subscribe", "like", "comment", "share"]
            },
            "social_links": {
                "purpose": "cross_platform_growth",
                "platforms": ["instagram", "twitter", "facebook", "website"]
            },
            "hashtags_end": {
                "purpose": "discoverability",
                "count": "5-8 relevant hashtags",
                "mix": ["broad", "niche", "trending"]
            }
        }
        
        # Thumbnail text psychology
        self.thumbnail_text_rules = {
            "max_words": 5,
            "font_size_min": 48,
            "color_contrast": "high",
            "emotion_alignment": True,
            "curiosity_gap": True
        }
    
    async def generate_complete_seo(self,
                                     topic: str,
                                     language: str,
                                     content_type: str,
                                     video_duration_minutes: int) -> dict:
        """
        Generate complete SEO package for video
        
        Args:
            topic: Video topic/title
            language: hindi/haryanvi/bhojpuri/english
            content_type: educational/story/news/vlog/devotional
            video_duration: Length for chapter planning
            
        Returns:
            Complete SEO data dictionary
        """
        self.logger.info(f"📈 Generating SEO for: {topic[:50]}...")
        
        try:
            # Get keyword category
            keywords = self.keyword_categories.get(content_type, self.keyword_categories["educational"])
            
            # Generate title options
            titles = await self._generate_title_options(topic, language, content_type)
            
            # Generate description
            description = await self._generate_description(topic, language, content_type, video_duration_minutes)
            
            # Generate tags
            tags = self._generate_tags(topic, language, content_type, keywords)
            
            # Generate thumbnail text
            thumbnail_text = self._generate_thumbnail_text(topic, language)
            
            # Compile complete SEO package
            seo_package = {
                "titles": titles,
                "description": description,
                "tags": tags,
                "thumbnail_text": thumbnail_text,
                "category": self._select_category(content_type),
                "language_metadata": {
                    "primary_language": language,
                    "detected_dialect": self._detect_dialect(language),
                    "regional_audience": self._identify_regional_audience(language)
                }
            }
            
            self.logger.success(f"✅ SEO package generated")
            return seo_package
            
        except Exception as e:
            self.logger.error(f"SEO generation failed: {e}")
            raise
    
    async def _generate_title_options(self, topic: str, language: str, content_type: str) -> list:
        """Generate multiple title options using different formulas"""
        
        titles = []
        
        # Question-based titles
        question_formula = self.title_formulas["question_based"]
        for example in question_formula["examples"]:
            title = example.replace("{topic}", topic)
            title = title.replace("{question_word}", "क्या")
            title = title.replace("{shocking_element}", "का असली सच?")
            titles.append({
                "title": title,
                "formula": "question_based",
                "predicted_ctr": 0.35,
                "language": language
            })
        
        # Listicle titles
        listicle_formula = self.title_formulas["listicle"]
        for example in listicle_formula["examples"]:
            title = example.replace("{topic}", topic)
            titles.append({
                "title": title,
                "formula": "listicle",
                "predicted_ctr": 0.40,
                "language": language
            })
        
        # Emotional hook titles
        emotion_formula = self.title_formulas["emotional_hook"]
        for example in emotion_formula["examples"]:
            title = example.replace("{topic}", topic)
            title = title.replace("{emotion_word}", "रुला देने वाला")
            title = title.replace("{outcome}", "")
            titles.append({
                "title": title,
                "formula": "emotional_hook",
                "predicted_ctr": 0.45,
                "language": language
            })
        
        self.logger.info(f"Generated {len(titles)} title options")
        return titles
    
    async def _generate_description(self, 
                                     topic: str,
                                     language: str,
                                     content_type: str,
                                     duration_minutes: int) -> str:
        """Generate YouTube-optimized description"""
        
        description_parts = []
        
        # Hook (first 2 lines - most important for CTR)
        hook = f"{topic} - इस विषय पर विस्तृत जानकारी और गहन विश्लेषण।\n"
        hook += f"जानिए {topic} के सभी पहलुओं को, जो आपके लिए उपयोगी साबित होगा।\n\n"
        description_parts.append(hook)
        
        # Detailed summary
        summary = f"इस वीडियो में हम {topic} पर चर्चा कर रहे हैं। "
        summary += f"यह विषय आज के समय में बहुत महत्वपूर्ण हो गया है क्योंकि इसका सीधा असर हमारे दैनिक जीवन पर पड़ता है।\n\n"
        summary += f"हम बात करेंगे:\n"
        summary += f"• {topic} का परिचय और महत्व\n"
        summary += f"• मुख्य बिंदु और विशेषताएं\n"
        summary += f"• व्यावहारिक उदाहरण और अनुप्रयोग\n"
        summary += f"• निष्कर्ष और भविष्य की दिशा\n\n"
        description_parts.append(summary)
        
        # Timestamps (if duration > 3 minutes)
        if duration_minutes >= 3:
            timestamps = "अध्यााय (Chapters):\n"
            timestamps += "0:00 परिचय\n"
            timestamps += f"{int(duration_minutes * 0.2):02d}:00 मुख्य अवधारणा\n"
            timestamps += f"{int(duration_minutes * 0.4):02d}:00 विस्तृत विश्लेषण\n"
            timestamps += f"{int(duration_minutes * 0.6):02d}:00 उदाहरण और अनुप्रयोग\n"
            timestamps += f"{int(duration_minutes * 0.8):02d}:00 निष्कर्ष\n"
            timestamps += f"{duration_minutes:02d}:00 समापन\n\n"
            description_parts.append(timestamps)
        
        # Call to action
        cta = "अगर यह वीडियो पसंद आए तो:\n"
        cta += "👍 LIKE करें\n"
        cta += "💬 COMMENT में अपनी राय दें\n"
        cta += "🔔 SUBSCRIBE करें और बेल आइकन दबाएं\n"
        cta += "📢 SHARE करें अपने दोस्तों के साथ\n\n"
        description_parts.append(cta)
        
        # Hashtags
        hashtags = self._generate_hashtags(content_type, language)
        description_parts.append(hashtags)
        
        full_description = "".join(description_parts)
        
        self.logger.info(f"Generated description ({len(full_description)} characters)")
        return full_description
    
    def _generate_tags(self, 
                       topic: str,
                       language: str,
                       content_type: str,
                       keywords: dict) -> list:
        """Generate comprehensive tag list"""
        
        tags = []
        
        # Primary Hindi keywords
        tags.extend(keywords["hindi_primary"][:5])
        
        # Secondary Hindi keywords
        tags.extend(keywords["hindi_secondary"][:3])
        
        # English boost keywords
        tags.extend(keywords["english_boost"][:5])
        
        # Topic-specific variations
        topic_words = topic.split()
        for word in topic_words[:3]:
            if len(word) > 3:
                tags.append(word)
                tags.append(f"{word} hindi")
                tags.append(f"{word} explained")
        
        # Broad category tags
        broad_tags = {
            "educational": ["education", "learning", "study", "knowledge"],
            "story": ["story", "kahani", "stories", "tales"],
            "news": ["news", "samachar", "breaking", "latest"],
            "vlog": ["vlog", "daily vlog", "lifestyle"],
            "devotional": ["bhakti", "devotional", "spiritual", "hindu"]
        }
        
        tags.extend(broad_tags.get(content_type, broad_tags["educational"]))
        
        # Language-specific tags
        if language == "hindi":
            tags.extend(["hindi", "hindi video", "hindi content"])
        elif language == "haryanvi":
            tags.extend(["haryanvi", "haryanvi video", "desi"])
        elif language == "bhojpuri":
            tags.extend(["bhojpuri", "bhojpuri video", "bhojpuriya"])
        
        self.logger.info(f"Generated {len(tags)} tags")
        return list(set(tags))  # Remove duplicates
    
    def _generate_thumbnail_text(self, topic: str, language: str) -> str:
        """Generate short, impactful thumbnail text"""
        
        # Extract key emotion/element from topic
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["shock", "reveal", "secret", "raaz", "sach"]):
            return "बड़ा खुलासा!"
        elif any(word in topic_lower for word in ["sad", "cry", "emotional", "rula"]):
            return "रुला देने वाला"
        elif any(word in topic_lower for word in ["how to", "kaise", "guide", "tutorial"]):
            return "आसान तरीका"
        elif any(word in topic_lower for word in ["why", "kyon", "reason", "vajah"]):
            return "असली वजह?"
        else:
            # Default: Create curiosity gap
            return "जानिए असली सच"
    
    def _generate_hashtags(self, content_type: str, language: str) -> str:
        """Generate relevant hashtags"""
        
        hashtag_map = {
            "educational": ["#Education", "#Learning", "#Knowledge", "#Hindi", "#Study"],
            "story": ["#Story", "#Kahani", "#HindiStory", "#Emotional", "#Inspiration"],
            "news": ["#News", "#Breaking", "#HindiNews", "#Latest", "#Update"],
            "vlog": ["#Vlog", "#DailyVlog", "#Lifestyle", "#HindiVlog", "#India"],
            "devotional": ["#Devotional", "#Bhakti", "#Spiritual", "#Hindu", "#Temple"]
        }
        
        base_hashtags = hashtag_map.get(content_type, hashtag_map["educational"])
        
        # Add language-specific hashtag
        lang_hashtag = {
            "hindi": "#Hindi",
            "haryanvi": "#Haryanvi",
            "bhojpuri": "#Bhojpuri",
            "english": "#English"
        }
        
        base_hashtags.append(lang_hashtag.get(language, "#Hindi"))
        
        return " ".join(base_hashtags[:8]) + "\n"
    
    def _select_category(self, content_type: str) -> str:
        """Select YouTube category ID"""
        
        category_map = {
            "educational": "Education",
            "story": "Entertainment",
            "news": "News & Politics",
            "vlog": "People & Blogs",
            "devotional": "Entertainment"
        }
        
        return category_map.get(content_type, "Education")
    
    def _detect_dialect(self, language: str) -> str:
        """Detect specific dialect based on language code"""
        
        dialect_map = {
            "hindi": "Standard Hindi (Khadi Boli)",
            "haryanvi": "Haryanvi (Bangaru/Bagri dialect)",
            "bhojpuri": "Bhojpuri (Purbi dialect)",
            "english": "Indian English"
        }
        
        return dialect_map.get(language, "Standard Hindi")
    
    def _identify_regional_audience(self, language: str) -> list:
        """Identify primary regional audience"""
        
        audience_map = {
            "hindi": ["Uttar Pradesh", "Delhi", "Madhya Pradesh", "Rajasthan", "Bihar"],
            "haryanvi": ["Haryana", "Western UP", "Delhi NCR", "Rajasthan"],
            "bhojpuri": ["Eastern UP", "Bihar", "Jharkhand", "Mumbai migrants"],
            "english": ["Metro cities", "Pan-India", "International"]
        }
        
        return audience_map.get(language, audience_map["hindi"])
    
    async def save_seo_package(self, seo_data: dict, output_path: str):
        """Save SEO package to JSON file"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(seo_data, f, indent=2, ensure_ascii=False)
        
        self.logger.success(f"✅ SEO package saved: {output_path}")


# Test function
async def test_seo_engine_v2():
    """Test advanced SEO engine"""
    engine = SEOEngineV2()
    
    print("\n📈 Testing SEO Engine V2")
    print("="*70)
    
    test_cases = [
        ("Climate Change Impact", "hindi", "educational", 5),
        ("Farmer's Emotional Journey", "hindi", "story", 8),
        ("Latest Election Updates", "hindi", "news", 3),
        ("My Daily Routine in Village", "haryanvi", "vlog", 10),
        ("Temple Visit Experience", "hindi", "devotional", 6)
    ]
    
    for topic, lang, ctype, duration in test_cases:
        print(f"\nGenerating SEO for: {topic} ({lang}, {ctype})")
        
        seo_data = await engine.generate_complete_seo(topic, lang, ctype, duration)
        
        print(f"✅ Titles: {len(seo_data['titles'])} options")
        print(f"   Best CTR: {max([t['predicted_ctr'] for t in seo_data['titles']]):.0%}")
        print(f"✅ Tags: {len(seo_data['tags'])} keywords")
        print(f"✅ Description: {len(seo_data['description'])} chars")
        print(f"✅ Thumbnail Text: {seo_data['thumbnail_text']}")
    
    print("\n" + "="*70)
    print("✅ SEO Engine V2 test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_seo_engine_v2())
