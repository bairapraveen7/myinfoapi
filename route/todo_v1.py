# Help me create the routes for todo which contains create and view todo, getAll todos

from crud.ticket import create_todo_db, get_all_todos_db, view_todo_db
from fastapi import APIRouter
from schema import todo
from schema.todo import  TodoCreateSchema
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/create")
def create_todo(todo: TodoCreateSchema):
    try:
        create_todo_db(todo.title, todo.description)
        return JSONResponse(content={"message": "Todo created successfully"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.get("/{id}")
def view_todo(id: int):
    try:

        todo = view_todo_db(id)
        if not todo:
            return JSONResponse(content={"error": "Todo not found"}, status_code=404)
        return JSONResponse(content=todo, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.get("/")
def get_all_todos():
    try:
        todos = get_all_todos_db()
        return JSONResponse(content=todos,status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)