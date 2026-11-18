# UNITAS (XUT) – Universal Trade & Asset Standard

**Ein neutraler, realwirtschaftlicher Referenz- und Verrechnungsstandard für den globalen Handel**  
*A Neutral, Real-Economy Reference and Settlement Standard for Global Trade*

[![License: MIT](https://shields.io)](https://opensource.org)
[![Status: Proof of Concept](https://shields.io)](https://github.io)

---

## 🌐 Live-Prototyp / Live Demo
👉 **[Hier den interaktiven UNITAS (XUT) 3-Wege-Handelsrechner starten / Launch Live Calculator]([https://github.io](https://unitas-xut.github.io/unitas-index/)**

Der zweisprachige Open-Source-Prototyp (`index.html`, umschaltbar zwischen 🇩🇪 Deutsch und 🇬🇧 Englisch) demonstriert:
* **Bidirektionale 3-Wege-Umrechnung** zwischen über 150 Weltwährungen und dem realwirtschaftlichen Kaufkraft-Anker **UNITAS (XUT)**.
* **Live-Marktdaten-Anbindung** an offizielle EZB-Devisenkurse und europäische Stromgroßhandelsbörsen (*Fraunhofer Energy-Charts*).
* **Interaktive Index-Simulation** zum Testen von Produktivitätssprüngen sowie einen **B2B-Transaktionskostenvergleich**.

---

# 🇩🇪 Whitepaper: Das UNITAS-System (XUT)

## 1. Executive Summary
Die zunehmende Vernetzung der Weltwirtschaft und der rasante Anstieg grenzüberschreitender Lieferketten erfordern moderne, kosteneffiziente und widerstandsfähige Abwicklungsmechanismen. Bestehende internationale Zahlungsstrukturen führen insbesondere im Handel mit aufstrebenden Schwellen- und Wachstumsmärkten häufig zu hohen Transaktionskosten, doppelten Währungsumrechnungen, Wechselkursrisiken sowie zur Bindung erheblicher Kapitalmittel in Fremdwährungsreserven.

Das **UNITAS-System** (**U**niversal **T**rade & **A**sset **S**tandard, ISO-konformes Kürzel: **XUT**) bietet hierfür eine **ergänzende, rein marktwirtschaftliche Infrastruktur**, ohne bestehende nationale Währungen zu ersetzen oder in die freie Preisbildung einzugreifen. Es kombiniert **ein transparentes, realwirtschaftliches Kaufkraft-Referenzmaß (1 Unitas / 1 XUT)** mit **einer dezentralen, bilanzlosen Verrechnungsplattform**.

---

## 2. Das Kernprinzip: Strikte Trennung von Maßstab, Zahlung und Markt
* **Der Unitas (XUT) als objektives Referenzmaß:** Der Unitas ist kein physisches Zahlungsmittel, keine Reservewährung und keine Preisvorgabe. Er dient als neutraler Umrechnungsmaßstab (ein „Urmeter“ für Kaufkraft), vergleichbar mit dem bewährten Prinzip inflationsgeschützter Vertrags-Recheneinheiten (wie der chilenischen *Unidad de Fomento*), skaliert auf den globalen Handel.
* **Freie Preisbildung:** Jeder Marktteilnehmer setzt seine Preise völlig frei nach Angebot und Nachfrage.
* **Bilanzloser Zahlungsverkehr (Layer 1):** Die Kernplattform führt selbst **keinen Devisentausch** durch, hält keine eigenen Währungsreserven und erzeugt keine Arbitrage-Anreize. Der Käufer zahlt in seiner eigenen Währung, das System errechnet über das Unitas-Referenzmaß den exakten Kaufkraft-Gegenwert und routet genau diese Zahlungswährung direkt an den Verkäufer weiter.
* **Nahtloser Komfort durch Banken-Schnittstellen (Layer 2 – Auto-FX-API):** Geschäftsbanken und Zahlungsdienstleister können über eine offene Programmierschnittstelle (*Auto-FX-Plugin*) eingehende Fremdwährungen auf Wunsch des Empfängers automatisch und wettbewerbsintensiv zum fairen Marktpreis in dessen Heimatwährung wandeln.

---

## 3. Der Wertmaßstab: Produktionsgüter, Energie & Infrastruktur-Dienstleistungen
Um Manipulationen, Zirkelschlüsse über Wechselkurse und statistische Verzögerungen auszuschließen, ist **1 Unitas (1 XUT)** ausschließlich an **physisch und technisch genormte, weltweit gehandelte Vorleistungen, Energie und Infrastruktur-Kapazitäten** gekoppelt *(im Live-Prototyp durch 5 Leit-Indikatoren abgebildet; in der produktiven Index-Engine auf 30–50 standardisierte Güter skaliert)*:

* **Energie:** Die physikalische Kilowattstunde (**kWh**) Strom (volumengewichteter Durchschnitt freier Stromgroßhandelsbörsen) sowie veredelte Energieträger.
* **Industrie-, Bau- & Basismaterialien:** Warmgewalzter Stahl, Betonstahl, Zementklinker, Flachglas, raffiniertes Kupfer, Aluminium, Basis-Chemikalien (Ammoniak, Polyethylen) sowie standardisierte Halbleiter.
* **Agrar- & Grundnahrungsmittel:** Standardisierter Mahlweizen, Mais, Sojabohnen und Speiseöl.
* **Physische & Digitale Infrastruktur-Dienstleistungen:** Standardisierte Container-Seefrachtraten (TEU), Luftfracht-Kapazitäten (Tonnenkilometer), standardisierte Cloud-Rechenleistung (vCPU-Stunden) sowie Cloud-Datenspeicher (Terabyte-Monat).

### Dynamische Mechanik & Echtzeit-Berechnung
1. **Dynamische Produktivitätsanpassung:** Der Warenkorb entspricht immer exakt **1 Unitas**. Steigt durch technologischen Fortschritt das Angebot eines Gutes, passen entsprechend mehr Einheiten in den 1-Unitas-Korb – Produktivitätsgewinne werden sofort als steigende reale Kaufkraft sichtbar.
2. **Sekundengenaue Preisberechnung & Gleitende 365-Tage-Gewichtung:** Der Referenzkurs wird sekundengenau aus laufenden Börsen- und Marktpreisen über ein unabhängiges Daten-Konsortium berechnet. Die prozentuale Gewichtung im Korb passt sich täglich sanft auf Basis eines **gleitenden 365-Tage-Durchschnitts** der realen Welthandelsvolumina an.

---

## 4. Stabilitäts-, Finanzierungs- und Governance-Architektur
* **Systemische „Brandmauer“:** Da UNITAS bilanzlos arbeitet, bleiben regionale Banken- oder Immobilienkrisen auf das jeweilige Land begrenzt und lösen keine globale Kettenreaktion aus.
* **Kostendeckende Gebührenstaffel:** Eine degressive Protokollgebühr (von **0,05 %** in der Startphase bis **0,001 %** im skalierten Dauerbetrieb) finanziert autark den technischen Betrieb, Marktdatenlizenzen und unabhängige Sicherheitsaudits – ohne politische Subventionstöpfe.
* **Zweigleisige, neutrale Rechtsstruktur:** Hüterin des Open-Source-Protokolls und des XUT-Referenz-Index ist eine eigentümerlose, gemeinnützige Struktur (Start als e. V. / gUG, internationale Skalierung als **Schweizer Stiftung** mit Spiegelzentrum in **Singapur**).
* **Drei-Stufen-Einführung:** (1) Offenes B2B-Vertragswerkzeug (*Dual-Pricing*) → (2) Integration über Geschäftsbanken (*Auto-FX-Plugin*) & regionale Foren (**AU, ASEAN, BRICS, OPEC**) → (3) Direkte **ISO-20022-Kopplung** an Zentralbanken.

---
---

# 🇬🇧 Whitepaper: The UNITAS System (XUT)

## 1. Executive Summary
Growing global economic interdependence and expanding cross-border supply chains require modern, cost-efficient, and resilient settlement mechanisms. Existing international payment structures—particularly in trade with emerging and growth markets—often result in high transaction costs, double currency conversions, FX risks, and capital immobilized in foreign exchange reserves.

The **UNITAS System** (**U**niversal **T**rade & **A**sset **S**tandard, ISO-compliant code: **XUT**) provides a **complementary, purely market-based infrastructure** without replacing national currencies or interfering with free price formation. It combines **a transparent, real-economy purchasing power benchmark (1 Unitas / 1 XUT)** with **a decentralized, balance-sheet-free settlement platform**.

---

## 2. Core Principle: Strict Separation of Benchmark, Payment, and Market
* **The Unitas (XUT) as an Objective Reference Benchmark:** The Unitas is neither physical legal tender nor a reserve currency, but a neutral unit of account (a "standard meter" for purchasing power), comparable to Chile's inflation-indexed *Unidad de Fomento* scaled to global trade.
* **Balance-Sheet-Free Settlement (Layer 1):** The core platform conducts **no FX swaps** and holds no currency reserves. The buyer pays in their own currency, the system computes the exact purchasing power equivalent via the Unitas benchmark, and routes that payment currency directly to the seller.
* **Seamless Banking Integration (Layer 2 – Auto-FX API):** Commercial banks and payment providers can use an open API (*Auto-FX Plugin*) to automatically convert incoming foreign currencies into the recipient's domestic currency at competitive market rates upon request.

---

## 3. The Value Benchmark: Production Goods, Energy & Infrastructure Services
To eliminate manipulation and statistical delays, **1 Unitas (1 XUT)** is anchored exclusively to **physically and technically standardized, globally traded inputs, energy, and infrastructure capacities** *(represented by 5 lead indicators in the live prototype; scaled to 30–50 standardized goods in the production Index Engine)*:

* **Energy:** The physical kilowatt-hour (**kWh**) of electricity (volume-weighted average across open wholesale power exchanges) and refined energy carriers.
* **Industrial, Construction & Base Materials:** Hot-rolled steel, rebar, cement clinker, flat glass, refined copper, aluminum, base chemicals (ammonia, polyethylene), and standardized semiconductors.
* **Agricultural & Staple Goods:** Standardized milling wheat, corn, soybeans, and edible oils.
* **Physical & Digital Infrastructure Services:** Standardized container sea-freight rates (TEU), air-freight capacities (ton-kilometers), standardized cloud computing power (vCPU-hours), and cloud data storage (terabyte-month).

### Dynamic Mechanics & Real-Time Pricing
1. **Dynamic Productivity Adjustment:** One basket always equals **1 Unitas**. As technological progress expands supply, more units fit into the 1 Unitas basket—translating global productivity gains directly into rising real purchasing power.
2. **Second-by-Second Pricing & 365-Day Rolling Window:** Reference rates update every second from live market feeds via an independent market data consortium, while basket weights rebalance gently each day using a **rolling 365-day average** of global trade volumes.

---

## 4. Stability, Funding, and Governance Architecture
• **Systemic "Firewall":** Balance-sheet-free settlement isolates domestic banking or real estate crises within their country of origin, preventing global contagion.
• **Self-Sustaining Degressive Fee Tier:** A protocol fee scaling down from 0.05% at launch to 0.001% at global scale covers infrastructure, market data feeds, and security audits without creating politically contested capital pools.
• **Neutral Dual Legal Structure:** Stewardship rests with an ownerless non-profit entity (scaling into a Swiss Foundation with a mirror hub in Singapore), supporting organic three-stage adoption from private B2B dual pricing and commercial bank Auto-FX APIs up to ISO 20022 central bank connectivity.
