# Nexora Intelligence Engine - Quick Start Guide

## 🚀 Starting the Application

```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

---

## ⚡ First Time Use

### 1. Initial Load (30-60 seconds)
- App loads theme and dependencies
- Flash news fetches automatically
- Models download on first brief generation

### 2. Quick Setup
1. **Set Topic** - Enter your focus area (e.g., "AI chips market")
2. **Add Keywords** - Comma-separated alerts (e.g., "NVIDIA, AMD, export")
3. **Enable Auto-refresh** - Toggle for live updates
4. **Save Settings** - Go to Settings & Diagnostics tab → Save Current Settings

---

## 📱 Main Features

### 🔴 **Flash News Tab**
- **What:** Real-time news feed with sentiment analysis
- **Use:** Monitor breaking news and top movers
- **Actions:**
  - Filter by sentiment/credibility
  - Pin important items
  - Add to notebook
  - View smart alerts

### 🧠 **Intelligence Brief Tab**
- **What:** AI-generated strategic analysis
- **Use:** Get decision-grade insights
- **Steps:**
  1. Click "Generate Advanced Brief"
  2. Wait for analysis (1-2 minutes first time)
  3. Review scenarios, actions, and triggers
  4. Export as Markdown/HTML/Playbook

### 📈 **Trends & Timeline Tab**
- **What:** Sentiment momentum and anomalies
- **Use:** Track market dynamics
- **Features:**
  - Entity momentum charts
  - Anomaly detection
  - Co-occurrence heatmaps
  - Volatility index

### 🔬 **Research Lab Tab**
- **What:** Topic clustering and network analysis
- **Use:** Discover patterns and connections
- **Features:**
  - Configurable clustering (3-10 clusters)
  - Bubble map visualizations
  - Interactive network graphs
  - Embeddings or TF-IDF

### 🚨 **Alerts & Rules Tab**
- **What:** Custom alert system with backtesting
- **Use:** Create sophisticated monitoring rules
- **Example Rule:**
  ```
  Name: NVIDIA Regulatory Alert
  ANY: keyword:NVIDIA, entity:NVDA
  ALL: sentiment>=-0.3
  Severity: High
  ```

### 📓 **Notebook Tab**
- **What:** Save items for deeper research
- **Use:** Build your intelligence collection
- **Actions:**
  - View saved items
  - Send to brief context
  - Clear notebook

### 🧾 **History & Exports Tab**
- **What:** Past briefs and export tools
- **Use:** Review analysis history
- **Features:**
  - Brief diffs (what changed)
  - ZIP bundle export
  - Session JSON export

### ⚙️ **Settings & Diagnostics Tab** (NEW)
- **What:** System management and diagnostics
- **Use:** Maintain system health
- **Features:**
  - Health checks
  - Cache clearing
  - Settings persistence
  - Session statistics
  - Advanced options

---

## 🎯 Common Workflows

### Workflow 1: Daily Intelligence Briefing
```
1. Open app → Flash News loads automatically
2. Review top movers and alerts
3. Click "Generate Advanced Brief"
4. Review scenarios and actions
5. Export brief as needed
6. Save settings for tomorrow
```

### Workflow 2: Create Custom Alerts
```
1. Go to Alerts & Rules tab
2. Click "Create New Rule"
3. Enter conditions:
   ANY: keyword:MyTopic
   ALL: sentiment>=0.5
4. Set severity and save
5. Test with "Backtest" button
6. Monitor alerts in Flash News
```

### Workflow 3: Research Deep Dive
```
1. Flash News → Pin interesting items
2. Add to Notebook
3. Research Lab → Generate clusters
4. View network graph
5. Trends → Check anomalies
6. Generate brief with context
```

### Workflow 4: System Maintenance
```
1. Settings & Diagnostics tab
2. Run health check
3. Clear caches if slow
4. Export session state
5. Reset if needed
```

---

## 🔧 Troubleshooting

### Problem: App won't start
**Fix:**
```bash
# Clear corrupted cache
Remove-Item -Path "models" -Recurse -Force
Remove-Item -Path "cache" -Recurse -Force

# Restart
streamlit run app.py
```

### Problem: Models not loading
**Fix:**
1. Go to Settings & Diagnostics
2. Click "Clear Model Cache"
3. Restart app
4. Models will re-download

### Problem: Slow performance
**Fix:**
1. Settings & Diagnostics → Clear Data Cache
2. Reduce news items (slider to 10-15)
3. Disable auto-refresh if not needed

### Problem: Brief generation fails
**Fix:**
- Works without historical context
- Check health diagnostics
- Try different query
- Clear caches

---

## 💡 Pro Tips

### 1. **Use Related Terms Expansion**
- Enable in sidebar for broader coverage
- Auto-expands queries with synonyms
- More comprehensive results

### 2. **Save Multiple Profiles**
- Create profiles for different topics
- Quick-switch between analyses
- Saves all settings

### 3. **Leverage Auto-Pilot**
- Enable for continuous monitoring
- Set refresh interval (15s recommended)
- Great for breaking news

### 4. **Master Alert Rules**
- Use ANY for broad matching
- Use ALL for precision
- Backtest before deploying
- Combine keywords with thresholds

### 5. **Export Everything**
- Save briefs as Markdown/HTML
- Export session states
- Create ZIP bundles
- Keep audit trail

---

## 📊 Understanding Metrics

### **Sentiment** (-1 to +1)
- -1.0 to -0.3: Negative
- -0.3 to +0.3: Neutral
- +0.3 to +1.0: Positive

### **Credibility** (0 to 1)
- 0.0 to 0.5: Low
- 0.5 to 0.7: Medium
- 0.7 to 1.0: High

### **Impact Score** (1 to 5)
- 1-2: Low impact
- 3: Medium impact
- 4-5: High impact

### **Volatility Index**
- < 0.2: Stable
- 0.2 to 0.4: Moderate
- > 0.4: Volatile

### **Z-Score** (Anomalies)
- > 2.0: Significant anomaly
- > 3.0: Extreme anomaly

---

## 🎨 Keyboard Shortcuts

- `Ctrl+R` - Refresh page
- `Ctrl+S` - Save (triggers browser save)
- `Esc` - Close modals
- `Tab` - Navigate elements

---

## 📂 Data Locations

### Configuration
- `data/settings.yml` - Your saved settings
- `data/rules.json` - Alert rules
- `data/watchlists.json` - Watchlists

### Cache
- `cache/*.json` - Temporary cache (5 min)
- `models/*` - Downloaded AI models

### History
- `data/memory.jsonl` - Historical context
- `data/alert_history.json` - Alert archive
- `data/articles.db` - SQLite database

---

## 🚀 Advanced Usage

### Custom Queries
```
Basic: "AI chips market"
Advanced: "NVIDIA GPU export restrictions China"
Multi-topic: "semiconductor supply chain"
```

### Alert Conditions
```
Keywords: keyword:NVIDIA, keyword:AMD
Catalysts: catalyst:Regulatory, catalyst:Earnings
Entities: entity:NVDA, entity:INTC
Thresholds: sentiment>=0.5, credibility>=0.7
Sources: source:Reuters, source:Bloomberg
```

### Export Formats
- **Markdown:** For documentation
- **HTML:** For reports
- **Playbook:** For operations
- **JSON:** For data analysis
- **ZIP:** Complete package

---

## 🌟 Best Practices

1. **Save Settings Often** - Don't lose configurations
2. **Use Profiles** - Quick topic switching
3. **Create Smart Rules** - Automate monitoring
4. **Export Regularly** - Keep analysis history
5. **Check Health** - Weekly diagnostics
6. **Clear Caches** - Monthly maintenance
7. **Update Keywords** - As topics evolve
8. **Review Diffs** - Track brief changes
9. **Use Notebook** - Build collections
10. **Monitor Alerts** - Stay informed

---

## 📞 Quick Reference Card

| Task | Location | Action |
|------|----------|--------|
| Change Topic | Sidebar | Enter text |
| Get Analysis | Brief Tab | Click button |
| Create Alert | Alerts Tab | New Rule |
| View History | History Tab | Expand items |
| Save Settings | Settings Tab | Save button |
| Clear Cache | Settings Tab | Clear buttons |
| Export Data | History/Settings | Download |
| Check Health | Settings Tab | Health Check |
| Reset System | Settings Tab | Reset Session |

---

**Ready to use Nexora Intelligence Engine v2.0!** 🎯

All features working. Zero errors. Maximum intelligence. 🚀

