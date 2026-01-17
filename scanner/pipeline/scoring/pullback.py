"""
Pullback Setup Scoring
======================

Identifies trend continuation after retracement (pullback to support).

Scoring Components:
1. Trend Strength (30%) - Established uptrend (above EMA50)
2. Pullback Depth (25%) - Healthy retracement to EMA20/50
3. Rebound Strength (25%) - Recovery from pullback
4. Volume Pattern (20%) - Volume decrease on pullback, increase on rebound

Penalties:
- Broken trend (below EMA50)
- Low liquidity
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class PullbackScorer:
    """Scores pullback setups (trend continuation)."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize pullback scorer.
        
        Args:
            config: Config dict with 'scoring' section
        """
        # Handle both dict and ScannerConfig object
        if hasattr(config, 'raw'):
            scoring_config = config.raw.get('scoring', {}).get('pullback', {})
        else:
            scoring_config = config.get('scoring', {}).get('pullback', {})
        
        # Thresholds
        self.min_trend_strength = scoring_config.get('min_trend_strength', 5)  # >5% above EMA50
        self.ideal_pullback_depth = scoring_config.get('ideal_pullback_depth', 5)  # 5-10% from EMA20
        self.max_pullback_depth = scoring_config.get('max_pullback_depth', 15)  # <15% (not too deep)
        
        self.min_rebound = scoring_config.get('min_rebound', 3)  # >3% bounce
        self.min_volume_spike = scoring_config.get('min_volume_spike', 1.3)  # 1.3x on rebound
        
        # Component weights
        self.weights = {
            'trend': 0.30,
            'pullback': 0.25,
            'rebound': 0.25,
            'volume': 0.20
        }
        
        logger.info("Pullback Scorer initialized")
    
    def score(
        self,
        symbol: str,
        features: Dict[str, Any],
        quote_volume_24h: float
    ) -> Dict[str, Any]:
        """
        Score a single symbol for pullback setup.
        
        Args:
            symbol: Trading pair
            features: Feature dict with '1d' and '4h'
            quote_volume_24h: 24h volume in USDT
        
        Returns:
            Score dict
        """
        f1d = features.get('1d', {})
        f4h = features.get('4h', {})
        
        # Components
        trend_score = self._score_trend(f1d)
        pullback_score = self._score_pullback(f1d)
        rebound_score = self._score_rebound(f1d, f4h)
        volume_score = self._score_volume(f1d, f4h)
        
        # Weighted total
        raw_score = (
            trend_score * self.weights['trend'] +
            pullback_score * self.weights['pullback'] +
            rebound_score * self.weights['rebound'] +
            volume_score * self.weights['volume']
        )
        
        # Penalties & Flags
        penalties = []
        flags = []
        
        # Broken trend penalty
        dist_ema50 = f1d.get('dist_ema50_pct')
        if dist_ema50 and dist_ema50 < 0:
            penalties.append(('broken_trend', 0.5))
            flags.append('broken_trend')
        
        # Low liquidity
        if quote_volume_24h < 500_000:
            penalties.append(('low_liquidity', 0.8))
            flags.append('low_liquidity')
        
        # Apply penalties
        final_score = raw_score
        for name, factor in penalties:
            final_score *= factor
        
        # Reasons
        reasons = self._generate_reasons(
            trend_score, pullback_score, rebound_score, volume_score,
            f1d, f4h, flags
        )
        
        return {
            'score': round(final_score, 2),
            'components': {
                'trend': round(trend_score, 2),
                'pullback': round(pullback_score, 2),
                'rebound': round(rebound_score, 2),
                'volume': round(volume_score, 2)
            },
            'penalties': {name: factor for name, factor in penalties},
            'flags': flags,
            'reasons': reasons
        }
    
    def _score_trend(self, f1d: Dict[str, Any]) -> float:
        """
        Score trend strength (0-100).
        
        Strong trend = well above EMA50, higher highs.
        """
        score = 0.0
        
        dist_ema50 = f1d.get('dist_ema50_pct')
        
        # Must be above EMA50
        if not dist_ema50 or dist_ema50 < 0:
            return 0.0
        
        # Distance score
        if dist_ema50 >= 15:  # >15% above
            score += 60
        elif dist_ema50 >= 10:
            score += 50
        elif dist_ema50 >= self.min_trend_strength:
            score += 40
        else:
            score += 20
        
        # Higher highs
        if f1d.get('hh_20'):
            score += 40
        
        return min(score, 100.0)
    
    def _score_pullback(self, f1d: Dict[str, Any]) -> float:
        """
        Score pullback depth (0-100).
        
        Ideal: Pullback to EMA20/50 support.
        """
        dist_ema20 = f1d.get('dist_ema20_pct', 100)
        dist_ema50 = f1d.get('dist_ema50_pct', 100)
        
        # Currently near EMA20 (ideal pullback level)
        if -2 <= dist_ema20 <= 2:  # Within 2% of EMA20
            return 100.0
        
        # Near EMA50 (deeper pullback)
        if -2 <= dist_ema50 <= 2:
            return 80.0
        
        # Between EMAs (healthy pullback)
        if dist_ema20 < 0 and dist_ema50 > 0:
            return 60.0
        
        # Above both (no pullback yet)
        if dist_ema20 > 5:
            return 20.0
        
        # Below both (too deep)
        if dist_ema50 < -5:
            return 10.0
        
        return 40.0
    
    def _score_rebound(self, f1d: Dict[str, Any], f4h: Dict[str, Any]) -> float:
        """
        Score rebound strength (0-100).
        
        Recent bounce from pullback low.
        """
        score = 0.0
        
        # 1d momentum
        r3 = f1d.get('r_3', 0)
        
        if r3 >= 10:  # >10% in 3 days
            score += 50
        elif r3 >= self.min_rebound:
            score += 30
        elif r3 > 0:
            score += 10
        
        # 4h momentum (recent)
        r3_4h = f4h.get('r_3', 0)
        
        if r3_4h >= 5:
            score += 50
        elif r3_4h >= 2:
            score += 30
        elif r3_4h > 0:
            score += 10
        
        return min(score, 100.0)
    
    def _score_volume(self, f1d: Dict[str, Any], f4h: Dict[str, Any]) -> float:
        """
        Score volume pattern (0-100).
        
        Ideal: Volume spike on rebound.
        """
        vol_spike_1d = f1d.get('volume_spike', 1.0)
        vol_spike_4h = f4h.get('volume_spike', 1.0)
        
        max_spike = max(vol_spike_1d, vol_spike_4h)
        
        if max_spike < self.min_volume_spike:
            return 0.0
        
        # Strong volume
        if max_spike >= 2.5:
            return 100.0
        
        # Moderate volume
        if max_spike >= 2.0:
            return 80.0
        
        # Linear scale
        ratio = (max_spike - self.min_volume_spike) / (2.0 - self.min_volume_spike)
        return ratio * 70.0
    
    def _generate_reasons(
        self,
        trend_score: float,
        pullback_score: float,
        rebound_score: float,
        volume_score: float,
        f1d: Dict[str, Any],
        f4h: Dict[str, Any],
        flags: List[str]
    ) -> List[str]:
        """Generate human-readable reasons."""
        reasons = []
        
        # Trend
        dist_ema50 = f1d.get('dist_ema50_pct', 0)
        if trend_score > 70:
            reasons.append(f"Strong uptrend ({dist_ema50:.1f}% above EMA50)")
        elif trend_score > 30:
            reasons.append(f"Moderate uptrend ({dist_ema50:.1f}% above EMA50)")
        else:
            reasons.append("Weak/no uptrend")
        
        # Pullback
        dist_ema20 = f1d.get('dist_ema20_pct', 0)
        if pullback_score > 70:
            reasons.append(f"At support level ({dist_ema20:.1f}% from EMA20)")
        elif pullback_score > 40:
            reasons.append("Healthy pullback depth")
        else:
            reasons.append("No clear pullback")
        
        # Rebound
        r3 = f1d.get('r_3', 0)
        if rebound_score > 60:
            reasons.append(f"Strong rebound ({r3:.1f}% in 3d)")
        elif rebound_score > 30:
            reasons.append("Moderate rebound")
        else:
            reasons.append("No rebound yet")
        
        # Volume
        vol_spike = max(f1d.get('volume_spike', 1.0), f4h.get('volume_spike', 1.0))
        if volume_score > 60:
            reasons.append(f"Strong volume ({vol_spike:.1f}x)")
        elif volume_score > 30:
            reasons.append(f"Moderate volume ({vol_spike:.1f}x)")
        
        # Flags
        if 'broken_trend' in flags:
            reasons.append("⚠️ Below EMA50 (trend broken)")
        
        if 'low_liquidity' in flags:
            reasons.append("⚠️ Low liquidity")
        
        return reasons


def score_pullbacks(
    features_data: Dict[str, Dict[str, Any]],
    volumes: Dict[str, float],
    config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Score all symbols for pullback setups and return ranked list.
    
    Args:
        features_data: Dict mapping symbol -> features
        volumes: Dict mapping symbol -> 24h volume
        config: Config dict
    
    Returns:
        List of scored symbols, sorted by score (descending)
    """
    scorer = PullbackScorer(config)
    results = []
    
    logger.info(f"Scoring {len(features_data)} symbols for pullback setups")
    
    for symbol, features in features_data.items():
        volume = volumes.get(symbol, 0)
        
        try:
            score_result = scorer.score(symbol, features, volume)
            
            results.append({
                'symbol': symbol,
                'score': score_result['score'],
                'components': score_result['components'],
                'penalties': score_result['penalties'],
                'flags': score_result['flags'],
                'reasons': score_result['reasons']
            })
            
        except Exception as e:
            logger.error(f"Failed to score {symbol}: {e}")
            continue
    
    # Sort by score (descending)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    logger.info(f"Pullback scoring complete: {len(results)} symbols scored")
    
    return results
