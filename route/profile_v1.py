from fastapi import APIRouter
from fastapi.responses import JSONResponse
from crud.profile import get_user_experience_details_db, get_user_profile_db

router = APIRouter()
@router.get("/{user_id}")
def get_user_profile(user_id: int):
    try:
        response = get_user_profile_db(user_id)
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@router.get("/experience/{experience_id}")
def get_user_experience_details(experience_id: int):
    try:
        response = get_user_experience_details_db(experience_id)
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)