import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Interactive Finance Dashboard
        
        Welcome to your personal finance analysis dashboard! This tool provides:
        - Stock data visualization with sample data
        - Interactive charts and analysis
        - Performance metrics calculations
        - Modern web interface
        
        *Note: This demo uses sample data. In production, this would connect to real financial APIs.*
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import altair as alt
    from datetime import datetime, timedelta
    import json
    
    # Enable Altair to render in marimo
    alt.data_transformers.enable('json')
    return alt, datetime, json, mo, np, pd, timedelta


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Stock Selection and Analysis""")
    return


@app.cell
def __(mo):
    # Create interactive widgets for stock selection
    stock_input = mo.ui.text(
        value="AAPL,GOOGL,MSFT,AMZN",
        label="Stock Tickers (comma-separated):",
        placeholder="Enter stock symbols like AAPL,GOOGL,MSFT"
    )
    
    period_selector = mo.ui.dropdown(
        options=["1M", "3M", "6M", "1Y"],
        value="3M",
        label="Time Period:"
    )
    
    chart_type = mo.ui.dropdown(
        options=["line", "area"],
        value="line",
        label="Chart Type:"
    )
    
    mo.hstack([stock_input, period_selector, chart_type], justify="space-around")
    return chart_type, period_selector, stock_input


@app.cell
def __(stock_input, period_selector, pd, np, datetime, timedelta):
    # Generate sample financial data for demonstration
    def generate_sample_data(tickers_str, period):
        tickers = [ticker.strip().upper() for ticker in tickers_str.split(',')]
        if not tickers or tickers == ['']:
            return pd.DataFrame(), []
        
        # Define period mapping
        period_days = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365}
        days = period_days.get(period, 90)
        
        # Generate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Sample data for demonstration
        sample_prices = {
            'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 420.0, 'AMZN': 150.0,
            'TSLA': 250.0, 'META': 320.0, 'NVDA': 470.0, 'JPM': 150.0
        }
        
        data = []
        for ticker in tickers:
            base_price = sample_prices.get(ticker, 100.0)
            # Generate realistic stock price movement
            np.random.seed(hash(ticker) % 2**32)  # Consistent randomness per ticker
            
            prices = [base_price]
            for i in range(1, len(date_range)):
                # Simulate realistic price movement
                change = np.random.normal(0, 0.02)  # 2% daily volatility
                new_price = prices[-1] * (1 + change)
                prices.append(max(new_price, base_price * 0.5))  # Prevent negative prices
            
            for date, price in zip(date_range, prices):
                data.append({
                    'Date': date,
                    'Price': round(price, 2),
                    'Ticker': ticker
                })
        
        return pd.DataFrame(data), tickers
    
    stock_data, selected_tickers = generate_sample_data(stock_input.value, period_selector.value)
    return generate_sample_data, selected_tickers, stock_data


@app.cell(hide_code=True)
def __(mo, selected_tickers, stock_data):
    if stock_data.empty:
        mo.md("⚠️ **No data available.** Please check your ticker symbols and try again.")
    else:
        mo.md(f"✅ **Sample data generated for:** {', '.join(selected_tickers)}")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Interactive Price Charts""")
    return


@app.cell
def __(alt, chart_type, mo, selected_tickers, stock_data):
    # Create interactive price chart
    def create_price_chart(data, tickers, chart_style="line"):
        if data.empty:
            return mo.md("No data to display")
        
        try:
            # Create the chart based on selected style
            base_chart = alt.Chart(data)
            
            if chart_style == "line":
                chart = base_chart.mark_line(point=True, strokeWidth=2).encode(
                    x=alt.X('Date:T', title='Date'),
                    y=alt.Y('Price:Q', title='Price ($)'),
                    color=alt.Color('Ticker:N', title='Stock', scale=alt.Scale(scheme='category10')),
                    tooltip=['Date:T', 'Ticker:N', 'Price:Q']
                )
            else:  # area
                chart = base_chart.mark_area(opacity=0.7).encode(
                    x=alt.X('Date:T', title='Date'),
                    y=alt.Y('Price:Q', title='Price ($)'),
                    color=alt.Color('Ticker:N', title='Stock', scale=alt.Scale(scheme='category10')),
                    tooltip=['Date:T', 'Ticker:N', 'Price:Q']
                )
            
            chart = chart.properties(
                width=700,
                height=400,
                title=f"Stock Price Analysis - {', '.join(tickers)}"
            ).resolve_scale(
                color='independent'
            )
            
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
def __(mo, pd, selected_tickers, stock_data, np):
    # Calculate and display performance metrics
    def calculate_metrics(data, tickers):
        if data.empty:
            return mo.md("No data available for metrics calculation")
        
        try:
            metrics = []
            
            for ticker in tickers:
                ticker_data = data[data['Ticker'] == ticker].sort_values('Date')
                
                if len(ticker_data) < 2:
                    continue
                
                current_price = ticker_data['Price'].iloc[-1]
                first_price = ticker_data['Price'].iloc[0]
                returns = ((current_price - first_price) / first_price) * 100
                
                # Calculate volatility (standard deviation of daily returns)
                daily_returns = ticker_data['Price'].pct_change().dropna()
                volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized
                
                # Calculate some additional metrics
                max_price = ticker_data['Price'].max()
                min_price = ticker_data['Price'].min()
                price_range = ((max_price - min_price) / min_price) * 100
                
                metrics.append({
                    'Ticker': ticker,
                    'Current Price': f"${current_price:.2f}",
                    'Total Return': f"{returns:+.2f}%",
                    'Volatility': f"{volatility:.2f}%",
                    'Price Range': f"{price_range:.2f}%",
                    'High': f"${max_price:.2f}",
                    'Low': f"${min_price:.2f}"
                })
            
            if not metrics:
                return mo.md("Unable to calculate metrics for the selected stocks")
            
            metrics_df = pd.DataFrame(metrics)
            return mo.ui.table(metrics_df, selection=None)
            
        except Exception as e:
            return mo.md(f"Error calculating metrics: {str(e)}")
    
    metrics_table = calculate_metrics(stock_data, selected_tickers)
    metrics_table
    return calculate_metrics, metrics_table


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""## Market Overview""")
    return


@app.cell
def __(alt, mo, pd, np, datetime, timedelta):
    # Market overview with sample data
    def get_market_overview():
        try:
            # Generate sample S&P 500 data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Sample S&P 500 index data
            np.random.seed(42)  # Consistent randomness
            base_price = 4200.0
            prices = [base_price]
            
            for i in range(1, len(date_range)):
                change = np.random.normal(0.001, 0.015)  # Small upward bias, moderate volatility
                new_price = prices[-1] * (1 + change)
                prices.append(max(new_price, base_price * 0.9))  # Floor at 10% drop
            
            current_price = prices[-1]
            prev_close = prices[0]
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            # Create chart data
            chart_data = []
            for date, price in zip(date_range, prices):
                chart_data.append({'Date': date, 'Price': price})
            
            df = pd.DataFrame(chart_data)
            
            # Create trend chart
            color = '#2E8B57' if change >= 0 else '#DC143C'  # Green for up, red for down
            
            trend_chart = alt.Chart(df).mark_line(color=color, strokeWidth=3).encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Price:Q', title='S&P 500 Index', scale=alt.Scale(zero=False)),
                tooltip=['Date:T', 'Price:Q']
            ).properties(
                width=600,
                height=250,
                title="S&P 500 Index - Last 30 Days (Sample Data)"
            )
            
            # Add area fill
            area_chart = alt.Chart(df).mark_area(
                opacity=0.3,
                color=color
            ).encode(
                x=alt.X('Date:T'),
                y=alt.Y('Price:Q', scale=alt.Scale(zero=False))
            )
            
            combined_chart = (area_chart + trend_chart).resolve_scale(
                y='shared'
            )
            
            # Display metrics and chart
            direction = "📈" if change >= 0 else "📉"
            status_color = "green" if change >= 0 else "red"
            
            overview_text = f"""
            ### S&P 500 Index Overview (Sample Data)
            
            **Current Level:** {current_price:.2f} {direction}  
            **30-Day Change:** {change:+.2f} points ({change_pct:+.2f}%)  
            **Status:** <span style="color: {status_color}">{'Bullish' if change >= 0 else 'Bearish'}</span>
            
            *Note: This is sample data for demonstration purposes.*
            """
            
            return mo.vstack([
                mo.md(overview_text),
                mo.ui.altair_chart(combined_chart)
            ])
            
        except Exception as e:
            return mo.md(f"Error generating market overview: {str(e)}")
    
    market_overview = get_market_overview()
    market_overview
    return get_market_overview, market_overview


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        ---
        
        ## About This Dashboard
        
        This interactive finance dashboard demonstrates the capabilities of [marimo](https://marimo.io/) for creating 
        browser-based data analysis applications. 
        
        **Key Features:**
        - **Reactive Interface** - Changes automatically update all dependent components
        - **Interactive Charts** - Built with Altair/Vega-Lite for smooth interactions
        - **WebAssembly Powered** - Runs entirely in your browser
        - **Sample Data** - Demonstrates realistic financial analysis patterns
        
        **Technology Stack:**
        - **marimo** - Reactive Python notebooks
        - **Altair** - Declarative statistical visualization
        - **Pandas** - Data manipulation and analysis
        - **WebAssembly** - High-performance browser execution
        
        **Production Integration:**
        In a production environment, this dashboard would connect to real financial data APIs such as:
        - Alpha Vantage
        - IEX Cloud  
        - Polygon.io
        - Yahoo Finance (via REST APIs)
        
        ---
        
        *This dashboard showcases the power of modern web technologies for financial analysis.*
        """
    )
    return


if __name__ == "__main__":
    app.run()