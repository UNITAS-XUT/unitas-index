import json
import urllib.request
from datetime import datetime, timezone

fx_url = "https://" + "://er-api.com" + "/v6/latest/USD"
pw_url = "https://" + "api.awattar.de" + "/v1/marketdata"
headers = {"User-Agent": "Mozilla/5.0"}

out = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "rates": {},
    "power_eur_mwh": None
}
excluded = {"RUB", "BYN", "IRR", "KPW", "SYP", "VES"}

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

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("RESULT:", out["fx_live"], out["power_live"])
