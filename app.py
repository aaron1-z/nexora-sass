import asyncio, time, json, os
from typing import Dict, List
import pandas as pd
import altair as alt
import streamlit as st
from datetime import datetime

from engine import (
    ensure_dirs, fetch_live_news, ingest_query, MemoryStore,
    analyze_articles, strategic_reason,
    build_trends, momentum_report, cluster_topics, source_heatmap,
    render_markdown, render_html, render_playbook,
    generate_alerts, save_watchlist, load_watchlists,
    save_alert_history, load_alert_history,
)

# ---------- Setup ----------
st.set_page_config(page_title="Nexora Intelligence Workbench", layout="wide")
ensure_dirs()

# ---------- Global State ----------
if "context" not in st.session_state:
    st.session_state["context"] = {
        "query": "AI chips market",
        "keywords": ["NVIDIA", "ARM", "AMD", "export"],
        "flash_data": [],
        "analysis_data": None,
        "alerts": [],
        "history": [],
    }
CTX = st.session_state["context"]

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🎛️ Controls & Settings")
    CTX["query"] = st.text_input("Focus Topic", CTX["query"])
    n_items = st.slider("News to Fetch", 5, 50, 24)
    lookback = st.slider("Historical Lookback (days)", 7, 90, 30)
    refresh_sec = st.slider("Auto-refresh (seconds)", 5, 60, 12)
    auto_refresh = st.toggle("Enable Live Auto-refresh", True)
    st.divider()
    kw_text = st.text_area("Alert Keywords", ", ".join(CTX["keywords"]))
    CTX["keywords"] = [k.strip() for k in kw_text.split(",") if k.strip()]

    st.subheader("📋 Watchlists")
    name = st.text_input("Save current keywords as", "")
    if st.button("Save Watchlist") and name:
        save_watchlist(name, CTX["keywords"])
        st.toast("Saved ✅")
    lists = load_watchlists()
    if lists:
        opt = st.selectbox("Load watchlist", [w["name"] for w in lists])
        if st.button("Load Selected"):
            for w in lists:
                if w["name"] == opt:
                    CTX["keywords"] = w["keywords"]; st.toast("Loaded ✅")
    st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")

# ---------- Auto-refresh ----------
if auto_refresh and int(time.time()) % refresh_sec == 0:
    st.rerun()

# ---------- Tabs ----------
tabs = st.tabs([
    "🔴 Flash News",
    "🧠 Intelligence Brief",
    "📈 Trends & Timeline",
    "🔬 Research Lab",
    "🚨 Watchlists & Alerts",
    "🧾 History & Exports",
])

# ===== Flash News =====
with tabs[0]:
    st.subheader("Live Flash Intelligence Feed")
    flash = fetch_live_news(limit=n_items)
    CTX["flash_data"] = flash

    if not flash:
        st.info("Fetching headlines…")
    else:
        df = pd.DataFrame(flash)
        df["impact"] = df["sentiment"].abs()*2 + df["credibility"] + df["catalysts"].apply(lambda x: len(x or []))
        df.sort_values("impact", ascending=False, inplace=True)

        colA, colB, colC = st.columns(3)
        colA.metric("Items", len(df))
        colB.metric("Avg Sentiment", f"{df['sentiment'].mean():+.2f}")
        colC.metric("Avg Credibility", f"{df['credibility'].mean():.2f}")

        min_abs = st.slider("Filter: min |sentiment|", 0.0, 1.0, 0.15, 0.05)
        min_cred = st.slider("Filter: min credibility", 0.0, 1.0, 0.6, 0.05)
        filt = (df["sentiment"].abs() >= min_abs) & (df["credibility"] >= min_cred)
        st.dataframe(df.loc[filt, ["title","source","sentiment","credibility","catalysts","link"]],
                     use_container_width=True, height=400)

        alerts = generate_alerts(flash, CTX["keywords"])
        CTX["alerts"] = alerts
        if alerts:
            st.success(f"{len(alerts)} Smart Alerts")
            for a in alerts[:8]:
                st.markdown(
                    f"- **[{', '.join(a['catalysts']) or 'Signal'}]** "
                    f"{a['title']} — *{a['source']}* | `{a['sentiment']:+.2f}` "
                    f"[Open]({a['link']})"
                )
            if st.button("Archive alerts"):
                save_alert_history(alerts); st.toast("Archived ✅")
        else:
            st.caption("No priority alerts right now.")

# ===== Intelligence Brief =====
with tabs[1]:
    st.subheader("Strategic Intelligence Brief")
    explain = st.caption("A decision-grade plan with scenarios, actions, KPIs, timelines, risks & mitigations.")
    if st.button("🧩 Generate Advanced Brief", type="primary"):
        with st.status("Collecting & reasoning…", expanded=True) as s:
            s.write("Ingesting sources…")
            articles = asyncio.run(ingest_query(CTX["query"], max_items=n_items))
            s.write(f"Fetched {len(articles)} items")
            s.update(label="Summarizing & tagging…")
            analyzed = analyze_articles(articles)
            mem = MemoryStore(); mem.add_documents(analyzed)
            retrieved = mem.similarity_search(CTX["query"], k=6, lookback_days=lookback)
            s.update(label="Strategic planning…")
            brief = strategic_reason(CTX["query"], analyzed, retrieved)
            CTX["analysis_data"] = brief
            st.session_state["context"]["history"].append({"query": CTX["query"], "reasoning": brief, "ts": datetime.now().isoformat()})
            s.update(label="Complete", state="complete")

    brief = CTX.get("analysis_data") or {}
    if brief:
        st.markdown("### 🧭 Executive Summary")
        st.write(brief.get("executive_summary",""))
        st.markdown("### ⚡ Immediate Impact")
        st.write(brief.get("immediate_impact",""))

        # scenarios
        st.markdown("### 🌲 Scenario Tree (30 days)")
        for sc in brief.get("scenarios", []):
            with st.expander(f"{sc.get('name','Scenario')} — Prob {sc.get('prob','?')}%", expanded=(sc.get("name")=="Base")):
                for p in sc.get("path", []):
                    st.markdown(f"- {p}")
                if sc.get("signals"):
                    st.caption("Signals to watch:")
                    for sig in sc.get("signals", []):
                        st.markdown(f"- {sig}")

        # actions deck
        st.markdown("### 🧰 Recommended Actions")
        for a in brief.get("actions", []):
            with st.expander(f"{a.get('title','Action')}", expanded=False):
                st.write(f"**Rationale:** {a.get('rationale','')}")
                if a.get("steps"): 
                    st.write("**Steps:**"); 
                    for sstep in a["steps"]: st.markdown(f"- {sstep}")
                st.write(f"**Sizing:** {a.get('sizing','')}")
                if a.get("kpis"):
                    st.write("**KPIs:**"); 
                    for k in a["kpis"]: st.markdown(f"- {k}")
                st.write(f"**Timeline:** {a.get('timeline','')}")
                if a.get("risks"):
                    st.write("**Key Risks:**"); 
                    for r in a["risks"]: st.markdown(f"- {r}")
                if a.get("mitigations"):
                    st.write("**Mitigations:**"); 
                    for m in a["mitigations"]: st.markdown(f"- {m}")

        if brief.get("watch_triggers"):
            st.markdown("### ⏱ IF/THEN Triggers")
            for t in brief["watch_triggers"]:
                st.markdown(f"- {t}")

        st.metric("Confidence", brief.get("confidence","Medium"))

        # downloads
        title = f"Intelligence Brief — {CTX['query']}"
        st.download_button("📄 Export Markdown", render_markdown(title, brief).encode("utf-8"),
                           file_name=f"{CTX['query'].replace(' ','_')}_brief.md")
        st.download_button("🌐 Export HTML", render_html(title, brief).encode("utf-8"),
                           file_name=f"{CTX['query'].replace(' ','_')}_brief.html")
        st.download_button("🧾 Export Playbook", render_playbook(CTX["query"], brief, CTX["alerts"]).encode("utf-8"),
                           file_name=f"{CTX['query'].replace(' ','_')}_playbook.txt")
    else:
        st.info("Click **Generate Advanced Brief** to produce a decision-grade plan.")

# ===== Trends & Timeline =====
with tabs[2]:
    st.subheader("Market & Sentiment Dynamics")
    tr = build_trends(CTX["flash_data"])
    mom = momentum_report(CTX["flash_data"])
    st.caption(f"Avg Flash Sentiment: {tr['sentiment_avg']:+.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Top Entities"); st.table(pd.DataFrame(tr["top_entities"], columns=["Entity","Count"]))
    with col2:
        st.write("Top Catalysts"); st.table(pd.DataFrame(tr["top_catalysts"], columns=["Catalyst","Count"]))

    st.write("Momentum — Δ(short-long)")
    st.table(pd.DataFrame(mom["entity_momentum"], columns=["Entity","Short","Long","Δ"]))
    st.table(pd.DataFrame(mom["catalyst_momentum"], columns=["Catalyst","Short","Long","Δ"]))

    st.write("Burst Activity")
    st.table(pd.DataFrame(mom["bursts"], columns=["Name","Mentions"]))

# ===== Research Lab =====
with tabs[3]:
    st.subheader("Topic Clusters & Source Mix")
    clusters = cluster_topics(CTX["flash_data"], k=6)
    for c in clusters:
        with st.expander(f"Cluster #{c['cluster']} ({c['count']}) — {', '.join(c['top_terms'])}"):
            for it in c["items"]:
                st.markdown(f"- **{it['title']}** — *{it.get('source','')}*  [Open]({it['link']})")
    heat = source_heatmap(CTX["flash_data"])
    if not heat.empty:
        st.bar_chart(heat.set_index("source"), height=280, use_container_width=True)
    else:
        st.caption("No sources yet.")

# ===== Watchlists & Alerts =====
with tabs[4]:
    st.subheader("Active Alerts & History")
    st.write("Keywords:", CTX["keywords"])
    hist = load_alert_history()
    if hist:
        st.dataframe(pd.DataFrame(hist), use_container_width=True)
    else:
        st.caption("No archived alerts yet.")
    if st.button("💾 Archive current alerts"):
        save_alert_history(CTX["alerts"]); st.toast("Archived ✅")

# ===== History & Exports =====
with tabs[5]:
    st.subheader("Session History")
    if not CTX["history"]:
        st.caption("No briefs yet.")
    else:
        for h in reversed(CTX["history"][-10:]):
            with st.expander(h["query"]):
                st.write(h["reasoning"].get("executive_summary",""))
                st.caption(h["reasoning"].get("confidence",""))

    st.divider()
    # safe export of session (avoid SessionStateProxy)
    def _safe_export() -> bytes:
        payload = {}
        for k, v in st.session_state.items():
            try: json.dumps(v); payload[k] = v
            except Exception: payload[k] = str(v)
        return json.dumps(payload, indent=2).encode("utf-8")

    st.download_button("📂 Export Session JSON", _safe_export(), file_name="nexora_session.json")

    out_dir = os.path.join("exports", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(out_dir, exist_ok=True)
    if st.button("🧭 Save Briefs to Disk"):
        try:
            brief = CTX.get("analysis_data") or {}
            title = f"Action Brief — {CTX['query']}"
            with open(os.path.join(out_dir, "brief.md"), "w", encoding="utf-8") as f:
                f.write(render_markdown(title, brief))
            with open(os.path.join(out_dir, "brief.html"), "w", encoding="utf-8") as f:
                f.write(render_html(title, brief))
            with open(os.path.join(out_dir, "session.json"), "wb") as f:
                f.write(_safe_export())
            st.success(f"Saved to {out_dir}")
        except Exception as e:
            st.error(f"Save failed: {e}")

st.caption("© Nexora Intelligence Engine — Decision-Grade Edition")
