from os.path import join
from random import randint
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.param_functions import Body
from fastapi.responses import RedirectResponse
from odmantic import ObjectId

from .database import db
from .models import Options, PersonModel

api = FastAPI(title="UH SAF Classifier API")


@api.get("/", include_in_schema=False, tags=["General"])
def index(request: Request):
    return RedirectResponse(join(request.url.path, "docs"))


@api.get("/empty", tags=["General"], response_model=PersonModel)
async def get_empty():
    result = await db.engine.find(PersonModel, PersonModel.causes_tags == [])
    if result:
        length = len(result)
        index = randint(0, length)
        return result[index]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Empty model was not found",
    )


@api.get("/tags", tags=["General"], response_model=List[Options])
async def get_tags():
    return list(Options)


@api.put("/classify/{id}", tags=["General"], response_model=PersonModel)
async def put_classify(
    id: ObjectId,
    tags: List[Options] = Body([]),
    others: Optional[str] = Body(None),
):
    result = await db.engine.find_one(PersonModel, PersonModel.id == id)
    if result:
        result.causes_tags = tags
        result.causes_others = others
        await db.engine.save(result)
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with id {id} was not found",
    )


@api.get("/persons", tags=["General"], response_model=List[PersonModel])
async def get_persons():
    return await db.engine.find(PersonModel)


@api.get("/persons/{id}", tags=["General"], response_model=PersonModel)
async def get_person(id: ObjectId):
    result = await db.engine.find_one(PersonModel, PersonModel.id == id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with id {id} was not found",
    )


@api.post("/persons", tags=["General"], response_model=PersonModel)
async def post_person(model: PersonModel):
    await db.engine.save(model)
    return model


@api.put("/persons/{id}", tags=["General"], response_model=PersonModel)
async def put_person(id: ObjectId, model: PersonModel):
    result = await db.engine.find_one(PersonModel, PersonModel.id == id)
    if result:
        update_data = model.dict(exclude_unset=True)
        updated_item = result.copy(update=update_data)
        await db.engine.save(updated_item)
        return updated_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with id {id} was not found",
    )


@api.delete("/persons", tags=["General"], response_model=PersonModel)
async def delete_person(id: ObjectId):
    result = await db.engine.find_one(PersonModel, PersonModel.id == id)
    if result:
        await db.engine.delete(result)
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with id {id} was not found",
    )
