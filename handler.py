"""
RunPod Serverless Handler for MOKSHA MVE-1
Debug version - checks volume and models
"""

import runpod
import os
import sys
from pathlib import Path

def generate_video(job):
    """
    Debug handler to check volume and models
    """
    import traceback
    
    try:
        print("=" * 50)
        print("🔍 HANDLER STARTED")
        print("=" * 50)
        
        # Check volume and models
        print("Checking /runpod-volume...")
        volume_exists = Path('/runpod-volume').exists()
        print(f"Volume exists: {volume_exists}")
        
        print("Checking /runpod-volume/checkpoints/s2-pro...")
        models_exist = Path('/runpod-volume/checkpoints/s2-pro').exists()
        print(f"Models path exists: {models_exist}")
        
        files = []
        if models_exist:
            files = [f.name for f in Path('/runpod-volume/checkpoints/s2-pro').iterdir()]
            print(f"Files found: {len(files)}")
        
        print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        print(f"FISH_SPEECH_MODEL_PATH: {os.environ.get('FISH_SPEECH_MODEL_PATH')}")
        print("=" * 50)
        
        # Return proper RunPod format
        return {
            "id": job.get('id', 'unknown'),
            "input": job,
            "output": {
                "success": True,
                "debug": {
                    "volume_exists": volume_exists,
                    "models_exist": models_exist,
                    "files_count": len(files),
                    "files": files[:5],
                    "python_path": sys.path,
                    "env_vars": {
                        "FISH_SPEECH": os.environ.get('FISH_SPEECH_MODEL_PATH'),
                        "PYTHONPATH": os.environ.get('PYTHONPATH'),
                    }
                }
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
