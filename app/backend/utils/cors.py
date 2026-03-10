from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def install_cors(app: FastAPI, allowed_origin: str | None) -> None:
    """
    Attach the FastAPI CORSMiddleware so the frontend can POST and GET safely.
    """

    origins = ["*"] if not allowed_origin or allowed_origin.strip() == "" else [allowed_origin]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
