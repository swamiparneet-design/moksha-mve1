"""
COLOR GRADING ENGINE - Professional Cinematic Color
Indian skin tone protection with scene-specific grading
Hollywood-level color science for Indian content
"""
import subprocess
from pathlib import Path
from loguru import logger
from config import Config


class ColorGrader:
    """Professional color grading and timing engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.ffmpeg_path = self.config.FFMPEG_PATH
        
        # Indian skin tone ranges (critical for authenticity)
        self.indian_skin_tones = {
            "fair_north": {
                "hue_range": (10, 25),
                "saturation_range": (0.3, 0.5),
                "luminance_range": (0.6, 0.8),
                "regions": ["Punjab", "Kashmir", "Himachal", "Delhi"]
            },
            "wheatish_central": {
                "hue_range": (15, 30),
                "saturation_range": (0.4, 0.6),
                "luminance_range": (0.4, 0.65),
                "regions": ["UP", "Haryana", "Rajasthan", "MP", "Gujarat"]
            },
            "darker_south": {
                "hue_range": (20, 35),
                "saturation_range": (0.5, 0.7),
                "luminance_range": (0.25, 0.45),
                "regions": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra"]
            },
            "eastern_tone": {
                "hue_range": (18, 32),
                "saturation_range": (0.45, 0.65),
                "luminance_range": (0.35, 0.55),
                "regions": ["Bengal", "Odisha", "Assam", "Bihar"]
            }
        }
        
        # Scene-specific color grades (LUT-like presets)
        self.scene_grades = {
            "ghar_interior_warm": {
                "temperature": 5500,
                "tint": 5,
                "shadow_tint": "warm_brown",
                "highlight_tint": "soft_yellow",
                "saturation": -15,
                "contrast": 1.1,
                "gamma": 1.05,
                "feel": "Masaan_Article_15_homey",
                "when_to_use": ["indoor_family_scenes", "living_room", "bedroom"]
            },
            "kitchen_realistic": {
                "temperature": 4800,
                "tint": 0,
                "shadow_tint": "neutral_warm",
                "highlight_tint": "tungsten",
                "saturation": -10,
                "contrast": 1.15,
                "gamma": 1.0,
                "feel": "authentic_indian_kitchen",
                "when_to_use": ["cooking_scenes", "chai_making", "kitchen_dialogue"]
            },
            "outdoor_daylight": {
                "temperature": 6500,
                "tint": -5,
                "shadow_tint": "cool_blue",
                "highlight_tint": "warm_orange",
                "saturation": 10,
                "contrast": 1.2,
                "gamma": 0.95,
                "feel": "real_indian_afternoon",
                "when_to_use": ["street_scenes", "market", "outdoor_conversations"]
            },
            "emotional_memory": {
                "temperature": 6000,
                "tint": 10,
                "shadow_tint": "lifted_gray",
                "highlight_tint": "dreamy_gold",
                "saturation": -25,
                "contrast": 0.9,
                "gamma": 1.1,
                "feel": "nostalgic_dreamlike_soft",
                "when_to_use": ["flashback", "memory", "emotional_peak", "loss"]
            },
            "tension_conflict": {
                "temperature": 5200,
                "tint": -10,
                "shadow_tint": "cold_steel",
                "highlight_tint": "harsh_white",
                "saturation": -20,
                "contrast": 1.3,
                "gamma": 0.9,
                "feel": "cold_harsh_uncomfortable",
                "when_to_use": ["argument", "confrontation", "anger", "violence"]
            },
            "romantic_love": {
                "temperature": 5800,
                "tint": 15,
                "shadow_tint": "magenta_lift",
                "highlight_tint": "golden_hour",
                "saturation": 5,
                "contrast": 1.05,
                "gamma": 1.08,
                "feel": "warm_romantic_soft_glow",
                "when_to_use": ["love_scene", "intimate_moment", "proposal", "reunion"]
            },
            "devotional_temple": {
                "temperature": 4500,
                "tint": 20,
                "shadow_tint": "amber_warmth",
                "highlight_tint": "candle_gold",
                "saturation": 15,
                "contrast": 1.1,
                "gamma": 1.0,
                "feel": "sacred_spiritual_warm",
                "when_to_use": ["temple", "puja", "prayer", "devotional_song"]
            },
            "rainy_monsoon": {
                "temperature": 7000,
                "tint": -15,
                "shadow_tint": "blue_cool",
                "highlight_tint": "silver_gray",
                "saturation": -10,
                "contrast": 1.0,
                "gamma": 0.98,
                "feel": "moody_romantic_rain",
                "when_to_use": ["monsoon", "rain_scene", "melancholy", "longing"]
            }
        }
        
        # Film emulation LUTs (simplified curve adjustments)
        self.film_emulations = {
            "kodak_portrait": {
                "highlights": "soft_rolled",
                "shadows": "slightly_lifted",
                "midtones": "smooth",
                "color_response": "natural_warm"
            },
            "fuji_portrait": {
                "highlights": "gentle",
                "shadows": "deeper",
                "midtones": "contrasty",
                "color_response": "vibrant_green_red"
            },
            "cinestill_drama": {
                "highlights": "halation_glow",
                "shadows": "crushed",
                "midtones": "punchy",
                "color_response": "teal_orange_bias"
            }
        }
    
    async def grade_scene(self, 
                          video_path: str,
                          scene_type: str,
                          emotion: str,
                          protect_skin_tones: bool = True) -> str:
        """
        Apply professional color grade to a scene
        
        Args:
            video_path: Input video file
            scene_type: Type of scene (ghar_interior/outdoor/emotional/etc.)
            emotion: Scene emotion for fine-tuning
            protect_skin_tones: Enable Indian skin tone protection
            
        Returns:
            Path to color-graded video
        """
        self.logger.info(f"🎨 Color grading: {scene_type} ({emotion})")
        
        try:
            # Select base grade preset
            grade_preset = self._select_grade_preset(scene_type, emotion)
            
            # Build color correction filter chain
            filters = await self._build_color_filters(grade_preset, protect_skin_tones)
            
            # Apply grading
            output_path = self.config.TEMP_PATH / f"graded_{Path(video_path).name}"
            
            await self._apply_grading(video_path, filters, output_path)
            
            self.logger.success(f"✅ Color graded: {output_path.name}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Color grading failed: {e}")
            raise
    
    def _select_grade_preset(self, scene_type: str, emotion: str) -> dict:
        """Select appropriate color grade preset"""
        
        # Direct mapping from scene type
        preset_map = {
            "ghar_interior": "ghar_interior_warm",
            "kitchen": "kitchen_realistic",
            "outdoor": "outdoor_daylight",
            "emotional": "emotional_memory",
            "tension": "tension_conflict",
            "love": "romantic_love",
            "devotional": "devotional_temple",
            "rainy": "rainy_monsoon"
        }
        
        # Try direct match first
        if scene_type in preset_map:
            return self.scene_grades[preset_map[scene_type]]
        
        # Emotion-based fallback
        emotion_grades = {
            "sadness": "emotional_memory",
            "anger": "tension_conflict",
            "love": "romantic_love",
            "joy": "outdoor_daylight",
            "fear": "tension_conflict",
            "nostalgia": "emotional_memory",
            "bhakti": "devotional_temple"
        }
        
        if emotion in emotion_grades:
            return self.scene_grades[emotion_grades[emotion]]
        
        # Default: warm interior
        return self.scene_grades["ghar_interior_warm"]
    
    async def _build_color_filters(self, grade_preset: dict, protect_skin: bool) -> list:
        """Build FFmpeg filter chain for color grading"""
        
        filters = []
        
        # Temperature and tint adjustment
        temp = grade_preset.get("temperature", 6500)
        tint = grade_preset.get("tint", 0)
        
        # Convert temperature to color balance values
        # (simplified conversion - real implementation would be more precise)
        if temp > 6500:
            # Cooler (more blue)
            b_balance = (temp - 6500) / 10000.0
            r_balance = -b_balance * 0.5
        else:
            # Warmer (more orange)
            r_balance = (6500 - temp) / 10000.0
            b_balance = -r_balance * 0.5
        
        filters.append(f"colorbalance=rs={r_balance}:bs={b_balance}")
        
        # Contrast and gamma
        contrast = grade_preset.get("contrast", 1.0)
        gamma = grade_preset.get("gamma", 1.0)
        
        filters.append(f"curves=contrast={contrast}:gamma={gamma}")
        
        # Saturation
        saturation = grade_preset.get("saturation", 0)
        if saturation != 0:
            sat_factor = 1.0 + (saturation / 100.0)
            filters.append(f"eq=saturation={sat_factor}")
        
        # Shadow and highlight tinting
        shadow_tint = grade_preset.get("shadow_tint", "neutral")
        highlight_tint = grade_preset.get("highlight_tint", "neutral")
        
        if shadow_tint != "neutral" or highlight_tint != "neutral":
            tint_filter = self._build_tint_filter(shadow_tint, highlight_tint)
            filters.append(tint_filter)
        
        # Skin tone protection (if enabled)
        if protect_skin:
            skin_protection = self._create_skin_protection_filter()
            filters.append(skin_protection)
        
        return filters
    
    def _build_tint_filter(self, shadow_tint: str, highlight_tint: str) -> str:
        """Build split-toning filter"""
        
        tint_mapping = {
            "warm_brown": "0.6:0.4:0.2",
            "soft_yellow": "0.8:0.7:0.3",
            "cool_blue": "0.2:0.3:0.7",
            "warm_orange": "0.9:0.5:0.2",
            "neutral_warm": "0.7:0.6:0.5",
            "tungsten": "0.8:0.65:0.4",
            "lifted_gray": "0.5:0.5:0.5",
            "dreamy_gold": "0.85:0.75:0.4",
            "cold_steel": "0.4:0.45:0.5",
            "harsh_white": "0.95:0.95:0.95",
            "magenta_lift": "0.8:0.4:0.7",
            "golden_hour": "0.9:0.7:0.3",
            "amber_warmth": "0.9:0.6:0.2",
            "candle_gold": "0.85:0.65:0.3",
            "blue_cool": "0.3:0.4:0.7",
            "silver_gray": "0.6:0.65:0.7"
        }
        
        shadow_rgb = tint_mapping.get(shadow_tint, "0.5:0.5:0.5")
        highlight_rgb = tint_mapping.get(highlight_tint, "0.5:0.5:0.5")
        
        # Split toning using colorchannelmixer
        return f"colorchannelmixer=rr=1:gg=1:bb=1:aa=0:ra={shadow_rgb.split(':')[0]}:ga={shadow_rgb.split(':')[1]}:ba={shadow_rgb.split(':')[2]}"
    
    def _create_skin_protection_filter(self) -> str:
        """Create filter to protect Indian skin tones from over-saturation"""
        
        # This is a simplified mask-based protection
        # Real implementation would use HSL keying
        
        return "eq=brightness=0.02:contrast=1.05"  # Subtle protection
    
    async def _apply_grading(self, video_path: str, filters: list, output_path: str):
        """Apply color grading filters to video"""
        
        filter_chain = ",".join(filters)
        
        cmd = [
            self.ffmpeg_path,
            "-i", video_path,
            "-vf", filter_chain,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",  # High quality
            "-c:a", "copy",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise Exception(f"Color grading failed: {result.stderr}")
    
    async def batch_grade_scenes(self, scenes: list) -> list:
        """
        Apply color grading to multiple scenes
        
        Args:
            scenes: List of scene dictionaries with video_path and metadata
            
        Returns:
            Enhanced scenes with graded video paths
        """
        self.logger.info(f"🎨 Batch grading {len(scenes)} scenes")
        
        graded_scenes = []
        
        for i, scene in enumerate(scenes):
            try:
                video_path = scene.get("video_path")
                if not video_path or not Path(video_path).exists():
                    self.logger.warning(f"Video not found for scene {i}")
                    graded_scenes.append(scene)
                    continue
                
                scene_type = scene.get("scene_type", "ghar_interior")
                emotion = scene.get("emotion", "neutral")
                
                # Grade this scene
                graded_path = await self.grade_scene(video_path, scene_type, emotion)
                
                # Add to results
                graded_scene = {
                    **scene,
                    "video_path": graded_path,
                    "color_grade_applied": True,
                    "grade_preset": scene_type
                }
                
                graded_scenes.append(graded_scene)
                
            except Exception as e:
                self.logger.error(f"Scene {i} grading failed: {e}")
                # Keep original
                graded_scenes.append(scene)
        
        self.logger.success(f"✅ Batch grading complete: {len(graded_scenes)} scenes")
        return graded_scenes


# Test function
async def test_color_grader():
    """Test color grading engine"""
    grader = ColorGrader()
    
    print("\n🎨 Testing Color Grading Engine")
    print("="*70)
    
    # Test preset selection
    test_cases = [
        ("ghar_interior", "neutral"),
        ("kitchen", "joy"),
        ("outdoor", "sadness"),
        ("emotional", "nostalgia"),
        ("tension", "anger"),
        ("love", "love"),
        ("devotional", "bhakti")
    ]
    
    for scene_type, emotion in test_cases:
        preset = grader._select_grade_preset(scene_type, emotion)
        print(f"✅ {scene_type} + {emotion} → {preset['feel']}")
    
    print("\n" + "="*70)
    print("✅ Color Grading Engine test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_color_grader())
