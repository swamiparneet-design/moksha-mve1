"""
AVATAR ENGINE - LivePortrait Integration (GPU)
Generates talking avatar videos from photo + audio
High-quality lip-sync with natural expressions
"""
from pathlib import Path
from loguru import logger
from config import Config
import subprocess
import sys


class AvatarEngine:
    """Avatar generation engine using LivePortrait for real-time lip-sync"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.api_key = self.config.RUNPOD_API_KEY
        self.liveportrait_path = "./LivePortrait"
        
    async def generate(
        self,
        scene: dict,
        job_id: str,
        reference_photo: str = None
    ) -> str:
        """
        Generate talking avatar video using LivePortrait
        
        Args:
            scene: Scene data with text and audio
            job_id: Job identifier
            reference_photo: Reference photo for avatar (optional)
            
        Returns:
            Path to generated avatar video
        """
        self.logger.info(f"🎭 Generating avatar with LivePortrait...")
        
        # Get audio path from scene
        audio_path = scene.get('audio_path')
        if not audio_path:
            self.logger.error("❌ No audio path provided")
            return await self._create_placeholder(scene, job_id)
        
        # Use reference photo or default avatar
        source_image = reference_photo or "./assets/default_avatar.jpg"
        
        # Output video path
        output_path = self.config.TEMP_PATH / f"avatar_{job_id}_scene{scene['scene']}.mp4"
        
        try:
            # LivePortrait inference command
            cmd = [
                sys.executable,
                "inference.py",
                "--source_image", source_image,
                "--driving_video", audio_path,
                "--output_path", str(output_path),
                "--no_flag_motion",
                "--no_crop",
            ]
            
            self.logger.info(f"🎬 Running LivePortrait: {source_image} + {audio_path}")
            
            # Run in LivePortrait directory
            result = subprocess.run(
                cmd,
                cwd=self.liveportrait_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0 and output_path.exists():
                self.logger.success(f"✅ Avatar generated: {output_path.name}")
                return str(output_path)
            else:
                self.logger.error(f"LivePortrait error: {result.stderr}")
                raise Exception(f"LivePortrait failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error("⏱️  LivePortrait timed out")
            raise Exception("LivePortrait timeout (5 minutes)")
        except FileNotFoundError:
            self.logger.warning("⚠️  LivePortrait not found - using fallback")
            return await self._create_fallback_avatar(scene, job_id)
        except Exception as e:
            self.logger.error(f"❌ Avatar generation failed: {e}")
            return await self._create_fallback_avatar(scene, job_id)
    
    async def _create_fallback_avatar(self, scene: dict, job_id: str) -> str:
        """Create fallback avatar with animated image + audio"""
        import ffmpeg
        
        # Create a simple colored background with text
        width, height = 1920, 1080
        duration = scene.get('duration_estimate', 5)
        
        # Get audio duration if available
        audio_path = scene.get('audio_path')
        if audio_path:
            try:
                import subprocess
                cmd = [
                    self.config.FFPROBE_PATH,
                    "-i", audio_path,
                    "-show_entries", "format=duration",
                    "-v", "quiet",
                    "-of", "csv=p=0"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    duration = float(result.stdout.strip())
            except:
                pass
        
        # Create gradient background
        video_path = self.config.TEMP_PATH / f"avatar_{job_id}_scene{scene['scene']}.mp4"
        
        # FFmpeg command for animated avatar placeholder
        cmd = [
            self.config.FFMPEG_PATH,
            "-f", "lavfi",
            "-i", f"color=c=blue@0.3:s={width}x{height}:d={duration}",
            "-vf", f"drawtext=text='Avatar Scene {scene['scene']}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-y",
            str(video_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if video_path.exists():
                self.logger.warning(f"⚠️  Fallback avatar created: {video_path.name}")
                return str(video_path)
        except Exception as e:
            self.logger.error(f"Fallback failed: {e}")
        
        return None
    
    async def _create_placeholder(self, scene: dict, job_id: str) -> str:
        """Legacy placeholder - redirects to fallback"""
        return await self._create_fallback_avatar(scene, job_id)
    
    async def ensure_consistent_face(self, job_id: str) -> str:
        """Ensure same face across all scenes in a video"""
        # TODO: Implement face consistency logic
        pass
