"""
AUDIO MIXER ENGINE - Professional Sound Engineering
Complete audio post-production with EQ, compression, reverb, and dynamics
Hollywood-level sound quality for Indian content
"""
import subprocess
from pathlib import Path
from loguru import logger
from config import Config


class AudioMixer:
    """Professional audio mixing and mastering engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.ffmpeg_path = self.config.FFMPEG_PATH
        
        # Voice EQ settings (professional standard)
        self.voice_eq = {
            "high_pass_filter": {
                "frequency_hz": 80,
                "slope_db_octave": 12,
                "purpose": "remove_rumble_low_end_noise"
            },
            "low_mid_cut": {
                "frequency_hz": 250,
                "gain_db": -3,
                "q_factor": 1.4,
                "purpose": "reduce_mud_boxiness"
            },
            "presence_boost": {
                "frequency_hz": 5000,
                "gain_db": 3,
                "q_factor": 2.0,
                "purpose": "add_clarity_intelligibility"
            },
            "air_band": {
                "frequency_hz": 12000,
                "gain_db": 2,
                "q_factor": 0.7,
                "purpose": "add_breath_detail_openness"
            }
        }
        
        # Compression settings
        self.compression_settings = {
            "voice": {
                "threshold_db": -18,
                "ratio": 3.0,
                "attack_ms": 5,
                "release_ms": 50,
                "knee_db": 6,
                "makeup_gain_db": 3,
                "purpose": "smooth_vocal_dynamics"
            },
            "bgm_gentle": {
                "threshold_db": -24,
                "ratio": 2.0,
                "attack_ms": 20,
                "release_ms": 100,
                "knee_db": 10,
                "purpose": "gentle_background_control"
            },
            "bgm_aggressive": {
                "threshold_db": -18,
                "ratio": 4.0,
                "attack_ms": 10,
                "release_ms": 50,
                "knee_db": 3,
                "purpose": "strong_ducking_with_voice"
            }
        }
        
        # Reverb presets for different spaces
        self.reverb_presets = {
            "intimate_room": {
                "room_size": 0.3,
                "damping": 0.5,
                "wet_level": 0.15,
                "dry_level": 0.85,
                "width": 0.8,
                "when_to_use": ["bedroom_scenes", "personal_confessions", "close_ups"]
            },
            "medium_hall": {
                "room_size": 0.6,
                "damping": 0.4,
                "wet_level": 0.25,
                "dry_level": 0.75,
                "width": 1.0,
                "when_to_use": ["living_room", "office", "normal_dialogue"]
            },
            "large_hall": {
                "room_size": 0.9,
                "damping": 0.3,
                "wet_level": 0.35,
                "dry_level": 0.65,
                "width": 1.0,
                "when_to_use": ["temple", "auditorium", "grand_spaces"]
            },
            "outdoor": {
                "room_size": 0.1,
                "damping": 0.8,
                "wet_level": 0.05,
                "dry_level": 0.95,
                "width": 0.5,
                "when_to_use": ["outside_scenes", "open_air", "natural_environments"]
            },
            "kitchen": {
                "room_size": 0.4,
                "damping": 0.6,
                "wet_level": 0.2,
                "dry_level": 0.8,
                "width": 0.7,
                "when_to_use": ["kitchen_scenes", "small_tiled_rooms"]
            }
        }
        
        # BGM dynamics processing
        self.bgm_processing = {
            "target_loudness_lufs": -20,
            "voice_priority_frequency_range": [500, 4000],
            "ducking_depth_db": -12,
            "ducking_attack_ms": 100,
            "ducking_release_ms": 300,
            "sidechain_source": "voice_track"
        }
    
    async def mix_audio_layers(self, 
                                voice_path: str,
                                bgm_path: str = None,
                                sfx_paths: list = None,
                                scene_type: str = "indoor") -> str:
        """
        Professional mixing of multiple audio layers
        
        Args:
            voice_path: Main dialogue/voice track
            bgm_path: Background music track
            sfx_paths: List of sound effects
            scene_type: Type of scene for spatial processing
            
        Returns:
            Path to final mixed audio
        """
        self.logger.info(f"🎵 Mixing audio layers for {scene_type} scene")
        
        try:
            # Validate inputs
            if not Path(voice_path).exists():
                raise FileNotFoundError(f"Voice track not found: {voice_path}")
            
            # Step 1: Process voice track (EQ + Compression)
            processed_voice = await self._process_voice(voice_path)
            
            # Step 2: Process BGM (ducking + EQ)
            processed_bgm = None
            if bgm_path and Path(bgm_path).exists():
                processed_bgm = await self._process_bgm(bgm_path, processed_voice)
            
            # Step 3: Add reverb based on scene type
            voice_with_reverb = await self._add_scene_reverb(processed_voice, scene_type)
            
            # Step 4: Mix all layers
            output_path = self.config.TEMP_PATH / f"mixed_audio_{Path(voice_path).stem}.wav"
            
            await self._mix_all_layers(voice_with_reverb, processed_bgm, sfx_paths, output_path)
            
            self.logger.success(f"✅ Audio mixed: {output_path.name}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Audio mixing failed: {e}")
            raise
    
    async def _process_voice(self, voice_path: str) -> str:
        """Apply EQ and compression to voice track"""
        
        self.logger.debug("🎤 Processing voice track (EQ + Compression)")
        
        output_path = self.config.TEMP_PATH / f"processed_voice_{Path(voice_path).stem}.wav"
        
        # Build FFmpeg filter chain for voice processing
        filters = []
        
        # High-pass filter (remove rumble)
        hp = self.voice_eq["high_pass_filter"]
        filters.append(f"highpass=f={hp['frequency_hz']}:slope={hp['slope_db_octave']}")
        
        # Low-mid cut (reduce mud)
        lm = self.voice_eq["low_mid_cut"]
        filters.append(f"equalizer=f={lm['frequency_hz']}:width_type=q:width={lm['q_factor']}:g={lm['gain_db']}")
        
        # Presence boost (add clarity)
        pb = self.voice_eq["presence_boost"]
        filters.append(f"equalizer=f={pb['frequency_hz']}:width_type=q:width={pb['q_factor']}:g={pb['gain_db']}")
        
        # Air band (add openness)
        ab = self.voice_eq["air_band"]
        filters.append(f"equalizer=f={ab['frequency_hz']}:width_type=q:width={ab['q_factor']}:g={ab['gain_db']}")
        
        # Compression
        comp = self.compression_settings["voice"]
        filters.append(
            f"acompressor=threshold={comp['threshold_db']}:ratio={comp['ratio']}:"
            f"attack={comp['attack_ms']}:release={comp['release_ms']}:"
            f"knee={comp['knee_db']}:makeup={comp['makeup_gain_db']}"
        )
        
        # Join filters
        filter_chain = ",".join(filters)
        
        # Run FFmpeg
        cmd = [
            self.ffmpeg_path,
            "-i", voice_path,
            "-af", filter_chain,
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            self.logger.error(f"FFmpeg voice processing failed: {result.stderr}")
            raise Exception(f"Voice processing failed: {result.stderr}")
        
        return str(output_path)
    
    async def _process_bgm(self, bgm_path: str, voice_reference: str) -> str:
        """Process BGM with ducking when voice is present"""
        
        self.logger.debug("🎵 Processing BGM with sidechain ducking")
        
        output_path = self.config.TEMP_PATH / f"processed_bgm_{Path(bgm_path).stem}.wav"
        
        # BGM EQ (cut frequencies where voice sits)
        filters = [
            "equalizer=f=1000:width_type=o:width=2:g=-6",  # Cut 1kHz for voice
            "equalizer=f=2000:width_type=o:width=2:g=-6",  # Cut 2kHz for voice clarity
        ]
        
        # Sidechain compression (ducking)
        duck = self.bgm_processing
        filters.append(
            f"acompressor=threshold={duck['ducking_depth_db']}:"
            f"ratio=4.0:attack={duck['ducking_attack_ms']}:release={duck['ducking_release_ms']}:"
            f"sidechain={voice_reference}"
        )
        
        # Volume normalization
        filters.append("loudnorm=I=-20:TP=-1.5:LRA=7")
        
        filter_chain = ",".join(filters)
        
        cmd = [
            self.ffmpeg_path,
            "-i", bgm_path,
            "-af", filter_chain,
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            self.logger.error(f"BGM processing failed: {result.stderr}")
            return bgm_path  # Fallback to original
        
        return str(output_path)
    
    async def _add_scene_reverb(self, audio_path: str, scene_type: str) -> str:
        """Add appropriate reverb for scene location"""
        
        self.logger.debug(f"🏛️ Adding reverb for: {scene_type}")
        
        # Select reverb preset
        preset = self.reverb_presets.get(scene_type, self.reverb_presets["medium_hall"])
        
        output_path = self.config.TEMP_PATH / f"reverb_audio_{Path(audio_path).stem}.wav"
        
        # Build reverb filter
        reverb_filter = (
            f"aecho=0.8:0.88:{preset['room_size']*100}:{preset['damping']*100}"
        )
        
        # Mix dry and wet signals
        full_filter = f"[0:a]{reverb_filter}[rev];[0:a][rev]mix=weights={preset['dry_level']} {preset['wet_level']}"
        
        cmd = [
            self.ffmpeg_path,
            "-i", audio_path,
            "-af", full_filter,
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            self.logger.warning(f"Reverb processing failed, using dry signal")
            return audio_path
        
        return str(output_path)
    
    async def _mix_all_layers(self, 
                              voice_path: str,
                              bgm_path: str,
                              sfx_paths: list,
                              output_path: str):
        """Mix all audio layers together"""
        
        self.logger.info("🎼 Mixing all audio layers")
        
        # Build input list
        inputs = ["-i", voice_path]
        if bgm_path:
            inputs.extend(["-i", bgm_path])
        
        if sfx_paths:
            for sfx in sfx_paths:
                inputs.extend(["-i", str(sfx)])
        
        # Build mix filter
        num_inputs = 1 + (1 if bgm_path else 0) + (len(sfx_paths) if sfx_paths else 0)
        
        # Simple volume-based mixing
        # Voice: 0dB (reference)
        # BGM: -18dB (background)
        # SFX: -12dB (subtle)
        
        volumes = ["1.0"]  # Voice
        if bgm_path:
            volumes.append("0.125")  # BGM at -18dB
        
        if sfx_paths:
            volumes.extend(["0.25"] * len(sfx_paths))  # SFX at -12dB
        
        # Create amix filter
        mix_filter = f"amix=inputs={num_inputs}:duration=first:dropout_transition=2"
        volume_filter = ",".join([f"[{i}:a]volume={vol}[a{i}]" for i, vol in enumerate(volumes)])
        final_mix = f"{volume_filter};{''.join([f'[a{i}]' for i in range(num_inputs)])}{mix_filter}"
        
        cmd = inputs + ["-filter_complex", final_mix, "-y", str(output_path)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            raise Exception(f"Final mix failed: {result.stderr}")
    
    async def measure_loudness(self, audio_path: str) -> dict:
        """Measure loudness metrics (LUFS, True Peak, etc.)"""
        
        cmd = [
            self.ffmpeg_path,
            "-i", audio_path,
            "-af", "ebur128=peak=true",
            "-f", "null",
            "-"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Parse output for LUFS values
        loudness_info = {
            "integrated_lufs": -20.0,  # Default fallback
            "true_peak_dbtp": -1.0,
            "loudness_range_lu": 5.0
        }
        
        # Extract from FFmpeg output (simplified parsing)
        for line in result.stderr.split('\n'):
            if 'Integrated loudness' in line:
                try:
                    loudness_info['integrated_lufs'] = float(line.split(':')[1].strip())
                except:
                    pass
            elif 'True peak' in line:
                try:
                    loudness_info['true_peak_dbtp'] = float(line.split(':')[1].strip())
                except:
                    pass
        
        return loudness_info


# Test function
async def test_audio_mixer():
    """Test audio mixer with sample files"""
    mixer = AudioMixer()
    
    print("\n🎵 Testing Audio Mixer Engine")
    print("="*70)
    
    # Create test silent audio files
    test_voice = Path("temp/test_voice.wav")
    test_voice.parent.mkdir(exist_ok=True)
    
    # Generate 5-second silent WAV
    import wave
    import struct
    
    sample_rate = 44100
    duration = 5
    
    with wave.open(str(test_voice), 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for _ in range(sample_rate * duration):
            wav.writeframes(struct.pack('h', 0))
    
    print(f"✅ Created test voice file: {test_voice}")
    
    # Test voice processing
    print("\n🎤 Testing voice processing...")
    processed = await mixer._process_voice(str(test_voice))
    print(f"✅ Voice processed: {processed}")
    
    # Test loudness measurement
    print("\n📊 Measuring loudness...")
    loudness = await mixer.measure_loudness(str(test_voice))
    print(f"Loudness: {loudness['integrated_lufs']} LUFS")
    
    print("\n" + "="*70)
    print("✅ Audio Mixer Engine test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_audio_mixer())
