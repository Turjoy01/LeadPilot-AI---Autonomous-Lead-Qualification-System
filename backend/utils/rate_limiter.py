from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_task = None
    
    async def is_allowed(self, key: str, max_requests: int, window_seconds: int = 60) -> bool:
        """Check if request is allowed under rate limit"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    async def cleanup_old_entries(self):
        """Periodically cleanup old entries"""
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            now = datetime.utcnow()
            cutoff = now - timedelta(minutes=10)
            
            keys_to_delete = []
            for key, timestamps in self.requests.items():
                self.requests[key] = [t for t in timestamps if t > cutoff]
                if not self.requests[key]:
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del self.requests[key]


# Global rate limiter instance
rate_limiter = RateLimiter()
