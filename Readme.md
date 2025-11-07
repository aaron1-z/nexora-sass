# ⚡ Nexora Intelligence Engine — Advanced Real-Time Edition

> **Transform news feeds into actionable strategic intelligence with AI-powered reasoning, sentiment analysis, and automated alerts.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Application opens at `http://localhost:8501`

**No API keys required** — Uses public Google News RSS feeds.

---

## ✨ What's New in This Version

### 🎨 **Modern Dark UI**
- Gradient cards with animations
- Real-time AI signal monitor
- Urgency badges with blink effects
- Professional data visualizations

### 🔴 **Enhanced Flash News**
- Real-time RSS feeds from multiple sources
- Sentiment timeline charts
- Keyword highlighting in headlines
- Top movers tracking (positive/negative)
- Smart alerts with urgency levels

### 🧠 **Advanced Intelligence Brief**
- Strategic reasoning with Flan-T5
- 30-day sentiment forecasts
- Scenario tree with probabilities (Bull/Base/Bear)
- Action recommendations with impact scores
- Confidence assessment with visual bars
- Multi-format exports (MD/HTML/Playbook)

### 📈 **Trends & Analytics**
- Dual-chart layouts (catalysts + momentum)
- Volatility Index calculation
- Sentiment evolution tracking
- Entity momentum analysis
- Burst activity detection

### 🔬 **Research Lab**
- Topic clustering (K-Means)
- Interactive network graphs (PyVis)
- Source distribution heatmaps
- Emerging themes discovery

### 🚨 **Smart Alerts**
- Auto-pilot continuous monitoring
- Urgency calculation (High/Medium/Low)
- Correlation analysis (co-occurring catalysts)
- Watchlist management
- Alert history archiving

### 🧾 **History & Exports**
- Session history with diff markers
- ZIP export bundles (MD/HTML/JSON)
- Timestamped filenames
- Metadata tracking

---

## 📊 Key Features

| Feature | Description |
|---------|-------------|
| **Real-Time Feeds** | Google News RSS (Business, Technology, Global) |
| **Sentiment Analysis** | VADER-based scoring (-1 to +1) |
| **Catalyst Detection** | 8 categories (M&A, Earnings, Regulatory, etc.) |
| **AI Reasoning** | Strategic briefs using Flan-T5 models |
| **Network Graphs** | Entity-Catalyst relationship mapping |
| **Auto-Pilot Mode** | Hands-free continuous monitoring |
| **Caching** | 5-minute TTL for performance |
| **No API Keys** | Completely free to use |

---

## 🎯 Use Cases

- **Market Intelligence** — Track sector trends and sentiment shifts
- **Risk Monitoring** — Automated alerts for negative catalysts
- **Strategic Planning** — AI-generated scenario analysis
- **Competitive Analysis** — Entity tracking and momentum detection
- **Research** — Topic clustering and correlation discovery

---

## 📐 Architecture

```
Nexora Intelligence Engine
├── Real-Time RSS Feeds (Google News)
│   ├── Sentiment Analysis (VADER)
│   ├── Catalyst Classification (8 categories)
│   └── Credibility Scoring (domain-based)
│
├── AI Reasoning Layer
│   ├── Article Summarization (BART/Flan-T5)
│   ├── Strategic Analysis (Flan-T5)
│   └── Scenario Generation (Bull/Base/Bear)
│
├── Analytics Engine
│   ├── Trend Analysis (momentum, volatility)
│   ├── Topic Clustering (K-Means)
│   ├── Network Graphs (NetworkX + PyVis)
│   └── Correlation Detection
│
├── Alert System
│   ├── Keyword Monitoring
│   ├── Urgency Calculation
│   ├── Auto-Pilot Mode
│   └── History Archiving
│
└── Storage & Caching
    ├── FAISS (vector search)
    ├── SQLite (article storage)
    └── JSON (watchlists, alerts)
```

---

## 🎨 Screenshots

### Flash News Dashboard
- Live sentiment timeline
- Top movers (positive/negative)
- Smart alerts with urgency badges

### Intelligence Brief
- Strategic scenarios with probabilities
- 30-day sentiment forecast
- Action cards with impact scores

### Trends & Timeline
- Dual-chart momentum analysis
- Sentiment evolution over time
- Volatility index tracking

### Research Lab
- Interactive network graphs
- Topic clustering visualization
- Source distribution heatmaps

---

## 📚 Documentation

- **[Full Documentation](SETUP_AND_FEATURES.md)** — Complete feature guide
- **[Test Suite](test_core.py)** — Core functionality tests

---

## 🔧 Configuration

### Environment Variables (Optional)

```bash
# Use smaller models for faster loading
export NEXORA_STRATEGY_MODEL="google/flan-t5-small"
export NEXORA_SUMMARY_MODEL="sshleifer/distilbart-cnn-12-6"
export NEXORA_EMBEDDER="sentence-transformers/all-MiniLM-L6-v2"

# Adjust log level
export NEXORA_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

### Sidebar Controls

- **Focus Topic** — Research area (e.g., "AI chips market")
- **News to Fetch** — 5-50 articles per refresh
- **Historical Lookback** — 7-90 days for context
- **Auto-refresh** — 5-60 seconds interval
- **Alert Keywords** — Comma-separated (e.g., "NVIDIA, AMD")
- **Auto-Pilot Mode** — Continuous monitoring toggle

---

## 🧪 Testing

Run the test suite to verify core functionality:

```bash
python3 test_core.py
```

Expected output:
```
✅ PASS — Imports
✅ PASS — Utilities
✅ PASS — Sentiment
✅ PASS — Catalysts
✅ PASS — Alerts
✅ PASS — Trends
✅ PASS — Exports

🎉 ALL TESTS PASSED — System ready for deployment
```

---

## 📦 Dependencies

### Core
- `streamlit==1.39.0` — UI framework
- `aiohttp==3.10.5` — Async HTTP
- `feedparser==6.0.11` — RSS parsing

### ML/AI
- `transformers==4.45.2` — LLM reasoning
- `sentence-transformers==3.0.1` — Embeddings
- `torch>=2.2.0` — PyTorch backend
- `vaderSentiment==3.3.2` — Sentiment analysis

### Data/Viz
- `pandas==2.2.3` — Data manipulation
- `altair==5.5.0` — Charts
- `plotly==5.24.1` — Interactive plots
- `networkx==3.2.1` — Graph algorithms
- `pyvis==0.3.2` — Network visualization

### Storage
- `faiss-cpu==1.12.0` — Vector search
- `scikit-learn==1.7.2` — Clustering

See `requirements.txt` for complete list.

---

## 🚀 Performance

- **Startup Time:** ~10s (first run with model downloads)
- **Refresh Cycle:** ~2-3s (25 articles)
- **Memory Usage:** ~1.5GB (with models loaded)
- **Cache Hit Rate:** ~80% (5min TTL)
- **Alert Latency:** <1s (keyword matching)

---

## 🔐 Privacy & Security

- ✅ **No API keys** required
- ✅ **Public RSS feeds** only
- ✅ **Local model execution**
- ✅ **Data stored locally**
- ✅ **No tracking or analytics**
- ✅ **Open-source** and auditable

---

## 🛠️ Troubleshooting

### Issue: Models downloading slowly
**Solution:** Pre-download models or use smaller variants (see Configuration)

### Issue: High memory usage
**Solution:** Set environment variables for smaller models

### Issue: RSS feeds not loading
**Solution:** Check internet connection; app uses cached data as fallback

### Issue: Slow performance
**Solution:** Reduce `n_items` slider, increase `refresh_sec`, disable auto-refresh

See [Full Documentation](SETUP_AND_FEATURES.md) for more troubleshooting tips.

---

## 🗺️ Roadmap

- [ ] Custom RSS source management
- [ ] Multi-language support
- [ ] Email/SMS alert delivery
- [ ] Mobile-responsive design
- [ ] API endpoint for integrations
- [ ] Sentiment prediction (LSTM)

---

## 📝 License

MIT License — See LICENSE file for details.

---

## 🙏 Credits

Built with:
- **Streamlit** — UI framework
- **HuggingFace Transformers** — AI reasoning
- **VADER** — Sentiment analysis
- **FAISS** — Vector search
- **Altair/Plotly** — Visualizations
- **PyVis/NetworkX** — Network graphs
- **Google News** — RSS feeds

---

## 📞 Support

For issues or questions:
1. Check [Full Documentation](SETUP_AND_FEATURES.md)
2. Review [Test Suite](test_core.py) output
3. Inspect browser console (F12)
4. Check Streamlit logs in terminal

---

**⚡ Nexora Intelligence Engine — Decision-Grade Intelligence, Powered by AI**

*Last Updated: 2024-11-07*
