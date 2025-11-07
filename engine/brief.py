from typing import Dict, Any, List
from .utils import clean_text

def _li(xs: List[str]) -> str:
    return "\n".join([f"- {clean_text(x)}" for x in xs or []])

def render_markdown(title: str, brief: Dict[str, Any]) -> str:
    esc = lambda s: clean_text(s or "")
    lines = [
        f"# {esc(title)}",
        "",
        "## Executive Summary",
        esc(brief.get("executive_summary", "")),
        "",
        "## Immediate Impact",
        esc(brief.get("immediate_impact", "")),
        "",
        "## Scenario Tree (30d)",
    ]
    for sc in brief.get("scenarios", []):
        lines += [
            f"### {sc.get('name','Scenario')}  —  Prob: {sc.get('prob','?')}%",
            _li(sc.get("path", [])),
            "**Signals to watch:**",
            _li(sc.get("signals", [])),
            "",
        ]
    lines += ["## Recommended Actions"]
    for a in brief.get("actions", []):
        lines += [
            f"### {a.get('title','Action')}",
            f"**Rationale:** {esc(a.get('rationale',''))}",
            "**Steps:**", _li(a.get("steps", [])),
            f"**Sizing:** {esc(a.get('sizing',''))}",
            "**KPIs:**", _li(a.get("kpis", [])),
            f"**Timeline:** {esc(a.get('timeline',''))}",
            "**Key Risks:**", _li(a.get("risks", [])),
            "**Mitigations:**", _li(a.get("mitigations", [])),
            "",
        ]
    lines += [
        "## IF/THEN Watch Triggers",
        _li(brief.get("watch_triggers", [])),
        "",
        f"**Confidence:** {esc(brief.get('confidence','Medium'))}",
    ]
    return "\n".join(lines)

def render_html(title: str, brief: Dict[str, Any]) -> str:
    md = render_markdown(title, brief).replace("\n\n", "<br/>").replace("\n","<br/>")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{clean_text(title)}</title>
<style>
body{{font-family:Inter,Segoe UI,Arial,sans-serif;margin:2rem;line-height:1.55;background:#0e1117;color:#e6e6e6}}
h1,h2,h3{{color:#fff}} .card{{background:#0b0d13;border:1px solid #1b2233;border-radius:14px;padding:18px;margin:14px 0}}
hr{{border:0;border-top:1px solid #1b2233;margin:16px 0}}
</style></head><body><div class="card">{md}</div></body></html>"""

def render_playbook(query: str, brief: Dict[str, Any], alerts: List[Dict[str, Any]]) -> str:
    esc = lambda s: clean_text(s or "")
    out = [f"Playbook for: {esc(query)}", f"Summary: {esc(brief.get('executive_summary',''))}", ""]
    if alerts:
        out.append("Priority Alerts:")
        for a in alerts[:6]:
            out.append(f"- [{', '.join(a.get('catalysts', []))}] {a.get('title','')} ({a.get('source','')})")
    out += ["", "Actions:"]
    for a in brief.get("actions", []):
        out.append(f"- {a.get('title','')}: {esc(a.get('rationale',''))} | KPIs: {', '.join(a.get('kpis', []))}")
    return "\n".join(out)
