import json
import time
import urllib.request
from datetime import datetime, timezone

fx_url = "https://" + "open." + "er-api.com" + "/v6/latest/USD"
pw_url = "https://" + "api.awattar.de" + "/v1/marketdata"
yahoo_base = "https://" + "query1." + "finance." + "yahoo.com" + "/v8/finance/chart/"
yahoo_suffix = "?" + "interval=1d&range=5d"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Ticker-Definitionen: (id, yahoo_ticker, umrechnungsfaktor_auf_norm_einheit)
yahoo_items = [
    ("gas", "NG=F", 1.0),                 # USD / MMBtu
    ("oil", "BZ=F", 0.0062898),           # USD / Barrel -> USD / Liter (1 bbl = 158.987 L)
    ("diesel", "HO=F", 0.264172),         # USD / Gallone -> USD / Liter (1 gal = 3.78541 L)
    ("steel", "HRC=F", 0.00110231),       # USD / Short Ton -> USD / kg (1 st = 907.185 kg)
    ("copper", "HG=F", 2.20462),          # USD / lb -> USD / kg
    ("aluminum", "ALI=F", 0.001),         # USD / Metric Ton -> USD / kg
    ("iron", "TIO=F", 0.001),             # USD / Metric Ton -> USD / kg
    ("gold", "GC=F", 0.0321507),          # USD / Troy oz -> USD / g (1 oz = 31.1035 g)
    ("silver", "SI=F", 0.0321507),        # USD / Troy oz -> USD / g
    ("platinum", "PL=F", 0.0321507),      # USD / Troy oz -> USD / g
    ("palladium", "PA=F", 0.0321507),     # USD / Troy oz -> USD / g
    ("lumber", "LBR=F", 0.423776),        # USD / 1000 bd ft -> USD / m3 (1000 bf = 2.3597 m3)
    ("wheat", "ZW=F", 0.00036744),        # US-Cent / Bushel -> USD / kg (1 bu = 27.2155 kg)
    ("corn", "ZC=F", 0.00039368),         # US-Cent / Bushel -> USD / kg (1 bu = 25.4012 kg)
    ("soybeans", "ZS=F", 0.00036744),     # US-Cent / Bushel -> USD / kg (1 bu = 27.2155 kg)
    ("soyoil", "ZL=F", 0.0220462),        # US-Cent / lb -> USD / kg
    ("sugar", "SB=F", 0.0220462),         # US-Cent / lb -> USD / kg
    ("coffee", "KC=F", 0.0220462),        # US-Cent / lb -> USD / kg
    ("cocoa", "CC=F", 0.001),             # USD / Metric Ton -> USD / kg
    ("cotton", "CT=F", 0.0220462),        # US-Cent / lb -> USD / kg
    ("rice", "ZR=F", 0.00022046)          # USD / cwt (100 lbs = 45.3592 kg) -> USD / kg
]

out = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "live_commodities_count": 0,
    "rates": {},
    "power_eur_mwh": None,
    "commodities": {}
}

def get_yahoo_price(ticker):
    req = urllib.request.Request(yahoo_base + ticker + yahoo_suffix, headers=headers)
    with urllib.request.urlopen(req, timeout=12) as r:
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
        out["rates"] = fx["rates"]
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

for item_id, ticker, factor in yahoo_items:
    try:
        raw_p = get_yahoo_price(ticker)
        if raw_p and raw_p > 0:
            out["commodities"][item_id] = round(raw_p * factor, 4)
            out["live_commodities_count"] += 1
        time.sleep(0.25)
    except Exception as e:
        print(f"Ticker {ticker} error:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"RESULT: fx={out['fx_live']}, power={out['power_live']}, commodities={out['live_commodities_count']}/21")
