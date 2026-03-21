"""
VOICE ENGINE - TTS Integration
Converts text to natural Hindi/Haryanvi/Bhojpuri speech
"""
import hashlib
from pathlib import Path
from loguru import logger
from config import Config


class VoiceEngine:
    """Voice generation engine using Svara-TTS or Fish Speech"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.cache_dir = self.config.CACHE_PATH / "voices"
        
        # Language voice models (placeholder for actual TTS integration)
        self.voice_models = {
            "hindi": {"male": "hi_male", "female": "hi_female"},
            "haryanvi": {"male": "hya_male", "female": "hya_female"},
            "bhojpuri": {"male": "bho_male", "female": "bho_female"}
        }
    
    async def generate(
        self,
        text: str,
        emotion: str = "neutral",
        language: str = "hindi",
        voice_type: str = "male",
        cache_key: str = None
    ) -> str:
        """
        Generate voice audio from text with natural pronunciation
        
        Args:
            text: Text to convert to speech
            emotion: excited/sad/angry/happy/neutral
            language: hindi/haryanvi/bhojpuri
            voice_type: male/female
            cache_key: Unique key for caching
            
        Returns:
            Path to generated audio file
        """
        # Create cache key if not provided
        if not cache_key:
            cache_key = f"{text}_{emotion}_{language}_{voice_type}"
        
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cached_audio = self._load_from_cache(cache_hash)
        
        if cached_audio:
            self.logger.info(f"🎤 Voice loaded from cache: {cache_hash[:8]}")
            return cached_audio
        
        # TEXT NORMALIZATION - Convert to natural spoken form
        from engines.text_normalizer import TextNormalizer
        normalizer = TextNormalizer()
        
        display_text, tts_text, pause_points = normalizer.normalize(text, language=language)
        tts_text_with_emotion = normalizer.add_emotion_markers(tts_text, emotion)
        
        self.logger.info(f"📝 Display: {display_text}")
        self.logger.info(f"🔊 TTS: {tts_text_with_emotion}")
        
        # Generate new voice
        self.logger.info(f"🎤 Generating voice: {language} {voice_type} - {emotion}")
        
        try:
            # FISH-SPEECH S2 PRO - Primary TTS (Natural Hindi Voice!)
            self.logger.info("🐟 Using Fish-Speech S2 Pro for natural voice generation")
            
            # Remove emotion markers before passing to Fish-Speech
            clean_tts_text = tts_text.replace('[speed:0.92] ', '').replace('[speed:1.05] ', '')
            
            # Generate with Fish-Speech
            audio_path = await self._generate_fish_speech(
                text=clean_tts_text,
                language=language,
                emotion=emotion,
                output_path=self.cache_dir / f"{cache_hash}.wav"
            )
            
            if audio_path and Path(audio_path).exists():
                self.logger.success(f"✅ Voice generated with Fish-Speech: {Path(audio_path).name}")
                self._save_to_cache(cache_hash, Path(audio_path))
                return str(audio_path)
            else:
                raise Exception("Fish-Speech returned invalid audio")
            
        except Exception as e:
            self.logger.error(f"❌ Voice generation failed: {e}")
            self.logger.warning("⚠️  Falling back to gTTS...")
            
            # FALLBACK TO gTTS (if Fish-Speech fails)
            try:
                from gtts import gTTS
                
                clean_tts_text = tts_text.replace('[speed:0.92] ', '')
                tts = gTTS(text=clean_tts_text, lang='hi', slow=False)
                audio_path = self.cache_dir / f"{cache_hash}.mp3"
                tts.save(str(audio_path))
                
                if audio_path.exists():
                    self.logger.success(f"✅ Voice generated with gTTS (fallback): {audio_path.name}")
                    self._save_to_cache(cache_hash, audio_path)
                    return str(audio_path)
            except Exception as fallback_error:
                self.logger.error(f"❌ Both TTS methods failed: {fallback_error}")
            
            return None
            raise
    
    async def _generate_fish_speech(
        self,
        text: str,
        language: str,
        emotion: str,
        output_path: Path
    ) -> str:
        """
        Generate voice using Fish-Speech S2 Pro
        
        Args:
            text: Text to synthesize
            language: hindi/haryanvi/bhojpuri
            emotion: excited/sad/angry/happy/neutral
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
        """
        import subprocess
        import sys
        
        try:
            self.logger.info(f"🐟 Fish-Speech inference: {text[:50]}...")
            
            # Fish-Speech inference command
            # Note: This will work once models are downloaded
            cmd = [
                sys.executable,
                "-m", "fish_speech.tools.inference",
                "--text", text,
                "--language", language,
                "--emotion", emotion,
                "--output", str(output_path),
                "--checkpoint-path", "checkpoints/s2-pro"
            ]
            
            # Run inference
            result = subprocess.run(
                cmd,
                cwd=r"C:\Amar\Project\AI-OS\Mokshya-AI\fish-speech",
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0 and output_path.exists():
                self.logger.success(f"✅ Fish-Speech completed successfully!")
                return str(output_path)
            else:
                self.logger.error(f"Fish-Speech error: {result.stderr}")
                raise Exception(f"Fish-Speech failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error("⏱️  Fish-Speech inference timed out")
            raise Exception("Fish-Speech timeout (5 minutes)")
        except FileNotFoundError:
            self.logger.warning("⚠️  Fish-Speech not found or models not downloaded yet")
            raise Exception("Fish-Speech not ready - models downloading in progress")
        except Exception as e:
            self.logger.error(f"❌ Fish-Speech inference failed: {e}")
            raise
    
    def _add_emotion_tags(self, text: str, emotion: str) -> str:
        """Add SSML-like emotion tags to text"""
        
        emotion_prefixes = {
            "excited": "<excited>",
            "sad": "<sad>",
            "angry": "<angry>",
            "happy": "<happy>",
            "curious": "<whisper>",
            "serious": "<serious>",
            "neutral": ""
        }
        
        emotion_suffixes = {
            "excited": "</excited>",
            "sad": "</sad>",
            "angry": "</angry>",
            "happy": "</happy>",
            "curious": "</whisper>",
            "serious": "</serious>",
            "neutral": ""
        }
        
        prefix = emotion_prefixes.get(emotion, "")
        suffix = emotion_suffixes.get(emotion, "")
        
        return f"{prefix} {text} {suffix}"
    
    def _create_silent_audio(self, cache_hash: str, word_count: int) -> Path:
        """Create silent audio file for testing (placeholder)"""
        import wave
        import struct
        
        # Calculate duration based on word count (avg 2.5 words/sec for Hindi)
        duration_sec = max(2, int(word_count / 2.5))
        sample_rate = 44100
        num_samples = int(sample_rate * duration_sec)
        
        audio_path = self.cache_dir / f"{cache_hash}.wav"
        
        try:
            # Create a simple WAV file with silence
            with wave.open(str(audio_path), 'w') as wav_file:
                # Set parameters
                n_channels = 1
                sampwidth = 2
                framerate = sample_rate
                n_frames = num_samples
                
                wav_file.setnchannels(n_channels)
                wav_file.setsampwidth(sampwidth)
                wav_file.setframerate(framerate)
                
                # Write silence (zeros)
                for _ in range(num_samples):
                    value = 0  # Silence
                    packed_value = struct.pack('h', value)
                    wav_file.writeframes(packed_value)
            
            self.logger.debug(f"🔇 Silent audio created: {duration_sec}s")
            return audio_path
            
        except Exception as e:
            self.logger.error(f"Failed to create silent audio: {e}")
            raise
    
    async def _call_tts_api(self, text: str, language: str, voice_type: str, emotion: str) -> Path:
        """
        Call external TTS API (Svara-TTS or Fish Speech)
        TODO: Implement actual TTS integration
        """
        # Placeholder for future TTS integration
        # Example endpoints:
        # - Svara-TTS: https://api.svaralabs.com/tts
        # - Fish Speech: Local deployment
        
        self.logger.warning("TTS API not implemented yet - using silent audio")
        cache_hash = hashlib.md5(f"{text}_{language}".encode()).hexdigest()
        return self._create_silent_audio(cache_hash, len(text.split()))
    
    def _load_from_cache(self, cache_hash: str) -> str:
        """Load audio from cache"""
        cache_files = list(self.cache_dir.glob(f"{cache_hash}.*"))
        if cache_files:
            return str(cache_files[0])
        return None
    
    def _save_to_cache(self, cache_hash: str, audio_path: str):
        """Save audio to cache (already saved, just log)"""
        self.logger.debug(f"💾 Voice cached: {cache_hash[:8]}")
    
    async def get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
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
                return float(result.stdout.strip())
        except Exception as e:
            self.logger.warning(f"Duration detection failed: {e}")
        
        # Fallback: estimate from file size (1 sec ≈ 88KB for WAV)
        try:
            file_size = Path(audio_path).stat().st_size
            return file_size / 88200
        except:
            return 5.0  # Default
    
    async def clone_voice(self, reference_audio: str, text: str) -> str:
        """
        Clone voice from reference audio (Fish Speech feature)
        TODO: Implement voice cloning
        """
        self.logger.info(f"🎤 Cloning voice from: {reference_audio}")
        # TODO: Implement Fish Speech voice cloning
        raise NotImplementedError("Voice cloning not implemented yet")
