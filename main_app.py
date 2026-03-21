"""
MOKSHA MVE-1 - Elite AI Video Production System
Main entry point for the application
"""
from loguru import logger
from config import Config

# Configure logging
logger.add(
    "logs/moksha_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG" if Config.DEBUG_MODE else "INFO"
)

class MokshaMVE1:
    """Main orchestrator for video production pipeline v2.0"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.version = "v2.0"
        
        # Initialize engines (will be imported later)
        self.script_engine = None
        self.voice_engine = None
        self.scene_planner = None
        self.video_engine = None
        self.avatar_engine = None
        self.broll_engine = None
        self.layer_engine = None
        self.thumbnail_engine = None
        self.seo_engine = None
        self.upload_engine = None
        
        # Safety engine
        self.safety_enabled = True
        
        self.logger.info(f"🎬 MOKSHA AI MEDIA CORE {self.version} initialized")
        self.logger.info("🛡️ Safety Engine: ENABLED")
        self.logger.info("🚀 Auto Viral Mode: ENABLED")
        
    def initialize_engines(self):
        """Initialize all engines"""
        try:
            from engines.script_engine import ScriptEngine
            from engines.voice_engine import VoiceEngine
            from engines.scene_planner import ScenePlanner
            from engines.video_engine import VideoEngine
            from engines.avatar_engine import AvatarEngine
            from engines.broll_engine import BrollEngine
            from engines.layer_engine import LayerEngine
            from engines.thumbnail_engine import ThumbnailEngine
            from engines.seo_engine import SEOEngine
            from engines.upload_engine import UploadEngine
            
            self.script_engine = ScriptEngine()
            self.voice_engine = VoiceEngine()
            self.scene_planner = ScenePlanner()
            self.video_engine = VideoEngine()
            self.avatar_engine = AvatarEngine()
            self.broll_engine = BrollEngine()
            self.layer_engine = LayerEngine()
            self.thumbnail_engine = ThumbnailEngine()
            self.seo_engine = SEOEngine()
            self.upload_engine = UploadEngine()
            
            self.logger.info("✅ All engines initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Engine initialization failed: {e}")
            raise
    
    async def create_video(
        self,
        topic: str,
        language: str = "hindi",
        style: str = "educational",
        voice_type: str = "male",
        avatar: bool = True,
        duration_minutes: int = 5,
        viral_mode: bool = True,
        safety_check: bool = True
    ):
        """
        Complete video creation pipeline with Auto Viral Mode
        
        Args:
            topic: Video topic
            language: hindi/haryanvi/bhojpuri/hinglish
            style: educational/story/news/vlog
            voice_type: male/female
            avatar: Use avatar or not
            duration_minutes: Target duration in minutes
            viral_mode: Enable auto-viral optimization
            safety_check: Enable content safety
        """
        job_id = f"job_{topic.replace(' ', '_')[:20]}"
        
        self.logger.info(f"🎯 Starting job: {job_id}")
        self.logger.info(f"Topic: {topic}, Language: {language}, Style: {style}")
        
        try:
            # Safety Check
            if safety_check and self.safety_enabled:
                self.logger.info("🛡️ Running safety check...")
                topic = await self._sanitize_topic(topic)
            
            # Step 1: Generate Script with Director Thinking
            self.logger.info("📝 Step 1: Director-level script generation...")
            script = await self.script_engine.generate(
                topic=topic,
                language=language,
                style=style,
                duration_minutes=duration_minutes,
                viral_mode=viral_mode
            )
            
            # Step 2: Plan Scenes with Emotion Flow
            self.logger.info("🎭 Step 2: Scene planning with emotion flow...")
            scenes = await self.scene_planner.plan(
                script=script,
                use_avatar=avatar,
                viral_mode=viral_mode,
                topic=topic  # Pass topic for storage detection
            )
            
            # Step 3: Generate Voice with Natural Breathing
            self.logger.info("🎤 Step 3: Voice generation with natural breathing...")
            for scene in scenes:
                audio_path = await self.voice_engine.generate(
                    text=scene["text"],
                    emotion=scene.get("emotion", "neutral"),
                    language=language,
                    voice_type=voice_type,
                    cache_key=f"{job_id}_scene_{scene['scene']}"
                )
                scene["audio_path"] = audio_path
                # Sync duration
                scene["duration_estimate"] = await self.voice_engine.get_duration(audio_path)
            
            # Step 4: Generate/Get Videos with Parallel Processing
            self.logger.info("🎬 Step 4: Parallel video generation...")
            
            # Check if we should use storage media (devotional/historical topics)
            topic_lower = topic.lower()
            devotional_keywords = ['hanuman', 'temple', 'god', 'puja', 'devotional', 'taj mahal', 'fort', 'palace', 'india', 'history']
            use_storage = any(kw in topic_lower for kw in devotional_keywords)
            
            if use_storage:
                self.logger.info("📁 STORAGE MODE: Using real footage from storage folder")
                # Override scene types to use storage
                for scene in scenes:
                    if scene.get("type") in ["broll", "storage_broll"]:
                        scene["force_storage"] = True
                        self.logger.info(f"🎯 Scene {scene['scene']} marked for storage media")
            
            await self._parallel_video_generation(scenes, job_id)
            
            # Step 5: Layer & Edit with Retention Optimization
            self.logger.info("✂️ Step 5: Editing with retention optimization...")
            final_video_path = await self.layer_engine.compile(
                scenes=scenes,
                output_path=str(self.config.OUTPUT_PATH / f"{job_id}_final.mp4"),
                viral_mode=viral_mode
            )
            
            # Step 6: Generate Thumbnail
            self.logger.info("🖼️ Step 6: Creating thumbnail...")
            thumbnail_path = await self.thumbnail_engine.generate(
                video_path=final_video_path,
                topic=topic,
                language=language
            )
            
            # Step 7: Generate SEO Data
            self.logger.info("📊 Step 7: Generating SEO data...")
            seo_data = await self.seo_engine.generate(
                topic=topic,
                language=language,
                style=style,
                duration_minutes=duration_minutes
            )
            
            # Step 8: Upload to YouTube
            self.logger.info("📤 Step 8: Uploading to YouTube...")
            upload_result = await self.upload_engine.upload(
                video_path=final_video_path,
                thumbnail_path=thumbnail_path,
                seo_data=seo_data
            )
            
            self.logger.success(f"✅ Job completed: {job_id}")
            self.logger.success(f"Final video: {final_video_path}")
            
            return {
                "job_id": job_id,
                "status": "success",
                "video_path": final_video_path,
                "thumbnail_path": thumbnail_path,
                "seo_data": seo_data,
                "upload_result": upload_result,
                "version": self.version,
                "viral_mode": viral_mode
            }
            
        except Exception as e:
            self.logger.error(f"❌ Job failed: {job_id} - {str(e)}")
            return {
                "job_id": job_id,
                "status": "error",
                "error": str(e),
                "version": self.version
            }
    
    async def _parallel_video_generation(self, scenes: list, job_id: str):
        """Generate videos in parallel for speed optimization"""
        import asyncio
        
        tasks = []
        for scene in scenes:
            if scene["type"] == "avatar":
                task = self.avatar_engine.generate(scene=scene, job_id=job_id)
            elif scene["type"] == "broll" or scene.get("force_storage"):
                # Use storage media if force_storage flag is set
                if scene.get("force_storage"):
                    self.logger.info(f"📁 Forcing storage usage for scene {scene['scene']}")
                    # Pass special keyword to trigger storage in broll_engine
                    scene["keyword"] = f"__STORAGE_FORCE__{scene.get('keyword', '')}"
                task = self.broll_engine.get_footage(
                    keyword=scene.get("keyword", ""),
                    duration=scene.get("duration_estimate", 5)
                )
            else:
                task = self.video_engine.generate(
                    prompt=scene.get("prompt", ""),
                    duration=scene.get("duration_estimate", 5)
                )
            tasks.append(task)
        
        # Parallel execution
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Assign results
        for i, scene in enumerate(scenes):
            if isinstance(results[i], str):
                scene["video_path"] = results[i]
            else:
                self.logger.error(f"Scene {i} video generation failed")
                scene["video_path"] = None
    
    async def _sanitize_topic(self, topic: str) -> str:
        """Sanitize topic for family-safe content"""
        # TODO: Implement safety filter
        return topic


if __name__ == "__main__":
    # Test initialization
    moksha = MokshaMVE1()
    print("MOKSHA MVE-1 Ready! 🚀")
    print(f"API Keys Status: {Config.validate_api_keys()}")
