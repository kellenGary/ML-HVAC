from fastapi import APIRouter

router = APIRouter(
    prefix="/action",
    tags=["action"],
    responses={404: {"description": "Not found"}}
)

@router.post("/fan_on")
async def fan_on():
    pass

@router.post("/fan_off")
async def fan_off():
    pass

@router.post("/fan_up")
async def fan_up():
    pass

@router.post("/fan_down")
async def fan_down():
    pass

@router.post("/heater_on")
async def heater_on():
    pass

@router.post("/heater_off")
async def heater_off():
    pass

@router.post("/heater_up")
async def heater_up():
    pass

@router.post("/heater_down")
async def heater_down():
    pass
