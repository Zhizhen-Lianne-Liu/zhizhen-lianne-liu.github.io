# Zhizhen Liu - Personal Blog & Finance Dashboard

[![Deploy Jekyll and Marimo to GitHub Pages](https://github.com/zhizhen-lianne-liu/zhizhen-lianne-liu.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/zhizhen-lianne-liu/zhizhen-lianne-liu.github.io/actions/workflows/deploy.yml)

This repository contains my personal blog and interactive finance analysis tools, hosted at [zhizhen-lianne-liu.github.io](https://zhizhen-lianne-liu.github.io).

## 🚀 Features

### Interactive Finance Dashboard
- **Real-time S&P 500 Analysis**: Live stock data with interactive charts
- **Multi-stock Comparison**: Compare performance across different stocks
- **Performance Metrics**: Returns, volatility, and volume analysis
- **WebAssembly Powered**: Runs entirely in your browser using Pyodide

### Personal Blog
- **Jekyll-powered**: Fast, static site generation
- **SEO Optimized**: Built-in search engine optimization
- **Responsive Design**: Works on desktop and mobile
- **GitHub Pages**: Free, reliable hosting

## 🛠️ Technology Stack

- **Frontend**: Jekyll, HTML5, CSS3, JavaScript
- **Interactive Apps**: [marimo](https://marimo.io/) notebooks exported to WebAssembly
- **Data Analysis**: Python, pandas, numpy, altair
- **Data Source**: Yahoo Finance API via yfinance
- **Deployment**: GitHub Actions + GitHub Pages
- **Version Control**: Git + GitHub

## 📊 Interactive Tools

### [Finance Dashboard](/finance/)
Real-time stock market analysis with:
- Stock price visualization
- Performance comparison tools
- Interactive charts with zoom/pan
- Market trend analysis

### [Original Analysis Notebook](/finance/baba-finance/)
The original Jupyter notebook converted to marimo format, featuring:
- S&P 500 data exploration
- Historical analysis examples
- Data processing demonstrations

## 🏗️ Project Structure

```
├── _config.yml              # Jekyll configuration
├── index.md                 # Homepage
├── about.md                 # About page
├── projects.md              # Projects showcase
├── _posts/                  # Blog posts
├── finance/
│   ├── index.md            # Finance tools landing page
│   ├── finance_dashboard.py # Interactive dashboard (marimo)
│   ├── finance_dashboard.html # Exported WebAssembly app
│   └── baba-finance/       # Original analysis notebooks
├── .github/workflows/       # GitHub Actions CI/CD
└── README.md               # This file
```

## 🚀 Local Development

### Prerequisites
- Ruby (for Jekyll)
- Python 3.8+ (for marimo)
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zhizhen-lianne-liu/zhizhen-lianne-liu.github.io.git
   cd zhizhen-lianne-liu.github.io
   ```

2. **Install Jekyll dependencies:**
   ```bash
   bundle install
   ```

3. **Install Python dependencies:**
   ```bash
   pip install marimo[recommended] yfinance pandas numpy altair
   ```

4. **Run Jekyll locally:**
   ```bash
   bundle exec jekyll serve
   ```

5. **Run marimo dashboard locally:**
   ```bash
   marimo run finance/finance_dashboard.py
   ```

### Making Changes

1. **Edit blog content**: Modify markdown files in the root or `_posts/` directory
2. **Update dashboard**: Edit `finance/finance_dashboard.py` and re-export to WebAssembly:
   ```bash
   marimo export html-wasm finance/finance_dashboard.py -o finance/finance_dashboard.html
   ```
3. **Deploy**: Push changes to main branch - GitHub Actions will automatically build and deploy

## 📝 Blog Posts

Recent posts:
- [Welcome to My Interactive Finance Blog](/_posts/2024-08-19-welcome-to-my-finance-blog.md)

## 🤝 Contributing

This is a personal blog/portfolio, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **Live Site**: [zhizhen-lianne-liu.github.io](https://zhizhen-lianne-liu.github.io)
- **Interactive Dashboard**: [Finance Tools](https://zhizhen-lianne-liu.github.io/finance/)
- **marimo**: [marimo.io](https://marimo.io/)
- **GitHub Pages**: [pages.github.com](https://pages.github.com/)

---

Built with ❤️ using Jekyll, marimo, and GitHub Pages.