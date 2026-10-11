# Knapsack — Disaster intelligence & relief command

Open `index.html`. This is a browser-local hackathon prototype. Internet access is needed for map tiles, fonts, Google Maps links and live weather requests. No accounts or secret credentials are required for the demo.

## A five-minute judge walkthrough

1. **Overview:** show the liquid glass dashboard and the red/yellow/green planning zones. All disaster areas are fictional scenarios, not official warnings.
2. **Risk atlas:** select Guwahati or Kathmandu. The map uses real geographic coordinates; the region colors are sample classifications. Open Google Maps to inspect the coordinate. City coordinates do not define flood boundaries. Geolocation, if permitted, shows its reported accuracy.
3. **Early warning:** load a demo scenario for a dependable presentation. Alternatively, fetch an Open-Meteo model forecast. The result identifies its source, location and fetch time. Demonstrate the seven-day rainfall and gust timeline. Monitoring is every five minutes only while the page is open; browser notifications depend on permission and browser support. No official flood prediction is made.
4. **Central depot:** record a sample pledge and a stock receipt. Funding is a ledger, not a payment gateway. Inventory quantities are kg.
5. **Quantum optimizer:** choose bundles and capacity, run simulated annealing and compare its impact score with the exact enumeration benchmark. Export the allocation CSV. The objective is maximize impact subject to weight capacity. This is a classical heuristic with a quantum-inspired binary energy concept; no quantum hardware or speedup is claimed. Demo optimizer bundles are separate from inventory-controlled dispatch.
6. **Fleet & dispatch:** start with 100 trucks and 50 boats. Dispatch one truck with 500 kg of supplies. Availability and stock decrease. Try an overloaded request to show validation. Mark the mission delivered: vehicles return, while shipped inventory remains consumed. Routing, transit times and road safety are not modeled.
7. **Alert network:** compose a clear fictional warning, choose area, level and channel, preview it, then simulate delivery. The ledger states that zero external messages were sent. The WhatsApp button opens a draft that the user chooses whether to send; it does not broadcast. Do not send demo warnings to real recipients.
8. **Project workflow:** show the six-stage flow and download the JSON snapshot.

## Data & integration boundaries

- Browser-local storage preserves incident reports, stock, pledges, fleet and alert simulations when browser storage is available. This is not shared or authenticated multi-user storage. No real contact list is collected.
- OpenStreetMap provides the keyless geographic iframe fallback. Optional Google Maps Embed API configuration accepts a restricted browser key in session memory. Do not enter server credentials or messaging tokens into the browser.
- Weather: https://open-meteo.com/en/docs — optional actual model forecasts. Short-term weather does not measure long-term climate change. Planning thresholds shown in the website are illustrative, not official IMD criteria.
- Google Maps setup: https://developers.google.com/maps/documentation/embed/get-api-key — enable the API and restrict the browser key before production use.
- WhatsApp integration: https://www.twilio.com/docs/whatsapp/api — production messaging requires opted-in subscribers, a backend, service credentials and appropriate approved templates. Delivery status must come from provider receipts, not simulated counts.
- Operational early-warning monitoring requires a scheduled backend, official verified data, sensor/river levels, flood models and supervised escalation. A browser tab cannot monitor after it closes or deliver nationwide warnings to unregistered phones.
- A complete production release also needs database storage, identity, authorization, audit logs, reliable background jobs, payment integration if collecting money, and verified dispatch routing.

## Verification

JavaScript syntax checks passed. The existing annealing solver passed 100 capacity and weight-consistency trials. Visual browser QA was blocked because the browser policy disallows `file://` pages. Live map and forecast availability remain dependent on the presenting browser and network.
