import aiohttp
import logging
from contants import Config

logger = logging.getLogger(__name__)

class DeviceManager:
    def __init__(self) -> None:
        self.config = Config()
        self.fan_status = {
            "on": False,
            "power_level": "0"
        }
        self.heater_status = {
            "on": False,
            "power_level": "0"
        }
        self.headers = {'BOND-Token': self.config.bond_token}
        self.base_url = f"http://{self.config.bond_ip}/v2/devices"

    async def _send_action(self, device_id: str, action: str, argument: dict | None = None):
        if not device_id:
            logger.warning(f"No device ID configured for action {action}")
            return

        url = f"{self.base_url}/{device_id}/actions/{action}"
        body = argument if argument else {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=self.headers, json=body) as response:
                    if response.status >= 400:
                        logger.error(f"Failed to send action {action} to {device_id}: {response.status}")
                        response_text = await response.text()
                        logger.error(f"Response: {response_text}")
        except Exception as e:
            logger.error(f"Error sending action to Bond Bridge: {e}")

    async def fan_switch(self):
        new_state = not self.fan_status["on"]
        action = "TurnOn" if new_state else "TurnOff"
        await self._send_action(self.config.fan_bond_id, action)
        self.fan_status["on"] = new_state
        if not new_state:
             self.fan_status["power_level"] = "0"
        return self.fan_status

    async def fan_up(self):
        current_speed = int(self.fan_status["power_level"])
        new_speed = current_speed + 1
        if new_speed > 3: # Assuming max speed 3
            new_speed = 3
        
        await self._send_action(self.config.fan_bond_id, "SetSpeed", {"argument": new_speed})
        self.fan_status["power_level"] = str(new_speed)
        self.fan_status["on"] = True
        return self.fan_status

    async def fan_down(self):
        current_speed = int(self.fan_status["power_level"])
        new_speed = current_speed - 1
        if new_speed < 1:
            new_speed = 1
        
        await self._send_action(self.config.fan_bond_id, "SetSpeed", {"argument": new_speed})
        self.fan_status["power_level"] = str(new_speed)
        self.fan_status["on"] = True
        return self.fan_status

    async def heater_switch(self):
        if not self.config.heater_bond_id:
            logger.warning("Heater Bond ID not configured")
            return {"error": "Heater not configured"}

        new_state = not self.heater_status["on"]
        action = "TurnOn" if new_state else "TurnOff"
        await self._send_action(self.config.heater_bond_id, action)
        self.heater_status["on"] = new_state
        return self.heater_status

    async def heater_up(self):
        if not self.config.heater_bond_id:
            return {"error": "Heater not configured"}
        # Placeholder for heater up
        logger.info("Heater up not fully implemented")
        return self.heater_status

    async def heater_down(self):
        if not self.config.heater_bond_id:
            return {"error": "Heater not configured"}
        # Placeholder for heater down
        logger.info("Heater down not fully implemented")
        return self.heater_status
