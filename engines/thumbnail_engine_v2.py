"""
THUMBNAIL ENGINE V2 - Enhanced CTR Optimization
Professional thumbnail generation with Indian psychology
Hollywood-level visual hooks for maximum clicks
"""
from pathlib import Path
from loguru import logger
from config import Config


class ThumbnailEngineV2:
    """Enhanced thumbnail generation with CTR psychology"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # CTR Psychology principles for Indian audience
        self.ctr_principles = {
            "curiosity_gap": {
                "technique": "show_intriguing_but_incomplete",
                "example": "Face with shocked expression but hidden object",
                "effectiveness": 0.85
            },
            "emotional_trigger": {
                "technique": "extreme_facial_emotion",
                "example": "Tears, shock, joy, anger - amplified",
                "effectiveness": 0.90
            },
            "regional_relatability": {
                "technique": "culturally_specific_elements",
                "example": "Indian clothing, settings, skin tones",
                "effectiveness": 0.80
            },
            "color_psychology": {
                "red_orange": "urgency_excitement_danger",
                "blue": "trust_calm_professionalism",
                "yellow": "optimism_attention_grabbing",
                "green": "growth_harmony_money",
                "purple": "luxury_mystery_spirituality"
            },
            "text_placement": {
                "rule_of_thirds": "place_key_element_at_intersections",
                "left_side_preference": "indian_audience_reads_left_to_right",
                "face_on_right": "text_on_left_face_on_right_performs_best"
            }
        }
        
        # Thumbnail templates for different content types
        self.templates = {
            "educational_explainer": {
                "layout": "face_left_text_right",
                "background": "blurred_relevant_scene",
                "text_style": "bold_white_yellow_outline",
                "emotion": "curious_engaging",
                "elements": ["host_face", "key_object", "bold_text_3-5_words"]
            },
            "emotional_story": {
                "layout": "close_up_face_center",
                "background": "dark_moody_gradient",
                "text_style": "white_glowing_edge",
                "emotion": "tears_or_shock",
                "elements": ["extreme_closeup_eyes", "single_tear_optional", "emotional_word"]
            },
            "controversial_topic": {
                "layout": "split_screen_contrast",
                "background": "red_vs_blue_split",
                "text_style": "bold_red_impact_font",
                "emotion": "angry_or_shocked",
                "elements": ["two_contrasting_images", "VS_text", "question_mark"]
            },
            "devotional_spiritual": {
                "layout": "deity_top_center_devotee_below",
                "background": "temple_golden_light",
                "text_style": "saffron_or_gold",
                "emotion": "bhakti_peaceful",
                "elements": ["deity_image", "namaste_hands", "shlok_text"]
            },
            "comedy_entertainment": {
                "layout": "action_freeze_frame",
                "background": "bright_vibrant_colors",
                "text_style": "playful_bubbly_font",
                "emotion": "laughing_exaggerated",
                "elements": ["mid_action_shot", "laugh_lines", "funny_expression"]
            }
        }
        
        # Text hook formulas (Hindi/Haryanvi)
        self.text_hooks = {
            "question_hook": [
                "क्या हुआ था असल में?",
                "क्यों किया उसने ऐसा?",
                "कौन सी सच्चाई सामने आई?",
                "कैसे बदली पूरी कहानी?"
            ],
            "shock_hook": [
                "सबको झटका!",
                "रोंगटे खड़े कर देने वाला सच",
                "ये कोई नहीं जानता था",
                "आखिरकार सामने आया"
            ],
            "emotion_hook": [
                "रुला देने वाली कहानी",
                "प्यार की असली परिभाषा",
                "त्याग की मिसाल",
                "माँ का दर्द"
            ],
            "curiosity_hook": [
                "अंदर की बात",
                "छुपा हुआ सच",
                "वो राज़ जो खुला",
                "कभी नहीं सुना होगा"
            ]
        }
    
    async def generate_thumbnail(self,
                                  video_path: str,
                                  topic: str,
                                  language: str = "hindi",
                                  content_type: str = "educational") -> str:
        """
        Generate high-CTR thumbnail from video
        
        Args:
            video_path: Source video file
            topic: Video topic/title
            language: hindi/haryanvi/bhojpuri/english
            content_type: Type of content for template selection
            
        Returns:
            Path to generated thumbnail image
        """
        self.logger.info(f"🖼️ Generating thumbnail for: {topic[:50]}...")
        
        try:
            # Select appropriate template
            template = self.templates.get(content_type, self.templates["educational_explainer"])
            
            # Extract best frame from video
            best_frame = await self._extract_best_frame(video_path, template)
            
            # Enhance frame (color correction, contrast)
            enhanced_frame = await self._enhance_frame(best_frame)
            
            # Add text overlay with hook
            text_overlay = self._select_best_hook(topic, language)
            
            # Composite final thumbnail
            output_path = self.config.OUTPUT_PATH / f"thumbnail_{Path(video_path).stem}.jpg"
            
            await self._composite_thumbnail(enhanced_frame, text_overlay, template, output_path)
            
            self.logger.success(f"✅ Thumbnail generated: {output_path.name}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Thumbnail generation failed: {e}")
            raise
    
    async def _extract_best_frame(self, video_path: str, template: dict) -> str:
        """Extract emotionally expressive frame from video"""
        
        self.logger.debug("🎬 Extracting best frame from video")
        
        # Use FFmpeg to extract multiple frames and select best
        temp_frames = self.config.TEMP_PATH / "frames"
        temp_frames.mkdir(exist_ok=True)
        
        # Extract 10 frames evenly distributed
        cmd = [
            self.config.FFMPEG_PATH,
            "-i", video_path,
            "-vf", "fps=1/10",
            "-q:v", "2",
            str(temp_frames / "frame_%03d.jpg")
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            raise Exception(f"Frame extraction failed: {result.stderr}")
        
        # Select first frame as default (in real implementation, use ML to detect best emotion)
        frames = list(temp_frames.glob("frame_*.jpg"))
        
        if frames:
            return str(frames[0])
        else:
            raise Exception("No frames extracted")
    
    async def _enhance_frame(self, frame_path: str) -> str:
        """Enhance frame with professional color grading"""
        
        self.logger.debug("🎨 Enhancing frame quality")
        
        output_path = self.config.TEMP_PATH / f"enhanced_{Path(frame_path).name}"
        
        # FFmpeg filters for enhancement
        filters = [
            "unsharp=5:5:1.0:5:5:0.0",  # Sharpening
            "eq=contrast=1.2:saturation=1.3:brightness=0.05",  # Pop colors
            "curves=vintage"  # Cinematic look
        ]
        
        cmd = [
            self.config.FFMPEG_PATH,
            "-i", frame_path,
            "-vf", ",".join(filters),
            "-q:v", "1",
            "-y",
            str(output_path)
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            self.logger.warning(f"Enhancement failed, using original")
            return frame_path
        
        return str(output_path)
    
    def _select_best_hook(self, topic: str, language: str) -> str:
        """Select or generate best text hook for thumbnail"""
        
        # Simple keyword-based selection
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["kya", "kyon", "kaun", "kaise", "what", "why", "how"]):
            # Already a question - use as-is
            return topic[:50]
        
        elif any(word in topic_lower for word in ["shocking", "shock", "revealed", "secret", "raaz", "sach"]):
            hooks = self.text_hooks["shock_hook"]
            return self._select_random_hook(hooks, language)
        
        elif any(word in topic_lower for word in ["emotional", "love", "pyaar", "sad", "cry", "rula"]):
            hooks = self.text_hooks["emotion_hook"]
            return self._select_random_hook(hooks, language)
        
        elif any(word in topic_lower for word in ["story", "kahani", "incident", "event"]):
            hooks = self.text_hooks["curiosity_hook"]
            return self._select_random_hook(hooks, language)
        
        else:
            # Default: create question from topic
            if language == "hindi":
                return f"{topic[:40]} - क्या है असली सच?"
            else:
                return f"{topic[:40]} - The Truth?"
    
    def _select_random_hook(self, hooks: list, language: str) -> str:
        """Select random hook from list"""
        import random
        return random.choice(hooks)
    
    async def _composite_thumbnail(self, 
                                    frame_path: str,
                                    text: str,
                                    template: dict,
                                    output_path: str):
        """Composite final thumbnail with text overlay"""
        
        self.logger.debug(f"🖼️ Compositing thumbnail with text: {text}")
        
        # Create thumbnail with ImageMagick or PIL
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Open base image
            img = Image.open(frame_path)
            img = img.resize((1280, 720))
            
            draw = ImageDraw.Draw(img)
            
            # Load font (try common Hindi fonts)
            font_paths = [
                "C:\\Windows\\Fonts\\mangal.ttf",
                "C:\\Windows\\Fonts\\kokila.ttf",
                "C:\\Windows\\Fonts\\arial.ttf"
            ]
            
            font_size = 48
            font = None
            
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
            
            if not font:
                font = ImageFont.load_default()
            
            # Calculate text position (rule of thirds - left side)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Position: Left side, vertically centered
            x = 50
            y = (720 - text_height) // 2
            
            # Draw text with outline
            outline_color = "yellow"
            fill_color = "white"
            
            # Outline (multiple passes for thickness)
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill=outline_color)
            
            # Main text
            draw.text((x, y), text, font=font, fill=fill_color)
            
            # Save thumbnail
            img.save(output_path, "JPEG", quality=95, optimize=True)
            
        except Exception as e:
            self.logger.error(f"PIL compositing failed: {e}")
            # Fallback: just copy the enhanced frame
            import shutil
            shutil.copy(frame_path, output_path)
    
    async def generate_variants(self, 
                                 video_path: str,
                                 topic: str,
                                 language: str = "hindi",
                                 num_variants: int = 3) -> list:
        """Generate multiple thumbnail variants for A/B testing"""
        
        self.logger.info(f"🎨 Generating {num_variants} thumbnail variants")
        
        variants = []
        
        content_types = ["educational_explainer", "emotional_story", "controversial_topic"]
        
        for i in range(num_variants):
            try:
                content_type = content_types[i % len(content_types)]
                
                variant_path = await self.generate_thumbnail(
                    video_path=video_path,
                    topic=f"{topic} (Variant {i+1})",
                    language=language,
                    content_type=content_type
                )
                
                variants.append({
                    "variant_number": i + 1,
                    "content_type": content_type,
                    "path": variant_path
                })
                
            except Exception as e:
                self.logger.error(f"Variant {i+1} generation failed: {e}")
                continue
        
        self.logger.success(f"✅ Generated {len(variants)} variants")
        return variants


# Test function
async def test_thumbnail_engine_v2():
    """Test enhanced thumbnail engine"""
    engine = ThumbnailEngineV2()
    
    print("\n🖼️ Testing Enhanced Thumbnail Engine")
    print("="*70)
    
    # Mock video path (use existing test video if available)
    test_video = Path("outputs/mock_tests/test_final.mp4")
    
    if not test_video.exists():
        print("⚠️  No test video found - creating placeholder thumbnail")
        # Create simple test image
        from PIL import Image
        img = Image.new('RGB', (1280, 720), color=(73, 109, 137))
        img.save("temp/test_thumbnail_base.jpg")
        test_video = Path("temp/test_thumbnail_base.jpg")
    
    # Test thumbnail generation
    test_topics = [
        ("Climate Change Secrets", "hindi", "educational_explainer"),
        ("Papa Beti Emotional Story", "hindi", "emotional_story"),
        ("Controversial Truth Revealed", "hindi", "controversial_topic")
    ]
    
    for topic, lang, ctype in test_topics:
        print(f"\nGenerating: {topic} ({ctype})")
        thumbnail_path = await engine.generate_thumbnail(
            str(test_video),
            topic,
            lang,
            ctype
        )
        print(f"✅ Thumbnail: {thumbnail_path}")
        if Path(thumbnail_path).exists():
            print(f"   Size: {Path(thumbnail_path).stat().st_size} bytes")
    
    print("\n" + "="*70)
    print("✅ Enhanced Thumbnail Engine test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_thumbnail_engine_v2())
