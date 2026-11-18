import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json, text/xml, */*"
}

output = {
    "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "fx_live": False,
    "power_live": False,
    "rates": {},
    "power_eur_mwh": None
}

excluded = {"RUB", "BYN", "IRR", "KPW", "SYP", "VES"}

# 1. Versuch: Frankfurter API (Offizielle EZB-Kurse)
try:
    req = urllib.request.Request("https://frankfurter.app", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and "rates" in data:
            rates = {"USD": 1.0}
            for k, v in data["rates"].items():
                if k not in excluded:
                    rates[k] = v
            output["rates"] = rates
            output["fx_live"] = True
except Exception as e:
    print("Frankfurter API warning:", e)

# 1b. Backup-Versuch: Direkter XML-Feed der Europäischen Zentralbank (EZB)
if not output["fx_live"]:
    try:
        req = urllib.request.Request("https://europa.eu", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            eur_rates = {"EUR": 1.0}
            for cube in root.findall(".//{http://ecb.int}Cube[@currency]"):
                curr = cube.attrib["currency"]
                rate = float(cube.attrib["rate"])
                if curr not in excluded:
                    eur_rates[curr] = rate
            if "USD" in eur_rates:
                usd_per_eur = eur_rates["USD"]
                output["rates"] = {k: round(v / usd_per_eur, 6) for k, v in eur_rates.items()}
                output["fx_live"] = True
    except Exception as e:
        print("ECB XML fallback warning:", e)

# 2. Stromgroßhandelspreis (Fraunhofer Energy-Charts API)
try:
    req = urllib.request.Request("https://energy-charts.info", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if data and isinstance(data.get("price"), list):
            valid = [p for p in data["price"] if isinstance(p, (int, float))]
            if valid:
                output["power_eur_mwh"] = round(sum(valid) / len(valid), 2)
                output["power_live"] = True
except Exception as e:
    print("Energy-Charts warning:", e)

with open("rates.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("Done:", output["fx_live"], output["power_live"])
