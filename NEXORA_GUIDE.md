# 🔮 Nexora Intelligence Workbench - YC-Ready Edition

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🎯 Product Overview

Nexora Intelligence Workbench is a **real-time intelligence terminal** that transforms raw news into **decision-grade strategic briefs**. Built for speed, insights, and reliability — completely local, no API keys required.

### Core Value Propositions

1. **Real-time Intelligence**: Live news from Google RSS, refreshed on-demand or auto-pilot mode
2. **Decision-Grade Briefs**: Structured scenarios (Bull/Base/Bear) with action plans and IF/THEN triggers
3. **Advanced Analytics**: Momentum tracking, topic clustering, co-occurrence analysis
4. **Smart Alerts**: Rule-based alert system with backtesting
5. **Beautiful UX**: Pro dark theme with micro-interactions and polished components

---

## 🎛️ Control Panel (Sidebar)

### Focus Topic
Type any topic you want to track (e.g., "AI chips", "quantum computing", "Tesla earnings")

### Region & Language
- **Region**: Global, US, EU, APAC, Custom
- **Language**: en, es, fr, de, zh

### Time Window
- 24h, 7d, 30d (affects context and historical analysis)

### Auto-Pilot Mode 🤖
- Toggle on to enable background refresh
- Adjust refresh interval (10-120 seconds)
- App will continuously fetch news and update AI Signal

### Keywords
- Add comma-separated keywords for highlighting
- Keywords are highlighted throughout the app in Flash News

### Related Terms Auto-Expand 🔗
- When enabled, automatically expands your query with synonyms and related terms
- Example: "AI chips" → "artificial intelligence", "semiconductor", "processor"

### Presets
- **Save Profile**: Save current settings as a preset
- **Load Profile**: Restore previously saved settings

---

## 📊 Tab 1: Flash News

### Features
- **Live RSS Feed**: Fetch real-time news from Google News
- **Filtering**: Min sentiment, min credibility, "only pinned"
- **Top Movers**: Headlines with highest absolute sentiment
- **Burst Detector**: Entities with sudden mention spikes
- **Keyword Highlighting**: Your keywords are highlighted in titles
- **Row Actions**:
  - 📝 **Add to Notebook**: Save interesting items
  - 🔗 **Read**: Open source article

### Metrics
- 📰 **Items**: Total headlines fetched
- 😊 **Avg Sentiment**: Average sentiment score (-1 to +1)
- ✅ **Avg Credibility**: Average credibility score (0 to 1)
- 🚨 **Alerts**: Number of triggered alert rules

### How to Use
1. Click **"📡 Fetch Live News"**
2. Review headlines and metrics
3. Apply filters to focus on high-impact items
4. Add interesting items to Notebook for later reference

---

## 🧠 Tab 2: Intelligence Brief

### Features
- **Executive Summary**: High-level overview
- **Immediate Impact**: Near-term implications
- **Scenario Tree**: 3 scenarios (Bull/Base/Bear) with probabilities
- **Actions Deck**: 4-8 actionable recommendations with impact scores (1-5)
- **IF/THEN Triggers**: 6-12 watch conditions for monitoring
- **Confidence Score**: High/Medium/Low with visual indicator

### How to Use
1. Fetch flash news first (Tab 1)
2. Click **"🧠 Generate Advanced Brief"**
3. Review scenarios, actions, and triggers
4. Export as Markdown, JSON, or ZIP bundle

### Brief Components

#### Scenarios
- **Bull**: Optimistic path with upside catalysts
- **Base**: Most likely path with balanced view
- **Bear**: Pessimistic path with downside risks

Each scenario includes:
- Probability (sum to ~100%)
- Path: Step-by-step progression
- Signals: Observable triggers

#### Actions
Each action includes:
- **Impact Score**: 1-5 (higher = more impactful)
- **Rationale**: Why this action matters
- **Steps**: Concrete implementation steps
- **Sizing**: Resource allocation guidance
- **KPIs**: Metrics to track success
- **Timeline**: T+7, T+30, T+60 milestones
- **Risks**: Potential downsides
- **Mitigations**: Risk management strategies

---

## 📈 Tab 3: Trends & Timeline

### Features
- **Sentiment Average**: Overall market sentiment
- **Volatility Index**: Sentiment standard deviation
- **Top Entities**: Most mentioned companies/orgs
- **Top Catalysts**: Most frequent catalyst types
- **Entity Momentum**: Short-term vs long-term sentiment comparison
- **Catalyst Momentum**: Momentum for each catalyst type

### Metrics Explained

#### Momentum (Δ Delta)
- **Positive Δ**: Short-term sentiment higher than long-term (bullish momentum)
- **Negative Δ**: Short-term sentiment lower than long-term (bearish momentum)
- Sorted by absolute delta to show strongest momentum shifts

#### Volatility Index
- Higher volatility = more sentiment swings
- Lower volatility = stable sentiment

### How to Use
1. Fetch flash news
2. Review bar charts for top entities and catalysts
3. Check momentum tables for directional insights
4. Use momentum data to inform brief interpretation

---

## 🔬 Tab 4: Research Lab

### Features
- **Topic Clustering**: Automatically groups related headlines
- **Source Heatmap**: Distribution of news sources
- **Notebook**: Saved items from Flash News

### Clustering
- Uses **TF-IDF + KMeans** algorithm
- Identifies 6 topic clusters automatically
- Shows top terms for each cluster
- Sample headlines for exploration

### How to Use
1. Fetch flash news
2. Click **"🔬 Run Clustering"**
3. Expand clusters to see topics and items
4. Review source distribution
5. Manage saved items in Notebook

---

## 🚨 Tab 5: Watchlists & Alerts

### Alert Rules System

Rules use a simple DSL (Domain Specific Language):

```json
{
  "name": "Regulatory spike",
  "any": ["keyword:ban", "catalyst:Regulatory"],
  "all": ["sentiment>=0.2"],
  "min_sentiment": 0.2,
  "min_credibility": 0.6,
  "severity": "High",
  "enabled": true
}
```

### Rule Components

- **ANY**: At least one condition must match (OR logic)
  - `keyword:X` - Title contains keyword X
  - `catalyst:Y` - Catalysts list contains Y
  - `entity:Z` - Entities list contains Z
  
- **ALL**: All conditions must match (AND logic)
  - `sentiment>=0.2` - Sentiment threshold
  - `credibility>=0.6` - Credibility threshold

- **Severity**: Low, Medium, High, Critical

### How to Use

1. **Create Rule**: Fill in the form and click "💾 Save Rule"
2. **Test Rule**: Click "🧪 Test" to see current matches
3. **Backtest Rule**: Click "📊 Backtest" to evaluate historical performance
4. **Run All Rules**: Click "🚨 Run All Rules Now" to trigger all enabled rules

### Backtesting Metrics
- **Matches**: Number of historical headlines that matched
- **Precision Proxy**: % of matches with |sentiment| >= 0.6 (significant)
- **Avg Sentiment**: Average sentiment of matched items

---

## 🧾 Tab 6: History & Export

### Features
- **Brief History**: All generated briefs with timestamps
- **Session Export**: Save entire session state
- **Session Import**: Restore previous session

### Export Options

#### Per-Brief Exports
- **Markdown**: Human-readable format
- **JSON**: Machine-readable format
- **ZIP Bundle**: Markdown + JSON + charts (when available)

#### Session Export
Includes:
- Current query and settings
- Flash data (last 50 items)
- All generated briefs
- Notebook items
- Alert rules
- History (last 100 items)
- Timestamp

### How to Use
1. Review brief history
2. Export individual briefs or entire session
3. Import session to restore previous state

---

## 🚀 Advanced Features

### AI Signal Banner
- Displayed at the top of the main page
- **⬆️ Bullish**: Positive sentiment + strong momentum
- **⬇️ Bearish**: Negative sentiment + strong momentum
- **⚖️ Neutral**: Balanced or weak momentum

Updated automatically in auto-pilot mode.

### Auto-Pilot Mode
- Enable in sidebar
- Refreshes flash news at configured interval
- Recomputes trends and momentum
- Updates AI Signal
- Runs in background without blocking UI

### Keyboard Shortcuts & Tips
- Use **Ctrl+K** (or Cmd+K on Mac) to search Streamlit components
- Use **R** to refresh the page
- **Esc** closes dialogs and expanders

---

## 🧪 Acceptance Test Checklist

Run these tests to verify all features work:

### ✅ 1. Application Launch
- [ ] App starts without errors
- [ ] All 6 tabs visible
- [ ] Sidebar renders completely
- [ ] Theme CSS loads (dark background, accent colors)

### ✅ 2. Focus Topic Change
- [ ] Type "quantum networking" in Focus Topic
- [ ] Click "Fetch Live News"
- [ ] Verify headlines update within 2 seconds
- [ ] Try other topics: "graphite", "ai chips", "tesla"

### ✅ 3. Intelligence Brief
- [ ] Fetch flash news
- [ ] Click "Generate Advanced Brief"
- [ ] Verify complete brief with 3 scenarios
- [ ] Verify 4+ actions with impact scores
- [ ] Verify 6+ IF/THEN triggers
- [ ] Check confidence indicator

### ✅ 4. Trends & Timeline
- [ ] After fetching news, go to Trends tab
- [ ] Verify non-empty bar charts
- [ ] Check momentum tables populate
- [ ] No "Series truth" errors

### ✅ 5. Research Lab
- [ ] Fetch 10+ headlines
- [ ] Click "Run Clustering"
- [ ] Verify clusters appear without error
- [ ] Check source heatmap visible

### ✅ 6. Alerts
- [ ] Create new rule
- [ ] Click "Test" to see current matches
- [ ] Click "Backtest" to see historical performance
- [ ] Verify rule saves
- [ ] Run all rules and see alerts

### ✅ 7. History & Export
- [ ] Generate 2+ briefs
- [ ] Check brief history shows both
- [ ] Export Markdown
- [ ] Export JSON
- [ ] Export session
- [ ] Import session and verify restoration

### ✅ 8. Auto-Pilot
- [ ] Enable auto-pilot
- [ ] Set refresh interval to 15s
- [ ] Wait 15+ seconds
- [ ] Verify flash data updates
- [ ] Verify AI signal updates
- [ ] Check no UI blocking

### ✅ 9. Performance
- [ ] First render < 2 seconds
- [ ] Flash refresh < 1 second (from cache)
- [ ] No spinner stalls
- [ ] UI remains responsive during background tasks

### ✅ 10. Error Handling
- [ ] Try empty focus topic → should show friendly message
- [ ] Generate brief with no data → should fallback gracefully
- [ ] All errors show helpful messages, not stack traces

---

## 🛠️ Troubleshooting

### Models Download Slowly
- First run downloads Flan-T5 and sentence-transformers models
- Models cached in `models/` directory
- Subsequent runs are faster

### RSS Fetch Fails
- Check internet connection
- Google News RSS might be rate-limited
- Wait 30-60 seconds and retry
- Enable cache to use recent data

### Clustering Errors
- Need at least 6 headlines for clustering
- If error persists, check sklearn installation
- Fallback creates single cluster with all items

### Auto-Pilot Not Updating
- Check interval setting (minimum 10s)
- Verify toggle is ON
- Check console for background task errors
- Try manual refresh first

---

## 📦 Dependencies

### Core
- **streamlit**: Web framework
- **aiohttp**: Async HTTP client
- **feedparser**: RSS parsing
- **pydantic**: Data validation
- **PyYAML**: Settings persistence

### ML/AI
- **transformers**: Flan-T5 for reasoning
- **sentence-transformers**: Embeddings
- **scikit-learn**: Clustering
- **torch**: PyTorch backend

### Analytics
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **altair**: Visualizations

### Utilities
- **vaderSentiment**: Sentiment analysis
- **networkx**: Graph analysis
- **beautifulsoup4**: HTML parsing

---

## 🎨 Customization

### Theme Colors
Edit `assets/theme.css`:
- `--bg`: Background color
- `--card`: Card background
- `--text`: Text color
- `--accent`: Accent/highlight color
- `--danger`: High severity color
- `--success`: Positive indicators

### Default Settings
Edit initial values in `app.py`:
- Default query
- Default keywords
- Default refresh interval
- Default region/language

### RSS Sources
Edit `engine/ingest.py`:
- Modify `_build_feed_url()` to use different RSS feeds
- Add multiple sources and merge results

---

## 💡 Best Practices

### For Daily Use
1. Set up **watchlists** for topics you track regularly
2. Save **presets** for different use cases
3. Enable **auto-pilot** during market hours
4. Review **briefs** daily and compare deltas
5. **Export session** before major changes

### For Research
1. Fetch **30+ headlines** for better clustering
2. Use **notebook** to collect interesting items
3. Run **backtests** on rules before relying on them
4. Compare **momentum** across time windows
5. Track **confidence scores** over time

### For Alerts
1. Start with **Medium severity**, adjust based on backtest
2. Use **keyword:X** for specific terms
3. Combine **any** and **all** for precision
4. Set **min_credibility >= 0.7** for high-quality sources
5. Backtest with at least **100 historical items**

---

## 🚀 Next Steps

### Immediate
1. ✅ Verify all acceptance tests pass
2. ✅ Customize default settings for your use case
3. ✅ Create watchlists and alert rules
4. ✅ Generate your first brief

### Short-term
- Add more RSS sources (industry-specific)
- Train custom sentiment model on your domain
- Build dashboard for multi-topic monitoring
- Integrate with Slack/Discord for alerts

### Long-term
- Add historical time-series charts
- Implement portfolio simulation
- Add collaborative features (team briefs)
- Build mobile companion app

---

## 📞 Support

For issues or questions:
1. Check this guide thoroughly
2. Review error messages (they're designed to be helpful!)
3. Check `streamlit` logs in terminal
4. Verify all dependencies installed: `pip install -r requirements.txt`

---

## 🎯 Product Philosophy

**Nexora is built on these principles:**

1. **Local-first**: No API keys, no cloud dependencies
2. **Fast**: < 2s first render, sub-second refreshes
3. **Reliable**: Deterministic fallbacks, graceful degradation
4. **Insightful**: Decision-grade output, not raw data dumps
5. **Beautiful**: YC-grade polish, not prototype aesthetics

---

**Built with ❤️ for strategic decision-makers**

Version: 1.0.0-YC-Ready

