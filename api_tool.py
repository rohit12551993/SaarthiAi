import logging
import time
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)


def test_api(
    url: str,
    method: str = "GET",
    headers: dict = None,
    params: dict = None,
    body: dict = None,
    timeout: int = 30,
):
    """
    Execute a REST API request.

    Supported Methods:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE
    """

    logger.info("=" * 60)
    logger.info("test_api TOOL CALLED")
    logger.info(f"Method : {method}")
    logger.info(f"URL    : {url}")
    logger.info("=" * 60)

    method = method.upper()

    headers = headers or {}
    params = params or {}
    body = body or {}

    # Validate URL format
    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        return {
            "success": False,
            "url": url,
            "method": method,
            "error": "Invalid URL format. Please provide a complete URL including http:// or https://"
        }

    start = time.time()

    try:

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body if method in ["POST", "PUT", "PATCH"] else None,
            timeout=timeout,
        )

        end = time.time()

        try:
            response_body = response.json()
        except Exception:
            response_body = response.text

        return {
            "success": True,
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "response_time_ms": round((end - start) * 1000),
            "headers": dict(response.headers),
            "response": response_body,
        }

    except requests.exceptions.Timeout as e:

        logger.exception(e)

        return {
            "success": False,
            "url": url,
            "method": method,
            "error": f"Request timed out: {str(e)}"
        }

    except requests.exceptions.ConnectionError as e:

        logger.exception(e)

        return {
            "success": False,
            "url": url,
            "method": method,
            "error": f"Connection error: {str(e)}"
        }

    except requests.exceptions.InvalidURL as e:

        logger.exception(e)

        return {
            "success": False,
            "url": url,
            "method": method,
            "error": f"Invalid URL: {str(e)}"
        }

    except requests.exceptions.RequestException as e:

        logger.exception(e)

        return {
            "success": False,
            "url": url,
            "method": method,
            "error": f"Request failed: {str(e)}"
        }

    except Exception as e:

        logger.exception(e)

        return {
            "success": False,
            "url": url,
            "method": method,
            "error": str(e)
        }
