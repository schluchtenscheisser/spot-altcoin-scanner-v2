"""
Pipeline Orchestration
======================

Orchestrates the full daily scanning pipeline.
"""

from __future__ import annotations
import logging
from datetime import datetime

from ..config import ScannerConfig
from ..clients.mexc_client import MEXCClient
from ..clients.marketcap_client import MarketCapClient
from ..clients.mapping import SymbolMapper
from .filters import UniverseFilters
from .shortlist import ShortlistSelector
from .ohlcv import OHLCVFetcher
from .features import FeatureEngine
from .scoring.reversal import score_reversals
from .scoring.breakout import score_breakouts
from .scoring.pullback import score_pullbacks
from .output import ReportGenerator
from .snapshot import SnapshotManager

logger = logging.getLogger(__name__)


def run_pipeline(config: ScannerConfig) -> None:
    """
    Orchestrates the full daily pipeline:
    1. Fetch universe (MEXC Spot USDT)
    2. Fetch market cap listings
    3. Run mapping layer
    4. Apply hard filters (market cap, liquidity, exclusions)
    5. Run cheap pass (shortlist)
    6. Fetch OHLCV for shortlist
    7. Compute features (1d + 4h)
    8. Compute scores (breakout / pullback / reversal)
    9. Write reports (Markdown + JSON)
    10. Write snapshot for backtests
    """
    run_mode = config.run_mode
    run_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    use_cache = run_mode in ['fast', 'standard']
    
    logger.info("=" * 80)
    logger.info(f"PIPELINE STARTING - {run_date}")
    logger.info(f"Mode: {run_mode}")
    logger.info("=" * 80)
    
    # Step 1: Fetch universe (MEXC Spot USDT)
    logger.info("\n[1/10] Fetching MEXC universe...")
    mexc = MEXCClient()
    universe = mexc.get_spot_usdt_symbols(use_cache=use_cache)
    logger.info(f"✓ Universe: {len(universe)} USDT pairs")
    
    # Get 24h tickers
    logger.info("  Fetching 24h tickers...")
    tickers = mexc.get_24h_tickers(use_cache=use_cache)
    ticker_map = {t['symbol']: t for t in tickers}
    logger.info(f"  ✓ Tickers: {len(ticker_map)} symbols")
    
    # Step 2: Fetch market cap listings
    logger.info("\n[2/10] Fetching market cap data...")
    cmc = MarketCapClient(api_key=config.cmc_api_key)
    # CMC data loaded inside mapper
    
    # Step 3: Run mapping layer
    logger.info("\n[3/10] Mapping MEXC → CMC...")
    mapper = SymbolMapper(cmc, config)
    mapping_result = mapper.map_universe(universe, use_cache=use_cache)
    logger.info(f"✓ Mapped: {mapping_result['mapped_count']}/{mapping_result['total_count']} "
               f"({mapping_result['mapping_rate']:.1f}%)")
    
    # Prepare data for filters
    symbols_with_data = []
    for symbol in universe:
        if symbol not in mapping_result['mapped']:
            continue
        
        ticker = ticker_map.get(symbol, {})
        mcap_data = mapping_result['mapped'][symbol]
        
        symbols_with_data.append({
            'symbol': symbol,
            'base': symbol.replace('USDT', ''),
            'quote_volume_24h': float(ticker.get('quoteVolume', 0)),
            'market_cap': mcap_data.get('market_cap')
        })
    
    # Step 4: Apply hard filters
    logger.info("\n[4/10] Applying universe filters...")
    filters = UniverseFilters(config.raw)
    filtered = filters.apply_all(symbols_with_data)
    logger.info(f"✓ Filtered: {len(filtered)} symbols")
    
    # Step 5: Run cheap pass (shortlist)
    logger.info("\n[5/10] Creating shortlist...")
    selector = ShortlistSelector(config.raw)
    shortlist = selector.select(filtered)
    logger.info(f"✓ Shortlist: {len(shortlist)} symbols")
    
    # Step 6: Fetch OHLCV for shortlist
    logger.info("\n[6/10] Fetching OHLCV data...")
    ohlcv_fetcher = OHLCVFetcher(mexc, config.raw)
    ohlcv_data = ohlcv_fetcher.fetch_all(shortlist)
    logger.info(f"✓ OHLCV: {len(ohlcv_data)} symbols with complete data")
    
    # Step 7: Compute features (1d + 4h)
    logger.info("\n[7/10] Computing features...")
    feature_engine = FeatureEngine(config.raw)
    features = feature_engine.compute_all(ohlcv_data)
    logger.info(f"✓ Features: {len(features)} symbols")
    
    # Prepare volume map for scoring
    volume_map = {s['symbol']: s['quote_volume_24h'] for s in shortlist}
    
    # Step 8: Compute scores (breakout / pullback / reversal)
    logger.info("\n[8/10] Scoring setups...")
    
    logger.info("  Scoring Reversals...")
    reversal_results = score_reversals(features, volume_map, config.raw)
    logger.info(f"  ✓ Reversals: {len(reversal_results)} scored")
    
    logger.info("  Scoring Breakouts...")
    breakout_results = score_breakouts(features, volume_map, config.raw)
    logger.info(f"  ✓ Breakouts: {len(breakout_results)} scored")
    
    logger.info("  Scoring Pullbacks...")
    pullback_results = score_pullbacks(features, volume_map, config.raw)
    logger.info(f"  ✓ Pullbacks: {len(pullback_results)} scored")
    
    # Step 9: Write reports (Markdown + JSON)
    logger.info("\n[9/10] Generating reports...")
    report_gen = ReportGenerator(config.raw)
    report_paths = report_gen.save_reports(
        reversal_results,
        breakout_results,
        pullback_results,
        run_date
    )
    logger.info(f"✓ Markdown: {report_paths['markdown']}")
    logger.info(f"✓ JSON: {report_paths['json']}")
    
    # Step 10: Write snapshot for backtests
    logger.info("\n[10/10] Creating snapshot...")
    snapshot_mgr = SnapshotManager(config.raw)
    snapshot_path = snapshot_mgr.create_snapshot(
        run_date=run_date,
        universe=[{'symbol': s} for s in universe],
        filtered=filtered,
        shortlist=shortlist,
        features=features,
        reversal_scores=reversal_results,
        breakout_scores=breakout_results,
        pullback_scores=pullback_results,
        metadata={'mode': run_mode}
    )
    logger.info(f"✓ Snapshot: {snapshot_path}")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Date: {run_date}")
    logger.info(f"Universe: {len(universe)} symbols")
    logger.info(f"Filtered: {len(filtered)} symbols")
    logger.info(f"Shortlist: {len(shortlist)} symbols")
    logger.info(f"Features: {len(features)} symbols")
    logger.info(f"\nScored:")
    logger.info(f"  Reversals: {len(reversal_results)}")
    logger.info(f"  Breakouts: {len(breakout_results)}")
    logger.info(f"  Pullbacks: {len(pullback_results)}")
    logger.info(f"\nOutputs:")
    logger.info(f"  Report: {report_paths['markdown']}")
    logger.info(f"  Snapshot: {snapshot_path}")
    logger.info("=" * 80)
