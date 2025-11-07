# 🚀 Nexora Intelligence Engine — Advanced Real-Time Edition

## Overview

**Nexora Intelligence Engine** is a professional-grade, real-time intelligence platform that transforms news feeds into actionable strategic insights. This enhanced version includes advanced AI reasoning, sentiment analysis, network visualization, and automated alert systems.

---

## ✨ Key Enhancements

### 1. **Modern Dark UI/UX** 🎨
- **Dark gradient theme** with animated elements
- **Gradient cards** with hover effects
- **Animated refresh indicators** for live data
- **Urgency badges** with blink animations (High/Medium/Low)
- **AI Signal badges** showing market sentiment (Bullish/Bearish/Neutral/Volatile)
- **Confidence bars** with visual indicators
- **Professional typography** and spacing

### 2. **Flash News Tab** 🔴
- **Real-time RSS feeds** from Google News (Business, Technology)
- **Sentiment timeline chart** showing sentiment evolution
- **Top Movers** section highlighting most positive/negative headlines
- **Keyword highlighting** in titles with golden background
- **Smart filters** for sentiment and credibility
- **Impact scoring** combining sentiment, credibility, and catalyst count
- **Priority alerts** with urgency levels and animated badges

### 3. **Intelligence Brief Tab** 🧠
- **Strategic reasoning** using Flan-T5 models
- **Scenario Tree** with Bull/Base/Bear probabilities
- **Visual probability charts** for scenario comparison
- **30-day sentiment forecast** with Altair line charts
- **Action cards** with impact scores and progress bars
- **Confidence assessment** with visual bar indicator
- **IF/THEN triggers** for automated monitoring
- **Multi-format exports** (Markdown, HTML, Playbook)

### 4. **Trends & Timeline Tab** 📈
- **Dual-chart layout** for catalysts and momentum
- **Volatility Index** calculation using standard deviation
- **Sentiment evolution** over time for top entities
- **Entity momentum** comparison (short vs long window)
- **Burst activity detection** for trending topics
- **Top entities tracking** with frequency counts
- **Interactive Altair charts** with tooltips and color coding

### 5. **Research Lab Tab** 🔬
- **Topic clustering** using TF-IDF and K-Means (6 clusters)
- **Cluster visualization** with scatter plots
- **Interactive network graphs** (Entities ↔ Catalysts) using PyVis
- **Source distribution heatmap** showing article counts per domain
- **Emerging themes discovery** analyzing top 15% by sentiment impact
- **Real-time cluster updates** with expanding details

### 6. **Alerts & Watchlists Tab** 🚨
- **Smart urgency levels** (High/Medium/Low) with color coding
- **Auto-pilot mode** for continuous monitoring
- **Keyword-based alerts** with regex matching
- **Correlation analysis** showing co-occurring catalyst pairs
- **Alert history** with archiving capability
- **Watchlist management** (save/load keyword sets)
- **Gradient cards** for each alert with full details

### 7. **History & Exports Tab** 🧾
- **Session history** with all generated briefs
- **Diff markers** showing changes between briefs (new/removed actions)
- **ZIP export bundles** containing:
  - Markdown files for each brief
  - HTML files with styling
  - JSON metadata and full data
  - Session metadata with timestamps
- **One-click session export** as JSON
- **Timestamped filenames** for organization

### 8. **AI Core Monitor** 🤖
- **Real-time sentiment drift** calculation
- **Volatility tracking** across all feeds
- **AI signal determination** (⬆ Bullish / ⬇ Bearish / ⚡ Volatile / ⚖ Neutral)
- **Live metrics dashboard** at top of page
- **Auto-refresh indicator** with pulsing animation

### 9. **Backend Optimizations** ⚡
- **5-minute caching** for RSS feeds (TTL: 300s)
- **Fallback to expired cache** when rate-limited
- **Rate limiting** (8 seconds between feeds)
- **Async feed fetching** with aiohttp
- **Memory-efficient storage** with FAISS + SQLite
- **Optimized sentiment analysis** using VADER
- **Parallel RSS parsing** for multiple sources

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager
- 4GB+ RAM (for local models)
- Internet connection (for RSS feeds)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download Models (Optional)

The application will automatically download required models on first run:
- `sentence-transformers/all-MiniLM-L6-v2` (embeddings)
- `google/flan-t5-base` (strategic reasoning)
- `facebook/bart-large-cnn` (summarization)

Models are cached in the `models/` directory.

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📊 Features Breakdown

### Real-Time Intelligence
- Fetches live headlines from Google News RSS feeds
- Processes 25+ articles per refresh cycle
- Updates every 15 seconds (configurable)
- No API keys required — uses public RSS feeds

### Sentiment Analysis
- **VADER sentiment scoring** (-1 to +1 scale)
- Multi-catalyst classification (M&A, Earnings, Regulatory, etc.)
- Credibility scoring based on source domain
- Time-series sentiment tracking

### Strategic Reasoning
- **Scenario planning** with Bull/Base/Bear paths
- **Action recommendations** with impact scores (0-100%)
- **Risk identification** and mitigation strategies
- **KPI tracking** suggestions
- **Timeline milestones** (T+2, T+7, T+30)

### Network Analysis
- **Entity extraction** from headlines
- **Catalyst co-occurrence** detection
- **Interactive graph visualization** with PyVis
- **Community detection** in topic clusters

### Alert System
- **Keyword monitoring** with regex support
- **Urgency calculation** based on multiple factors
- **Auto-pilot mode** for hands-free monitoring
- **Alert archiving** for historical tracking

---

## 🎯 Usage Guide

### Basic Workflow

1. **Set Focus Topic** — Enter your research area (e.g., "AI chips market")
2. **Configure Keywords** — Add alert keywords (e.g., "NVIDIA", "regulation")
3. **Enable Auto-refresh** — Toggle live updates (recommended)
4. **Review Flash News** — Check sentiment trends and top movers
5. **Generate Brief** — Click "Generate Advanced Brief" for strategic analysis
6. **Explore Trends** — Analyze momentum and volatility
7. **Check Alerts** — Monitor urgent signals
8. **Export Results** — Download briefs in multiple formats

### Advanced Features

#### Auto-Pilot Mode
Enable in sidebar to continuously monitor keywords. Alerts trigger automatically when:
- Sentiment exceeds ±0.6
- 3+ catalysts detected in a single article
- Any keyword matches in title/summary

#### Watchlists
Save frequently-used keyword sets for quick switching:
1. Enter keywords in sidebar
2. Name the watchlist
3. Click "Save Watchlist"
4. Load anytime from dropdown

#### Export Bundles
Generate complete ZIP archives with:
- All briefs in Markdown format
- Styled HTML versions
- Full JSON data dumps
- Metadata with timestamps

---

## 📐 Architecture

```
app.py                    # Main Streamlit UI
├── engine/
│   ├── __init__.py       # Module exports
│   ├── utils.py          # Utilities, analytics, AI signals
│   ├── live.py           # RSS feed fetching (cached)
│   ├── ingest.py         # Deep article ingestion
│   ├── sentiment.py      # VADER sentiment scoring
│   ├── classify.py       # Catalyst classification
│   ├── credibility.py    # Source credibility weights
│   ├── trends.py         # Trend analysis, volatility
│   ├── alerts.py         # Alert generation, correlations
│   ├── research.py       # Clustering, network graphs
│   ├── reason_analyst.py # Article summarization
│   ├── reason_strategic.py # Strategic brief generation
│   ├── memory.py         # FAISS + SQLite storage
│   ├── brief.py          # Export formatting
│   ├── predictors.py     # Momentum reports
│   └── storage.py        # Watchlist/alert persistence
├── models/               # Cached ML models
├── data/                 # FAISS index, SQLite DB, watchlists
├── cache/                # RSS feed cache (5min TTL)
└── exports/              # Generated briefs and bundles
```

---

## 🔬 Technical Details

### RSS Sources
- Google News Global Feed
- Google News Business
- Google News Technology
- Reuters (filtered via site: operator)
- Bloomberg (filtered via site: operator)

### Catalyst Categories
1. **M&A** — Mergers, acquisitions, takeovers
2. **Earnings** — EPS, guidance, results
3. **Regulatory** — Lawsuits, sanctions, bans
4. **Macroeconomy** — Inflation, rates, GDP
5. **Product/Tech** — Launches, AI, chips
6. **Geopolitics** — Tariffs, conflicts, export controls
7. **ESG** — Climate, emissions, sustainability
8. **Supply Chain** — Shortages, logistics

### Sentiment Drift Calculation
```python
recent_sentiment = mean(last_5_items)
older_sentiment = mean(next_5_items)
drift = recent_sentiment - older_sentiment
```

### Volatility Index
```python
volatility = stddev(all_sentiments)
```

### AI Signal Logic
```
IF sentiment_avg > 0.2 AND drift > 0.1:
    signal = "⬆ Bullish"
ELIF sentiment_avg < -0.2 AND drift < -0.1:
    signal = "⬇ Bearish"
ELIF volatility > 0.4:
    signal = "⚡ Volatile"
ELSE:
    signal = "⚖ Neutral"
```

---

## 🚀 Performance Optimizations

1. **Caching Strategy**
   - RSS feeds: 5 minutes
   - Article bodies: 1 hour
   - Embeddings: Persistent (FAISS index)

2. **Rate Limiting**
   - Minimum 8 seconds between feed fetches
   - Concurrent article downloads (8 workers)

3. **Memory Management**
   - SQLite for article storage
   - FAISS for vector search
   - Incremental JSONL logs

4. **Model Loading**
   - Lazy initialization
   - CPU-only inference (no GPU required)
   - Quantization support (optional)

---

## 📊 Data Flow

```
1. User sets focus topic
2. RSS feeds fetched (Google News)
3. Articles parsed, sentiment scored
4. Catalysts classified, credibility assessed
5. Alerts generated if keywords match
6. User requests brief
7. Deep article ingestion (async)
8. Articles summarized and tagged
9. Historical context retrieved (FAISS)
10. Strategic reasoning (Flan-T5)
11. Scenarios, actions, triggers generated
12. Results displayed with charts
13. Export options available
```

---

## 🎨 UI/UX Highlights

- **Dark gradient background** (#0a0e27 → #1a1f3a)
- **Gradient cards** with hover effects
- **Animated urgency badges** (blink for High)
- **AI signal display** with gradient background
- **Confidence bars** with indicator markers
- **Altair charts** for data visualization
- **PyVis network graphs** for relationships
- **Responsive layout** (wide mode)
- **Tab-based navigation** with icons
- **Toast notifications** for actions

---

## 🔐 Security & Privacy

- **No external API keys** required
- **Public RSS feeds only** (Google News)
- **Local model execution** (no cloud calls)
- **Data stored locally** (FAISS, SQLite)
- **No user tracking** or analytics
- **Open-source** and auditable

---

## 🐛 Troubleshooting

### Issue: Models downloading slowly
**Solution:** Pre-download models:
```python
from transformers import pipeline
pipeline("text2text-generation", model="google/flan-t5-base")
```

### Issue: High memory usage
**Solution:** Use smaller models via environment variables:
```bash
export NEXORA_STRATEGY_MODEL="google/flan-t5-small"
export NEXORA_SUMMARY_MODEL="sshleifer/distilbart-cnn-12-6"
```

### Issue: RSS feeds not loading
**Solution:** Check network connection and RSS source availability. The app will use cached data if available.

### Issue: Slow performance
**Solution:**
1. Reduce `n_items` slider value
2. Increase `refresh_sec` to 30+
3. Disable auto-refresh when not needed
4. Clear cache folder periodically

---

## 📈 Roadmap & Future Enhancements

- [ ] Custom RSS source management
- [ ] Multi-language support
- [ ] Email/SMS alert delivery
- [ ] Database export (PostgreSQL)
- [ ] API endpoint for external integrations
- [ ] Mobile-responsive design
- [ ] Dark/light theme toggle
- [ ] Voice briefing generation (TTS)
- [ ] Backtesting framework
- [ ] Sentiment prediction (LSTM/Transformers)

---

## 📝 License & Credits

**Nexora Intelligence Engine** — MIT License

### Technologies Used
- **Streamlit** — UI framework
- **Transformers (HuggingFace)** — LLM reasoning
- **VADER Sentiment** — Sentiment analysis
- **FAISS** — Vector similarity search
- **Altair** — Data visualization
- **PyVis** — Network graphs
- **NetworkX** — Graph algorithms
- **scikit-learn** — Clustering (K-Means)
- **feedparser** — RSS parsing
- **aiohttp** — Async HTTP
- **BeautifulSoup** — HTML parsing

### Data Sources
- Google News RSS (Public feeds)
- No proprietary data used

---

## 🤝 Contributing

This is an autonomous intelligence platform. To extend:

1. **Add new catalysts** — Edit `engine/classify.py`
2. **Add RSS sources** — Edit `engine/live.py`
3. **Customize UI** — Modify CSS in `app.py`
4. **Add analytics** — Extend `engine/utils.py`
5. **Improve reasoning** — Tune prompts in `engine/reason_strategic.py`

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Inspect browser console (F12)
4. Check Streamlit logs in terminal

---

**Built with ⚡ by Nexora — Powering Decision-Grade Intelligence**

*Last Updated: 2024-11-07*
