import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Interactive Finance Dashboard

        Welcome to your personal finance analysis dashboard! This tool provides:
        - Real-time stock data visualization powered by Alpha Vantage
        - Interactive charts and analysis with live market data
        - Performance metrics calculations using actual prices
        - Modern web interface with automatic data updates

        *Data is updated daily after market close via automated GitHub Actions.*
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
def __(stock_input, period_selector, pd, np, datetime, timedelta, json):
    # Load real financial data from JSON files
    def load_real_data(tickers_str, period):
        tickers = [ticker.strip().upper() for ticker in tickers_str.split(',')]
        if not tickers or tickers == ['']:
            return pd.DataFrame(), [], None

        try:
            # Try to load real data from JSON files
            try:
                # For WebAssembly, use JavaScript fetch via js module
                import js
                from pyodide.ffi import to_js
                
                # Create a synchronous fetch using XMLHttpRequest
                def fetch_json_sync(url):
                    print(f"DEBUG: Attempting to fetch {url}")
                    xhr = js.XMLHttpRequest.new()
                    xhr.open('GET', url, False)  # False = synchronous
                    xhr.send(None)
                    print(f"DEBUG: XMLHttpRequest status: {xhr.status}")
                    print(f"DEBUG: XMLHttpRequest statusText: {xhr.statusText}")
                    if xhr.status == 200:
                        print(f"DEBUG: Response received, length: {len(xhr.responseText)}")
                        data = json.loads(xhr.responseText)
                        print(f"DEBUG: JSON parsed successfully, type: {type(data)}")
                        return data
                    else:
                        print(f"DEBUG: HTTP error {xhr.status}: {xhr.statusText}")
                        raise Exception(f"HTTP {xhr.status}: {xhr.statusText}")
                
                print("DEBUG: Fetching stock data...")
                stock_data = fetch_json_sync('./data/stock_data.json')
                print("DEBUG: Fetching timestamp info...")
                timestamp_info = fetch_json_sync('./data/last_updated.json')
                print("DEBUG: Both files fetched successfully")
                
            except (ImportError, Exception) as e:
                print(f"WebAssembly fetch failed: {e}")
                # Fallback to direct file access for local testing
                try:
                    with open('data/stock_data.json', 'r') as f:
                        stock_data = json.load(f)
                    
                    with open('data/last_updated.json', 'r') as f:
                        timestamp_info = json.load(f)
                except Exception as file_err:
                    print(f"File access failed: {file_err}")
                    raise Exception(f"Both WebAssembly fetch and local file access failed")

            # Convert to DataFrame and filter
            df = pd.DataFrame(stock_data)
            df['Date'] = pd.to_datetime(df['Date'])

            # Filter for requested tickers
            available_tickers = [t for t in tickers if t in df['Ticker'].unique()]
            if not available_tickers:
                return pd.DataFrame(), [], {'error': 'No data available for requested tickers'}

            df_filtered = df[df['Ticker'].isin(available_tickers)]

            # Apply period filter
            period_days = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365}
            days = period_days.get(period, 90)
            cutoff_date = datetime.now() - timedelta(days=days)
            df_filtered = df_filtered[df_filtered['Date'] >= cutoff_date]

            return df_filtered, available_tickers, timestamp_info

        except Exception as e:
            print(f"Error loading real data: {e}")
            return pd.DataFrame(), [], {'error': f'Failed to load data: {str(e)}'}


    stock_data, selected_tickers, data_info = load_real_data(stock_input.value, period_selector.value)
    return load_real_data, selected_tickers, stock_data, data_info


@app.cell(hide_code=True)
def __(mo, selected_tickers, stock_data, data_info):
    if stock_data.empty:
        if data_info and 'error' in data_info:
            mo.md(f"❌ **Error:** {data_info['error']}\n\n*Please ensure data has been collected via GitHub Actions.*")
        else:
            mo.md("⚠️ **No data available.** Please check your ticker symbols and try again.")
    else:
        last_updated = data_info.get('last_updated', 'Unknown')
        market_date = data_info.get('market_date', 'Unknown')
        real_data_ratio = data_info.get('real_data_ratio', 'Unknown')
        mo.md(f"📈 **Real market data loaded for:** {', '.join(selected_tickers)}\n\n**Last updated:** {last_updated} | **Market date:** {market_date} | **Real data:** {real_data_ratio}")
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
def __(alt, mo, pd, np, datetime, timedelta, json):
    # Market overview with real S&P 500 data
    def get_market_overview():
        try:
            # Try to load real market overview data
            try:
                try:
                    # For WebAssembly, use JavaScript XMLHttpRequest
                    import js
                    
                    def fetch_json_sync(url):
                        print(f"DEBUG MARKET: Attempting to fetch {url}")
                        xhr = js.XMLHttpRequest.new()
                        xhr.open('GET', url, False)
                        xhr.send(None)
                        print(f"DEBUG MARKET: XMLHttpRequest status: {xhr.status}")
                        if xhr.status == 200:
                            print(f"DEBUG MARKET: Response received, length: {len(xhr.responseText)}")
                            data = json.loads(xhr.responseText)
                            print(f"DEBUG MARKET: JSON parsed successfully")
                            return data
                        else:
                            print(f"DEBUG MARKET: HTTP error {xhr.status}: {xhr.statusText}")
                            raise Exception(f"HTTP {xhr.status}: {xhr.statusText}")
                    
                    print("DEBUG MARKET: Starting market data fetch...")
                    market_data = fetch_json_sync('./data/market_overview.json')
                    print("DEBUG MARKET: Market data fetched successfully")
                    
                except (ImportError, Exception) as e:
                    print(f"WebAssembly fetch failed: {e}")
                    # Fallback to direct file access for local testing
                    with open('data/market_overview.json', 'r') as f:
                        market_data = json.load(f)

                current_price = market_data['current_price']
                change = market_data['change']
                change_pct = market_data['change_pct']

                # Create chart data from real data
                df = pd.DataFrame(market_data['data'])
                df['Date'] = pd.to_datetime(df['Date'])

                data_source_note = "Real Market Data"
                title_suffix = "(Real Data)"

            except Exception as e:
                print(f"No market overview data available: {e}")
                return mo.md(f"❌ **Market overview unavailable:** No real data found.\n\n*Please ensure GitHub Actions has run to collect Alpha Vantage data.*")

            # Create trend chart
            color = '#2E8B57' if change >= 0 else '#DC143C'  # Green for up, red for down

            trend_chart = alt.Chart(df).mark_line(color=color, strokeWidth=3).encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Price:Q', title='S&P 500 Index', scale=alt.Scale(zero=False)),
                tooltip=['Date:T', 'Price:Q']
            ).properties(
                width=600,
                height=250,
                title=f"S&P 500 Index - Last 30 Days {title_suffix}"
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
            ### S&P 500 Index Overview ({data_source_note})

            **Current Level:** {current_price:.2f} {direction}
            **30-Day Change:** {change:+.2f} points ({change_pct:+.2f}%)
            **Status:** <span style="color: {status_color}">{'Bullish' if change >= 0 else 'Bearish'}</span>

            *Data Source: {data_source_note}*
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

        **Key Features:**
        - **Reactive Interface** - Changes automatically update all dependent components
        - **Interactive Charts** - Built with Altair/Vega-Lite for smooth interactions
        - **WebAssembly Powered** - Runs entirely in your browser
        - **Real Data** - Scheduled using Github Actions calling on Alpha Vantage API

        **Technology Stack:**
        - **marimo** - Reactive Python notebooks
        - **Altair** - Declarative statistical visualization
        - **Pandas** - Data manipulation and analysis
        - **WebAssembly** - High-performance browser execution

        """
    )
    return


if __name__ == "__main__":
    app.run()