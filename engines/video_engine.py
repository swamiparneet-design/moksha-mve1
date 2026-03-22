"""
VIDEO ENGINE - LTX-Video 2.3 Integration (GPU)
Generates high-quality videos from text prompts
Production-ready with RunPod deployment
"""
from pathlib import Path
from loguru import logger
from config import Config
import subprocess
import sys


class VideoEngine:
    """Video generation engine using LTX-Video 2.3 on RunPod GPU"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.api_key = self.config.RUNPOD_API_KEY
        self.endpoint_id = self.config.RUNPOD_ENDPOINT_ID
        self.ltx_video_path = "./LTX-Video"
    
    async def generate(
        self,
        prompt: str,
        duration: int = 5,
        resolution: str = "720p"
    ) -> str:
        """
        Generate video from prompt using LTX-Video 2.3
        
        Args:
            prompt: Video description/prompt
            duration: Duration in seconds
            resolution: 720p/1080p/4K
            
        Returns:
            Path to generated video
        """
        self.logger.info(f"🎬 Generating video with LTX-Video 2.3...")
        
        # Resolution mapping
        res_map = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4K": (3840, 2160)
        }
        width, height = res_map.get(resolution, (1920, 1080))
        
        # Output video path
        output_path = self.config.TEMP_PATH / f"video_{hash(prompt) % 10000}.mp4"
        
        try:
            # LTX-Video inference command
            cmd = [
                sys.executable,
                "sample/edit.py",
                "--prompt", prompt,
                "--output_path", str(output_path),
                "--width", str(width),
                "--height", str(height),
                "--num_frames", str(duration * 24),  # 24 fps
                "--guidance_scale", "7.5",
            ]
            
            self.logger.info(f"🎥 Running LTX-Video: {prompt[:50]}...")
            
            # Run in LTX-Video directory
            result = subprocess.run(
                cmd,
                cwd=self.ltx_video_path,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for longer videos
            )
            
            if result.returncode == 0 and output_path.exists():
                self.logger.success(f"✅ Video generated: {output_path.name}")
                return str(output_path)
            else:
                error_msg = result.stderr or "Unknown error"
                self.logger.error(f"LTX-Video error: {error_msg}")
                raise Exception(f"LTX-Video failed: {error_msg}")
                
        except subprocess.TimeoutExpired:
            self.logger.error("⏱️  LTX-Video timed out")
            raise Exception("LTX-Video timeout (10 minutes)")
        except FileNotFoundError:
            self.logger.warning("⚠️  LTX-Video not found - using fallback")
            return await self._create_fallback_video(prompt, duration, resolution)
        except Exception as e:
            self.logger.error(f"❌ Video generation failed: {e}")
            return await self._create_fallback_video(prompt, duration, resolution)
    
    async def _create_fallback_video(self, prompt: str, duration: int, resolution: str) -> str:
        """Create fallback video with animated text + BGM"""
        width, height = 1920, 1080
        
        # Create cinematic background
        video_path = self.config.TEMP_PATH / f"video_{hash(prompt) % 10000}.mp4"
        
        # FFmpeg command for cinematic text animation
        cmd = [
            self.config.FFMPEG_PATH,
            "-f", "lavfi",
            "-i", f"color=c=black@1:s={width}x{height}:d={duration}",
            "-vf", (
                f"drawtext=text='{prompt[:100]}':"
                "fontsize=48:fontcolor=white:"
                "x=(w-text_w)/2:y=(h-text_h)/2:"
                "enable='between(t,0,3)',"
                "fade=t=in:st=0:d=1,"
                "fade=t=out:st=2:d=1"
            ),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "23",
            "-y",
            str(video_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if video_path.exists():
                self.logger.warning(f"⚠️  Fallback video created: {video_path.name}")
                return str(video_path)
        except Exception as e:
            self.logger.error(f"Fallback failed: {e}")
        
        return None
    
    async def _create_placeholder(self, prompt: str, duration: int) -> str:
        """Legacy placeholder - redirects to fallback"""
        return await self._create_fallback_video(prompt, duration, "1080p")
    
    async def _call_runpod(self, prompt: str, duration: int) -> str:
        """Call RunPod LTX-Video endpoint"""
        import runpod
        
        try:
            self.logger.info(f"☁️  Calling RunPod endpoint: {self.endpoint_id}")
            
            input_data = {
                "prompt": prompt,
                "duration": duration,
                "model": "ltx-video-2.3",
                "resolution": "1080p",
                "fps": 24
            }
            
            # Call RunPod endpoint
            job = runpod.run(endpoint_id=self.endpoint_id, input=input_data)
            result = runpod.get_job_status(job['id'])
            
            if result.get('output', {}).get('video_url'):
                video_url = result['output']['video_url']
                self.logger.success(f"✅ RunPod video generated: {video_url}")
                return video_url
            else:
                self.logger.error(f"RunPod failed: {result}")
                return None
                
        except Exception as e:
            self.logger.error(f"RunPod API error: {e}")
            return None
