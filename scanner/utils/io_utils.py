"""
I/O utilities for file operations and caching.
"""

import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


def load_json(filepath: str | Path) -> dict | list:
    """
    Load JSON from file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, filepath: str | Path, indent: int = 2) -> None:
    """
    Save data as JSON to file.
    
    Args:
        data: Data to serialize
        filepath: Output file path
        indent: JSON indentation (default: 2)
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_cache_path(cache_type: str, date: Optional[str] = None) -> Path:
    """
    Get standardized cache file path.
    
    Args:
        cache_type: Type of cache (e.g., 'universe', 'marketcap', 'klines')
        date: Date string (YYYY-MM-DD), defaults to today
        
    Returns:
        Path to cache file
    """
    if date is None:
        from .time_utils import utc_date
        date = utc_date()
    
    cache_dir = Path("data/raw") / date
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return cache_dir / f"{cache_type}.json"


def cache_exists(cache_type: str, date: Optional[str] = None) -> bool:
    """Check if cache file exists for given type and date."""
    return get_cache_path(cache_type, date).exists()


def load_cache(cache_type: str, date: Optional[str] = None) -> Optional[dict | list]:
    """
    Load cached data if exists.
    
    Returns:
        Cached data or None if not found
    """
    cache_path = get_cache_path(cache_type, date)
    if cache_path.exists():
        return load_json(cache_path)
    return None


def save_cache(data: Any, cache_type: str, date: Optional[str] = None) -> None:
    """Save data to cache."""
    cache_path = get_cache_path(cache_type, date)
    save_json(data, cache_path)
