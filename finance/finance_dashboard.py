import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Interactive S&P 500 Finance Dashboard
        
        Welcome to your personal finance analysis dashboard! This interactive tool allows you to:
        - Analyze S&P 500 stock performance
        - Compare multiple stocks
        - Visualize trends with interactive charts
        - Filter by sectors and date ranges
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import yfinance as yf
    import altair as alt
    import warnings
    from datetime import datetime, timedelta
    
    warnings.filterwarnings("ignore")
    
    # Enable Altair to render in marimo
    alt.data_transformers.enable('json')
    return alt, datetime, mo, np, pd, timedelta, warnings, yf


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Stock Selection and Time Period""")
    return


@app.cell
def __(mo):
    # Create interactive widgets for stock selection and time period
    stock_input = mo.ui.text(
        value="AAPL,GOOGL,MSFT,AMZN,TSLA",
        label="Stock Tickers (comma-separated):",
        placeholder="Enter stock symbols like AAPL,GOOGL,MSFT"
    )
    
    period_selector = mo.ui.dropdown(
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="6mo",
        label="Time Period:"
    )
    
    chart_type = mo.ui.dropdown(
        options=["line", "area", "candlestick"],
        value="line",
        label="Chart Type:"
    )
    
    mo.hstack([stock_input, period_selector, chart_type], justify="space-around")
    return chart_type, period_selector, stock_input


@app.cell
def __(stock_input, period_selector, yf, pd, mo):
    # Fetch stock data based on user inputs
    def fetch_stock_data(tickers_str, period):
        try:
            tickers = [ticker.strip().upper() for ticker in tickers_str.split(',')]
            if not tickers or tickers == ['']:
                return pd.DataFrame(), []
            
            # Download data for selected tickers
            data = yf.download(tickers, period=period, progress=False)
            
            if data.empty:
                return pd.DataFrame(), tickers
            
            # Handle single vs multiple ticker data structure
            if len(tickers) == 1:
                # Single ticker - restructure data
                data.columns = pd.MultiIndex.from_product([data.columns, tickers])
            
            return data, tickers
            
        except Exception as e:
            mo.status.toast(f"Error fetching data: {str(e)}", kind="danger")
            return pd.DataFrame(), []
    
    stock_data, selected_tickers = fetch_stock_data(stock_input.value, period_selector.value)
    return fetch_stock_data, selected_tickers, stock_data


@app.cell(hide_code=True)
def __(mo, selected_tickers, stock_data):
    if stock_data.empty:
        mo.md("⚠️ **No data available.** Please check your ticker symbols and try again.")
    else:
        mo.md(f"✅ **Successfully loaded data for:** {', '.join(selected_tickers)}")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Interactive Price Charts""")
    return


@app.cell
def __(alt, chart_type, mo, pd, selected_tickers, stock_data):
    # Create interactive price chart
    def create_price_chart(data, tickers, chart_style="line"):
        if data.empty:
            return mo.md("No data to display")
        
        try:
            # Prepare data for visualization
            chart_data = []
            
            for ticker in tickers:
                try:
                    if 'Close' in data.columns.levels[0]:
                        close_prices = data['Close'][ticker].dropna()
                    else:
                        # Single ticker case
                        close_prices = data['Close'].dropna()
                    
                    for date, price in close_prices.items():
                        chart_data.append({
                            'Date': date,
                            'Price': price,
                            'Ticker': ticker
                        })
                except (KeyError, IndexError):
                    continue
            
            if not chart_data:
                return mo.md("No valid price data available")
            
            df = pd.DataFrame(chart_data)
            
            # Create the chart based on selected style
            base_chart = alt.Chart(df).add_selection(
                alt.selection_interval(bind='scales')
            )
            
            if chart_style == "line":
                chart = base_chart.mark_line(point=True).encode(
                    x=alt.X('Date:T', title='Date'),
                    y=alt.Y('Price:Q', title='Price ($)'),
                    color=alt.Color('Ticker:N', title='Stock'),
                    tooltip=['Date:T', 'Ticker:N', 'Price:Q']
                )
            elif chart_style == "area":
                chart = base_chart.mark_area(opacity=0.7).encode(
                    x=alt.X('Date:T', title='Date'),
                    y=alt.Y('Price:Q', title='Price ($)'),
                    color=alt.Color('Ticker:N', title='Stock'),
                    tooltip=['Date:T', 'Ticker:N', 'Price:Q']
                )
            else:  # candlestick - simplified as line for now
                chart = base_chart.mark_line().encode(
                    x=alt.X('Date:T', title='Date'),
                    y=alt.Y('Price:Q', title='Price ($)'),
                    color=alt.Color('Ticker:N', title='Stock'),
                    tooltip=['Date:T', 'Ticker:N', 'Price:Q']
                )
            
            chart = chart.properties(
                width=700,
                height=400,
                title=f"Stock Price Comparison - {', '.join(tickers)}"
            ).interactive()
            
            return mo.ui.altair_chart(chart)
            
        except Exception as e:
            return mo.md(f"Error creating chart: {str(e)}")
    
    price_chart = create_price_chart(stock_data, selected_tickers, chart_type.value)
    price_chart
    return create_price_chart, price_chart


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Performance Metrics""")
    return


@app.cell
def __(mo, pd, selected_tickers, stock_data):
    # Calculate and display performance metrics
    def calculate_metrics(data, tickers):
        if data.empty:
            return mo.md("No data available for metrics calculation")
        
        try:
            metrics = []
            
            for ticker in tickers:
                try:
                    if 'Close' in data.columns.levels[0]:
                        prices = data['Close'][ticker].dropna()
                        volumes = data['Volume'][ticker].dropna() if 'Volume' in data.columns.levels[0] else None
                    else:
                        prices = data['Close'].dropna()
                        volumes = data['Volume'].dropna() if 'Volume' in data.columns else None
                    
                    if len(prices) < 2:
                        continue
                    
                    current_price = prices.iloc[-1]
                    first_price = prices.iloc[0]
                    returns = ((current_price - first_price) / first_price) * 100
                    volatility = prices.pct_change().std() * np.sqrt(252) * 100  # Annualized volatility
                    avg_volume = volumes.mean() if volumes is not None else 0
                    
                    metrics.append({
                        'Ticker': ticker,
                        'Current Price': f"${current_price:.2f}",
                        'Total Return': f"{returns:.2f}%",
                        'Volatility': f"{volatility:.2f}%",
                        'Avg Daily Volume': f"{avg_volume:,.0f}" if avg_volume > 0 else "N/A"
                    })
                    
                except (KeyError, IndexError, TypeError):
                    continue
            
            if not metrics:
                return mo.md("Unable to calculate metrics for the selected stocks")
            
            metrics_df = pd.DataFrame(metrics)
            return mo.ui.table(metrics_df, selection=None)
            
        except Exception as e:
            return mo.md(f"Error calculating metrics: {str(e)}")
    
    import numpy as np
    metrics_table = calculate_metrics(stock_data, selected_tickers)
    metrics_table
    return calculate_metrics, metrics_table, np


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## S&P 500 Market Overview""")
    return


@app.cell
def __(alt, mo, pd, yf):
    # S&P 500 overview
    def get_sp500_overview():
        try:
            # Get S&P 500 index data
            sp500 = yf.download("^GSPC", period="1mo", progress=False)
            
            if sp500.empty:
                return mo.md("Unable to fetch S&P 500 data")
            
            current_price = sp500['Close'].iloc[-1]
            prev_close = sp500['Close'].iloc[0]
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            # Create a simple trend chart
            chart_data = []
            for date, price in sp500['Close'].items():
                chart_data.append({'Date': date, 'Price': price})
            
            df = pd.DataFrame(chart_data)
            
            trend_chart = alt.Chart(df).mark_line(color='blue', strokeWidth=2).encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Price:Q', title='S&P 500 Index'),
                tooltip=['Date:T', 'Price:Q']
            ).properties(
                width=600,
                height=200,
                title="S&P 500 Index - Last 30 Days"
            )
            
            # Display metrics and chart
            status_color = "green" if change >= 0 else "red"
            direction = "↗️" if change >= 0 else "↘️"
            
            overview_text = f"""
            ### S&P 500 Index Overview
            
            **Current Level:** {current_price:.2f} {direction}  
            **30-Day Change:** {change:+.2f} ({change_pct:+.2f}%)
            """
            
            return mo.vstack([
                mo.md(overview_text),
                mo.ui.altair_chart(trend_chart)
            ])
            
        except Exception as e:
            return mo.md(f"Error fetching S&P 500 data: {str(e)}")
    
    sp500_overview = get_sp500_overview()
    sp500_overview
    return get_sp500_overview, sp500_overview


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ---
        
        ## About This Dashboard
        
        This interactive finance dashboard is built with [marimo](https://marimo.io/) and provides real-time analysis of stock market data using the Yahoo Finance API. 
        
        **Features:**
        - Real-time stock price data
        - Interactive charts with zoom and pan
        - Performance metrics calculation
        - S&P 500 market overview
        - Responsive design for web deployment
        
        **Data Source:** Yahoo Finance API via yfinance library  
        **Last Updated:** Real-time data (market hours)
        
        ---
        """
    )
    return


if __name__ == "__main__":
    app.run()