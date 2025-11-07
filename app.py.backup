import asyncio, time, json, os, zipfile, io
from typing import Dict, List
import pandas as pd
import altair as alt
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

from engine import (
    ensure_dirs, fetch_live_news, ingest_query, MemoryStore,
    analyze_articles, strategic_reason,
    build_trends, sentiment_evolution, momentum_report, cluster_topics, source_heatmap, build_network_graph,
    render_markdown, render_html, render_playbook,
    generate_alerts, find_correlations, calculate_urgency,
    save_watchlist, load_watchlists,
    save_alert_history, load_alert_history,
    calculate_sentiment_drift, calculate_volatility, get_ai_signal,
    highlight_keywords, generate_forecast_data,
)

# ========== SETUP ==========
st.set_page_config(page_title="⚡ Nexora Intelligence Engine", layout="wide", initial_sidebar_state="expanded")
ensure_dirs()

# ========== DARK THEME & ANIMATIONS ==========
st.markdown("""
<style>
/* Main dark theme with gradients */
.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
}

/* Gradient cards */
.gradient-card {
    background: linear-gradient(135deg, #1e2746 0%, #2a3556 100%);
    border-radius: 14px;
    padding: 20px;
    margin: 12px 0;
    border: 1px solid #3a4566;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}

.gradient-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}

/* Metric cards with glow */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
}

/* Animated refresh indicator */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.refresh-indicator {
    animation: pulse 2s ease-in-out infinite;
    color: #4CAF50;
    font-weight: 600;
}

/* Alert urgency badges */
.urgency-high {
    background: #ff4444;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
    animation: blink 1.5s ease-in-out infinite;
}

.urgency-medium {
    background: #ff9800;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
}

.urgency-low {
    background: #4CAF50;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* AI Signal badge */
.ai-signal {
    font-size: 1.4rem;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 8px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: inline-block;
    margin: 8px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    background-color: #1e2746;
    border: 1px solid #3a4566;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: 2px solid #667eea;
}

/* Data tables */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Confidence bar */
.confidence-bar {
    height: 20px;
    border-radius: 10px;
    background: linear-gradient(90deg, #ff4444 0%, #ff9800 50%, #4CAF50 100%);
    position: relative;
    margin: 10px 0;
}

.confidence-indicator {
    position: absolute;
    width: 4px;
    height: 30px;
    background: white;
    top: -5px;
    box-shadow: 0 0 8px rgba(255,255,255,0.8);
}
</style>
""", unsafe_allow_html=True)

# ========== GLOBAL STATE ==========
if "context" not in st.session_state:
    st.session_state["context"] = {
        "query": "AI chips market",
        "keywords": ["NVIDIA", "ARM", "AMD", "export"],
        "flash_data": [],
        "analysis_data": None,
        "alerts": [],
        "history": [],
        "auto_pilot": False,
    }
CTX = st.session_state["context"]

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### ⚡ Nexora Control Center")
    st.divider()
    
    CTX["query"] = st.text_input("🎯 Focus Topic", CTX["query"])
    n_items = st.slider("📰 News to Fetch", 5, 50, 24)
    lookback = st.slider("📅 Historical Lookback (days)", 7, 90, 30)
    refresh_sec = st.slider("🔄 Auto-refresh (seconds)", 5, 60, 15)
    auto_refresh = st.toggle("🔴 Enable Live Auto-refresh", True)
    
    st.divider()
    st.markdown("### 🚨 Alert Keywords")
    kw_text = st.text_area("Keywords (comma-separated)", ", ".join(CTX["keywords"]), height=80)
    CTX["keywords"] = [k.strip() for k in kw_text.split(",") if k.strip()]
    
    # Auto-pilot mode
    CTX["auto_pilot"] = st.toggle("🤖 Auto-pilot Mode (Continuous monitoring)", CTX.get("auto_pilot", False))
    
    st.divider()
    st.markdown("### 📋 Watchlists")
    name = st.text_input("Save current keywords as", "")
    if st.button("💾 Save Watchlist") and name:
        save_watchlist(name, CTX["keywords"])
        st.success("✅ Saved!")
    
    lists = load_watchlists()
    if lists:
        opt = st.selectbox("Load watchlist", [""] + [w["name"] for w in lists])
        if opt and st.button("📥 Load Selected"):
            for w in lists:
                if w["name"] == opt:
                    CTX["keywords"] = w["keywords"]
                    st.success("✅ Loaded!")
                    st.rerun()
    
    st.divider()
    st.caption(f"🕐 Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    if auto_refresh:
        st.markdown('<p class="refresh-indicator">● LIVE</p>', unsafe_allow_html=True)

# ========== AUTO-REFRESH ==========
if auto_refresh and int(time.time()) % refresh_sec == 0:
    st.rerun()

# ========== AI SIGNAL MONITOR ==========
if CTX.get("flash_data"):
    sentiment_avg = sum(it.get("sentiment", 0.0) for it in CTX["flash_data"]) / len(CTX["flash_data"])
    drift = calculate_sentiment_drift(CTX["flash_data"])
    volatility = calculate_volatility(CTX["flash_data"])
    ai_signal = get_ai_signal(sentiment_avg, drift, volatility)
    
    st.markdown(f'<div class="ai-signal">🤖 AI Signal: {ai_signal}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Avg Sentiment", f"{sentiment_avg:+.3f}")
    col2.metric("📈 Drift", f"{drift:+.3f}")
    col3.metric("⚡ Volatility", f"{volatility:.3f}")
    col4.metric("📰 Items", len(CTX["flash_data"]))

st.divider()

# ========== TABS ==========
tabs = st.tabs([
    "🔴 Flash News",
    "🧠 Intelligence Brief",
    "📈 Trends & Timeline",
    "🔬 Research Lab",
    "🚨 Alerts & Watchlists",
    "🧾 History & Exports",
])

# ========== TAB 1: FLASH NEWS ==========
with tabs[0]:
    st.markdown("### 🔴 Live Flash Intelligence Feed")
    
    flash = fetch_live_news(limit=n_items)
    CTX["flash_data"] = flash
    
    if not flash:
        st.info("⏳ Fetching headlines...")
    else:
        df = pd.DataFrame(flash)
        df["impact"] = df["sentiment"].abs()*2 + df["credibility"] + df["catalysts"].apply(lambda x: len(x or []))
        df.sort_values("impact", ascending=False, inplace=True)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📰 Items", len(df))
        col2.metric("📊 Avg Sentiment", f"{df['sentiment'].mean():+.2f}")
        col3.metric("🎯 Avg Credibility", f"{df['credibility'].mean():.2f}")
        col4.metric("🔥 High Impact", len(df[df["impact"] > 4]))
        
        # Sentiment timeline chart
        st.markdown("#### 📈 Sentiment Timeline")
        if "timestamp" in df.columns:
            timeline_df = df[["timestamp", "sentiment"]].copy()
            timeline_df["time"] = pd.to_datetime(timeline_df["timestamp"], unit="s")
            
            chart = alt.Chart(timeline_df).mark_line(point=True, strokeWidth=3).encode(
                x=alt.X("time:T", title="Time"),
                y=alt.Y("sentiment:Q", title="Sentiment", scale=alt.Scale(domain=[-1, 1])),
                color=alt.condition(
                    alt.datum.sentiment > 0,
                    alt.value("#4CAF50"),
                    alt.value("#ff4444")
                ),
                tooltip=["time:T", "sentiment:Q"]
            ).properties(height=200)
            
            st.altair_chart(chart, use_container_width=True)
        
        # Top Movers
        st.markdown("#### 🚀 Top Movers (Sentiment)")
        top_positive = df.nlargest(3, "sentiment")[["title", "sentiment", "source"]]
        top_negative = df.nsmallest(3, "sentiment")[["title", "sentiment", "source"]]
        
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**🟢 Most Positive**")
            for _, row in top_positive.iterrows():
                st.markdown(f"- **{row['title'][:80]}...** ({row['sentiment']:+.2f}) — *{row['source']}*")
        
        with colB:
            st.markdown("**🔴 Most Negative**")
            for _, row in top_negative.iterrows():
                st.markdown(f"- **{row['title'][:80]}...** ({row['sentiment']:+.2f}) — *{row['source']}*")
        
        st.divider()
        
        # Filters
        st.markdown("#### 🔍 Filter & Explore")
        min_abs = st.slider("Min |sentiment|", 0.0, 1.0, 0.15, 0.05)
        min_cred = st.slider("Min credibility", 0.0, 1.0, 0.6, 0.05)
        filt = (df["sentiment"].abs() >= min_abs) & (df["credibility"] >= min_cred)
        
        # Keyword highlighting
        display_df = df.loc[filt, ["title","source","sentiment","credibility","catalysts","link"]].copy()
        if CTX["keywords"]:
            display_df["title"] = display_df["title"].apply(lambda t: highlight_keywords(t, CTX["keywords"]))
        
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Smart Alerts
        st.divider()
        st.markdown("#### 🚨 Smart Alerts")
        alerts = generate_alerts(flash, CTX["keywords"])
        CTX["alerts"] = alerts
        
        if alerts:
            st.success(f"✅ {len(alerts)} Priority Alerts Detected")
            for a in alerts[:8]:
                urgency = a.get("urgency", "Low")
                urgency_class = f"urgency-{urgency.lower()}"
                st.markdown(
                    f'<div class="gradient-card">'
                    f'<span class="{urgency_class}">{urgency}</span> '
                    f'<strong>[{", ".join(a["catalysts"][:3]) or "Signal"}]</strong> '
                    f'{a["title"]} — <em>{a["source"]}</em> | '
                    f'<code>{a["sentiment"]:+.2f}</code> '
                    f'<a href="{a["link"]}" target="_blank">🔗 Open</a>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            if st.button("📥 Archive Alerts"):
                save_alert_history(alerts)
                st.success("✅ Archived!")
        else:
            st.info("💤 No priority alerts right now.")

# ========== TAB 2: INTELLIGENCE BRIEF ==========
with tabs[1]:
    st.markdown("### 🧠 Strategic Intelligence Brief")
    st.caption("Decision-grade plan with scenarios, actions, KPIs, timelines, risks & mitigations.")
    
    if st.button("🧩 Generate Advanced Brief", type="primary"):
        with st.status("🔄 Collecting & reasoning...", expanded=True) as status:
            status.write("📡 Ingesting sources...")
            articles = asyncio.run(ingest_query(CTX["query"], max_items=n_items))
            status.write(f"✅ Fetched {len(articles)} items")
            
            status.update(label="🧠 Summarizing & tagging...")
            analyzed = analyze_articles(articles)
            mem = MemoryStore()
            mem.add_documents(analyzed)
            retrieved = mem.similarity_search(CTX["query"], k=6, lookback_days=lookback)
            
            status.update(label="🎯 Strategic planning...")
            brief = strategic_reason(CTX["query"], analyzed, retrieved)
            CTX["analysis_data"] = brief
            st.session_state["context"]["history"].append({
                "query": CTX["query"], 
                "reasoning": brief, 
                "ts": datetime.now().isoformat()
            })
            
            status.update(label="✅ Complete", state="complete")
    
    brief = CTX.get("analysis_data") or {}
    
    if brief:
        # Executive Summary
        st.markdown("### 🧭 Executive Summary")
        st.markdown(f'<div class="gradient-card">{brief.get("executive_summary", "")}</div>', unsafe_allow_html=True)
        
        # Immediate Impact
        st.markdown("### ⚡ Immediate Impact")
        st.markdown(f'<div class="gradient-card">{brief.get("immediate_impact", "")}</div>', unsafe_allow_html=True)
        
        # Scenario Tree
        st.markdown("### 🌲 Scenario Tree (30 days)")
        scenarios = brief.get("scenarios", [])
        if scenarios:
            # Scenario probability chart
            scenario_df = pd.DataFrame([
                {"Scenario": sc.get("name", ""), "Probability": sc.get("prob", 0)}
                for sc in scenarios
            ])
            
            chart = alt.Chart(scenario_df).mark_bar().encode(
                x=alt.X("Probability:Q", title="Probability (%)", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Scenario:N", title=""),
                color=alt.Color("Scenario:N", scale=alt.Scale(
                    domain=["Bull", "Base", "Bear"],
                    range=["#4CAF50", "#2196F3", "#ff4444"]
                )),
                tooltip=["Scenario", "Probability"]
            ).properties(height=150)
            
            st.altair_chart(chart, use_container_width=True)
            
            for sc in scenarios:
                with st.expander(f"{sc.get('name','Scenario')} — Probability: {sc.get('prob','?')}%", 
                                expanded=(sc.get("name")=="Base")):
                    st.markdown("**Narrative Path:**")
                    for p in sc.get("path", []):
                        st.markdown(f"- {p}")
                    
                    if sc.get("signals"):
                        st.markdown("**🔔 Signals to Watch:**")
                        for sig in sc.get("signals", []):
                            st.markdown(f"- {sig}")
        
        # 30-Day Forecast Chart
        st.markdown("### 📊 30-Day Sentiment Forecast")
        if CTX.get("flash_data"):
            sent_avg = sum(it.get("sentiment", 0.0) for it in CTX["flash_data"]) / len(CTX["flash_data"])
            vol = calculate_volatility(CTX["flash_data"])
            forecast = generate_forecast_data(sent_avg, vol, days=30)
            forecast_df = pd.DataFrame(forecast)
            
            forecast_chart = alt.Chart(forecast_df).mark_line(strokeWidth=2).encode(
                x=alt.X("day:Q", title="Days Ahead"),
                y=alt.Y("sentiment:Q", title="Projected Sentiment", scale=alt.Scale(domain=[-1, 1])),
                color=alt.value("#667eea"),
                tooltip=["day", "sentiment"]
            ).properties(height=200)
            
            st.altair_chart(forecast_chart, use_container_width=True)
        
        # Actions Deck
        st.markdown("### 🧰 Recommended Actions")
        for a in brief.get("actions", []):
            impact_score = a.get("impact_score", 0.7)
            impact_pct = int(impact_score * 100)
            
            with st.expander(f"{a.get('title','Action')} — Impact: {impact_pct}%", expanded=False):
                # Impact score bar
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-indicator" style="left:{impact_pct}%"></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Rationale:** {a.get('rationale','')}")
                
                if a.get("steps"):
                    st.markdown("**Steps:**")
                    for step in a["steps"]:
                        st.markdown(f"- {step}")
                
                st.markdown(f"**Sizing:** {a.get('sizing','')}")
                
                if a.get("kpis"):
                    st.markdown("**KPIs:**")
                    for k in a["kpis"]:
                        st.markdown(f"- {k}")
                
                st.markdown(f"**Timeline:** {a.get('timeline','')}")
                
                if a.get("risks"):
                    st.markdown("**⚠️ Key Risks:**")
                    for r in a["risks"]:
                        st.markdown(f"- {r}")
                
                if a.get("mitigations"):
                    st.markdown("**🛡️ Mitigations:**")
                    for m in a["mitigations"]:
                        st.markdown(f"- {m}")
        
        # IF/THEN Triggers
        if brief.get("watch_triggers"):
            st.markdown("### ⏱ IF/THEN Watch Triggers")
            for t in brief["watch_triggers"]:
                st.markdown(f'<div class="gradient-card">• {t}</div>', unsafe_allow_html=True)
        
        # Confidence
        conf = brief.get("confidence", "Medium")
        conf_map = {"High": 85, "Medium": 60, "Low": 35}
        conf_val = conf_map.get(conf, 60)
        
        st.markdown("### 📊 Confidence Assessment")
        st.markdown(f"""
        <div class="confidence-bar">
            <div class="confidence-indicator" style="left:{conf_val}%"></div>
        </div>
        <p style="text-align:center; font-weight:600; font-size:1.2rem;">{conf}</p>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Export buttons
        st.markdown("### 📥 Export Options")
        col1, col2, col3 = st.columns(3)
        
        title = f"Intelligence Brief — {CTX['query']}"
        
        with col1:
            st.download_button(
                "📄 Export Markdown",
                render_markdown(title, brief).encode("utf-8"),
                file_name=f"{CTX['query'].replace(' ','_')}_brief_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            )
        
        with col2:
            st.download_button(
                "🌐 Export HTML",
                render_html(title, brief).encode("utf-8"),
                file_name=f"{CTX['query'].replace(' ','_')}_brief_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
            )
        
        with col3:
            st.download_button(
                "🧾 Export Playbook",
                render_playbook(CTX["query"], brief, CTX["alerts"]).encode("utf-8"),
                file_name=f"{CTX['query'].replace(' ','_')}_playbook_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            )
    else:
        st.info("💡 Click **Generate Advanced Brief** to produce a decision-grade strategic plan.")

# ========== TAB 3: TRENDS & TIMELINE ==========
with tabs[2]:
    st.markdown("### 📈 Market & Sentiment Dynamics")
    
    if not CTX["flash_data"]:
        st.info("⏳ Waiting for flash data...")
    else:
        tr = build_trends(CTX["flash_data"])
        mom = momentum_report(CTX["flash_data"])
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Avg Sentiment", f"{tr['sentiment_avg']:+.3f}")
        col2.metric("⚡ Volatility Index", f"{tr.get('volatility', 0.0):.3f}")
        col3.metric("🎯 Top Entities", len(tr["top_entities"]))
        
        st.divider()
        
        # Dual-chart layout: Catalysts & Momentum
        st.markdown("#### 📊 Top Catalysts & Momentum")
        
        colA, colB = st.columns(2)
        
        with colA:
            st.markdown("**Top Catalysts**")
            if tr["top_catalysts"]:
                cat_df = pd.DataFrame(tr["top_catalysts"], columns=["Catalyst", "Count"])
                cat_chart = alt.Chart(cat_df).mark_bar().encode(
                    x=alt.X("Count:Q"),
                    y=alt.Y("Catalyst:N", sort="-x"),
                    color=alt.value("#FF9800"),
                    tooltip=["Catalyst", "Count"]
                ).properties(height=300)
                st.altair_chart(cat_chart, use_container_width=True)
            else:
                st.caption("No catalysts detected.")
        
        with colB:
            st.markdown("**Entity Momentum (Short vs Long)**")
            if mom["entity_momentum"]:
                mom_df = pd.DataFrame(mom["entity_momentum"], columns=["Entity", "Short", "Long", "Delta"])
                mom_chart = alt.Chart(mom_df).mark_bar().encode(
                    x=alt.X("Delta:Q", title="Momentum Δ"),
                    y=alt.Y("Entity:N", sort="-x"),
                    color=alt.condition(
                        alt.datum.Delta > 0,
                        alt.value("#4CAF50"),
                        alt.value("#ff4444")
                    ),
                    tooltip=["Entity", "Short", "Long", "Delta"]
                ).properties(height=300)
                st.altair_chart(mom_chart, use_container_width=True)
            else:
                st.caption("No momentum data.")
        
        st.divider()
        
        # Sentiment Evolution Chart
        st.markdown("#### 📈 Sentiment Evolution Over Time")
        evo_df = sentiment_evolution(CTX["flash_data"])
        
        if not evo_df.empty:
            # Take top 5 entities by frequency
            top_ents = evo_df["entity"].value_counts().head(5).index.tolist()
            evo_df_filtered = evo_df[evo_df["entity"].isin(top_ents)]
            
            evo_chart = alt.Chart(evo_df_filtered).mark_line(point=True).encode(
                x=alt.X("time_bucket:T", title="Time"),
                y=alt.Y("sentiment:Q", title="Sentiment", scale=alt.Scale(domain=[-1, 1])),
                color=alt.Color("entity:N", legend=alt.Legend(title="Entity")),
                tooltip=["time_bucket:T", "entity:N", "sentiment:Q"]
            ).properties(height=300)
            
            st.altair_chart(evo_chart, use_container_width=True)
        else:
            st.caption("Not enough time-series data yet.")
        
        st.divider()
        
        # Top Entities & Burst Activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏢 Top Entities**")
            if tr["top_entities"]:
                ent_df = pd.DataFrame(tr["top_entities"], columns=["Entity", "Count"])
                st.dataframe(ent_df, use_container_width=True, hide_index=True)
            else:
                st.caption("No entities detected.")
        
        with col2:
            st.markdown("**🔥 Burst Activity**")
            if mom["bursts"]:
                burst_df = pd.DataFrame(mom["bursts"], columns=["Name", "Mentions"])
                st.dataframe(burst_df.head(10), use_container_width=True, hide_index=True)
            else:
                st.caption("No burst activity.")

# ========== TAB 4: RESEARCH LAB ==========
with tabs[3]:
    st.markdown("### 🔬 Research Lab — Clustering & Network Analysis")
    
    if not CTX["flash_data"]:
        st.info("⏳ Waiting for flash data...")
    else:
        # Topic Clustering
        st.markdown("#### 🧬 Topic Clusters")
        clusters = cluster_topics(CTX["flash_data"], k=6)
        
        for c in clusters:
            with st.expander(f"Cluster #{c['cluster']} ({c['count']} items) — {', '.join(c['top_terms'][:5])}"):
                for it in c["items"][:8]:
                    st.markdown(f"- **{it['title']}** — *{it.get('source','')}* [🔗 Open]({it['link']})")
        
        st.divider()
        
        # Cluster visualization (scatter plot)
        st.markdown("#### 📊 Cluster Distribution")
        if clusters:
            cluster_viz_df = pd.DataFrame([
                {"cluster": c["cluster"], "count": c["count"], "label": ", ".join(c["top_terms"][:3])}
                for c in clusters
            ])
            
            cluster_chart = alt.Chart(cluster_viz_df).mark_circle(size=200).encode(
                x=alt.X("cluster:O", title="Cluster ID"),
                y=alt.Y("count:Q", title="Item Count"),
                size=alt.Size("count:Q", legend=None),
                color=alt.Color("cluster:N", legend=None),
                tooltip=["cluster", "count", "label"]
            ).properties(height=300)
            
            st.altair_chart(cluster_chart, use_container_width=True)
        
        st.divider()
        
        # Network Graph
        st.markdown("#### 🕸️ Entity-Catalyst Network Graph")
        if st.button("🔄 Generate Network Graph"):
            with st.spinner("Building network..."):
                graph_html = build_network_graph(CTX["flash_data"])
                components.html(graph_html, height=520, scrolling=False)
        
        st.divider()
        
        # Source Heatmap
        st.markdown("#### 📡 Source Distribution")
        heat = source_heatmap(CTX["flash_data"])
        if not heat.empty:
            heat_chart = alt.Chart(heat.head(15)).mark_bar().encode(
                x=alt.X("count:Q", title="Article Count"),
                y=alt.Y("source:N", sort="-x", title="Source"),
                color=alt.value("#2196F3"),
                tooltip=["source", "count"]
            ).properties(height=400)
            st.altair_chart(heat_chart, use_container_width=True)
        else:
            st.caption("No source data available.")
        
        st.divider()
        
        # Emerging Themes (Top 15% by sentiment impact)
        st.markdown("#### 🚀 Discover Emerging Themes")
        if st.button("🔍 Analyze Top 15% by Sentiment Impact"):
            sorted_items = sorted(CTX["flash_data"], key=lambda x: abs(x.get("sentiment", 0.0)), reverse=True)
            top_15pct = sorted_items[:max(1, len(sorted_items) // 7)]
            
            emerging = cluster_topics(top_15pct, k=4)
            st.success(f"✅ Found {len(emerging)} emerging theme clusters")
            
            for c in emerging:
                with st.expander(f"🔥 Theme #{c['cluster']} ({c['count']}) — {', '.join(c['top_terms'][:4])}"):
                    for it in c["items"][:6]:
                        st.markdown(f"- {it['title']} ({it.get('sentiment', 0):+.2f})")

# ========== TAB 5: ALERTS & WATCHLISTS ==========
with tabs[4]:
    st.markdown("### 🚨 Alerts & Watchlists")
    
    # Auto-pilot status
    if CTX.get("auto_pilot"):
        st.success("✅ Auto-pilot Mode: ACTIVE — Continuously monitoring for alerts")
    else:
        st.info("💤 Auto-pilot Mode: OFF")
    
    st.markdown("**Active Keywords:**")
    st.code(", ".join(CTX["keywords"]) if CTX["keywords"] else "None")
    
    st.divider()
    
    # Current Alerts
    st.markdown("#### 🔴 Current Alerts")
    if CTX["alerts"]:
        for a in CTX["alerts"]:
            urgency = a.get("urgency", "Low")
            urgency_class = f"urgency-{urgency.lower()}"
            
            st.markdown(f"""
            <div class="gradient-card">
                <span class="{urgency_class}">{urgency}</span>
                <strong>{a['title']}</strong><br/>
                <em>{a['source']}</em> | Sentiment: <code>{a['sentiment']:+.2f}</code><br/>
                Catalysts: {', '.join(a['catalysts'][:4])}<br/>
                <a href="{a['link']}" target="_blank">🔗 Open Article</a>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📥 Archive All Current Alerts"):
            save_alert_history(CTX["alerts"])
            st.success("✅ Alerts archived!")
    else:
        st.info("💤 No active alerts.")
    
    st.divider()
    
    # Smart Correlations
    st.markdown("#### 🔗 Smart Correlations — Co-occurring Catalysts")
    if CTX["flash_data"]:
        correlations = find_correlations(CTX["flash_data"], min_cooccurrence=2)
        
        if correlations:
            corr_df = pd.DataFrame(correlations, columns=["Catalyst 1", "Catalyst 2", "Co-occurrence"])
            st.dataframe(corr_df, use_container_width=True, hide_index=True)
            
            st.caption("💡 These catalyst pairs frequently appear together, indicating potential thematic connections.")
        else:
            st.caption("No strong correlations detected yet.")
    
    st.divider()
    
    # Alert History
    st.markdown("#### 📜 Alert History")
    hist = load_alert_history()
    
    if hist:
        hist_df = pd.DataFrame(hist)
        if "urgency" in hist_df.columns:
            hist_df = hist_df.sort_values("urgency", ascending=False)
        
        st.dataframe(hist_df[["title", "source", "sentiment", "urgency"]].head(20), use_container_width=True, hide_index=True)
    else:
        st.caption("No archived alerts yet.")

# ========== TAB 6: HISTORY & EXPORTS ==========
with tabs[5]:
    st.markdown("### 🧾 History & Exports")
    
    if not CTX["history"]:
        st.info("💡 No briefs generated yet. Generate an Intelligence Brief first.")
    else:
        st.markdown(f"**📊 Total Briefs in Session:** {len(CTX['history'])}")
        
        st.divider()
        
        # Show briefs with diff markers
        st.markdown("#### 📚 Previous Briefs")
        
        for i, h in enumerate(reversed(CTX["history"][-10:])):
            idx = len(CTX["history"]) - i - 1
            ts = datetime.fromisoformat(h["ts"]).strftime("%Y-%m-%d %H:%M:%S")
            
            with st.expander(f"Brief #{idx + 1}: {h['query']} — {ts}"):
                st.markdown(f"**Executive Summary:**")
                st.write(h["reasoning"].get("executive_summary", ""))
                
                st.markdown(f"**Confidence:** {h['reasoning'].get('confidence', 'N/A')}")
                
                # Diff marker: compare with previous
                if i < len(CTX["history"]) - 1:
                    prev = CTX["history"][idx - 1] if idx > 0 else None
                    if prev:
                        prev_actions = set(a.get("title", "") for a in prev["reasoning"].get("actions", []))
                        curr_actions = set(a.get("title", "") for a in h["reasoning"].get("actions", []))
                        
                        new_actions = curr_actions - prev_actions
                        removed_actions = prev_actions - curr_actions
                        
                        if new_actions:
                            st.success(f"🆕 New actions: {', '.join(new_actions)}")
                        if removed_actions:
                            st.warning(f"🗑️ Removed actions: {', '.join(removed_actions)}")
        
        st.divider()
        
        # Export Bundle
        st.markdown("#### 📦 Export Complete Bundle")
        st.caption("Generate a ZIP file containing Markdown, HTML, JSON, and metadata.")
        
        if st.button("🗜️ Generate Export Bundle"):
            with st.spinner("Building export bundle..."):
                # Create in-memory ZIP
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Add each brief
                    for i, h in enumerate(CTX["history"]):
                        query_safe = h["query"].replace(" ", "_")[:30]
                        
                        # Markdown
                        md_content = render_markdown(f"Brief: {h['query']}", h["reasoning"])
                        zf.writestr(f"brief_{i+1}_{query_safe}_{timestamp}.md", md_content)
                        
                        # HTML
                        html_content = render_html(f"Brief: {h['query']}", h["reasoning"])
                        zf.writestr(f"brief_{i+1}_{query_safe}_{timestamp}.html", html_content)
                        
                        # JSON
                        json_content = json.dumps(h, indent=2, default=str)
                        zf.writestr(f"brief_{i+1}_{query_safe}_{timestamp}.json", json_content)
                    
                    # Add session metadata
                    meta = {
                        "export_time": datetime.now().isoformat(),
                        "total_briefs": len(CTX["history"]),
                        "query": CTX["query"],
                        "keywords": CTX["keywords"],
                    }
                    zf.writestr("metadata.json", json.dumps(meta, indent=2))
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Export Bundle (ZIP)",
                    data=zip_buffer,
                    file_name=f"nexora_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )
        
        st.divider()
        
        # Session export
        st.markdown("#### 💾 Export Current Session (JSON)")
        
        def _safe_export() -> bytes:
            payload = {}
            for k, v in st.session_state.items():
                try:
                    json.dumps(v)
                    payload[k] = v
                except Exception:
                    payload[k] = str(v)
            return json.dumps(payload, indent=2, default=str).encode("utf-8")
        
        st.download_button(
            "📂 Export Session JSON",
            _safe_export(),
            file_name=f"nexora_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

# ========== FOOTER ==========
st.divider()
st.markdown("""
<div style="text-align:center; padding:20px; color:#888;">
    <strong>⚡ Nexora Intelligence Engine</strong> — Decision-Grade Edition<br/>
    Real-time intelligence powered by Google News RSS, AI reasoning, and advanced analytics.<br/>
    © 2024 Nexora | All data sourced from public feeds
</div>
""", unsafe_allow_html=True)
