import json
import ssl
import urllib.request
from datetime import datetime, timezone

# SSL-Zertifikatsprüfung auf Runner-Umgebungen lockern
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "*/*"
}

output = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "rates": {},
    "power_eur_mwh": None
}

excluded = {"RUB", "BYN", "IRR", "KPW", "SYP", "VES"}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)

# 1. Weltwährungen über jsDelivr & GitHub-Raw-Mirror abrufen
fx_urls = [
    "https://jsdelivr.net",
    "https://pages.dev"
]

for url in fx_urls:
    try:
        data = fetch_json(url)
        if data and "usd" in data:
            rates = {}
            for k, v in data["usd"].items():
                code = k.upper()
                if len(code) == 3 and code.isalpha() and code not in excluded and isinstance(v, (int, float)) and v > 0:
                    rates[code] = round(float(v), 6)
            if len(rates) > 50:
                output["rates"] = rates
                output["fx_live"] = True
                print("FX success from:", url)
                break
    except Exception as e:
        print("FX error:", url, repr(e))

# 2. Stromgroßhandelspreis über aWATTar DE & AT abrufen
power_urls = [
    "https://awattar.de",
    "https://awattar.at"
]

for url in power_urls:
    try:
        data = fetch_json(url)
        if data and isinstance(data.get("data"), list) and len(data["data"]) > 0:
            prices = [item["marketprice"] for item in data["data"] if isinstance(item.get("marketprice"), (int, float))]
            if prices:
                output["power_eur_mwh"] = round(sum(prices) / len(prices), 2)
                output["power_live"] = True
                print("Power success from:", url)
                break
    except Exception as e:
        print("Power error:", url, repr(e))

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Final Result -> fx_live={output['fx_live']}, power_live={output['power_live']}")
