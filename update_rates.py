import json
import urllib.request
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "UNITAS-Index-Aggregator/1.0 (+https://github.com)",
    "Accept": "application/json"
}

output = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "rates": {},
    "power_eur_mwh": None
}

excluded = {"RUB", "BYN", "IRR", "KPW", "SYP", "VES"}

# 1. Weltwährungen über jsDelivr Open-Currency-CDN (GitHub-freundlich, 160+ Währungen)
try:
    url = "https://jsdelivr.net"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and "usd" in data:
            rates = {}
            for k, v in data["usd"].items():
                code = k.upper()
                if len(code) == 3 and code.isalpha() and code not in excluded and isinstance(v, (int, float)) and v > 0:
                    rates[code] = round(float(v), 6)
            if len(rates) > 50:
                output["rates"] = rates
                output["fx_live"] = True
except Exception as e:
    print("FX CDN warning:", e)

# 2. Stromgroßhandelspreis über offene EPEX-SPOT / aWATTar API (DE/AT)
try:
    req = urllib.request.Request("https://awattar.de", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and isinstance(data.get("data"), list) and len(data["data"]) > 0:
            prices = [item["marketprice"] for item in data["data"] if isinstance(item.get("marketprice"), (int, float))]
            if prices:
                output["power_eur_mwh"] = round(sum(prices) / len(prices), 2)
                output["power_live"] = True
except Exception as e:
    print("Power API warning:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Done: fx_live={output['fx_live']} ({len(output['rates'])} currencies), power_live={output['power_live']} ({output['power_eur_mwh']} EUR/MWh)")
