# ✅ Quick Verification Guide

Run these commands to verify the Nexora Intelligence Engine is ready to deploy.

---

## 1. Syntax Check

```bash
cd /workspace
python3 -m py_compile app.py
python3 -m py_compile engine/*.py
```

**Expected:** No output (success)

**Status:** ✅ Already verified — all files compile successfully

---

## 2. Dependency Check

```bash
pip install -r requirements.txt
```

**Expected:** All packages install successfully

**Time:** ~2-5 minutes (depending on network)

---

## 3. Test Suite

```bash
python3 test_core.py
```

**Expected output:**
```
✅ All engine imports successful
✅ Utility functions working
✅ Sentiment analysis working
✅ Catalyst classification working
✅ Alert system working
✅ Trend analysis working
✅ Export functions working

🎉 ALL TESTS PASSED — System ready for deployment
```

---

## 4. Launch Application

```bash
streamlit run app.py
```

**Expected:**
- Opens browser at http://localhost:8501
- Dark gradient theme visible
- Sidebar controls present
- Tabs load without errors

---

## 5. Feature Verification Checklist

### Tab 1: Flash News 🔴
- [ ] Headlines load from RSS
- [ ] Sentiment timeline chart displays
- [ ] Top Movers section shows positive/negative
- [ ] Keyword highlighting works (test with keywords)
- [ ] Smart alerts appear with urgency badges
- [ ] Filters work (sentiment, credibility sliders)

### Tab 2: Intelligence Brief 🧠
- [ ] Click "Generate Advanced Brief" button
- [ ] Status shows progress
- [ ] Executive summary displays
- [ ] Scenario tree with probabilities shows
- [ ] 30-day forecast chart renders
- [ ] Action cards with impact scores display
- [ ] Confidence bar appears
- [ ] Export buttons work (MD/HTML/Playbook)

### Tab 3: Trends & Timeline 📈
- [ ] Avg Sentiment metric displays
- [ ] Volatility Index calculates
- [ ] Top Catalysts bar chart shows
- [ ] Entity Momentum chart displays
- [ ] Sentiment Evolution line chart renders
- [ ] Top Entities table populates
- [ ] Burst Activity table shows data

### Tab 4: Research Lab 🔬
- [ ] Topic clusters display with expandable details
- [ ] Cluster Distribution scatter plot shows
- [ ] "Generate Network Graph" button works
- [ ] Interactive network graph renders (PyVis)
- [ ] Source Distribution heatmap displays
- [ ] "Discover Emerging Themes" button works

### Tab 5: Alerts & Watchlists 🚨
- [ ] Auto-pilot toggle works
- [ ] Current alerts display with urgency colors
- [ ] Smart Correlations table shows
- [ ] Alert history loads (after archiving)
- [ ] Watchlist save/load functions work

### Tab 6: History & Exports 🧾
- [ ] Previous briefs display (after generating)
- [ ] Diff markers show (new/removed actions)
- [ ] "Generate Export Bundle" creates ZIP
- [ ] ZIP contains MD/HTML/JSON files
- [ ] Session export JSON downloads

### Global Features
- [ ] AI Signal badge displays at top
- [ ] Live refresh indicator pulses
- [ ] Metrics update automatically (if auto-refresh enabled)
- [ ] Dark gradient theme consistent throughout
- [ ] Animations work (hover effects, blink badges)
- [ ] No console errors in browser (F12)

---

## 6. Performance Check

### Load Times
- [ ] Initial load: < 15 seconds
- [ ] Tab switches: < 1 second
- [ ] Chart rendering: < 2 seconds
- [ ] RSS refresh: < 5 seconds

### Memory Usage
- [ ] Initial: ~500MB
- [ ] With models loaded: ~1.5GB
- [ ] After 10 refreshes: < 2GB

### Cache Validation
```bash
ls -lh cache/
```
- [ ] Cache files present after first fetch
- [ ] File timestamps update every 5 minutes

---

## 7. Error Handling

### Test Error Scenarios
1. **No internet connection**
   - [ ] App uses cached data
   - [ ] Shows info message, not error

2. **Empty keywords**
   - [ ] App handles gracefully
   - [ ] No crashes

3. **Generate brief with no data**
   - [ ] Shows appropriate message
   - [ ] No exceptions

---

## 8. Export Validation

### Test Exports
1. **Markdown export**
   ```bash
   # After generating brief, click "Export Markdown"
   # Verify .md file downloads
   ```
   - [ ] File contains proper formatting
   - [ ] All sections present

2. **HTML export**
   ```bash
   # Click "Export HTML"
   # Open in browser
   ```
   - [ ] Styled correctly
   - [ ] Dark theme applied
   - [ ] Readable format

3. **ZIP bundle**
   ```bash
   # Click "Generate Export Bundle"
   # Extract and verify contents
   ```
   - [ ] Contains MD, HTML, JSON files
   - [ ] Metadata.json present
   - [ ] Filenames include timestamps

---

## 9. Data Persistence

### Verify Storage
```bash
ls -la data/
```

Expected files:
- [ ] `memory.jsonl` (article memory)
- [ ] `embeddings.faiss` (vector index)
- [ ] `articles.db` (SQLite database)
- [ ] `watchlists/` (directory with saved watchlists)
- [ ] `alerts_history.json` (archived alerts)

---

## 10. Browser Compatibility

Test in:
- [ ] Chrome/Edge (recommended)
- [ ] Firefox
- [ ] Safari

Verify:
- [ ] CSS renders correctly
- [ ] Charts display properly
- [ ] Interactions work smoothly

---

## Common Issues & Solutions

### Issue: Import errors
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Model download fails
```
ConnectionError: ...
```
**Solution:**
- Check internet connection
- Try smaller models (see SETUP_AND_FEATURES.md)

### Issue: High memory usage
**Solution:**
```bash
export NEXORA_STRATEGY_MODEL="google/flan-t5-small"
export NEXORA_SUMMARY_MODEL="sshleifer/distilbart-cnn-12-6"
```

### Issue: Slow performance
**Solution:**
- Reduce `n_items` slider to 10-15
- Increase refresh interval to 30s+
- Disable auto-refresh when not needed

---

## Final Verification Command

Run all checks in sequence:

```bash
cd /workspace

echo "1. Syntax check..."
python3 -m py_compile app.py engine/*.py && echo "✅ Syntax OK"

echo "2. Test suite..."
python3 test_core.py

echo "3. Launch application..."
echo "Run: streamlit run app.py"
echo "Then verify features in browser"
```

---

## Success Criteria

✅ All syntax checks pass
✅ Test suite shows 100% pass rate
✅ Application launches without errors
✅ All 6 tabs load and function correctly
✅ Charts render properly
✅ Exports work as expected
✅ No browser console errors

---

## Ready to Deploy? ✅

If all checks pass:

1. ✅ **Code is production-ready**
2. ✅ **All features implemented**
3. ✅ **Documentation complete**
4. ✅ **Tests passing**

**Status: READY FOR PRODUCTION USE**

---

*Quick Verification Guide*
*Version: 1.0*
*Last Updated: 2024-11-07*
