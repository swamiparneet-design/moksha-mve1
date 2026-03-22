"""
RunPod Serverless Handler for MOKSHA MVE-1
Production version - generates real audio with Fish-Speech
"""

import runpod
import os
import sys
from pathlib import Path
import asyncio

async def generate_video(job):
    """
    Production handler - generates audio using Fish-Speech
    """
    import traceback
    
    try:
        print("=" * 50)
        print("🎤 AUDIO GENERATION STARTED")
        print("=" * 50)
        
        # Get input parameters
        input_data = job.get('input', job)
        text = input_data.get('text', 'Test')
        language = input_data.get('language', 'hindi')
        emotion = input_data.get('emotion', 'neutral')
        
        print(f"Text: {text}")
        print(f"Language: {language}")
        print(f"Emotion: {emotion}")
        
        # Import voice engine
        from engines.voice_engine import VoiceEngine
        
        # Initialize voice engine
        voice_engine = VoiceEngine()
        
        # Generate audio (returns cached path automatically)
        output_path = await voice_engine.generate(
            text=text,
            language=language,
            emotion=emotion
        )
        
        print(f"✅ Audio generated: {output_path}")
        
        # Check if file exists
        audio_exists = Path(output_path).exists()
        print(f"Audio file exists: {audio_exists}")
        
        return {
            "id": job.get('id', 'unknown'),
            "input": job,
            "output": {
                "success": True,
                "audio_path": output_path,
                "audio_exists": audio_exists,
                "message": "Audio generation successful"
            }
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            "id": job.get('id', 'unknown'),
            "input": job,
            "output": {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        }


# Start RunPod serverless handler
if __name__ == "__main__":
    runpod.serverless.start({
        "handler": generate_video,
        "reference_counter_interval": 60
    })
