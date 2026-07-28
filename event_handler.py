import logging
import requests

logger = logging.getLogger(__name__)

def handle_event(api_url: str, payload: dict) -> dict:
    """
    Connect to an external API and process the response.
    Handles unicode characters and potential network timeouts gracefully.
    """
    if not isinstance(api_url, str):
        logger.error("Invalid API URL: must be a string.")
        return {"success": False, "error": "Invalid URL format"}

    try:
        # Gracefully handle potential unicode encoding/decoding issues
        encoded_payload = {}
        for k, v in payload.items():
            if isinstance(v, str):
                encoded_payload[k] = v.encode('utf-8', errors='ignore').decode('utf-8')
            else:
                encoded_payload[k] = v

        response = requests.post(api_url, json=encoded_payload, timeout=10)
        
        # Raise an exception for HTTP error status codes (4xx/5xx)
        response.raise_for_status()
        
        # Parse response safely
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            data = response.json()
        else:
            data = response.text

        return {
            "success": True,
            "status_code": response.status_code,
            "data": data
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to external API: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in event_handler: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Example usage / demo
    logging.basicConfig(level=logging.INFO)
    print(handle_event("https://httpbin.org/post", {"text": "Hello, 🌟 Unicode Test!"}))
