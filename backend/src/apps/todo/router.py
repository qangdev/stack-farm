from typing import List
from fastapi import (
    APIRouter,
    Request,
    Body,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import models as todo_model



router = APIRouter()


@router.post("/", response_description="Add new task")
async def create_task(request: Request, task: todo_model.NewTaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await request.app.mongodb["tasks"].insert_one(task)
    created_task = await request.app.mongodb["tasks"].find_one({"_id": new_task.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=create_task
    )


@router.get("/", response_description="List all tasks", response_model=List[todo_model.ViewTaskModel])
async def list_tasks(request: Request):
    return await request.app.mongodb["tasks"].find({})
    

@router.get("/{id}", response_description="Get a single task by its ID", response_model=todo_model.ViewTaskModel)
async def show_task(request: Request, id: str):
    if task:= await request.app.mongodb["tasks"].find_one({"_id": id}) is not None:
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.put("/{id}", response_description="Update a task",
response_model=todo_model.ViewTaskModel)
async def update_task(request: Request, id: str, task: todo_model.UpdateTaskModel = Body(...)):
    task = {k: v for k, v in task.dict().items() if v is not None}

    if len(task) >= 1:
        update_result = await request.app.mongodb["tasks"].update_one({"_id": id}, {"$set": task})
        if update_result.modified_count == 1:
            if updated_task := await request.app.mongodb["tasks"].find_one({"_id": id}) is not None:
                return update_task
    if existing_task := await request.app.mongodb["tasks"].find_one({"_id": id}) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete Task")
async def delete_task(request: Request, id: str):
    delete_result = await request.app.mongo["tasks"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found")
