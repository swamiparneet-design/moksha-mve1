"""
MOKSHA MVE-1 - FastAPI Server
REST API for video production pipeline
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from loguru import logger

from config import Config
from main_app import MokshaMVE1


# Initialize FastAPI app
app = FastAPI(
    title="MOKSHA MVE-1",
    description="Elite AI Video Production System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
config = Config()

# Initialize main system
moksha_system = None


class VideoRequest(BaseModel):
    """Request model for video creation"""
    topic: str
    language: Optional[str] = "hindi"
    style: Optional[str] = "educational"
    voice_type: Optional[str] = "male"
    avatar: Optional[bool] = True
    duration_minutes: Optional[int] = 5


class JobStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: str
    message: Optional[str] = None
    video_path: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global moksha_system
    
    logger.info("🚀 Starting MOKSHA MVE-1 server...")
    
    try:
        moksha_system = MokshaMVE1()
        # Initialize all engines immediately
        moksha_system.initialize_engines()
        logger.info("✅ MOKSHA MVE-1 ready!")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "MOKSHA MVE-1",
        "version": "1.0.0",
        "status": "running",
        "api_keys_configured": config.validate_api_keys()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/create-video", response_model=JobStatus)
async def create_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Create a new video from topic
    
    This runs in background to avoid timeout
    """
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    
    logger.info(f"📹 New video request: Job {job_id}")
    logger.info(f"Topic: {request.topic}, Language: {request.language}")
    
    if not moksha_system:
        raise HTTPException(status_code=500, detail="System not initialized")
    
    # Run in background
    background_tasks.add_task(
        process_video_job,
        job_id,
        request
    )
    
    return JobStatus(
        job_id=job_id,
        status="queued",
        message="Video creation started"
    )


async def process_video_job(job_id: str, request: VideoRequest):
    """Process video creation job"""
    try:
        result = await moksha_system.create_video(
            topic=request.topic,
            language=request.language,
            style=request.style,
            voice_type=request.voice_type,
            avatar=request.avatar,
            duration_minutes=request.duration_minutes
        )
        
        logger.success(f"✅ Job {job_id} completed: {result.get('status')}")
        
    except Exception as e:
        logger.error(f"❌ Job {job_id} failed: {e}")


@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job status"""
    # TODO: Implement proper job tracking with Redis
    return JobStatus(
        job_id=job_id,
        status="processing",
        message="Job tracking not yet implemented"
    )


@app.get("/config")
async def get_config():
    """Get current configuration (safe info only)"""
    return {
        "supported_languages": config.SUPPORTED_LANGUAGES,
        "default_language": config.DEFAULT_LANGUAGE,
        "ffmpeg_configured": bool(config.FFMPEG_PATH),
        "redis_configured": bool(config.REDIS_URL),
        "debug_mode": config.DEBUG_MODE
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🎬 MOKSHA MVE-1 Server starting...")
    
    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.DEBUG_MODE
    )
