from openai import OpenAI
import os, json

def classify_and_reason(texts:list[str], domain:str="commodities")->list[dict]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
    You are an expert market analyst.
    For each event below, extract:
    - category (Policy / Supply / Regulation / ESG / Demand / Financial)
    - short impact summary (≤3 sentences)
    - actionable next steps (≤3 items)
    Return JSON list.
    Events: {texts[:5]}
    """
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )
    try:
        data = json.loads(res.choices[0].message.content)
        return data
    except Exception:
        return [{"category":"General","impact":res.choices[0].message.content,"actions":[]}]
