from functools import lru_cache
from config import Settings


@lru_cache
def get_settings():
    """Return the app settings."""
    return Settings()