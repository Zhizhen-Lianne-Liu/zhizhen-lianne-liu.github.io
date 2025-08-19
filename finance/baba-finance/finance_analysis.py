import marimo

__generated_with = "0.14.17"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Importing libraries
        """
    )
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import yfinance as yf
    import matplotlib.pyplot as plt
    # '%matplotlib inline' command supported automatically in marimo
    # magic command not supported in marimo; please file an issue to add support
    # %config InlineBackend.figure_format='retina'
    import warnings
    warnings.filterwarnings("ignore")
    return pd, yf


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Getting ticker data from yfinance
        """
    )
    return


@app.cell
def _(yf):
    sp500ticker = yf.Ticker("^GSPC")
    recentsp = sp500ticker.history(period="5d")
    return (recentsp,)


@app.cell
def _(recentsp):
    recentsp.head(10)
    return


@app.cell
def _(yf):
    recentsp2 = yf.download("^GSPC", period='5d')
    recentsp2.head(10)
    return


@app.cell
def _(pd, yf):
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    print(tickers.head())
    _data = yf.download(tickers.Symbol.to_list(), '2021-1-1', '2021-7-12', auto_adjust=True)['Close']
    print(_data.head())
    return


@app.cell
def _(pd):
    spdata = pd.read_csv('sp500data.csv')
    spdata.head()
    return (spdata,)


@app.cell
def _(spdata):
    sptickers = spdata['Symbol'].tolist()
    return (sptickers,)


@app.cell
def _(sptickers, yf):
    _data = yf.download(sptickers, period='1d')
    print(_data.head())
    return


@app.cell
def _(yf):
    data2 = yf.download('AAPL', period='1d')
    data2.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""

        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

