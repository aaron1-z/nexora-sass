import re, json
from datetime import datetime
from uuid import uuid4
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_text(t):
    return re.sub(r'\s+', ' ', t.strip())

def normalize_items(items):
    out=[]
    for it in items:
        text = clean_text(it.get("summary","")) or clean_text(it.get("title",""))
        out.append({
            "uid": str(uuid4()),
            "title": it["title"],
            "text": text,
            "timestamp": it.get("published"),
            "source": it.get("source"),
            "link": it.get("link")
        })
    return out

# store to json for persistence
def store(items, path="data/memory/news.jsonl"):
    with open(path,"a",encoding="utf8") as f:
        for i in items: f.write(json.dumps(i)+"\n")
