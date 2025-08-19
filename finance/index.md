---
layout: page
title: Interactive Finance Tools
permalink: /finance/
---

# Interactive Finance Dashboard

Welcome to my interactive S&P 500 analysis dashboard! This tool provides real-time market analysis with interactive visualizations that run entirely in your browser.

## 🔗 Launch Dashboard

<div style="text-align: center; margin: 2rem 0;">
  <a href="finance_dashboard.html" class="btn btn-primary" style="padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
    🚀 Open Interactive Dashboard
  </a>
</div>

## Features

### 📊 Real-Time Stock Analysis
- Enter any stock symbols (e.g., AAPL, GOOGL, MSFT, AMZN)
- Choose from multiple time periods (1 month to 5 years)
- View different chart types (line, area, candlestick)

### 📈 Performance Metrics  
- Current stock prices
- Total return calculations
- Volatility analysis
- Average daily trading volume

### 🎮 Interactive Charts
- Zoom and pan functionality
- Hover for detailed data points
- Multi-stock comparison
- Responsive design for all devices

### 🏢 Market Overview
- Real-time S&P 500 index tracking
- 30-day trend visualization
- Market performance indicators

## How It Works

This dashboard is built with [marimo](https://marimo.io/), a reactive Python notebook framework that creates interactive web applications. The entire analysis engine runs in your browser using WebAssembly - no server required!

**Data Source**: Yahoo Finance API via the `yfinance` Python library  
**Visualization**: Altair/Vega-Lite for interactive charts  
**Technology**: Python, WebAssembly, HTML5

## Getting Started

1. Click the "Open Interactive Dashboard" button above
2. Wait for the app to load (first time may take a few seconds)
3. Enter stock symbols in the text field (comma-separated)
4. Select your preferred time period and chart type
5. Explore the interactive visualizations!

## Example Analysis

Try these popular stock combinations:
- **Tech Giants**: `AAPL,GOOGL,MSFT,AMZN`
- **Electric Vehicles**: `TSLA,RIVN,LCID,F`
- **Banking**: `JPM,BAC,WFC,C`
- **Healthcare**: `JNJ,PFE,UNH,ABBV`

## Technical Details

The dashboard includes several Python modules:
- **Data Fetching**: Real-time stock data via Yahoo Finance
- **Analysis Engine**: Pandas and NumPy for calculations
- **Visualization**: Altair for interactive charts
- **UI Components**: marimo widgets for user interaction

All code is open source and available on [GitHub](https://github.com/zhizhen-lianne-liu/zhizhen-lianne-liu.github.io).

---

*Having trouble? The dashboard works best in modern browsers with JavaScript enabled. For the full experience, use Chrome, Firefox, Safari, or Edge.*