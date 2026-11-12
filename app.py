from flask import Flask, render_template_string
import requests
import time
import os
from datetime import datetime

app = Flask(__name__)

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?ts={}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="30">
<title>WinGo Results Archive</title>
<style>
:root{color-scheme:dark;--bg:#090b13;--panel:#121626;--line:#252d43;--muted:#9ba5bd;--text:#f4f6ff;--purple:#9b7bff;--green:#39d69a;--red:#ff718b}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% 0%,#211944 0,transparent 34%),var(--bg);color:var(--text);font:15px/1.5 system-ui, sans-serif}
main{max-width:1050px;margin:auto;padding:28px 16px 48px}.top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
h1{font-size:clamp(25px,5vw,38px);margin:0}.sub{color:var(--muted);margin:7px 0 22px}
.pill{border:1px solid var(--line);border-radius:99px;padding:7px 12px;color:var(--muted);font-size:12px}
.panel{background:linear-gradient(145deg,#171c2e,#101421);border:1px solid var(--line);border-radius:18px;padding:18px;margin:14px 0;box-shadow:0 12px 35px #0004}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.metric{background:#0c1020;border:1px solid var(--line);border-radius:14px;padding:14px}.metric small{color:var(--muted)}.metric strong{display:block;font-size:24px;margin-top:4px}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;min-width:440px}th,td{text-align:left;padding:12px 10px;border-bottom:1px solid var(--line)}th{font-size:12px;color:var(--muted);font-weight:600}
.tag{display:inline-block;padding:4px 10px;border-radius:99px;font-weight:700;font-size:12px}.big{background:#153c31;color:var(--green)}.small{background:#401d2a;color:var(--red)}
.note{color:var(--muted);font-size:13px}.error{color:#ffb3c0}.footer{margin-top:18px;color:var(--muted);font-size:12px}
@media(max-width:620px){.row{grid-template-columns:1fr 1fr}.metric:last-child{grid-column:1/-1}main{padding-top:20px}}
</style>
</head>
<body><main>
<div class="top"><div><h1>WinGo Results Archive</h1><div class="sub">A simple viewer for published draw history</div></div><span class="pill">AUTO-REFRESH · 30 SEC</span></div>
{% if error %}<section class="panel error">{{ error }}</section>{% endif %}
<section class="row">
 <div class="metric"><small>Records loaded</small><strong>{{ records|length }}</strong></div>
 <div class="metric"><small>Latest period</small><strong style="font-size:17px">{{ latest_period }}</strong></div>
 <div class="metric"><small>Last updated</small><strong style="font-size:17px">{{ updated }}</strong></div>
</section>
<section class="panel">
<h2 style="margin:0 0 12px;font-size:18px">Recent published results</h2>
<div class="table-wrap"><table><thead><tr><th>Period</th><th>Number</th><th>Size label</th></tr></thead><tbody>
{% for r in records %}
<tr><td>{{ r.period }}</td><td>{{ r.number }}</td><td><span class="tag {{ 'big' if r.size == 'BIG' else 'small' }}">{{ r.size }}</span></td></tr>
{% else %}<tr><td colspan="3">No results available right now.</td></tr>{% endfor %}
</tbody></table></div>
</section>
<section class="panel">
<h2 style="margin:0 0 8px;font-size:18px">Important note</h2>
<p class="note">This page only displays historical results returned by the source. Past outcomes do not establish what a future result will be. The BIG/SMALL labels are simple descriptions of the published number (5–9 = BIG; 0–4 = SMALL), not predictions or betting advice. Random draw outcomes cannot be reliably predicted from this history.</p>
</section>
<div class="footer">Data source: published WinGo history endpoint · This site is an independent viewer and is not affiliated with the source.</div>
</main></body></html>
"""

@app.route("/")
def home():
    records, error = [], None
    try:
        response = requests.get(API_URL.format(int(time.time() * 1000)),
                                headers=HEADERS, timeout=12)
        response.raise_for_status()
        payload = response.json()
        items = payload.get("data", {}).get("list", [])
        for item in items[:30]:
            try:
                number = int(item["number"])
                records.append({
                    "period": str(item.get("issueNumber", "—")),
                    "number": number,
                    "size": "BIG" if number >= 5 else "SMALL"
                })
            except (KeyError, TypeError, ValueError):
                continue
    except requests.RequestException:
        error = "Could not reach the results source. Please refresh in a little while."
    except (ValueError, AttributeError):
        error = "The results source returned data in an unexpected format."

    return render_template_string(
        PAGE,
        records=records,
        error=error,
        latest_period=records[0]["period"] if records else "—",
        updated=datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= int(os.environ.get("PORT", 5000)))
