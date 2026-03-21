"""
Celery Worker for MOKSHA MVE-1
Background task processing with Redis
"""
from celery import Celery
from loguru import logger
import sys

from config import Config

# Initialize configuration
config = Config()

# Create Celery app
celery_app = Celery(
    'moksha_worker',
    broker=config.REDIS_URL,
    backend=config.REDIS_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    worker_prefetch_multiplier=1
)


@celery_app.task(bind=True, max_retries=3)
def create_video_task(
    self,
    topic: str,
    language: str = "hindi",
    style: str = "educational",
    voice_type: str = "male",
    avatar: bool = True,
    duration_minutes: int = 5
):
    """
    Celery task for video creation
    
    Runs in background using worker pool
    """
    from main_app import MokshaMVE1
    
    job_id = self.request.id
    
    logger.info(f"🎬 Starting Celery job: {job_id}")
    logger.info(f"Topic: {topic}, Language: {language}, Style: {style}")
    
    try:
        # Initialize system
        moksha = MokshaMVE1()
        
        # Create video
        result = moksha.create_video(
            topic=topic,
            language=language,
            style=style,
            voice_type=voice_type,
            avatar=avatar,
            duration_minutes=duration_minutes
        )
        
        logger.success(f"✅ Job {job_id} completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Job {job_id} failed: {e}")
        
        # Retry logic
        try:
            raise self.retry(exc=e, countdown=60)
        except:
            logger.error(f"Job {job_id} failed after retries")
            return {
                "job_id": job_id,
                "status": "error",
                "error": str(e)
            }


if __name__ == "__main__":
    logger.info("👷 Starting Celery Worker...")
    logger.info(f"Redis Broker: {config.REDIS_URL}")
    
    # Start worker
    argv = [
        'worker',
        '--loglevel=info',
        f'--broker={config.REDIS_URL}',
        '--concurrency=2'  # Adjust based on CPU cores
    ]
    
    celery_app.worker_main(argv)
