from os.path import join
from typing import List

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from .database import db
from .models import Options, PersonModel

api = FastAPI(title="UH SAF Classifier API")


@api.get("/", include_in_schema=False, tags=["General"])
def index(request: Request):
    return RedirectResponse(join(request.url.path, "docs"))


@api.get("/empty", tags=["General"], response_model=PersonModel)
async def get_empty():
    result = await db.engine.find_one(PersonModel, PersonModel.causes_tags == [])
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Empty model not found",
    )


@api.get("/options", tags=["General"], response_model=List[Options])
async def get_options():
    return list(Options)
