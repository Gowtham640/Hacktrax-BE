from __future__ import annotations

import logging

from fastapi import FastAPI

from app.backend import config
from app.backend.api.routes.v1.teams import router as teams_router
from app.backend.utils.cors import install_cors

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Hacktrax Backend", version="0.1.0")
install_cors(app, config.FRONTEND_ORIGIN)
app.include_router(teams_router)

@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Hacktrax backend application starting up using %s", config.DATABASE_NAME)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Hacktrax backend is ready to receive responses."}


@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck")
def leapcell_health_check() -> dict[str, str]:
    return {"status": "ok"}
