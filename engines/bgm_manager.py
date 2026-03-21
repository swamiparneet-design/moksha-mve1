"""
BGM Manager - Background Music Integration
"""
from pathlib import Path
from loguru import logger


class BGMManager:
    """Manage background music for videos"""
    
    def __init__(self):
        self.storage_path = Path("c:/Amar/Project/AI-OS/Mokshya-AI/storage")
        self.logger = logger
        self.bgm_files = {}
        
    def get_bgm(self, mood: str = "devotional") -> str | None:
        """Get BGM file path based on mood"""
        
        # Check storage folder first
        if self.storage_path.exists():
            bgm_keywords = {
                'devotional': ['flute', 'temple', 'bell', 'chanting', 'om', 'bhajan'],
                'emotional': ['sad', 'piano', 'violin', 'ambient'],
                'energetic': ['upbeat', 'fast', 'drums', 'rhythm'],
                'neutral': ['bgm', 'background', 'instrumental']
            }
            
            keywords = bgm_keywords.get(mood, bgm_keywords['neutral'])
            
            for ext in ['.mp3', '.wav', '.m4a']:
                for audio_file in self.storage_path.glob(f"*{ext}"):
                    if any(kw in audio_file.name.lower() for kw in keywords):
                        self.logger.info(f"✅ Found {mood} BGM: {audio_file.name}")
                        return str(audio_file)
        
        # No BGM found
        self.logger.warning(f"⚠️ No {mood} BGM found in storage")
        return None
    
    def create_silent_bgm(self, duration: int = 60) -> str:
        """Create silent BGM (no music) as fallback"""
        from pathlib import Path
        import subprocess
        
        output_path = Path("c:/Amar/Project/AI-OS/Mokshya-AI/temp/silent_bgm.mp3")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create silent audio with FFmpeg
        cmd = [
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(duration),
            "-y",
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.logger.info(f"✅ Created silent BGM: {duration}s")
            return str(output_path)
        except Exception as e:
            self.logger.error(f"Failed to create silent BGM: {e}")
            return None
