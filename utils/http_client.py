import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    """
    Create a reusable HTTP session with:
    - User-Agent
    - Automatic retries
    - Timeout handled during requests
    """

    session = requests.Session()

    # Identify our scraper politely
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    })

    # Retry temporary HTTP failures
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def get_page(session, url, timeout=10):
    """
    Fetch a webpage using the shared session.
    """

    response = session.get(
        url,
        timeout=timeout
    )

    response.raise_for_status()

    return response