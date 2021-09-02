from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from pandas import DataFrame, Series

EMA = lambda close, len: EMAIndicator(close, len).ema_indicator()
xup = lambda left, right=0: (left.shift() < (right.shift() if isinstance(right, Series) else right)) & (left > right)
xdn = lambda left, right=0: (left.shift() > (right.shift() if isinstance(right, Series) else right)) & (left < right)


def strategy(
    data: DataFrame,
    config: dict
) -> DataFrame:
    data['buy_rsi'] = RSIIndicator(data.close, config['buy_rsi_len']).rsi()
    data['buy_fast'] = EMA(data.close, config['buy_fast_len'])
    data['buy_slow'] = EMA(data.close, config['buy_slow_len'])
    macd = data['buy_fast'] - data['buy_slow']
    signal = EMA(macd, config['buy_sig_len'])
    macdas = macd - signal
    sigdas = EMA(macdas, config['buy_sig_len'])
    data['buy_hist'] = macdas - sigdas

    data['sell_rsi'] = RSIIndicator(data.close, config['sell_rsi_len']).rsi()
    data['sell_fast'] = EMA(data.close, config['sell_fast_len'])
    data['sell_slow'] = EMA(data.close, config['sell_slow_len'])
    macd = data['sell_fast'] - data['sell_slow']
    signal = EMA(macd, config['sell_sig_len'])
    macdas = macd - signal
    sigdas = EMA(macdas, config['sell_sig_len'])
    data['sell_hist'] = macdas - sigdas

    data.loc[((data['buy_hist'] > 0) & (data['buy_rsi'] < config['rsi_lb'])), 'buy'] = data.close
    data.loc[((data['sell_hist'] < 0) & (data['sell_rsi'] > config['rsi_ub'])), 'sell'] = data.close
    return data

config_range = {
    'buy_slow_len': [25,50],
    'buy_fast_len': [5,24],
    'buy_sig_len': [1,12],
    'buy_rsi_len': [5,50],
    'sell_slow_len': [25,50],
    'sell_fast_len': [5,24],
    'sell_sig_len': [1,12],
    'sell_rsi_len': [5,50],
    'rsi_lb': [0.0,70.0],
    'rsi_ub': [30.0,100.0],
    "stop_limit_buy": [0.001, 0.01],
    "stop_limit_sell": [0.001, 0.01],
    "stop_limit_loss": [0.001, 0.01],
    'min_ticks': [
        'buy_slow_len',
        'buy_fast_len',
        'buy_sig_len',
        'buy_rsi_len',
        'sell_slow_len',
        'sell_fast_len',
        'sell_sig_len',
        'sell_rsi_len',
    ]
}
