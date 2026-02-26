from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from databricks.sdk.core import Config
from databricks import sql
import os
import logging
import traceback
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
cfg = Config()

WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID")
HTTP_PATH = f"/sql/1.0/warehouses/{WAREHOUSE_ID}"
QUERY = (
    "SELECT station_id, name, state, latitude, longitude, "
    "elevation_m, wind_speed_ms, wind_direction_deg "
    "FROM hive_metastore.geoanalytics_placer.wind_stations "
    "ORDER BY station_id"
)


def fetch_stations(access_token: str | None):
    connect_args = dict(
        server_hostname=cfg.host,
        http_path=HTTP_PATH,
    )
    if access_token:
        connect_args["access_token"] = access_token
    else:
        connect_args["credentials_provider"] = lambda: cfg.authenticate

    with sql.connect(**connect_args) as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY)
            rows = cursor.fetchall()
            cols = [d[0] for d in cursor.description]
            return [dict(zip(cols, row)) for row in rows]


@app.get("/api/stations")
async def stations(request: Request):
    try:
        access_token = request.headers.get("x-forwarded-access-token")
        logger.info("Using %s auth", "user-token" if access_token else "service-principal")
        data = fetch_stations(access_token)
        return JSONResponse(content=data)
    except Exception as e:
        logger.error("Error in /api/stations:\n%s", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
