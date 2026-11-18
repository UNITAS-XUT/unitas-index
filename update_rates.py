import json
import urllib.request
from datetime import datetime, timezone

fx_url = "https://" + "open." + "er-api.com" + "/v6/latest/USD"
pw_url = "https://" + "api.awattar.de" + "/v1/marketdata"
copper_url = "https://" + "stooq.com" + "/q/d/l/" + "?" + "s=hg.f&i=d"
wheat_url = "https://" + "stooq.com" + "/q/d/l/" + "?" + "s=zw.f&i=d"
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

def get_stooq_close(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        lines = r.read().decode("utf-8").strip().splitlines()
    if len(lines) >= 2:
        cols = lines.pop().split(",")
        close_str = cols.pop().strip()
        if close_str not in ("N/D", "", "Close"):
            return float(close_str)
    return None

try:
    req = urllib.request.Request(fx_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        fx = json.loads(r.read().decode("utf-8"))
    if isinstance(fx, dict) and "rates" in fx:
        out["rates"] = {k: v for k, v in fx["rates"].items() if k not in excluded}
        out["fx_live"] = len(out["rates"]) > 20
except Exception as e:
    print("FX error:", e)

try:
    req = urllib.request.Request(pw_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        pw = json.loads(r.read().decode("utf-8"))
    if isinstance(pw, dict) and isinstance(pw.get("data"), list) and pw["data"]:
        prices = [x["marketprice"] for x in pw["data"] if isinstance(x.get("marketprice"), (int, float))]
        if prices:
            out["power_eur_mwh"] = round(sum(prices) / len(prices), 2)
            out["power_live"] = True
except Exception as e:
    print("Power error:", e)

try:
    # HG.F ist in US-Cent pro Pfund (1 kg = 2.20462 lbs)
    c_cents_lb = get_stooq_close(copper_url)
    if c_cents_lb and c_cents_lb > 0:
        out["copper_usd_kg"] = round((c_cents_lb / 100.0) * 2.20462, 4)
        out["copper_live"] = True
except Exception as e:
    print("Copper error:", e)

try:
    # ZW.F ist in US-Cent pro Bushel (1 Bushel Weizen = 27.2155 kg)
    w_cents_bu = get_stooq_close(wheat_url)
    if w_cents_bu and w_cents_bu > 0:
        out["wheat_usd_kg"] = round((w_cents_bu / 100.0) / 27.2155, 4)
        out["wheat_live"] = True
except Exception as e:
    print("Wheat error:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("RESULT:", out["fx_live"], out["power_live"], out["copper_live"], out["wheat_live"])
