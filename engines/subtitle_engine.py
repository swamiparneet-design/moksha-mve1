"""
SUBTITLE ENGINE - Professional Subtitle Generation
Multi-language support with styled subtitles for Indian content
Hollywood-level timing and positioning
"""
import json
from pathlib import Path
from loguru import logger
from config import Config


class SubtitleEngine:
    """Professional subtitle generation and styling engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # Font configurations for Indian languages
        self.font_configs = {
            "hindi": {
                "primary_font": "Noto Sans Devanagari",
                "fallback_fonts": ["Mangal", "Kokila", "Arial Unicode MS"],
                "unicode_range": "U+0900-097F",  # Devanagari
                "line_height": 1.4,
                "letter_spacing": 0.05
            },
            "haryanvi": {
                "primary_font": "Noto Sans Devanagari",
                "fallback_fonts": ["Mangal", "Kokila"],
                "unicode_range": "U+0900-097F",
                "line_height": 1.4,
                "letter_spacing": 0.05,
                "regional_style": "informal_bold"
            },
            "bhojpuri": {
                "primary_font": "Noto Sans Devanagari",
                "fallback_fonts": ["Mangal", "Kokila"],
                "unicode_range": "U+0900-097F",
                "line_height": 1.3,
                "letter_spacing": 0.08
            },
            "english": {
                "primary_font": "Arial",
                "fallback_fonts": ["Helvetica", "Verdana"],
                "unicode_range": "Latin",
                "line_height": 1.2,
                "letter_spacing": 0.02
            }
        }
        
        # Subtitle styles based on context
        self.subtitle_styles = {
            "standard_dialogue": {
                "font_size": 48,
                "font_color": "&HFFFFFF",  # White
                "outline_color": "&H000000",  # Black
                "outline_width": 2,
                "shadow_offset": 1,
                "background_alpha": "&H80000000",  # Semi-transparent black
                "margin_vertical": 60,
                "margin_horizontal": 100,
                "alignment": "2",  # Bottom center
                "bold": False,
                "italic": False
            },
            "emotional_emphasis": {
                "font_size": 52,
                "font_color": "&H00FFFF",  # Cyan for emotion
                "outline_color": "&H000000",
                "outline_width": 3,
                "shadow_offset": 2,
                "background_alpha": "&HC000000",
                "margin_vertical": 60,
                "margin_horizontal": 100,
                "alignment": "2",
                "bold": True,
                "italic": False,
                "special_effect": "slight_glow"
            },
            "whisper_internal": {
                "font_size": 42,
                "font_color": "&HAAAAAA",  # Gray
                "outline_color": "&H000000",
                "outline_width": 1,
                "shadow_offset": 0,
                "background_alpha": "&H60000000",
                "margin_vertical": 80,
                "margin_horizontal": 100,
                "alignment": "2",
                "bold": False,
                "italic": True,
                "special_effect": "fade_in_out"
            },
            "shout_exclamation": {
                "font_size": 56,
                "font_color": "&H0000FF",  # Yellow for intensity
                "outline_color": "&H000000",
                "outline_width": 3,
                "shadow_offset": 2,
                "background_alpha": "&HE000000",
                "margin_vertical": 60,
                "margin_horizontal": 100,
                "alignment": "2",
                "bold": True,
                "italic": False,
                "special_effect": "slight_shake"
            },
            "song_lyrics": {
                "font_size": 50,
                "font_color": "&HFF99FF",  # Light pink
                "outline_color": "&H000080",  # Dark blue outline
                "outline_width": 2,
                "shadow_offset": 1,
                "background_alpha": "&H90000000",
                "margin_vertical": 100,
                "margin_horizontal": 100,
                "alignment": "2",
                "bold": False,
                "italic": True,
                "special_effect": "karaoke_style"
            },
            "title_card": {
                "font_size": 72,
                "font_color": "&HFFFFFF",
                "outline_color": "&H000000",
                "outline_width": 3,
                "shadow_offset": 3,
                "background_alpha": "&HF0000000",
                "margin_vertical": 400,
                "margin_horizontal": 100,
                "alignment": "7",  # Top center
                "bold": True,
                "italic": False,
                "special_effect": "fade_in_hold_fade_out"
            }
        }
        
        # Timing rules for different languages
        self.timing_rules = {
            "hindi": {
                "characters_per_second": 15,
                "minimum_duration": 1.0,
                "maximum_duration": 6.0,
                "gap_between_subtitles": 0.2,
                "reading_speed_multiplier": 1.0
            },
            "haryanvi": {
                "characters_per_second": 14,  # Slightly slower
                "minimum_duration": 1.2,
                "maximum_duration": 6.5,
                "gap_between_subtitles": 0.25,
                "reading_speed_multiplier": 0.95
            },
            "bhojpuri": {
                "characters_per_second": 14,
                "minimum_duration": 1.2,
                "maximum_duration": 6.5,
                "gap_between_subtitles": 0.25,
                "reading_speed_multiplier": 0.95
            },
            "english": {
                "characters_per_second": 17,
                "minimum_duration": 0.8,
                "maximum_duration": 5.0,
                "gap_between_subtitles": 0.15,
                "reading_speed_multiplier": 1.05
            }
        }
    
    async def generate_subtitles(self, 
                                  scenes: list,
                                  language: str = "hindi",
                                  style_preset: str = "standard_dialogue") -> str:
        """
        Generate complete subtitle file from scenes
        
        Args:
            scenes: List of scene dictionaries with text and timing
            language: Primary language (hindi/haryanvi/bhojpuri/english)
            style_preset: Subtitle style preset
            
        Returns:
            Path to generated subtitle file (.ass format)
        """
        self.logger.info(f"📝 Generating {language} subtitles for {len(scenes)} scenes")
        
        try:
            # Get language-specific configs
            font_config = self.font_configs.get(language, self.font_configs["hindi"])
            timing_rule = self.timing_rules.get(language, self.timing_rules["hindi"])
            base_style = self.subtitle_styles.get(style_preset, self.subtitle_styles["standard_dialogue"])
            
            # Generate subtitle events
            subtitle_events = await self._generate_subtitle_events(scenes, timing_rule, base_style)
            
            # Create ASS subtitle file
            output_path = self.config.OUTPUT_PATH / f"subtitles_{language}.ass"
            
            await self._write_ass_file(output_path, subtitle_events, font_config, base_style)
            
            self.logger.success(f"✅ Subtitles generated: {output_path.name}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Subtitle generation failed: {e}")
            raise
    
    async def _generate_subtitle_events(self, 
                                         scenes: list,
                                         timing_rule: dict,
                                         base_style: dict) -> list:
        """Generate timed subtitle events from scenes"""
        
        events = []
        current_time = 0.0
        
        for i, scene in enumerate(scenes):
            try:
                text = scene.get("text", "")
                emotion = scene.get("emotion", "neutral")
                duration = scene.get("duration_estimate", 3.0)
                
                # Skip empty dialogue
                if not text or len(text.strip()) < 2:
                    continue
                
                # Calculate optimal duration based on text length
                char_count = len(text)
                calculated_duration = char_count / timing_rule["characters_per_second"]
                
                # Clamp duration within acceptable range
                final_duration = max(
                    timing_rule["minimum_duration"],
                    min(timing_rule["maximum_duration"], calculated_duration)
                )
                
                # Use scene duration if provided and reasonable
                if duration > 0:
                    final_duration = min(final_duration, duration * 0.9)  # Leave some margin
                
                # Determine style based on emotion/intensity
                event_style = self._select_style_for_emotion(emotion, base_style)
                
                # Format text for ASS (handle line breaks)
                formatted_text = self._format_subtitle_text(text, emotion)
                
                # Create subtitle event
                start_time = current_time + timing_rule["gap_between_subtitles"]
                end_time = start_time + final_duration
                
                event = {
                    "start": start_time,
                    "end": end_time,
                    "text": formatted_text,
                    "style": event_style,
                    "scene_number": i + 1,
                    "emotion": emotion
                }
                
                events.append(event)
                
                # Update current time
                current_time = end_time
                
            except Exception as e:
                self.logger.error(f"Subtitle event generation failed for scene {i}: {e}")
                continue
        
        self.logger.info(f"Generated {len(events)} subtitle events")
        return events
    
    def _select_style_for_emotion(self, emotion: str, base_style: dict) -> dict:
        """Select appropriate subtitle style based on emotion"""
        
        emotion_style_map = {
            "joy": "standard_dialogue",
            "sadness": "emotional_emphasis",
            "anger": "shout_exclamation",
            "fear": "emotional_emphasis",
            "surprise": "shout_exclamation",
            "love": "emotional_emphasis",
            "whisper": "whisper_internal",
            "song": "song_lyrics",
            "neutral": "standard_dialogue"
        }
        
        style_name = emotion_style_map.get(emotion, "standard_dialogue")
        return self.subtitle_styles.get(style_name, base_style)
    
    def _format_subtitle_text(self, text: str, emotion: str) -> str:
        """Format text with ASS tags for styling"""
        
        # Escape special ASS characters
        text = text.replace("{", "\\{").replace("}", "\\}")
        text = text.replace("\\", "\\\\")
        
        # Add emphasis tags based on emotion
        if emotion in ["anger", "shout"]:
            text = f"{{\\b1}}{text}{{\\b0}}"  # Bold
        elif emotion in ["whisper", "internal"]:
            text = f"{{\\i1}}{text}{{\\i0}}"  # Italic
        elif emotion in ["sadness", "love"]:
            text = f"{{\\q2}}{text}"  # Better line breaks
        
        # Handle natural pauses (add line breaks)
        pause_markers = ["।", ".", "?", "!", "..."]
        for marker in pause_markers:
            if marker in text and len(text) > 60:
                # Split at natural pause
                parts = text.split(marker, 1)
                if len(parts) == 2 and len(parts[0]) > 20:
                    text = f"{parts[0]}{marker}\\N{parts[1]}"
                    break
        
        return text
    
    async def _write_ass_file(self, 
                               output_path: str,
                               events: list,
                               font_config: dict,
                               base_style: dict):
        """Write ASS subtitle file with headers and events"""
        
        ass_content = []
        
        # ASS File Header
        ass_content.append("[Script Info]")
        ass_content.append("; MOKSHA AI - Professional Subtitles")
        ass_content.append(f"Title: MOKSHA Video Subtitles")
        ass_content.append(f"ScriptType: v4.00+")
        ass_content.append(f"PlayResX: 1920")
        ass_content.append(f"PlayResY: 1080")
        ass_content.append(f"Timer: 100.0000")
        ass_content.append("")
        
        # Styles Section
        ass_content.append("[V4+ Styles]")
        ass_content.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
        
        # Add base style
        style_line = (
            f"Style: Default,"
            f"{font_config['primary_font']},"
            f"{base_style['font_size']},"
            f"&H00FFFFFF,"  # Primary (white)
            f"&H000000FF,"  # Secondary
            f"&H00000000,"  # Outline (black)
            f"&H00000000,"  # Back
            f"{-1 if base_style['bold'] else 0},"  # Bold
            f"{-1 if base_style['italic'] else 0},"  # Italic
            "0,0,100,100,0,0,1,"
            f"{base_style['outline_width']},"
            f"{base_style['shadow_offset']},"
            f"{base_style['alignment']},"
            f"{base_style['margin_horizontal']},"
            f"{base_style['margin_horizontal']},"
            f"{base_style['margin_vertical']},"
            "0"
        )
        ass_content.append(style_line)
        ass_content.append("")
        
        # Events Section
        ass_content.append("[Events]")
        ass_content.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")
        
        # Add subtitle events
        for event in events:
            start_time = self._seconds_to_ass_time(event["start"])
            end_time = self._seconds_to_ass_time(event["end"])
            
            effect_tags = []
            if "special_effect" in event["style"]:
                effect_tags.append(event["style"]["special_effect"])
            
            effect_str = ",".join(effect_tags) if effect_tags else ""
            
            event_line = (
                f"Dialogue: 0,"
                f"{start_time},"
                f"{end_time},"
                f"Default,"
                f"Scene_{event['scene_number']},"
                f"0,0,0,"
                f"{effect_str},"
                f"{event['text']}"
            )
            ass_content.append(event_line)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write('\n'.join(ass_content))
    
    def _seconds_to_ass_time(self, seconds: float) -> str:
        """Convert seconds to ASS time format (H:MM:SS.cc)"""
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centiseconds = int((seconds % 1) * 100)
        
        return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"
    
    async def burn_subtitles(self, video_path: str, subtitle_path: str) -> str:
        """Burn subtitles into video using FFmpeg"""
        
        self.logger.info(f"🔥 Burning subtitles to video")
        
        output_path = self.config.TEMP_PATH / f"subtitled_{Path(video_path).name}"
        
        # Convert .ass to .ssa for better FFmpeg compatibility
        cmd = [
            self.config.FFMPEG_PATH,
            "-i", video_path,
            "-vf", f"ass={subtitle_path}",
            "-c:a", "copy",
            "-preset", "medium",
            "-crf", "18",
            "-y",
            str(output_path)
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            raise Exception(f"Subtitle burning failed: {result.stderr}")
        
        self.logger.success(f"✅ Subtitles burned: {output_path.name}")
        return str(output_path)


# Test function
async def test_subtitle_engine():
    """Test subtitle engine"""
    engine = SubtitleEngine()
    
    print("\n📝 Testing Subtitle Engine")
    print("="*70)
    
    # Mock scenes
    test_scenes = [
        {"text": "नमस्ते दोस्तों! आज हम बात करेंगे एक महत्वपूर्ण विषय की।", "emotion": "neutral", "duration_estimate": 4},
        {"text": "यह सच में बहुत दुखद घटना है।", "emotion": "sadness", "duration_estimate": 3},
        {"text": "तुमने ऐसा क्यों किया?! मुझे बहुत गुस्सा आ रहा है!", "emotion": "anger", "duration_estimate": 4},
        {"text": "[whispering] मैं तुमसे प्यार करती हूँ...", "emotion": "love", "duration_estimate": 3},
        {"text": "क्या यह सच हो सकता है?", "emotion": "surprise", "duration_estimate": 2}
    ]
    
    # Generate Hindi subtitles
    subtitle_path = await engine.generate_subtitles(test_scenes, language="hindi")
    print(f"✅ Hindi subtitles generated: {subtitle_path}")
    
    # Verify file exists
    if Path(subtitle_path).exists():
        print(f"   File size: {Path(subtitle_path).stat().st_size} bytes")
        
        # Show first few lines
        with open(subtitle_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:20]
            print("\n   Preview:")
            for line in lines:
                print(f"   {line.rstrip()}")
    
    print("\n" + "="*70)
    print("✅ Subtitle Engine test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_subtitle_engine())
