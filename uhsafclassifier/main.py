import asyncio
from os.path import join
from pathlib import Path
from typing import Optional

import typer
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from .api.main import api
from .api.v1.database import db
from .api.v1.models import PersonModel
from .api.v1.utils import export_excel, import_excel

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/api", api)


@app.get("/", include_in_schema=False)
def index(request: Request):
    return RedirectResponse(join(request.url.path, "api", ""))


typer_app = typer.Typer()


@typer_app.command(name="import")
def import_excel_command(
    filename: Optional[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
):
    result = import_excel(str(filename))
    asyncio.get_event_loop().run_until_complete(db.engine.save_all(result))
    typer.echo("Finish!!!")


@typer_app.command(name="export")
def export_excel_command(
    path: Optional[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    result = asyncio.get_event_loop().run_until_complete(db.engine.find(PersonModel))
    export_excel(path=str(path), data=result)
    typer.echo("Finish!!!")
