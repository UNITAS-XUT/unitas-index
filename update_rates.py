import json
import urllib.request
from datetime import datetime, timezone

fx_url = "https://" + "open." + "er-api.com" + "/v6/latest/USD"
pw_url = "https://" + "api.awattar.de" + "/v1/marketdata"
copper_url = "https://" + "://yahoo.com" + "/v8/finance/chart/HG=F" + "?" + "interval=1d&range=5d"
wheat_url = "https://" + "://yahoo.com" + "/v8/finance/chart/ZW=F" + "?" + "interval=1d&range=5d"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

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

def get_yahoo_price(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode("utf-8"))
    result_list = data.get("chart", {}).get("result", [])
    if result_list:
        meta = result_list.pop().get("meta", {})
        price = meta.get("regularMarketPrice") or meta.get("previousClose")
        if isinstance(price, (int, float)) and price > 0:
            return float(price)
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
    # HG=F ist in USD pro Pfund (1 kg = 2.20462 lbs)
    c_usd_lb = get_yahoo_price(copper_url)
    if c_usd_lb and c_usd_lb > 0:
        out["copper_usd_kg"] = round(c_usd_lb * 2.20462, 4)
        out["copper_live"] = True
except Exception as e:
    print("Copper error:", e)

try:
    # ZW=F ist in US-Cent pro Bushel (1 Bushel Weizen = 27.2155 kg)
    w_cents_bu = get_yahoo_price(wheat_url)
    if w_cents_bu and w_cents_bu > 0:
        out["wheat_usd_kg"] = round((w_cents_bu / 100.0) / 27.2155, 4)
        out["wheat_live"] = True
except Exception as e:
    print("Wheat error:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("RESULT:", out["fx_live"], out["power_live"], out["copper_live"], out["wheat_live"])
