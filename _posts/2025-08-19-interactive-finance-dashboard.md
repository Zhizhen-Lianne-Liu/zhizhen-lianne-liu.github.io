---
title: Interactive Finance Dashboard
date: 2025-08-19 14:00:00 -0500
categories: [Finance, Technology]
tags: [finance, dashboard, marimo, webassembly, data-visualization, python]
---

A little personal experiment to explore financial data visualization using modern web technologies.

## Why These Tools?

**marimo over Jupyter**: Reactive updates mean changing one input automatically recalculates everything downstream, unlike Jupyter's manual cell execution.

**Alpha Vantage over Yahoo Finance**: Yahoo's API became unreliable with frequent rate limiting. Alpha Vantage offers 25 free daily calls with consistent data format.

**WebAssembly over server-side**: Runs entirely in the browser without backend infrastructure. Alternative would be Flask/FastAPI + database, but that adds deployment complexity.

**GitHub Actions for data**: Scheduled collection runs daily after market close. Could use client-side API calls, but that would hit rate limits quickly with multiple users.

## Architecture

Python analysis → WebAssembly → Browser execution. Data pipeline collects real market data daily and serves it as static JSON files.

**→ [View the full finance tools page](/finance/) for usage instructions and to launch the dashboard**