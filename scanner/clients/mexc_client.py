"""
MEXC API Client for Spot market data.

Responsibilities:
- Fetch spot symbol list (exchangeInfo)
- Fetch 24h ticker data (bulk)
- Fetch OHLCV (klines) for specific pairs

API Docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/
"""

import time
from typing import Dict, List, Optional, Any
import requests
from ..utils.logging_utils import get_logger
from ..utils.io_utils import load_cache, save_cache, cache_exists


logger = get_logger(__name__)


class MEXCClient:
    """
    MEXC Spot API client with rate-limit handling and caching.
    """
    
    BASE_URL = "https://api.mexc.com"
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_backoff: float = 3.0,
        timeout: int = 30
    ):
        """
        Initialize MEXC client.
        
        Args:
            max_retries: Maximum retry attempts on failure
            retry_backoff: Seconds to wait between retries
            timeout: Request timeout in seconds
        """
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.timeout = timeout
        self.session = requests.Session()
        
        # Rate limiting (conservative)
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    def _rate_limit(self) -> None:
        """Apply rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint (e.g., '/api/v3/exchangeInfo')
            params: Query parameters
            
        Returns:
            JSON response
            
        Raises:
            requests.RequestException: On persistent failure
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                self._rate_limit()
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    timeout=self.timeout
                )
                
                # Handle rate limit (429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', self.retry_backoff))
                    logger.warning(f"Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_backoff * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"Request failed after {self.max_retries} attempts")
                    raise
        
        raise requests.RequestException("Unexpected error in retry loop")
    
    def get_exchange_info(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get exchange info (symbols, trading rules).
        
        Args:
            use_cache: Use cached data if available (today)
            
        Returns:
            Exchange info dict with 'symbols' list
        """
        cache_key = "mexc_exchange_info"
        
        if use_cache and cache_exists(cache_key):
            logger.info("Loading exchange info from cache")
            return load_cache(cache_key)
        
        logger.info("Fetching exchange info from MEXC API")
        data = self._request("GET", "/api/v3/exchangeInfo")
        
        save_cache(data, cache_key)
        return data
    
    def get_spot_usdt_symbols(self, use_cache: bool = True) -> List[str]:
        """
        Get all Spot USDT trading pairs.
        
        Returns:
            List of symbols (e.g., ['BTCUSDT', 'ETHUSDT', ...])
        """
        exchange_info = self.get_exchange_info(use_cache=use_cache)
        
        symbols = []
        for symbol_info in exchange_info.get("symbols", []):
            # Filter: USDT quote, Spot, Trading status
            # Note: MEXC uses status="1" for enabled (not "ENABLED")
            if (
                symbol_info.get("quoteAsset") == "USDT" and
                symbol_info.get("isSpotTradingAllowed", False) and
                symbol_info.get("status") == "1"
            ):
                symbols.append(symbol_info["symbol"])
        
        logger.info(f"Found {len(symbols)} USDT Spot pairs")
        return symbols
    
    def get_24h_tickers(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get 24h ticker statistics for all symbols (bulk).
        
        Returns:
            List of ticker dicts with keys:
            - symbol
            - lastPrice
            - priceChangePercent
            - quoteVolume
            - volume
            etc.
        """
        cache_key = "mexc_24h_tickers"
        
        if use_cache and cache_exists(cache_key):
            logger.info("Loading 24h tickers from cache")
            return load_cache(cache_key)
        
        logger.info("Fetching 24h tickers from MEXC API")
        data = self._request("GET", "/api/v3/ticker/24hr")
        
        save_cache(data, cache_key)
        logger.info(f"Fetched {len(data)} ticker entries")
        return data
