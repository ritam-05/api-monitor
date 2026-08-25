import httpx
import time
from typing import Dict, Any

async def check_endpoint(url: str, method: str = "GET", timeout: int = 5) -> Dict[str, Any]:
    """
    Makes an HTTP request to the given URL and measures the response.
    Returns a dictionary with status, timing, and error information.
    """
    start_time = time.time()
    result = {
        "is_success": False,
        "status_code": None,
        "response_time_ms": 0.0,
        "error_message": None
    }
    
    try:
        # We use an async client to prevent blocking the server while waiting for the network
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(method, url)
            result["status_code"] = response.status_code
            # We consider HTTP codes under 400 (like 200 OK or 301 Redirect) as "healthy"
            result["is_success"] = response.status_code < 400
            
    except httpx.TimeoutException:
        result["error_message"] = "Connection timed out"
    except httpx.RequestError as e:
        result["error_message"] = f"Request failed: {str(e)}"
    except Exception as e:
        result["error_message"] = f"Unexpected error: {str(e)}"
        
    end_time = time.time()
    # Calculate response time in milliseconds
    result["response_time_ms"] = round((end_time - start_time) * 1000, 2)
    
    return result