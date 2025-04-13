
# 📈 Crypto Trading Strategies – Team Crypto Mavericks  
**Powered by Zelta Automations**

---

## 📁 Project Overview

This repository contains a diverse collection of crypto trading strategies built using a combination of **algorithmic trading**, **machine learning**, **reinforcement learning**, and **fundamental analysis**.

The folder is organized into two main directories:   
1.**Fundamental Strategies of BTC and ETH**   
2.**ML Integrated Strategies**

Each strategy is accompanied by:
1. **`.ipynb` File**  
   - Core strategy implementation and backtesting logic.  
   - Naming convention: `strategyNo.instrument.speciality.ipynb`  
   - Some outputs are visualized, but execution is best done on **Google Colab** for compatibility.

2. **`.csv` Output**  
   - Contains long/short position data generated from the strategy logic.

3. **(Optional) Explanatory File**  
   - Describes the core idea, indicators used, and rationale behind the strategy.

---

## ⚙️ Technical Details

### 🔧 Libraries & Frameworks Used
- `pandas`  
- `numpy`  
- `pandas_ta` (`!pip install pandas_ta`)  
- `ta` (`!pip install ta`)  
- `matplotlib` (for plotting)

All strategies are developed in Python and are Google Colab compatible.

---

### 🧰 Handling Common Data Issues

If you face errors while reading datetime columns, apply one of the following fixes:

#### ✅ Recommended Approach
```python
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['datetime'])
df.set_index('datetime', inplace=True)
```

#### 🛠️ Alternative (System/Format Dependent)
```python
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
df.set_index('datetime', inplace=True)
```

---

### 📂 Dataset Integration

Datasets are included alongside the strategy files and are typically loaded like:
```python
df = pd.read_csv('/content/filename.csv')
```
The filename usually matches the dataset relevant to the specific strategy.

---

### 📉 Equity Curve Visualization (Optional)

To visualize the equity performance of a strategy, append this after the execution block:

```python
# Plot equity curve
plt.figure(figsize=(14, 7))
plt.plot(df.index, balance_history, label='Equity Curve', color='blue')
plt.title('Equity Curve')
plt.xlabel('Date')
plt.ylabel('Balance (USD)')
plt.grid()
plt.legend()
plt.show()
```

---

### 🔁 Backtesting Framework  
Test Data 
https://drive.google.com/drive/folders/1z4dkAlHSWMDtmLH2sTYYY-vY0IGOaGlG
https://drive.google.com/drive/folders/1VloVIKEbdcpTJgE_JqAJyBeARFnIlGsP
Backtesting is powered by the **Untrade SDK**, by **Zelta Automations**.  
Implementation examples are included within the notebooks.

---

## 🔬 Strategy Types

- **Machine Learning & Reinforcement Learning Approaches:**  
  Utilized models such as XGBoost, Random Forests, K-Means Clustering, Monte Carlo simulations, and Q-Learning.

- **Indicator-Based Strategies:**  
  Integrated technical indicators including MACD, EMA, PSAR, RSI, and others.

- **Fundamental & Hybrid Approaches:**  
  Combined trend-following and momentum strategies with fundamental market signals.

- **Performance Highlights:**  
  - Sharpe ratios exceeding **20+** in some strategies.  
  - Returns of **2500%+** achieved on selected strategies with minimal drawdowns.  
  - Collaboration with researchers helped cut down development time by over **40%**.

---

## 👥 Team Crypto Mavericks

- **Chirag Ashish Agrawal**  
- **Aditya Prakash**
- **Parth Sharma**

---

