# Financial Intelligence - Markets

Real-time financial data analysis for stocks, crypto, and currencies via Yahoo Finance.

## 📊 Overview

Market analysis features:
- Stock data and news
- Cryptocurrency prices
- Currency exchange rates
- Company financials
- Stock comparison
- Technical analysis

## 📝 Commands

### /markets - Get Market Data
```bash
/markets <keyword> [extra]
```

**Examples:**
```bash
# Stocks
/markets tesla
/markets shell
/markets nio

# Crypto
/markets btc
/markets eth
/markets doge

# Currencies
/markets usd
/markets eur

# Detailed analysis
/markets tesla statistics
/markets shell financials
/markets nio analysis

# Compare stocks
/markets compare tsla nio
/markets compare aapl msft
```

## 📈 Data Types

### Basic Stock Data
```bash
/markets <company>
```

Shows:
- Current price
- Performance metrics
- Price chart (ASCII)
- Top news articles

### Cryptocurrency
```bash
/markets <crypto>
```

Shows:
- Latest price
- Performance (1d, 7d, 30d)
- Market cap
- Circulating supply
- Volume
- ASCII chart

### Currency Exchange
```bash
/markets <currency>
```

Shows:
- Current exchange rate
- Performance data
- Volume and range
- ASCII chart

### Detailed Analysis

**statistics:**
```bash
/markets <company> statistics
```
Key stats, valuation, financial highlights

**history:**
```bash
/markets <company> history
```
Historical price data

**profile:**
```bash
/markets <company> profile
```
Industry, sector, employees, business summary

**financials:**
```bash
/markets <company> financials
```
Financial statements

**analysis:**
```bash
/markets <company> analysis
```
Analyst recommendations and estimates

**options:**
```bash
/markets <company> options
```
Options chain and expiration dates

**holders:**
```bash
/markets <company> holders
```
Major and institutional shareholders

**sustainability:**
```bash
/markets <company> sustainability
```
ESG scores and metrics

### Stock Comparison
```bash
/markets compare <stock1> <stock2>
```

Compares:
- Market capitalization
- Revenue growth
- Profit margins
- Financial ratios
- P/E ratio
- Debt-to-equity
- ROE, ROA
- Dividend yield

## 🔧 Configuration

Uses Yahoo Finance API:
- Real-time data
- No API key required
- Internet connection needed

## 💡 Best Practices

**Stock Tickers:**
```bash
✅ /markets tsla      # Tesla
✅ /markets aapl      # Apple  
✅ /markets msft      # Microsoft
```

**Crypto Symbols:**
```bash
✅ /markets btc       # Bitcoin
✅ /markets eth       # Ethereum
✅ /markets ada       # Cardano
```

**Currency Codes:**
```bash
✅ /markets usd       # US Dollar
✅ /markets eur       # Euro
✅ /markets jpy       # Japanese Yen
```

## 🚨 Troubleshooting

**Symbol not found:** Check ticker symbol spelling
**No data:** Verify internet connection
**Timeout:** Retry or try simpler query

## 🎯 Use Cases

**Investment Research:**
```bash
/markets tesla statistics
/markets compare tsla nio
```

**Crypto Monitoring:**
```bash
/markets btc
/markets eth
```

**Market Overview:**
```bash
/markets aapl
/markets googl
/markets msft
```

## 📊 Access Control

**R-Grade Required** for markets features

---

**Financial intelligence in real-time.** 📊