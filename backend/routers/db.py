from fastapi import APIRouter

router = APIRouter(
    prefix="/db",
    tags=["db"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def fetch_data():
    pass
