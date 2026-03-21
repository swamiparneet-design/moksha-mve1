"""
RunPod Serverless Handler for MOKSHA MVE-1
Handles video generation requests via Fish-Speech TTS
"""

import runpod
import os
import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/workspace')

def generate_video(job):
    """
    Main handler for video generation requests
    
    Args:
        job (dict): Contains 'input' with text, language, emotion, etc.
    
    Returns:
        dict: Result with audio_path or error message
    """
    import asyncio
    
    async def _generate():
        try:
            # Parse input
            job_input = job.get('input', {})
            text = job_input.get('text', '')
            language = job_input.get('language', 'hindi')
            emotion = job_input.get('emotion', 'neutral')
            voice_type = job_input.get('voice_type', 'male')
            
            if not text:
                return {"error": "No text provided"}
            
            print(f"🎬 Processing request: {text[:50]}...")
            print(f"Language: {language}, Emotion: {emotion}")
            
            # Import voice engine
            from engines.voice_engine import VoiceEngine
            
            # Initialize
            voice_engine = VoiceEngine()
            
            # Generate audio
            cache_key = f"{text}_{language}_{emotion}_{voice_type}"
            audio_path = await voice_engine.generate(
                text=text,
                emotion=emotion,
                language=language,
                voice_type=voice_type,
                cache_key=cache_key
            )
            
            if audio_path and Path(audio_path).exists():
                print(f"✅ Audio generated: {audio_path}")
                return {
                    "success": True,
                    "audio_path": audio_path,
                    "duration": len(audio_path) if hasattr(audio_path, '__len__') else 0
                }
            else:
                return {"error": "Failed to generate audio", "success": False}
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    # Run async function
    return asyncio.run(_generate())


# Start RunPod serverless handler
if __name__ == "__main__":
    runpod.serverless.start({
        "handler": generate_video,
        "reference_counter_interval": 60
    })
