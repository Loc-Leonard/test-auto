import requests # библиотека для http-запросов
import logging # логирование
import sys # запись логов в stdout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://tools-httpstatus.pickup-services.com"

STATUS_CODES = [200, 201, 301, 404, 500]

class HTTPClientError(Exception):
    """Исключения для 4xx"""
    pass

class HTTPServerError(Exception):
    """Исключения для 5xx"""
    pass

def make_request(code: int) -> None:
    url = f"{BASE_URL}/{code}"
    logger.info(f"-> Requesting: GET {url}")

    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        status = response.status_code
        body = response.text.strip() or "(empty body)"

        if 100 <= status <= 399:
            logger.info(f"[OK] Status: {status} | Body: {body[:200]}")
        elif 400 <= status <= 499:
            raise HTTPClientError(
                f"Client error: status={status}, body={body[:200]}"
            )
        elif 500 <= status <= 599:
            raise HTTPServerError(
                f"Server error: status={status}, body={body[:200]}"
            )
    except HTTPClientError as e:
        logger.error(f"[HTTPClientError] {e}")
    except HTTPServerError as e:
        logger.error(f"[HTTPServerError] {e}")
    except requests.RequestException as e:
        logger.error(f"[RequestException] Failed to reach {url}: {e}")

def main():
    logger.info ("=== HTTP Status Checker Starting ===")
    for code in STATUS_CODES:
        make_request(code)
    logger.info("=== HTTP Status Checker Finished ===")

if __name__ == "__main__":
    main()