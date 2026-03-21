"""
Audio assets manager for Hanuman Chalisa and devotional content
"""
from pathlib import Path
from loguru import logger


class AudioAssets:
    """Manage pre-recorded devotional audio files"""
    
    def __init__(self):
        self.storage_path = Path("c:/Amar/Project/AI-OS/Mokshya-AI/storage")
        self.logger = logger
        self.hanuman_chalisa_keywords = [
            'hanuman chalisa', 'hanuman ji', 'hanuman', 'bajrang bali',
            'sankat mochan', 'bajrangbali', 'mahavir'
        ]
    
    def get_hanuman_chalisa_audio(self) -> str | None:
        """Find Hanuman Chalisa audio in storage"""
        if not self.storage_path.exists():
            return None
        
        # Search for audio files
        audio_extensions = ['.mp3', '.wav', '.m4a', '.aac']
        
        for ext in audio_extensions:
            for audio_file in self.storage_path.glob(f"*{ext}"):
                # Check if filename contains Hanuman keywords
                if any(kw in audio_file.name.lower() for kw in self.hanuman_chalisa_keywords):
                    self.logger.info(f"✅ Found Hanuman Chalisa audio: {audio_file.name}")
                    return str(audio_file)
        
        self.logger.warning("⚠️ No Hanuman Chalisa audio found in storage")
        return None
    
    def get_devotional_bgm(self) -> str | None:
        """Find devotional background music"""
        if not self.storage_path.exists():
            return None
        
        bgm_keywords = ['bgm', 'instrumental', 'flute', 'temple', 'bell', 'chanting']
        
        for ext in ['.mp3', '.wav', '.m4a']:
            for audio_file in self.storage_path.glob(f"*{ext}"):
                if any(kw in audio_file.name.lower() for kw in bgm_keywords):
                    self.logger.info(f"✅ Found devotional BGM: {audio_file.name}")
                    return str(audio_file)
        
        return None
