import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings

# Rate limiting storage
request_counts = {}

def add_rate_limiter(app: FastAPI):
    """Add rate limiting middleware to the FastAPI application."""
    
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old requests
        for ip in list(request_counts.keys()):
            request_counts[ip] = [timestamp for timestamp in request_counts[ip] 
                                if current_time - timestamp < settings.RATE_LIMIT_WINDOW]
        
        # Check rate limit
        if client_ip in request_counts:
            if len(request_counts[client_ip]) >= settings.RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Please try again later."}
                )
            request_counts[client_ip].append(current_time)
        else:
            request_counts[client_ip] = [current_time]
        
        response = await call_next(request)
        return response