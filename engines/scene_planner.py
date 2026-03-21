"""
SCENE PLANNER - Python NLP Logic
Decides scene types: Avatar, B-Roll, or Mixed
"""
from loguru import logger
from config import Config


class ScenePlanner:
    """Scene planning engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # Keywords for scene type detection
        self.avatar_keywords = [
            "मैं", "हम", "तुम", "आप", "बता", "सुन", "देख", 
            "explain", "tell", "say", "speak", "narrate"
        ]
        
        self.broll_keywords = [
            "जगह", "स्थान", "शहर", "गाँव", "बाज़ार", "नदी", "पहाड़",
            "place", "location", "city", "village", "market", "river", "mountain",
            "footage", "scene", "view", "landscape"
        ]
        
        self.emotion_mapping = {
            "excited": ["zoom_in", "fast_cut"],
            "sad": ["slow_motion", "fade"],
            "angry": ["shake", "red_filter"],
            "happy": ["bright", "bounce"],
            "curious": ["zoom_slow", "mystery"],
            "serious": ["stable", "focus"],
            "neutral": ["standard"]
        }
    
    async def plan(self, script: list, use_avatar: bool = True, viral_mode: bool = True, topic: str = "") -> list:
        """
        Plan scenes from script with emotion flow and viral optimization
        
        Args:
            script: List of scene texts from Script Engine
            use_avatar: Whether to use avatar
            viral_mode: Enable viral retention rules
            topic: Video topic for storage detection
            
        Returns:
            Enhanced scene list with types, prompts, and effects
        """
        self.logger.info(f"🎭 Planning scenes for {len(script)} items")
        self.topic = topic  # Store topic for devotional detection
        
        planned_scenes = []
        
        for i, scene_data in enumerate(script):
            try:
                # Enhance scene data
                enhanced_scene = await self._analyze_scene(scene_data, use_avatar, i)
                planned_scenes.append(enhanced_scene)
                
            except Exception as e:
                self.logger.error(f"Scene {i} planning failed: {e}")
                # Fallback to basic scene
                planned_scenes.append({
                    **scene_data,
                    "type": "avatar" if use_avatar else "broll",
                    "prompt": f"Person explaining, Indian setting, cinematic lighting"
                })
        
        # Apply viral retention rules
        if viral_mode:
            planned_scenes = self._apply_viral_retention_rules(planned_scenes)
        else:
            planned_scenes = self._apply_retention_rules(planned_scenes)
        
        self.logger.success(f"✅ Scenes planned: {len(planned_scenes)} total")
        return planned_scenes
    
    async def _analyze_scene(self, scene_data: dict, use_avatar: bool, index: int) -> dict:
        """Analyze single scene and determine type"""
        
        text = scene_data.get("text", "").lower()
        emotion = scene_data.get("emotion", "neutral")
        
        # Count keyword matches
        avatar_score = sum(1 for kw in self.avatar_keywords if kw in text)
        broll_score = sum(1 for kw in self.broll_keywords if kw in text)
        
        # Determine scene type
        if not use_avatar:
            scene_type = "broll"
        elif avatar_score > broll_score:
            scene_type = "avatar"
        elif broll_score > avatar_score:
            scene_type = "broll"
        else:
            # Default pattern: alternate for engagement
            scene_type = "mixed" if index % 2 == 0 else "avatar"
        
        # Generate prompt for video generation
        prompt = self._generate_prompt(scene_data, scene_type)
        
        # Get visual effects based on emotion
        effects = self.emotion_mapping.get(emotion, ["standard"])
        
        # FORCE storage media usage for devotional/historical topics
        keyword = scene_data.get("keyword", self._extract_keyword(text))
        topic_lower = self.topic.lower()
        
        # If topic is devotional/historical, ALWAYS use storage
        devotional_keywords = ['hanuman', 'temple', 'god', 'puja', 'devotional', 'taj mahal', 'fort', 'palace', 'india', 'history']
        if any(kw in topic_lower for kw in devotional_keywords):
            scene_type = "storage_broll"  # Special flag to force storage usage
            self.logger.info(f"🎯 Devotional/Historical topic detected - forcing storage media for scene {index}")
        
        return {
            **scene_data,
            "type": scene_type,
            "prompt": prompt,
            "effects": effects,
            "keyword": keyword
        }
    
    def _generate_prompt(self, scene_data: dict, scene_type: str) -> str:
        """Generate detailed prompt for video generation"""
        
        language = scene_data.get("language", "hindi")
        emotion = scene_data.get("emotion", "neutral")
        text = scene_data.get("text", "")
        
        if scene_type == "avatar":
            prompt = f"""
Young Indian person explaining in {language},
natural facial expression: {emotion},
modern indoor setting, natural daylight,
cinematic lighting, stable camera,
24fps, 720p, realistic face,
smooth movement, no distortion,
high detail, professional look
""".strip()
            
        elif scene_type == "broll":
            keyword = scene_data.get("keyword", "general")
            prompt = f"""
{keyword} footage, Indian context,
cinematic quality, stable shot,
24fps, 720p, high detail,
realistic colors, professional
""".strip()
            
        else:  # mixed
            prompt = f"""
Mixed scene with person and background elements,
Indian setting, {emotion} mood,
cinematic lighting, dynamic composition,
24fps, 720p, realistic, smooth transitions
""".strip()
        
        return prompt
    
    def _extract_keyword(self, text: str) -> str:
        """Extract main keyword from text for B-roll search"""
        # Simple keyword extraction (can be improved with NLP)
        words = text.split()
        
        # Remove common words
        stop_words = ["hai", "hai", "ke", "ki", "mein", "par", "aur", "the", "a", "an", "the"]
        filtered_words = [w for w in words if w.lower() not in stop_words]
        
        # Return first meaningful word(s)
        if len(filtered_words) >= 2:
            return " ".join(filtered_words[:2])
        elif filtered_words:
            return filtered_words[0]
        else:
            return "india"
    
    def _apply_viral_retention_rules(self, scenes: list) -> list:
        """Apply aggressive YouTube retention optimization for viral content"""
        
        # Rule 1: First 3 seconds MUST be SHOCK HOOK
        if len(scenes) > 0:
            scenes[0]["effects"] = ["dramatic_zoom", "hook_text", "shock_effect"]
            scenes[0]["hook"] = True
            scenes[0]["hook_type"] = "shock_question"
        
        # Rule 2: Every 3 seconds add cut or zoom (aggressive)
        for i, scene in enumerate(scenes):
            if i % 1 == 0:  # Every scene
                if "zoom" not in str(scene.get("effects", [])):
                    scene["effects"].append("quick_zoom")
                scene["visual_change"] = True
        
        # Rule 3: Every 15-20 seconds (3-4 scenes) major pattern break
        for i in range(3, len(scenes), 4):
            scenes[i]["pattern_break"] = True
            scenes[i]["effects"] = ["transition", "color_change", "angle_switch", "speed_ramp"]
            scenes[i]["engagement_boost"] = True
        
        # Rule 4: Create curiosity gaps
        for i in range(2, len(scenes) - 1, 3):
            scenes[i]["curiosity_gap"] = True
            scenes[i]["suspense_build"] = True
        
        # Rule 5: Last scene = Strong CTA + Payoff
        if len(scenes) > 0:
            scenes[-1]["cta"] = True
            scenes[-1]["payoff"] = True
            scenes[-1]["effects"].append("end_screen_cta")
        
        # Rule 6: Add engagement triggers throughout
        for i in range(1, len(scenes) - 1):
            if i % 2 == 0:
                scenes[i]["engagement_trigger"] = f"question_{i}"
        
        return scenes
    
    def get_scene_transitions(self, scenes: list) -> list:
        """Get transition effects between scenes"""
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_type = scenes[i]["type"]
            next_type = scenes[i + 1]["type"]
            
            if current_type == next_type:
                transitions.append("smooth_cut")
            elif current_type == "avatar" and next_type == "broll":
                transitions.append("fade_out")
            elif current_type == "broll" and next_type == "avatar":
                transitions.append("fade_in")
            else:
                transitions.append("cross_dissolve")
        
        return transitions
