import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
from datetime import datetime

# Load the historical data
df = pd.read_csv('BTC_2019_2023_1d.csv')  # Replace with your CSV file path

# Parse the 'datetime' column correctly
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d')
df.set_index('datetime', inplace=True)

# Calculate Heikin Ashi Candles
df['HA_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
df['HA_open'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
df['HA_high'] = df[['high', 'HA_open', 'HA_close']].max(axis=1)
df['HA_low'] = df[['low', 'HA_open', 'HA_close']].min(axis=1)

# Calculate technical indicators using the 'ta' library
df['RSI'] = ta.momentum.RSIIndicator(df['HA_close'], window=14).rsi()
macd = ta.trend.MACD(df['HA_close'], window_slow=26, window_fast=12, window_sign=9)
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()
df['MACD_Hist'] = macd.macd_diff()
df['ema_05'] = ta.trend.EMAIndicator(df['HA_close'], window=5).ema_indicator()
df['ema_10'] = ta.trend.EMAIndicator(df['HA_close'], window=10).ema_indicator()
df['ema_30'] = ta.trend.EMAIndicator(df['HA_close'], window=30).ema_indicator()
df['ATR'] = ta.volatility.AverageTrueRange(df['HA_high'], df['HA_low'], df['HA_close'], window=14).average_true_range()

# Initialize trading parameters
rsi_buy_threshold = 30  # Adjusted buy threshold for better entry
rsi_sell_threshold = 60  # Adjusted sell threshold for better exit
trailing_stop_multiplier = 2  # Multiplier for ATR in stop-loss
transaction_cost = 0.00

# Initialize variables
in_position = False
position_type = 0  # 1 for long, -1 for short
entry_price = 0
highest_price = 0
lowest_price = float('inf')
net_profit = 0
balance = 10000
btc_amount = 0
trade_count = 0
winning_trades = 0
losing_trades = 0
max_drawdown_value = 0
peak_balance = balance
signal_history = [0] * len(df)
balance_history = []

# Loop through DataFrame row by row
for i, (index, row) in enumerate(df.iterrows()):
    current_price = row['close']
    rsi = row['RSI']
    macd_value = row['MACD']
    macd_signal = row['MACD_Signal']
    ema_10 = row['ema_10']
    volume = row['volume']

    # Volume threshold for entering trades (e.g., average volume over last 10 days)
    volume_threshold = df['volume'].rolling(window=10).mean().iloc[i]

    # Buy condition: Strong bullish signal based on RSI, MACD, EMA, and volume
    if (rsi > rsi_buy_threshold and ema_10 > row['ema_30'] and macd_value > macd_signal and 
        current_price > ema_10 and volume > volume_threshold and not in_position):
        # Enter long position
        entry_price = current_price
        btc_amount = (balance * (1 - transaction_cost)) / entry_price
        highest_price = entry_price
        in_position = True
        position_type = 1
        trade_count += 1
        signal_history[i] = 1  # Buy signal
    
    # Sell condition for long: Stop-loss based on trailing stop or strong bearish signals
    elif in_position and position_type == 1:
        if current_price > highest_price:
            highest_price = current_price
        
        # Dynamic stop-loss based on ATR
        stop_loss_price = entry_price - (trailing_stop_multiplier * row['ATR'])

        if current_price <= stop_loss_price or (rsi < rsi_sell_threshold or macd_value < macd_signal):
            # Exit long position
            balance = btc_amount * current_price * (1 - transaction_cost)
            profit = (current_price - entry_price) * btc_amount
            net_profit += profit
            if profit > 0:
                winning_trades += 1
            else:
                losing_trades += 1
            in_position = False
            signal_history[i] = -1  # Sell signal

    # Record balance history
    balance_history.append(balance)

    # Max drawdown tracking
    peak_balance = max(peak_balance, balance)
    drawdown = (peak_balance - balance) / peak_balance
    max_drawdown_value = max(max_drawdown_value, drawdown)

    # Define trade type based on signals
trade_type = []
for signal in signal_history:
    if signal == 1:
        trade_type.append("Buy")
    elif signal == -1:
        trade_type.append("Sell")
    else:
        trade_type.append("Hold")

# Add signal and trade_type columns to the DataFrame
df['signals'] = signal_history
df['trade_type'] = trade_type


# Add signal column to DataFrame and save to CSV with timestamp
df['Signal'] = signal_history
current_time = datetime.now().strftime("%Y-%m-%d")
output_filename = f'untrade4.csv'
df.to_csv(output_filename, columns=['close', 'Signal'])

print(f'Signal CSV saved as {output_filename}')