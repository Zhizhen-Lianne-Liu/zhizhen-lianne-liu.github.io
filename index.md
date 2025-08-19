---
layout: home
title: Welcome
---

# Welcome to My Personal Blog

Hi! I'm Zhizhen Liu, and this is my personal blog where I share insights about finance, technology, and data analysis.

## Featured Projects

### 🔗 [Interactive Finance Dashboard](/finance/)
Real-time S&P 500 analysis tool with interactive charts and market data visualization. Built with marimo and powered by Yahoo Finance API.

**Features:**
- Live stock price tracking
- Interactive charts with zoom and pan
- Performance metrics and volatility analysis  
- S&P 500 market overview
- Multi-stock comparison tools

---

## Recent Posts

{% for post in site.posts limit:3 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

---

## About This Site

This blog is built with Jekyll and hosted on GitHub Pages. The interactive finance tools are powered by [marimo](https://marimo.io/), enabling reactive notebooks that run entirely in your browser using WebAssembly.

All code is open source and available on [GitHub](https://github.com/zhizhen-lianne-liu/zhizhen-lianne-liu.github.io).