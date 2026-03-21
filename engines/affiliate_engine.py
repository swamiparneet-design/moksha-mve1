"""
AFFILIATE ENGINE - Automatic Affiliate Link Integration
Generates contextual affiliate links based on video topic
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from config import Config


class AffiliateEngine:
    """Automatic affiliate link generator"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.blog_url = self.config.BLOG_URL
        self.affiliate_enabled = self.config.AFFILIATE_ENABLED
        
        # Pre-configured affiliate programs (add more as needed)
        self.affiliate_programs = {
            "technology": {
                "amazon": "https://amzn.to/3xyz123",  # Your Amazon Associates link
                "flipkart": "https://fkrt.it/abc123",  # Your Flipkart Affiliate link
            },
            "books": {
                "amazon_kindle": "https://amzn.to/books123",
                "goodreads": "https://www.goodreads.com/user/yourprofile"
            },
            "software": {
                "hostinger": "https://hostinger.com/?REF=yourid",
                "canva": "https://canva.com/?ref=yourid"
            }
        }
    
    async def generate_links(self, topic: str, language: str = "hindi") -> dict:
        """
        Generate relevant affiliate links based on video topic
        
        Args:
            topic: Video topic
            language: Content language
            
        Returns:
            Dictionary with relevant affiliate links
        """
        self.logger.info(f"🔗 Generating affiliate links for: {topic}")
        
        # Auto-detect category from topic
        category = self._detect_category(topic)
        
        # Get relevant links
        links = self._get_affiliate_links(category)
        
        # Add blog link if available
        if self.blog_url:
            blog_post = await self._find_relevant_blog_post(topic)
            if blog_post:
                links['blog_post'] = blog_post
        
        self.logger.success(f"✅ Generated {len(links)} affiliate links")
        return links
    
    def _detect_category(self, topic: str) -> str:
        """Auto-detect product category from topic"""
        topic_lower = topic.lower()
        
        # Category keywords
        categories = {
            "technology": ["ai", "tech", "software", "computer", "phone", "app", "digital"],
            "books": ["book", "novel", "reading", "author", "story"],
            "software": ["hosting", "website", "design", "tool", "saas"],
            "education": ["course", "learn", "tutorial", "class", "study"],
            "finance": ["money", "invest", "stock", "crypto", "bank"],
            "health": ["health", "fitness", "yoga", "diet", "wellness"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in topic_lower for keyword in keywords):
                return category
        
        return "general"
    
    def _get_affiliate_links(self, category: str) -> dict:
        """Get affiliate links for specific category"""
        links = {
            "category": category,
            "primary": "",
            "secondary": [],
            "disclaimer": "This video contains affiliate links. I may earn a small commission at no extra cost to you."
        }
        
        # Get links from pre-configured programs
        if category in self.affiliate_programs:
            program = self.affiliate_programs[category]
            links["primary"] = list(program.values())[0] if program else ""
            links["secondary"] = list(program.values())[1:] if len(program) > 1 else []
        
        # Fallback to Amazon general
        if not links["primary"]:
            links["primary"] = "https://amzn.to/3xyz123"
        
        return links
    
    async def _find_relevant_blog_post(self, topic: str) -> str:
        """Find or create relevant blog post URL"""
        if not self.blog_url:
            return ""
        
        # Simple URL construction (can be enhanced with actual blog search)
        topic_slug = topic.lower().replace(" ", "-").replace("/", "-")
        return f"{self.blog_url}/blog/{topic_slug}"
    
    def add_custom_affiliate(self, category: str, program_name: str, link: str):
        """Add custom affiliate program"""
        if category not in self.affiliate_programs:
            self.affiliate_programs[category] = {}
        
        self.affiliate_programs[category][program_name] = link
        self.logger.info(f"✅ Added custom affiliate: {program_name} in {category}")


# Quick test
if __name__ == "__main__":
    import asyncio
    
    async def test():
        engine = AffiliateEngine()
        
        # Test different topics
        topics = [
            "Artificial Intelligence",
            "Best Books for Success",
            "Website Hosting Guide",
            "Stock Market Basics"
        ]
        
        for topic in topics:
            print(f"\n📝 Topic: {topic}")
            links = await engine.generate_links(topic)
            print(f"   Category: {links['category']}")
            print(f"   Primary Link: {links['primary']}")
            print(f"   Blog Post: {links.get('blog_post', 'N/A')}")
    
    asyncio.run(test())
