"""
Test script for CustomPortfolio class
"""

import pandas as pd
import numpy as np
import vectorbtpro as vbt
import matplotlib.pyplot as plt
from scripts.portfolio.custom_portfolio import CustomPortfolio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_functionality():
    """Test basic portfolio functionality"""
    # Generate sample data
    np.random.seed(42)
    price = pd.Series(np.random.randn(100).cumsum() + 100)
    price.index = pd.date_range('2020-01-01', periods=100)
    
    # Generate random entry/exit signals
    entries = pd.Series(False, index=price.index)
    entries.iloc[10] = True  # Buy at index 10
    entries.iloc[40] = True  # Buy at index 40
    entries.iloc[70] = True  # Buy at index 70
    
    exits = pd.Series(False, index=price.index)
    exits.iloc[30] = True  # Sell at index 30
    exits.iloc[60] = True  # Sell at index 60
    exits.iloc[90] = True  # Sell at index 90
    
    # Create regular portfolio
    pf_regular = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D'
    )
    
    # Create CustomPortfolio with no SL/TP (should behave the same)
    pf_custom_no_sltp = CustomPortfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D'
    )
    
    # Test that both portfolios have the same final value
    logger.info(f"Regular portfolio final value: {pf_regular.final_value}")
    logger.info(f"Custom portfolio (no SL/TP) final value: {pf_custom_no_sltp.final_value}")
    assert abs(pf_regular.final_value - pf_custom_no_sltp.final_value) < 0.01
    
    logger.info("Basic portfolio test: PASSED")
    return pf_regular, pf_custom_no_sltp

def test_stop_loss():
    """Test stop loss functionality"""
    # Generate sample data with a price that drops significantly
    price = pd.Series(np.linspace(100, 110, 50).tolist() + np.linspace(110, 90, 20).tolist() + np.linspace(90, 120, 30).tolist())
    price.index = pd.date_range('2020-01-01', periods=100)
    
    # Generate entry signal at the beginning
    entries = pd.Series(False, index=price.index)
    entries.iloc[5] = True  # Buy early
    
    exits = pd.Series(False, index=price.index)
    exits.iloc[95] = True  # Sell at the end
    
    # Create regular portfolio without SL/TP
    pf_regular = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D'
    )
    
    # Create CustomPortfolio with 10% stop loss
    pf_custom_sl = CustomPortfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D',
        stop_loss=0.1  # 10% stop loss
    )
    
    # Test that the SL portfolio has a different (hopefully better) final value
    logger.info(f"Regular portfolio final value: {pf_regular.final_value}")
    logger.info(f"Stop Loss portfolio final value: {pf_custom_sl.final_value}")
    
    # Get the trades
    regular_trades = CustomPortfolio.get_trades_df(pf_regular)
    sl_trades = CustomPortfolio.get_trades_df(pf_custom_sl)
    
    logger.info("Regular portfolio trades:")
    logger.info(regular_trades)
    
    logger.info("Stop Loss portfolio trades:")
    logger.info(sl_trades)
    
    # The SL portfolio should have exited earlier
    assert sl_trades['Exit Time'].iloc[0] < regular_trades['Exit Time'].iloc[0]
    
    logger.info("Stop loss test: PASSED")
    return pf_regular, pf_custom_sl

def test_take_profit():
    """Test take profit functionality"""
    # Generate sample data with a price that rises significantly and then drops
    price = pd.Series(np.linspace(100, 130, 50).tolist() + np.linspace(130, 110, 50).tolist())
    price.index = pd.date_range('2020-01-01', periods=100)
    
    # Generate entry signal at the beginning
    entries = pd.Series(False, index=price.index)
    entries.iloc[5] = True  # Buy early
    
    exits = pd.Series(False, index=price.index)
    exits.iloc[95] = True  # Sell at the end
    
    # Create regular portfolio without SL/TP
    pf_regular = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D'
    )
    
    # Create CustomPortfolio with 20% take profit
    pf_custom_tp = CustomPortfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D',
        take_profit=0.2  # 20% take profit
    )
    
    # Test that the TP portfolio has a different final value
    logger.info(f"Regular portfolio final value: {pf_regular.final_value}")
    logger.info(f"Take Profit portfolio final value: {pf_custom_tp.final_value}")
    
    # Get the trades
    regular_trades = CustomPortfolio.get_trades_df(pf_regular)
    tp_trades = CustomPortfolio.get_trades_df(pf_custom_tp)
    
    logger.info("Regular portfolio trades:")
    logger.info(regular_trades)
    
    logger.info("Take Profit portfolio trades:")
    logger.info(tp_trades)
    
    # The TP portfolio should have exited earlier
    assert tp_trades['Exit Time'].iloc[0] < regular_trades['Exit Time'].iloc[0]
    
    logger.info("Take profit test: PASSED")
    return pf_regular, pf_custom_tp

def test_multiple_columns():
    """Test multiple columns functionality"""
    # Generate sample data for two assets
    np.random.seed(42)
    price1 = pd.Series(np.random.randn(100).cumsum() + 100)
    price2 = pd.Series(np.random.randn(100).cumsum() + 120)
    
    price = pd.DataFrame({
        'ASSET1': price1,
        'ASSET2': price2
    })
    price.index = pd.date_range('2020-01-01', periods=100)
    
    # Generate entry signals
    entries = pd.DataFrame(False, index=price.index, columns=price.columns)
    entries.loc[price.index[10], 'ASSET1'] = True
    entries.loc[price.index[20], 'ASSET2'] = True
    
    exits = pd.DataFrame(False, index=price.index, columns=price.columns)
    exits.loc[price.index[50], 'ASSET1'] = True
    exits.loc[price.index[60], 'ASSET2'] = True
    
    # Create CustomPortfolio with 10% stop loss and 20% take profit
    pf_custom = CustomPortfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D',
        stop_loss=0.1,
        take_profit=0.2
    )
    
    logger.info(f"Multi-asset portfolio final value: {pf_custom.final_value}")
    
    # Get the trades
    trades = CustomPortfolio.get_trades_df(pf_custom)
    logger.info("Multi-asset portfolio trades:")
    logger.info(trades)
    
    # There should be at least one trade per asset
    assert len(trades) >= 2
    
    logger.info("Multiple columns test: PASSED")
    return pf_custom

if __name__ == "__main__":
    logger.info("Testing CustomPortfolio class...")
    
    # Run tests
    pf_regular, pf_custom_no_sltp = test_basic_functionality()
    pf_regular_sl, pf_custom_sl = test_stop_loss()
    pf_regular_tp, pf_custom_tp = test_take_profit()
    pf_multi = test_multiple_columns()
    
    logger.info("All tests PASSED!")
    
    # Create plots but skip the visualization part which causes errors
    try:
        # Save plots to individual files instead of trying to combine them
        pf_regular_sl.plot(title='Regular Portfolio').write_image('regular_portfolio.png')
        logger.info("Regular portfolio plot saved to 'regular_portfolio.png'")
        
        pf_custom_sl.plot(title='Portfolio with 10% Stop Loss').write_image('stop_loss_portfolio.png')
        logger.info("Stop loss portfolio plot saved to 'stop_loss_portfolio.png'")
        
        pf_regular_tp.plot(title='Regular Portfolio').write_image('regular_tp_portfolio.png')
        logger.info("Regular take profit portfolio plot saved to 'regular_tp_portfolio.png'")
        
        pf_custom_tp.plot(title='Portfolio with 20% Take Profit').write_image('take_profit_portfolio.png')
        logger.info("Take profit portfolio plot saved to 'take_profit_portfolio.png'")
        
        pf_multi.plot(title='Multi-Asset Portfolio').write_image('multi_asset_portfolio.png')
        logger.info("Multi-asset portfolio plot saved to 'multi_asset_portfolio.png'")
    except Exception as e:
        logger.warning(f"Could not create plots: {str(e)}")
        logger.info("Skipping plot creation, but all tests passed successfully") 