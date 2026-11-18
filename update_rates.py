import json
import urllib.request
from datetime import datetime, timezone

output = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "rates": {},
    "power_eur_mwh": None
}

try:
    req = urllib.request.Request("https://er-api.com", headers={"User-Agent": "UNITAS-Index-Engine/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and "rates" in data:
            excluded = ["RUB", "BYN", "IRR", "KPW", "SYP", "VES"]
            rates = {k: v for k, v in data["rates"].items() if k not in excluded}
            output["rates"] = rates
            output["fx_live"] = True
except Exception as e:
    print("FX fetch warning:", e)

try:
    req = urllib.request.Request("https://energy-charts.info", headers={"User-Agent": "UNITAS-Index-Engine/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and isinstance(data.get("price"), list):
            valid = [p for p in data["price"] if isinstance(p, (int, float))]
            if valid:
                output["power_eur_mwh"] = round(sum(valid) / len(valid), 2)
                output["power_live"] = True
except Exception as e:
    print("Power fetch warning:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("rates.json successfully updated:", output["updated_utc"])
