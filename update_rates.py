import json
import urllib.request
from datetime import datetime, timezone

fx_url = "https://" + "open." + "er-api.com" + "/v6/latest/USD"
pw_url = "https://" + "api.awattar.de" + "/v1/marketdata"
copper_url = "https://" + "fred.stlouisfed.org" + "/graph/fredgraph.csv?id=PCOPPUSDM&cosd=2025-01-01"
wheat_url = "https://" + "fred.stlouisfed.org" + "/graph/fredgraph.csv?id=PWHEAMTUSDM&cosd=2025-01-01"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

out = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "copper_live": False,
    "wheat_live": False,
    "rates": {},
    "power_eur_mwh": None,
    "copper_usd_kg": None,
    "wheat_usd_kg": None
}
excluded = {"RUB", "BYN", "IRR", "KPW", "SYP", "VES"}

def get_latest_fred_kg(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        lines = r.read().decode("utf-8").strip().splitlines()
    for line in reversed(lines):
        parts = line.split(",")
        if len(parts) == 2 and parts[1] not in (".", "", "VALUE"):
            try:
                usd_per_ton = float(parts[1])
                return round(usd_per_ton / 1000.0, 4)
            except ValueError:
                continue
    return None

try:
    req = urllib.request.Request(fx_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        fx = json.loads(r.read().decode("utf-8"))
    if isinstance(fx, dict) and "rates" in fx:
        out["rates"] = {k: v for k, v in fx["rates"].items() if k not in excluded}
        out["fx_live"] = len(out["rates"]) > 20
except Exception as e:
    print("FX error:", e)

try:
    req = urllib.request.Request(pw_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        pw = json.loads(r.read().decode("utf-8"))
    if isinstance(pw, dict) and isinstance(pw.get("data"), list) and pw["data"]:
        prices = [x["marketprice"] for x in pw["data"] if isinstance(x.get("marketprice"), (int, float))]
        if prices:
            out["power_eur_mwh"] = round(sum(prices) / len(prices), 2)
            out["power_live"] = True
except Exception as e:
    print("Power error:", e)

try:
    c_val = get_latest_fred_kg(copper_url)
    if c_val and c_val > 0:
        out["copper_usd_kg"] = c_val
        out["copper_live"] = True
except Exception as e:
    print("Copper error:", e)

try:
    w_val = get_latest_fred_kg(wheat_url)
    if w_val and w_val > 0:
        out["wheat_usd_kg"] = w_val
        out["wheat_live"] = True
except Exception as e:
    print("Wheat error:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("RESULT:", out["fx_live"], out["power_live"], out["copper_live"], out["wheat_live"])
