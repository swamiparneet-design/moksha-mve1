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
    try:
        # Check volume and models
        volume_exists = Path('/runpod-volume').exists()
        models_exist = Path('/runpod-volume/checkpoints/s2-pro').exists()
        
        files = []
        if models_exist:
            files = [f.name for f in Path('/runpod-volume/checkpoints/s2-pro').iterdir()]
        
        return {
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
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# Start RunPod serverless handler
if __name__ == "__main__":
    runpod.serverless.start({
        "handler": generate_video,
        "reference_counter_interval": 60
    })
