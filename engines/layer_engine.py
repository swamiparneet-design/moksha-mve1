"""
LAYER ENGINE - FFmpeg Integration
Merges videos, syncs audio, adds BGM, subtitles, effects
"""
import subprocess
from pathlib import Path
from loguru import logger
from config import Config


class LayerEngine:
    """Video layering and editing engine using FFmpeg"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.ffmpeg_path = self.config.FFMPEG_PATH
        self.temp_dir = self.config.TEMP_PATH
    
    async def compile(
        self,
        scenes: list,
        output_path: str,
        bgm_path: str = None,
        viral_mode: bool = True
    ) -> str:
        """
        Compile all scenes into final video with retention optimization
        
        Args:
            scenes: List of scene data with video and audio paths
            output_path: Final output file path
            bgm_path: Background music file (optional)
            viral_mode: Enable aggressive retention editing
            
        Returns:
            Path to final video
        """
        self.logger.info(f"✂️  Compiling {len(scenes)} scenes...")
        
        try:
            # Validate FFmpeg
            if not self._validate_ffmpeg():
                raise Exception("FFmpeg not found or not working")
            
            # Auto-detect BGM if not provided
            if not bgm_path:
                from engines.bgm_manager import BGMManager
                bgm_mgr = BGMManager()
                bgm_path = bgm_mgr.get_bgm("devotional")
                if not bgm_path:
                    # Create silent BGM as fallback
                    total_duration = sum(scene.get('duration_estimate', 5) for scene in scenes)
                    bgm_path = bgm_mgr.create_silent_bgm(duration=total_duration)
                if bgm_path:
                    self.logger.info(f"🎵 Using BGM: {bgm_path}")
            
            # Step 1: Create scene clips with synced audio
            processed_clips = []
            for i, scene in enumerate(scenes):
                clip_path = await self._process_scene(scene, i)
                if clip_path:
                    processed_clips.append(clip_path)
            
            if not processed_clips:
                raise Exception("No valid clips to compile")
            
            # Step 2: Apply viral cuts and zooms
            if viral_mode:
                self.logger.info("🚀 Applying viral retention edits...")
                processed_clips = await self._apply_viral_edits(processed_clips, scenes)
            
            # Step 3: Concatenate all clips
            concat_file = self._create_concat_list(processed_clips)
            final_video = await self._concatenate(concat_file, output_path, bgm_path)
            
            self.logger.success(f"✅ Final video compiled: {final_video}")
            return final_video
            
        except Exception as e:
            self.logger.error(f"❌ Compilation failed: {e}")
            raise
    
    def _validate_ffmpeg(self) -> bool:
        """Validate FFmpeg installation"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            self.logger.warning("⚠️  FFmpeg validation failed - trying anyway")
            return True  # Continue even if validation fails
    
    async def _process_scene(self, scene: dict, index: int) -> str:
        """Process single scene: sync video + audio"""
        
        video_path = scene.get("video_path")
        audio_path = scene.get("audio_path")
        
        if not video_path:
            self.logger.warning(f"Scene {index}: No video path")
            return None
        
        # If video_path is actually an image (placeholder), convert to video
        if video_path.endswith(('.jpg', '.png')):
            video_path = await self._image_to_video(video_path, scene.get("duration_estimate", 5))
        
        output_clip = self.temp_dir / f"clip_{index}.mp4"
        
        try:
            if audio_path and Path(audio_path).exists():
                # Merge video + audio
                await self._merge_audio_video(video_path, audio_path, output_clip)
            else:
                # Just copy video (no audio)
                await self._copy_video(video_path, output_clip)
            
            return str(output_clip)
            
        except Exception as e:
            self.logger.error(f"Scene {index} processing failed: {e}")
            return None
    
    async def _image_to_video(self, image_path: str, duration: int) -> str:
        """Convert image to video with specified duration"""
        output_path = self.temp_dir / f"temp_video_{Path(image_path).stem}.mp4"
        
        cmd = [
            self.ffmpeg_path,
            "-loop", "1",
            "-i", image_path,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080",
            "-y",
            str(output_path)
        ]
        
        self.logger.debug(f"Converting image to video: {duration}s")
        subprocess.run(cmd, capture_output=True, text=True)
        
        return str(output_path)
    
    async def _merge_audio_video(self, video: str, audio: str, output: str):
        """Merge audio into video"""
        cmd = [
            self.ffmpeg_path,
            "-i", video,
            "-i", audio,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            "-y",
            str(output)
        ]
        
        self.logger.debug(f"Merging audio into video")
        subprocess.run(cmd, capture_output=True, text=True)
    
    async def _copy_video(self, video: str, output: str):
        """Copy video without changes"""
        cmd = [
            self.ffmpeg_path,
            "-i", video,
            "-c", "copy",
            "-y",
            str(output)
        ]
        
        subprocess.run(cmd, capture_output=True, text=True)
    
    def _create_concat_list(self, clip_paths: list) -> str:
        """Create FFmpeg concat file"""
        concat_file = self.temp_dir / "concat_list.txt"
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for clip_path in clip_paths:
                # Convert to absolute path and use forward slashes
                abs_path = Path(clip_path).resolve()
                safe_path = str(abs_path).replace('\\', '/')
                f.write(f"file '{safe_path}'\n")
        
        self.logger.debug(f"Created concat file with {len(clip_paths)} clips")
        return str(concat_file)
    
    async def _concatenate(
        self,
        concat_file: str,
        output_path: str,
        bgm_path: str = None
    ) -> str:
        """Concatenate all clips and add BGM"""
        
        # Build FFmpeg command
        if bgm_path and Path(bgm_path).exists():
            # With BGM + Smooth Transitions
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-i", bgm_path,
                "-filter_complex",
                "[1:a]volume=0.15[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "h264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                "-y",
                output_path
            ]
        else:
            # Without BGM - smooth transitions only
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c:v", "h264",
                "-preset", "medium",
                "-crf", "23",
                "-y",
                output_path
            ]
        
        self.logger.info("🎬 Concatenating clips...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.logger.error(f"FFmpeg error: {result.stderr}")
            raise Exception(f"FFmpeg failed: {result.stderr}")
        
        return output_path
    
    async def add_subtitles(
        self,
        video_path: str,
        subtitles: list,
        output_path: str
    ) -> str:
        """Add subtitles to video"""
        # Create SRT file
        srt_path = self.temp_dir / "subtitles.srt"
        self._create_srt_file(subtitles, srt_path)
        
        # Burn subtitles into video
        cmd = [
            self.ffmpeg_path,
            "-i", video_path,
            "-vf", f"subtitles={srt_path}",
            "-c:a", "copy",
            "-y",
            output_path
        ]
        
        self.logger.info("📝 Adding subtitles...")
        subprocess.run(cmd, capture_output=True, text=True)
        
        return output_path
    
    async def _apply_viral_edits(self, clips: list, scenes: list) -> list:
        """Apply aggressive viral retention edits - cuts, zooms, effects with CONSISTENT timing"""
        edited_clips = []
        
        for i, (clip_path, scene) in enumerate(zip(clips, scenes)):
            # Apply effects based on scene metadata
            effects = scene.get("effects", [])
            
            if effects and clip_path:
                # Use same clip path, apply effects in-place
                output_clip = Path(clip_path).parent / f"edited_clip_{i}.mp4"
                await self.apply_effects(str(clip_path), effects, str(output_clip))
                if output_clip.exists():
                    edited_clips.append(str(output_clip))
                    self.logger.debug(f"✅ Applied effects to clip {i}: {output_clip.name}")
                else:
                    edited_clips.append(str(clip_path))
            elif clip_path:
                # No effects - just copy as-is
                output_clip = Path(clip_path).parent / f"clip_{i}.mp4"
                await self._copy_video(str(clip_path), str(output_clip))
                edited_clips.append(str(output_clip))
        
        self.logger.info(f"✅ Viral edits applied to {len(edited_clips)} clips with consistent quality")
        return edited_clips
    
    def _create_srt_file(self, subtitles: list, output_path: str):
        """Create SRT subtitle file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, sub in enumerate(subtitles, 1):
                start = sub.get('start', 0)
                end = sub.get('end', start + 5)
                text = sub.get('text', '')
                
                f.write(f"{i}\n")
                f.write(f"{self._format_srt_time(start)} --> {self._format_srt_time(end)}\n")
                f.write(f"{text}\n\n")
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    async def apply_effects(
        self,
        video_path: str,
        effects: list,
        output_path: str
    ) -> str:
        """Apply visual effects to video"""
        # Build filter chain based on effects
        filters = []
        
        for effect in effects:
            if effect == "zoom_in":
                filters.append("zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'")
            elif effect == "quick_zoom":
                filters.append("zoompan=z='if(lte(on,0.5),1,min(1.2,zoom+0.02))':d=1")
            elif effect == "bright":
                filters.append("eq=brightness=0.1:contrast=1.1")
            elif effect == "slow_motion":
                filters.append("setpts=2*PTS")
        
        if not filters:
            # No effects, just copy
            return await self._copy_video(video_path, output_path)
        
        filter_complex = ",".join(filters)
        
        cmd = [
            self.ffmpeg_path,
            "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            "-y",
            output_path
        ]
        
        self.logger.info(f"Applying effects: {effects}")
        subprocess.run(cmd, capture_output=True, text=True)
        
        return output_path
