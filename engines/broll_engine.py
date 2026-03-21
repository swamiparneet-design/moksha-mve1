"""
B-ROLL ENGINE - Pexels API Integration
Fetches free stock footage for scenes
"""
import hashlib
from pathlib import Path
from loguru import logger
from config import Config


class BrollEngine:
    """B-roll footage engine using Pexels API"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.cache_dir = self.config.CACHE_PATH / "broll"
        self.api_key = self.config.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com/videos"
    
    async def get_footage(self, keyword: str, duration: int = 5, orientation: str = "landscape", cache: bool = True) -> str:
        """Get B-roll footage - prioritize Hanuman/devotional content for storage"""
        import os
        
        self.logger.info(f"🔍 Getting footage for: {keyword}")
        
        # Check if FORCE_STORAGE flag is present
        force_storage = "__STORAGE_FORCE__" in keyword
        if force_storage:
            self.logger.info("⚡ STORAGE FORCE MODE ACTIVATED")
            keyword = keyword.replace("__STORAGE_FORCE__", "")
        
        # ALWAYS check storage folder first (production mode)
        storage_dir = self.config.STORAGE_PATH
        self.logger.info(f"📁 Checking storage: {storage_dir.absolute()}")
        
        if storage_dir.exists():
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            
            storage_videos = [f for f in storage_dir.iterdir() 
                             if f.is_file() and f.suffix.lower() in video_extensions]
            storage_images = [f for f in storage_dir.iterdir() 
                             if f.is_file() and f.suffix.lower() in image_extensions]
            
            self.logger.info(f"📊 Storage scan: {len(storage_videos)} videos, {len(storage_images)} images")
            
            # PRIORITY 1: Hanuman/devotional videos for devotional topics
            if force_storage or any(kw in keyword.lower() for kw in ['hanuman', 'god', 'temple', 'puja', 'devotional']):
                hanuman_videos = [f for f in storage_videos if 'hanuman' in f.name.lower() or 'god' in f.name.lower()]
                if hanuman_videos:
                    selected_video = hanuman_videos[0]  # Use first Hanuman video
                    self.logger.info(f"✅ PRIORITY: Using Hanuman/devotional video: {selected_video.name}")
                    return str(selected_video)
            
            # PRIORITY 2: Any storage video
            if storage_videos or storage_images:
                self.logger.info(f"📁 Found {len(storage_videos)} videos and {len(storage_images)} images in storage")
                
                if storage_videos:
                    # Prefer larger/higher quality videos
                    sorted_videos = sorted(storage_videos, key=lambda x: x.stat().st_size, reverse=True)
                    selected_video = sorted_videos[hash(keyword) % len(sorted_videos)]
                    self.logger.info(f"✅ Using storage video: {selected_video.name} ({round(selected_video.stat().st_size/1024, 1)}KB)")
                    return str(selected_video)
                elif storage_images:
                    selected_image = storage_images[hash(keyword) % len(storage_images)]
                    self.logger.info(f"✅ Converting storage image to video: {selected_image.name}")
                    cache_hash = self._generate_cache_hash(keyword, 'storage')
                    return await self._image_to_video_ffmpeg(str(selected_image), duration, cache_hash)
        
        # No storage media - fallback to Pexels or placeholder
        cache_key = f"{keyword}_{duration}_{orientation}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cached_video = self._load_from_cache(cache_hash)
        
        if cached_video:
            self.logger.info(f"💾 B-roll loaded from cache: {cache_hash[:8]}")
            return cached_video
        
        self.logger.info(f"🎬 Searching B-roll for: {keyword}")
        
        try:
            if not self.api_key:
                self.logger.warning("⚠️ Pexels API key missing - using placeholder")
                video_path = self._create_placeholder_video(cache_hash, keyword)
            else:
                video_path = await self._search_and_download(
                    keyword, duration, orientation, cache_hash
                )
            
            self._save_to_cache(cache_hash, video_path)
            self.logger.success(f"✅ B-roll obtained: {video_path.name}")
            return str(video_path)
            
        except Exception as e:
            self.logger.error(f"❌ B-roll fetch failed: {e}")
            return str(self._create_placeholder_video(cache_hash, keyword))
    
    async def _search_and_download(
        self,
        keyword: str,
        duration: int,
        orientation: str,
        cache_hash: str
    ) -> Path:
        """Search Pexels and download best match"""
        import aiohttp
        
        headers = {"Authorization": self.api_key}
        params = {
            "query": keyword,
            "per_page": 5,
            "orientation": orientation
        }
        
        async with aiohttp.ClientSession() as session:
            # Search videos
            async with session.get(
                self.base_url + "/search",
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    raise Exception(f"Pexels API error: {response.status}")
                
                data = await response.json()
                
                if not data.get("videos"):
                    self.logger.warning(f"No results for: {keyword}")
                    return self._create_placeholder_video(cache_hash, keyword)
                
                # Find best matching video
                best_video = self._select_best_video(data["videos"], duration)
                
                if not best_video:
                    return self._create_placeholder_video(cache_hash, keyword)
                
                # Download video
                video_url = best_video["video_files"][0]["link"]
                video_path = self.cache_dir / f"{cache_hash}.mp4"
                
                async with session.get(video_url) as video_response:
                    if video_response.status == 200:
                        with open(video_path, 'wb') as f:
                            while True:
                                chunk = await video_response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        
                        self.logger.debug(f"📥 Downloaded: {video_path.name}")
                        return video_path
                    else:
                        raise Exception(f"Download failed: {video_response.status}")
    
    def _select_best_video(self, videos: list, target_duration: int) -> dict:
        """Select best video from search results"""
        
        best_score = 0
        best_video = None
        
        for video in videos:
            score = 0
            
            # Duration match (prefer videos close to target duration)
            video_duration = video.get("duration", 0)
            if video_duration >= target_duration:
                score += 50
            elif video_duration >= target_duration * 0.7:
                score += 30
            
            # Quality check (prefer HD)
            video_files = video.get("video_files", [])
            for vf in video_files:
                if vf.get("quality") == "hd":
                    score += 30
                    break
                elif vf.get("quality") == "sd":
                    score += 10
            
            # Resolution preference
            width = video_files[0].get("width", 0) if video_files else 0
            if width >= 1920:
                score += 20
            elif width >= 1280:
                score += 10
            
            if score > best_score:
                best_score = score
                best_video = video
        
        return best_video
    
    def _create_placeholder_video(self, cache_hash: str, keyword: str) -> Path:
        """Create placeholder video for testing - converts to MP4"""
        from PIL import Image, ImageDraw, ImageFont
        import subprocess
        
        # Create a simple colored frame with text
        width, height = 1920, 1080
        image = Image.new('RGB', (width, height), color=(30, 30, 50))
        draw = ImageDraw.Draw(image)
        
        # Add text
        text = f"B-ROLL PLACEHOLDER\n{keyword.upper()}"
        
        # Try to use default font
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Save as image first
        temp_image = self.cache_dir / f"{cache_hash}_temp.jpg"
        image.save(temp_image)
        
        # Convert to video using FFmpeg
        video_path = self.cache_dir / f"{cache_hash}.mp4"
        cmd = [
            self.config.FFMPEG_PATH,
            "-loop", "1",
            "-i", str(temp_image),
            "-c:v", "libx264",
            "-t", "5",
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080",
            "-y",
            str(video_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            # Clean up temp image
            if temp_image.exists():
                temp_image.unlink()
            self.logger.debug(f"Created placeholder video: {video_path.name}")
            return video_path
        except Exception as e:
            self.logger.error(f"FFmpeg conversion failed: {e}")
            return temp_image  # Fallback to image
    
    async def _image_to_video_ffmpeg(self, image_path: str, duration: int, cache_hash: str) -> str:
        """Convert image to video using FFmpeg"""
        import subprocess
        from pathlib import Path
        
        output_video = self.cache_dir / f"{cache_hash}.mp4"
        cmd = [
            self.config.FFMPEG_PATH,
            "-loop", "1",
            "-i", image_path,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            "-y",
            str(output_video)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and output_video.exists():
                self.logger.info(f"✅ Image converted to video: {output_video.name}")
                return str(output_video)
            else:
                self.logger.error(f"FFmpeg error: {result.stderr}")
                return image_path
        except Exception as e:
            self.logger.error(f"FFmpeg conversion failed: {e}")
            return image_path
    
    def _load_from_cache(self, cache_hash: str) -> str:
        """Load video from cache"""
        cache_files = list(self.cache_dir.glob(f"{cache_hash}.*"))
        if cache_files:
            # Prefer mp4 over jpg
            for ext in ['.mp4', '.mov', '.avi', '.jpg']:
                for f in cache_files:
                    if f.suffix == ext:
                        return str(f)
            return str(cache_files[0])
        return None
    
    def _save_to_cache(self, cache_hash: str, video_path: str):
        """Save video to cache (already saved, just log)"""
        self.logger.debug(f"💾 B-roll cached: {cache_hash[:8]}")
    
    async def search_multiple(
        self,
        keywords: list,
        duration: int = 5
    ) -> list:
        """Search and download multiple B-roll clips"""
        tasks = [
            self.get_footage(keyword, duration)
            for keyword in keywords
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = []
        for i, result in enumerate(results):
            if isinstance(result, str):
                successful.append({
                    "keyword": keywords[i],
                    "path": result
                })
            else:
                self.logger.error(f"B-roll failed for {keywords[i]}: {result}")
        
        return successful
