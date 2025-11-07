#!/usr/bin/env python3
"""
Core functionality test for Nexora Intelligence Engine.
Run this before deploying to verify all modules load correctly.
"""

import sys

def test_imports():
    """Test all critical imports."""
    print("🔍 Testing imports...")
    
    try:
        from engine import (
            ensure_dirs, fetch_live_news, ingest_query, MemoryStore,
            analyze_articles, strategic_reason,
            build_trends, sentiment_evolution, momentum_report, 
            cluster_topics, source_heatmap, build_network_graph,
            render_markdown, render_html, render_playbook,
            generate_alerts, find_correlations, calculate_urgency,
            save_watchlist, load_watchlists,
            save_alert_history, load_alert_history,
            calculate_sentiment_drift, calculate_volatility, get_ai_signal,
            highlight_keywords, generate_forecast_data,
        )
        print("✅ All engine imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_utilities():
    """Test utility functions."""
    print("\n🔍 Testing utility functions...")
    
    try:
        from engine.utils import (
            calculate_sentiment_drift,
            calculate_volatility,
            get_ai_signal,
            highlight_keywords,
            generate_forecast_data,
        )
        
        # Test sample data
        sample_items = [
            {"sentiment": 0.5, "catalysts": ["Earnings"]},
            {"sentiment": 0.3, "catalysts": ["M&A"]},
            {"sentiment": -0.2, "catalysts": ["Regulatory"]},
            {"sentiment": 0.1, "catalysts": ["Product/Tech"]},
            {"sentiment": 0.4, "catalysts": ["Earnings"]},
        ]
        
        drift = calculate_sentiment_drift(sample_items)
        vol = calculate_volatility(sample_items)
        signal = get_ai_signal(0.2, drift, vol)
        
        print(f"  Drift: {drift:.3f}")
        print(f"  Volatility: {vol:.3f}")
        print(f"  AI Signal: {signal}")
        
        # Test keyword highlighting
        text = "NVIDIA announces new AI chips"
        highlighted = highlight_keywords(text, ["NVIDIA", "AI"])
        assert "<mark" in highlighted
        
        # Test forecast generation
        forecast = generate_forecast_data(0.3, 0.2, days=10)
        assert len(forecast) == 10
        
        print("✅ Utility functions working")
        return True
        
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False

def test_sentiment():
    """Test sentiment analysis."""
    print("\n🔍 Testing sentiment analysis...")
    
    try:
        from engine.sentiment import score_sentiment
        
        positive = score_sentiment("This is amazing and wonderful news!")
        negative = score_sentiment("Terrible disaster and catastrophic failure.")
        neutral = score_sentiment("The company reported its quarterly results.")
        
        print(f"  Positive: {positive:.3f}")
        print(f"  Negative: {negative:.3f}")
        print(f"  Neutral: {neutral:.3f}")
        
        assert positive > 0.3
        assert negative < -0.3
        assert -0.3 < neutral < 0.3
        
        print("✅ Sentiment analysis working")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment test failed: {e}")
        return False

def test_catalysts():
    """Test catalyst classification."""
    print("\n🔍 Testing catalyst classification...")
    
    try:
        from engine.classify import classify_catalysts
        
        text1 = "Company announces merger and acquisition deal"
        text2 = "New regulations and antitrust lawsuit filed"
        text3 = "Earnings beat expectations with strong guidance"
        
        cats1 = classify_catalysts(text1)
        cats2 = classify_catalysts(text2)
        cats3 = classify_catalysts(text3)
        
        print(f"  M&A text: {cats1}")
        print(f"  Regulatory text: {cats2}")
        print(f"  Earnings text: {cats3}")
        
        assert "M&A" in cats1
        assert "Regulatory" in cats2
        assert "Earnings" in cats3
        
        print("✅ Catalyst classification working")
        return True
        
    except Exception as e:
        print(f"❌ Catalyst test failed: {e}")
        return False

def test_alerts():
    """Test alert generation."""
    print("\n🔍 Testing alert generation...")
    
    try:
        from engine.alerts import generate_alerts, calculate_urgency, find_correlations
        
        sample_items = [
            {
                "title": "NVIDIA announces record earnings",
                "link": "http://example.com/1",
                "source": "Reuters",
                "sentiment": 0.8,
                "catalysts": ["Earnings", "Product/Tech"],
                "timestamp": 1234567890,
            },
            {
                "title": "AMD faces regulatory challenges",
                "link": "http://example.com/2",
                "source": "Bloomberg",
                "sentiment": -0.6,
                "catalysts": ["Regulatory", "M&A"],
                "timestamp": 1234567891,
            }
        ]
        
        alerts = generate_alerts(sample_items, ["NVIDIA", "AMD"])
        print(f"  Generated {len(alerts)} alerts")
        
        urgency = calculate_urgency(0.8, 3, 2)
        print(f"  Sample urgency: {urgency}")
        
        corr = find_correlations(sample_items, min_cooccurrence=1)
        print(f"  Correlations: {corr}")
        
        print("✅ Alert system working")
        return True
        
    except Exception as e:
        print(f"❌ Alert test failed: {e}")
        return False

def test_trends():
    """Test trend analysis."""
    print("\n🔍 Testing trend analysis...")
    
    try:
        from engine.trends import build_trends, sentiment_evolution
        import time
        
        sample_items = [
            {
                "title": "NVIDIA reports strong growth",
                "sentiment": 0.7,
                "catalysts": ["Earnings"],
                "timestamp": time.time(),
            },
            {
                "title": "AMD announces new chips",
                "sentiment": 0.5,
                "catalysts": ["Product/Tech"],
                "timestamp": time.time(),
            }
        ]
        
        trends = build_trends(sample_items)
        print(f"  Avg sentiment: {trends['sentiment_avg']:.3f}")
        print(f"  Volatility: {trends.get('volatility', 0.0):.3f}")
        print(f"  Top entities: {len(trends['top_entities'])}")
        
        print("✅ Trend analysis working")
        return True
        
    except Exception as e:
        print(f"❌ Trend test failed: {e}")
        return False

def test_exports():
    """Test export functions."""
    print("\n🔍 Testing export functions...")
    
    try:
        from engine.brief import render_markdown, render_html, render_playbook
        
        sample_brief = {
            "executive_summary": "Test summary",
            "immediate_impact": "Test impact",
            "scenarios": [
                {"name": "Bull", "prob": 40, "path": ["Path 1"], "signals": ["Signal 1"]}
            ],
            "actions": [
                {
                    "title": "Test Action",
                    "rationale": "Test rationale",
                    "steps": ["Step 1"],
                    "sizing": "10%",
                    "kpis": ["KPI 1"],
                    "timeline": "T+7",
                    "risks": ["Risk 1"],
                    "mitigations": ["Mitigation 1"]
                }
            ],
            "watch_triggers": ["Trigger 1"],
            "confidence": "Medium"
        }
        
        md = render_markdown("Test Brief", sample_brief)
        html = render_html("Test Brief", sample_brief)
        playbook = render_playbook("Test Query", sample_brief, [])
        
        assert len(md) > 100
        assert len(html) > 100
        assert len(playbook) > 50
        
        print(f"  Markdown: {len(md)} chars")
        print(f"  HTML: {len(html)} chars")
        print(f"  Playbook: {len(playbook)} chars")
        
        print("✅ Export functions working")
        return True
        
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("NEXORA INTELLIGENCE ENGINE — CORE FUNCTIONALITY TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    
    if results[0][1]:  # Only continue if imports work
        results.append(("Utilities", test_utilities()))
        results.append(("Sentiment", test_sentiment()))
        results.append(("Catalysts", test_catalysts()))
        results.append(("Alerts", test_alerts()))
        results.append(("Trends", test_trends()))
        results.append(("Exports", test_exports()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED — System ready for deployment")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED — Review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
