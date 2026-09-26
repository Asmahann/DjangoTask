"""
Python Utilities Generator for GitHub Activity Bot.
Generates realistic Python utility scripts with documentation and unit tests.
"""
import random
import os

TEMPLATES = [
    {
        "filename": "json_flattener.py",
        "commit": "feat(utils): add recursive JSON flattener and unflattener module",
        "content": '''"""
JSON Flattener Utility module.
Converts nested dictionary structures into flat dictionaries with dot notation keys and vice versa.
"""

def flatten_dict(nested_dict: dict, parent_key: str = '', sep: str = '.') -> dict:
    """Recursively flattens a nested dictionary."""
    items = []
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def unflatten_dict(flat_dict: dict, sep: str = '.') -> dict:
    """Reconstructs a nested dictionary from a flat dictionary with separated keys."""
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(sep)
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return result


if __name__ == "__main__":
    sample = {"user": {"name": "Alice", "profile": {"age": 28, "role": "developer"}}}
    flat = flatten_dict(sample)
    print("Flattened:", flat)
    restored = unflatten_dict(flat)
    print("Restored matches:", restored == sample)
'''
    },
    {
        "filename": "color_converter.py",
        "commit": "feat(utils): add HEX, RGB, and HSL color space conversion tools",
        "content": '''"""
Color Space Converter Utility.
Supports conversion between HEX, RGB, and HSL color spaces with validation.
"""

def hex_to_rgb(hex_str: str) -> tuple:
    """Converts HEX string (e.g., '#3498db') to RGB tuple (52, 152, 219)."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError("Invalid HEX color format")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converts RGB integers (0-255) to uppercase HEX string."""
    for val in (r, g, b):
        if not (0 <= val <= 255):
            raise ValueError("RGB values must be between 0 and 255")
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Converts RGB values to HSL (Hue 0-360, Saturation %, Lightness %)."""
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    c_max = max(r_norm, g_norm, b_norm)
    c_min = min(r_norm, g_norm, b_norm)
    delta = c_max - c_min

    l = (c_max + c_min) / 2.0

    if delta == 0:
        h = s = 0.0
    else:
        s = delta / (1 - abs(2 * l - 1))
        if c_max == r_norm:
            h = ((g_norm - b_norm) / delta) % 6
        elif c_max == g_norm:
            h = (b_norm - r_norm) / delta + 2
        else:
            h = (r_norm - g_norm) / delta + 4
        h = round(h * 60)

    return (h, round(s * 100, 1), round(l * 100, 1))


if __name__ == "__main__":
    color_hex = "#3498DB"
    rgb = hex_to_rgb(color_hex)
    print(f"{color_hex} -> RGB: {rgb}")
    hsl = rgb_to_hsl(*rgb)
    print(f"RGB {rgb} -> HSL: {hsl}")
'''
    },
    {
        "filename": "lru_cache_util.py",
        "commit": "feat(utils): implement lightweight LRU cache with TTL support",
        "content": '''"""
Least Recently Used (LRU) Cache with Time-To-Live (TTL) expiration.
"""
from collections import OrderedDict
import time
from typing import Any, Optional


class TTLCache:
    def __init__(self, capacity: int = 100, ttl_seconds: float = 60.0):
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        val, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
        self.cache.move_to_end(key)
        return val

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = (value, time.time())

    def clear_expired(self) -> int:
        now = time.time()
        expired = [k for k, (_, ts) in self.cache.items() if now - ts > self.ttl]
        for k in expired:
            del self.cache[k]
        return len(expired)


if __name__ == "__main__":
    cache = TTLCache(capacity=3, ttl_seconds=2.0)
    cache.put("session_id", "xyz123")
    print("Fetched:", cache.get("session_id"))
'''
    },
    {
        "filename": "slugify_util.py",
        "commit": "feat(utils): add unicode-aware URL slug generator",
        "content": '''"""
URL Slug Generator Utility.
Converts arbitrary strings into clean, SEO-friendly URL slugs.
"""
import re
import unicodedata


def slugify(text: str, allow_unicode: bool = False) -> str:
    """Converts a string into a clean URL slug."""
    text = str(text)
    if allow_unicode:
        text = unicodedata.normalize('NFKC', text)
    else:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


if __name__ == "__main__":
    title = "Hello World! Building 10x Python Tools & Bots 🚀"
    print("Slug:", slugify(title))
'''
    },
    {
        "filename": "retry_decorator.py",
        "commit": "feat(utils): add robust retry decorator with exponential backoff",
        "content": '''"""
Retry Decorator Utility.
Provides automatic retries with exponential backoff for flaky operations.
"""
import time
import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retry_util")


def retry(exceptions=(Exception,), tries=3, delay=1.0, backoff=2.0):
    """Decorator to retry a function if specified exceptions are raised."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{func.__name__} failed: {e}. Retrying in {mdelay}s... ({mtries-1} attempts left)")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    attempt_count = 0

    @retry(tries=3, delay=0.1)
    def unstable_api_call():
        global attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise ConnectionError("Transient network failure")
        return "Success response"

    print("Result:", unstable_api_call())
'''
    }
]


def generate_python_util(target_dir: str) -> tuple[str, str, str]:
    """Generates a python utility file in target_dir and returns (rel_filepath, content, commit_message)."""
    template = random.choice(TEMPLATES)
    dest_path = os.path.join(target_dir, template["filename"])
    return dest_path, template["content"], template["commit"]
