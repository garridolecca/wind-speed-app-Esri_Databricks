# Wind Speed Analysis App

Interactive wind speed visualization built with the **ArcGIS Maps SDK for JavaScript 5.0**, deployed as a **Databricks App**.

## Features

- **Flow Renderer** — animated wind trails coloured by speed (blue → green → yellow)
- **Click-to-inspect** — click any point on the map to query the NLDAS ImageServer and retrieve U/V wind components
- **Speed gauge** — half-doughnut chart that fills and colour-shifts dynamically
- **Compass rose** — canvas-drawn compass showing the wind direction arrow
- **Speed scale bar** — gradient bar with a live position marker for the clicked speed
- **Regional distribution chart** — bar chart of typical wind speed ranges across CONUS

## Data Source

[NLDAS Hourly Wind Data](https://tiledimageservices.arcgis.com/V6ZHFr6zdgNZuVG0/arcgis/rest/services/NLDAS_Hourly_8_30_2021/ImageServer) — North American Land Data Assimilation System, hosted on ArcGIS Online.

## Stack

| Layer | Technology |
|---|---|
| Map & layers | ArcGIS Maps SDK for JavaScript 5.0 |
| Charts | Chart.js 4.4 |
| Backend | FastAPI + uvicorn (port 8000) |
| Hosting | Databricks Apps (Azure) |

## Live App

https://wind-speed-2437429139389964.4.azure.databricksapps.com

## Local Development

```bash
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000.

## Deployment (Databricks CLI)

```bash
# Upload source
databricks workspace import-dir . /Workspace/Users/<user>/apps/wind-speed --profile <profile>

# Deploy
databricks apps deploy wind-speed \
  --source-code-path /Workspace/Users/<user>/apps/wind-speed \
  --profile <profile>
```
