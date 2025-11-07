"""
Nexora Intelligence Workbench - YC-Ready Product
Real-time intelligence terminal with decision-grade briefs
"""
import streamlit as st
import asyncio
import pandas as pd
import json
import os
import time
from datetime import datetime
import yaml

# Engine imports
from engine.models import Brief, Scenario, ActionPlan
from engine.ingest import fetch_live_news, expand_terms
from engine.reason_strategic import strategic_reason
from engine.trends import build_trends, momentum_report
from engine.research import cluster_topics, source_heatmap
from engine.alerts import load_rules, save_rules, run_rules, backtest_rule
from engine.tasks import TaskLoop
from engine.utils import (
    ensure_dirs,
    highlight,
    time_ago,
    save_zip_bundle,
    dedupe_by_id,
    safe_export_json,
    log,
    DATA_DIR
)

# ---------- Page Config ----------
st.set_page_config(
    page_title="Nexora Intelligence Workbench",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Theme Injection ----------
try:
    with open("assets/theme.css", "r", encoding="utf-8") as _f:
        st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# ---------- Ensure Directories ----------
ensure_dirs()

# ---------- Session State Init ----------
if "context" not in st.session_state:
    st.session_state["context"] = {
        "query": "AI chips market",
        "region": "Global",
        "language": "en",
        "time_window": "24h",
        "refresh_interval": 15,
        "auto_pilot": False,
        "expand_terms": False,
        "keywords": ["NVIDIA", "ARM", "AMD", "export", "ban"],
        "watchlists": {},
        "flash_data": [],
        "history": [],
        "briefs": [],
        "notebook": [],
        "rules": load_rules(),
        "task_loop": None,
        "last_refresh": 0,
        "ai_signal": "Neutral",
    }

CTX = st.session_state["context"]

# ---------- Settings Persistence ----------
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.yml")

def save_settings():
    """Save current settings to YAML"""
    try:
        settings = {
            "query": CTX["query"],
            "region": CTX["region"],
            "language": CTX["language"],
            "time_window": CTX["time_window"],
            "refresh_interval": CTX["refresh_interval"],
            "expand_terms": CTX["expand_terms"],
            "keywords": CTX["keywords"],
            "watchlists": CTX["watchlists"],
        }
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            yaml.dump(settings, f)
        st.toast("✅ Settings saved", icon="✅")
    except Exception as e:
        st.error(f"Failed to save settings: {e}")

def load_settings():
    """Load settings from YAML"""
    if not os.path.exists(SETTINGS_PATH):
        return
    
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = yaml.safe_load(f)
        
        if settings:
            for key in ["query", "region", "language", "time_window", "refresh_interval", "expand_terms", "keywords", "watchlists"]:
                if key in settings:
                    CTX[key] = settings[key]
        st.toast("✅ Settings loaded", icon="✅")
    except Exception as e:
        st.error(f"Failed to load settings: {e}")

# ---------- Auto-Pilot Background Task ----------
async def _autopilot_refresh():
    """Background refresh task for auto-pilot mode"""
    try:
        # Fetch fresh news
        flash = await fetch_live_news(
            limit=30,
            query=CTX["query"],
            expand=CTX["expand_terms"]
        )
        
        # Update context
        CTX["flash_data"] = flash
        CTX["last_refresh"] = time.time()
        
        # Compute AI signal
        if flash:
            trends = build_trends(flash)
            momentum = momentum_report(flash)
            
            # Heuristic: positive momentum + positive sentiment = bullish
            sent_avg = trends["sentiment_avg"]
            has_momentum = any(abs(x[3]) > 0.2 for x in momentum["entity_momentum"][:3])
            
            if sent_avg > 0.2 and has_momentum:
                CTX["ai_signal"] = "Bullish"
            elif sent_avg < -0.2 and has_momentum:
                CTX["ai_signal"] = "Bearish"
            else:
                CTX["ai_signal"] = "Neutral"
        
        log.info("Auto-pilot refresh completed")
        
    except Exception as e:
        log.error(f"Auto-pilot refresh failed: {e}")

# ---------- Sidebar: Control Panel 2.0 ----------
with st.sidebar:
    st.title("🎛️ Control Panel")
    
    # Focus Topic
    query = st.text_input("🔍 Focus Topic", CTX["query"], key="input_query")
    if query != CTX["query"]:
        CTX["query"] = query
    
    # Region & Language
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("🌍 Region", ["Global", "US", "EU", "APAC", "Custom"], index=0)
        CTX["region"] = region
    
    with col2:
        language = st.selectbox("🗣️ Language", ["en", "es", "fr", "de", "zh"], index=0)
        CTX["language"] = language
    
    # Time Window
    time_window = st.selectbox("⏰ Time Window", ["24h", "7d", "30d"], index=0)
    CTX["time_window"] = time_window
    
    st.divider()
    
    # Auto-Pilot
    auto_pilot = st.toggle("🤖 Auto-Pilot", CTX["auto_pilot"])
    
    if auto_pilot != CTX["auto_pilot"]:
        CTX["auto_pilot"] = auto_pilot
        
        if auto_pilot:
            # Start task loop
            if CTX["task_loop"] is None or not CTX["task_loop"].is_running:
                CTX["task_loop"] = TaskLoop(interval_s=CTX["refresh_interval"])
                CTX["task_loop"].start(_autopilot_refresh)
                st.toast("🚀 Auto-Pilot activated", icon="🚀")
        else:
            # Stop task loop
            if CTX["task_loop"] and CTX["task_loop"].is_running:
                CTX["task_loop"].stop()
                st.toast("⏸️ Auto-Pilot paused", icon="⏸️")
    
    # Refresh Interval
    if auto_pilot:
        refresh_interval = st.slider("🔄 Refresh (sec)", 10, 120, CTX["refresh_interval"], 5)
        CTX["refresh_interval"] = refresh_interval
    
    st.divider()
    
    # Keywords
    st.subheader("🔑 Keywords")
    keywords_str = st.text_area("Comma-separated", ", ".join(CTX["keywords"]), height=80)
    CTX["keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]
    
    # Related Terms Expansion
    expand_terms = st.toggle("🔗 Auto-Expand Related Terms", CTX["expand_terms"])
    CTX["expand_terms"] = expand_terms
    
    if expand_terms:
        related = expand_terms(CTX["query"])
        st.caption(f"📎 Expanded: {', '.join(related[:5])}")
    
    st.divider()
    
    # Presets
    st.subheader("💾 Presets")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Profile"):
            profile_name = f"profile_{len(CTX['watchlists']) + 1}"
            CTX["watchlists"][profile_name] = {
                "query": CTX["query"],
                "keywords": CTX["keywords"],
                "expand_terms": CTX["expand_terms"],
            }
            save_settings()
    
    with col2:
        if CTX["watchlists"] and st.button("📂 Load Profile"):
            first_profile = list(CTX["watchlists"].values())[0]
            CTX["query"] = first_profile.get("query", CTX["query"])
            CTX["keywords"] = first_profile.get("keywords", CTX["keywords"])
            CTX["expand_terms"] = first_profile.get("expand_terms", CTX["expand_terms"])
            st.rerun()
    
    st.divider()
    
    # Last Refresh
    if CTX["last_refresh"]:
        st.caption(f"🕐 Last refresh: {time_ago(CTX['last_refresh'])}")
    
    # Manual Refresh
    if st.button("🔄 Refresh Now"):
        asyncio.run(_autopilot_refresh())
        st.rerun()

# ---------- AI Signal Banner ----------
signal_class = "ai-signal-neutral"
signal_icon = "⚖️"

if CTX["ai_signal"] == "Bullish":
    signal_class = "ai-signal-bullish"
    signal_icon = "⬆️"
elif CTX["ai_signal"] == "Bearish":
    signal_class = "ai-signal-bearish"
    signal_icon = "⬇️"

st.markdown(f"""
<div class="{signal_class}">
    {signal_icon} AI Signal: <strong>{CTX["ai_signal"]}</strong>
</div>
""", unsafe_allow_html=True)

# ---------- Main Tabs ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔴 Flash News",
    "🧠 Intelligence Brief",
    "📈 Trends & Timeline",
    "🔬 Research Lab",
    "🚨 Watchlists & Alerts",
    "🧾 History & Export"
])

# ========== TAB 1: FLASH NEWS ==========
with tab1:
    st.header("🔴 Flash News")
    
    # Filters
    with st.expander("⚙️ Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_sent = st.slider("Min |Sentiment|", 0.0, 1.0, 0.0, 0.1)
        with col2:
            min_cred = st.slider("Min Credibility", 0.0, 1.0, 0.0, 0.1)
        with col3:
            only_pinned = st.checkbox("Only Pinned")
    
    # Fetch News Button
    if st.button("📡 Fetch Live News", type="primary"):
        with st.spinner("Fetching news..."):
            flash = asyncio.run(fetch_live_news(
                limit=30,
                query=CTX["query"],
                expand=CTX["expand_terms"]
            ))
            CTX["flash_data"] = flash
            CTX["history"].extend(flash)
            CTX["history"] = dedupe_by_id(CTX["history"])[-500:]  # Keep last 500
            CTX["last_refresh"] = time.time()
            st.rerun()
    
    # Flash Data
    flash = CTX["flash_data"]
    
    if not flash:
        st.info("👆 Click 'Fetch Live News' to load headlines")
    else:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📰 Items", len(flash))
        
        with col2:
            avg_sent = sum(f.get("sentiment", 0) for f in flash) / len(flash)
            st.metric("😊 Avg Sentiment", f"{avg_sent:+.2f}")
        
        with col3:
            avg_cred = sum(f.get("credibility", 0) for f in flash) / len(flash)
            st.metric("✅ Avg Credibility", f"{avg_cred:.2f}")
        
        with col4:
            alerts = run_rules(CTX["rules"], flash)
            st.metric("🚨 Alerts", len(alerts))
        
        st.divider()
        
        # Top Movers
        if len(flash) >= 5:
            st.subheader("📊 Top Movers")
            sorted_flash = sorted(flash, key=lambda x: abs(x.get("sentiment", 0)), reverse=True)[:5]
            
            for item in sorted_flash:
                sentiment = item.get("sentiment", 0)
                emoji = "🟢" if sentiment > 0 else "🔴" if sentiment < 0 else "⚪"
                title_hl = highlight(item.get("title", ""), CTX["keywords"])
                st.markdown(f"{emoji} **{sentiment:+.2f}** | {title_hl}", unsafe_allow_html=True)
        
        st.divider()
        
        # Flash Table
        st.subheader("📋 Headlines")
        
        # Apply filters
        filtered = flash
        if min_sent > 0:
            filtered = [f for f in filtered if abs(f.get("sentiment", 0)) >= min_sent]
        if min_cred > 0:
            filtered = [f for f in filtered if f.get("credibility", 0) >= min_cred]
        
        if not filtered:
            st.warning("No headlines match filters")
        else:
            for idx, item in enumerate(filtered[:20]):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        title_hl = highlight(item.get("title", ""), CTX["keywords"])
                        st.markdown(f"**{title_hl}**", unsafe_allow_html=True)
                        
                        # Metadata
                        source = item.get("source", "Unknown")
                        ts = item.get("timestamp", 0)
                        sentiment = item.get("sentiment", 0)
                        credibility = item.get("credibility", 0)
                        
                        st.caption(f"📰 {source} | 🕐 {time_ago(ts)} | 😊 {sentiment:+.2f} | ✅ {credibility:.2f}")
                        
                        # Catalysts & Entities
                        catalysts = item.get("catalysts", [])
                        if catalysts:
                            pills = " ".join([f'<span class="pill">{c}</span>' for c in catalysts[:3]])
                            st.markdown(pills, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("📝", key=f"note_{idx}"):
                            CTX["notebook"].append(item)
                            st.toast("Added to notebook", icon="📝")
                        
                        link = item.get("link", "#")
                        st.markdown(f"[🔗 Read]({link})")
                
                st.divider()

# ========== TAB 2: INTELLIGENCE BRIEF ==========
with tab2:
    st.header("🧠 Intelligence Brief")
    
    if st.button("🧠 Generate Advanced Brief", type="primary"):
        if not CTX["flash_data"]:
            st.warning("⚠️ No flash data. Fetch news first.")
        else:
            with st.spinner("Generating strategic brief..."):
                try:
                    # Generate brief
                    brief_data = strategic_reason(
                        query=CTX["query"],
                        analyzed=CTX["flash_data"],
                        historical=CTX["history"][-100:]
                    )
                    
                    # Create Brief object
                    brief = Brief(**brief_data)
                    
                    # Store in history
                    CTX["briefs"].append(brief.dict())
                    
                    st.success("✅ Brief generated!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to generate brief: {e}")
    
    # Show most recent brief
    if CTX["briefs"]:
        latest_brief = Brief(**CTX["briefs"][-1])
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        st.markdown(f"<div class='card'>{latest_brief.executive_summary}</div>", unsafe_allow_html=True)
        
        # Immediate Impact
        st.subheader("⚡ Immediate Impact")
        st.markdown(f"<div class='card'>{latest_brief.immediate_impact}</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Scenarios
        st.subheader("🎯 Scenario Tree")
        
        for scenario in latest_brief.scenarios:
            with st.expander(f"**{scenario.name}** - {scenario.prob}%", expanded=False):
                st.progress(scenario.prob / 100)
                
                st.markdown("**Path:**")
                for step in scenario.path:
                    st.markdown(f"- {step}")
                
                st.markdown("**Signals:**")
                for signal in scenario.signals:
                    st.markdown(f"🔔 {signal}")
        
        st.divider()
        
        # Actions Deck
        st.subheader("🎬 Actions Deck")
        
        for action in latest_brief.actions:
            impact_class = "impact-high" if action.impact_score >= 4 else "impact-medium" if action.impact_score >= 3 else "impact-low"
            
            with st.expander(f"**{action.title}** | Impact: {action.impact_score}/5", expanded=False):
                st.markdown(f"<span class='{impact_class}'>Impact Score: {action.impact_score}</span>", unsafe_allow_html=True)
                
                st.markdown(f"**Rationale:** {action.rationale}")
                
                if action.steps:
                    st.markdown("**Steps:**")
                    for step in action.steps:
                        st.markdown(f"- {step}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Sizing:** {action.sizing}")
                    st.markdown(f"**Timeline:** {action.timeline}")
                
                with col2:
                    if action.kpis:
                        st.markdown("**KPIs:**")
                        for kpi in action.kpis:
                            st.markdown(f"- {kpi}")
                
                if action.risks:
                    st.markdown("**Risks:**")
                    for risk in action.risks:
                        st.markdown(f"⚠️ {risk}")
                
                if action.mitigations:
                    st.markdown("**Mitigations:**")
                    for mitigation in action.mitigations:
                        st.markdown(f"✅ {mitigation}")
        
        st.divider()
        
        # Watch Triggers
        st.subheader("🔔 IF/THEN Triggers")
        
        for trigger in latest_brief.watch_triggers:
            st.markdown(f"- {trigger}")
        
        st.divider()
        
        # Confidence
        st.subheader("📊 Confidence")
        confidence_score = {"High": 0.85, "Medium": 0.6, "Low": 0.35}.get(latest_brief.confidence, 0.5)
        st.progress(confidence_score)
        st.caption(f"Confidence: **{latest_brief.confidence}**")
        
        # Export
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export Markdown"):
                md = f"# Intelligence Brief: {CTX['query']}\n\n"
                md += f"Generated: {latest_brief.created_at}\n\n"
                md += f"## Executive Summary\n\n{latest_brief.executive_summary}\n\n"
                md += f"## Immediate Impact\n\n{latest_brief.immediate_impact}\n\n"
                st.download_button("📥 Download MD", md, f"brief_{int(time.time())}.md", "text/markdown")
        
        with col2:
            if st.button("📦 Export JSON"):
                json_str = json.dumps(latest_brief.dict(), indent=2)
                st.download_button("📥 Download JSON", json_str, f"brief_{int(time.time())}.json", "application/json")
        
        with col3:
            if st.button("🗜️ Export ZIP Bundle"):
                files = {
                    "brief.json": json.dumps(latest_brief.dict(), indent=2),
                    "brief.md": f"# Brief: {CTX['query']}\n\n{latest_brief.executive_summary}",
                }
                import io
                import zipfile
                
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, "w") as z:
                    for name, data in files.items():
                        z.writestr(name, data)
                buffer.seek(0)
                
                st.download_button("📥 Download ZIP", buffer, f"brief_{int(time.time())}.zip", "application/zip")
    
    else:
        st.info("👆 Generate a brief to see results")

# ========== TAB 3: TRENDS & TIMELINE ==========
with tab3:
    st.header("📈 Trends & Timeline")
    
    if not CTX["flash_data"]:
        st.info("👆 Fetch news first to see trends")
    else:
        # Build trends
        trends = build_trends(CTX["flash_data"])
        momentum = momentum_report(CTX["flash_data"])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Avg Sentiment", f"{trends['sentiment_avg']:+.2f}")
        
        with col2:
            st.metric("📈 Volatility Index", f"{trends['volatility']:.3f}")
        
        with col3:
            st.metric("🔑 Top Entities", len(trends['top_entities']))
        
        with col4:
            st.metric("⚡ Top Catalysts", len(trends['top_catalysts']))
        
        st.divider()
        
        # Top Entities
        st.subheader("🏢 Top Entities")
        
        if trends['top_entities']:
            entity_df = pd.DataFrame(trends['top_entities'], columns=["Entity", "Mentions"])
            st.bar_chart(entity_df.set_index("Entity")["Mentions"])
        else:
            st.caption("No entities detected")
        
        # Top Catalysts
        st.subheader("⚡ Top Catalysts")
        
        if trends['top_catalysts']:
            catalyst_df = pd.DataFrame(trends['top_catalysts'], columns=["Catalyst", "Mentions"])
            st.bar_chart(catalyst_df.set_index("Catalyst")["Mentions"])
        else:
            st.caption("No catalysts detected")
        
        st.divider()
        
        # Momentum Tables
        st.subheader("🚀 Entity Momentum")
        
        if momentum['entity_momentum']:
            mom_df = pd.DataFrame(momentum['entity_momentum'], columns=["Entity", "Short Avg", "Long Avg", "Delta"])
            st.dataframe(mom_df, use_container_width=True)
        else:
            st.caption("Insufficient data for momentum analysis")
        
        st.subheader("⚡ Catalyst Momentum")
        
        if momentum['catalyst_momentum']:
            cat_mom_df = pd.DataFrame(momentum['catalyst_momentum'], columns=["Catalyst", "Short Avg", "Long Avg", "Delta"])
            st.dataframe(cat_mom_df, use_container_width=True)
        else:
            st.caption("Insufficient data for momentum analysis")

# ========== TAB 4: RESEARCH LAB ==========
with tab4:
    st.header("🔬 Research Lab")
    
    if not CTX["flash_data"]:
        st.info("👆 Fetch news first for research")
    else:
        # Cluster Topics
        st.subheader("🧬 Topic Clusters")
        
        if st.button("🔬 Run Clustering"):
            with st.spinner("Clustering topics..."):
                clusters = cluster_topics(CTX["flash_data"], k=6)
                st.session_state["clusters"] = clusters
                st.rerun()
        
        if "clusters" in st.session_state and st.session_state["clusters"]:
            clusters = st.session_state["clusters"]
            
            for cluster in clusters:
                with st.expander(f"📦 Cluster {cluster['cluster']} ({cluster['count']} items)"):
                    st.markdown(f"**Top Terms:** {', '.join(cluster['top_terms'][:6])}")
                    
                    st.markdown("**Sample Items:**")
                    for item in cluster['items'][:5]:
                        st.markdown(f"- {item.get('title', '')[:100]}")
        
        st.divider()
        
        # Source Heatmap
        st.subheader("📰 Source Distribution")
        
        source_df = source_heatmap(CTX["flash_data"])
        if not source_df.empty:
            st.bar_chart(source_df.set_index("source")["count"])
        else:
            st.caption("No sources found")
        
        st.divider()
        
        # Notebook
        st.subheader("📔 Notebook")
        
        if CTX["notebook"]:
            st.caption(f"📝 {len(CTX['notebook'])} saved items")
            
            for idx, item in enumerate(CTX["notebook"][-10:]):
                with st.container():
                    st.markdown(f"**{item.get('title', '')}**")
                    st.caption(f"📰 {item.get('source', '')} | 🕐 {time_ago(item.get('timestamp', 0))}")
                    
                    if st.button("🗑️ Remove", key=f"remove_notebook_{idx}"):
                        CTX["notebook"].remove(item)
                        st.rerun()
                    
                    st.divider()
        else:
            st.info("📝 No saved items. Use '📝' button in Flash News to add items.")

# ========== TAB 5: WATCHLISTS & ALERTS ==========
with tab5:
    st.header("🚨 Watchlists & Alerts")
    
    # Rules Editor
    st.subheader("⚙️ Alert Rules")
    
    with st.expander("➕ Create New Rule", expanded=True):
        rule_name = st.text_input("Rule Name", "Unnamed Rule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            any_keywords = st.text_input("Any Keywords (comma-separated)", "ban, restriction")
            any_catalysts = st.text_input("Any Catalysts (comma-separated)", "Regulatory")
        
        with col2:
            min_sentiment = st.slider("Min Sentiment", -1.0, 1.0, 0.2, 0.1)
            min_credibility = st.slider("Min Credibility", 0.0, 1.0, 0.6, 0.1)
        
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        
        if st.button("💾 Save Rule"):
            # Build rule
            any_conds = []
            if any_keywords:
                for kw in any_keywords.split(","):
                    kw = kw.strip()
                    if kw:
                        any_conds.append(f"keyword:{kw}")
            
            if any_catalysts:
                for cat in any_catalysts.split(","):
                    cat = cat.strip()
                    if cat:
                        any_conds.append(f"catalyst:{cat}")
            
            rule = {
                "name": rule_name,
                "any": any_conds,
                "all": [f"sentiment>={min_sentiment}"],
                "min_sentiment": min_sentiment,
                "min_credibility": min_credibility,
                "severity": severity,
                "enabled": True,
            }
            
            CTX["rules"].append(rule)
            save_rules(CTX["rules"])
            st.toast("✅ Rule saved", icon="✅")
            st.rerun()
    
    st.divider()
    
    # Existing Rules
    st.subheader("📋 Saved Rules")
    
    if CTX["rules"]:
        for idx, rule in enumerate(CTX["rules"]):
            with st.expander(f"📌 {rule.get('name', 'Unnamed')} | {rule.get('severity', 'Medium')}"):
                st.json(rule)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🧪 Test", key=f"test_rule_{idx}"):
                        if CTX["flash_data"]:
                            alerts = run_rules([rule], CTX["flash_data"])
                            st.info(f"✅ Matched {len(alerts)} items")
                        else:
                            st.warning("⚠️ No flash data to test")
                
                with col2:
                    if st.button("📊 Backtest", key=f"backtest_rule_{idx}"):
                        if CTX["history"]:
                            results = backtest_rule(rule, CTX["history"])
                            st.json(results)
                        else:
                            st.warning("⚠️ No historical data")
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_rule_{idx}"):
                        CTX["rules"].pop(idx)
                        save_rules(CTX["rules"])
                        st.rerun()
    else:
        st.info("📝 No rules yet. Create one above.")
    
    st.divider()
    
    # Run All Rules
    if st.button("🚨 Run All Rules Now", type="primary"):
        if not CTX["flash_data"]:
            st.warning("⚠️ No flash data. Fetch news first.")
        else:
            alerts = run_rules(CTX["rules"], CTX["flash_data"])
            
            if alerts:
                st.success(f"✅ {len(alerts)} alerts triggered")
                
                for alert in alerts[:20]:
                    severity_class = f"severity-{alert['severity'].lower()}"
                    st.markdown(f"<span class='{severity_class}'>🚨 {alert['severity']}</span> | **{alert['rule_name']}**", unsafe_allow_html=True)
                    st.markdown(f"{alert['title']}")
                    st.caption(f"📰 {alert['source']} | [🔗 Read]({alert['link']})")
                    st.divider()
            else:
                st.info("✅ No alerts triggered")

# ========== TAB 6: HISTORY & EXPORT ==========
with tab6:
    st.header("🧾 History & Export")
    
    # Brief History
    st.subheader("📚 Brief History")
    
    if CTX["briefs"]:
        st.caption(f"📊 {len(CTX['briefs'])} briefs generated")
        
        for idx, brief_data in enumerate(reversed(CTX["briefs"])):
            brief = Brief(**brief_data)
            
            with st.expander(f"📄 Brief #{len(CTX['briefs']) - idx} | {brief.created_at[:10]}"):
                st.markdown(f"**Executive Summary:** {brief.executive_summary[:200]}...")
                st.markdown(f"**Confidence:** {brief.confidence}")
                
                if st.button("📥 Export", key=f"export_brief_{idx}"):
                    json_str = json.dumps(brief.dict(), indent=2)
                    st.download_button(
                        "📥 Download JSON",
                        json_str,
                        f"brief_{idx}.json",
                        "application/json",
                        key=f"download_brief_{idx}"
                    )
    else:
        st.info("📝 No briefs generated yet")
    
    st.divider()
    
    # Session Export
    st.subheader("💾 Session Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📦 Export Session"):
            session_data = {
                "query": CTX["query"],
                "flash_data": CTX["flash_data"][:50],
                "briefs": CTX["briefs"],
                "notebook": CTX["notebook"],
                "rules": CTX["rules"],
                "history": CTX["history"][-100:],
                "exported_at": datetime.utcnow().isoformat(),
            }
            
            json_str = safe_export_json(session_data)
            st.download_button(
                "📥 Download Session JSON",
                json_str,
                f"nexora_session_{int(time.time())}.json",
                "application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📂 Import Session JSON", type="json")
        
        if uploaded_file:
            try:
                session_data = json.load(uploaded_file)
                
                # Restore state
                for key in ["query", "flash_data", "briefs", "notebook", "rules", "history"]:
                    if key in session_data:
                        CTX[key] = session_data[key]
                
                st.success("✅ Session imported!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Failed to import: {e}")

# ---------- Footer ----------
st.divider()
st.caption("🔮 Nexora Intelligence Workbench | YC-Ready Edition | © 2025")
