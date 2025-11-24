from fastapi import APIRouter
from device_manager import DeviceManager

dm = DeviceManager()

router = APIRouter(
    prefix="/action",
    tags=["action"],
    responses={404: {"description": "Not found"}}
)

@router.post("/fan_switch")
async def fan_switch():
    response = await dm.fan_switch()
    if (response == "error"):
        return False
    return response

@router.post("/fan_up")
async def fan_up():
    response = await dm.fan_up()
    if (response == "error"):
        return False
    return response

@router.post("/fan_down")
async def fan_down():
    response = await dm.fan_down()
    if (response == "error"):
        return False
    return response

@router.post("/heater_switch")
async def heater_on():
    response = await dm.heater_switch()
    if (response == "error"):
        return False
    return response

@router.post("/heater_up")
async def heater_up():
    response = await dm.heater_up()
    if (response == "error"):
        return False
    return response

@router.post("/heater_down")
async def heater_down():
    response = await dm.heater_down()
    if (response == "error"):
        return False
    return response
