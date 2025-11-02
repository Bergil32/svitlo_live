from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_CITY, CONF_STREET, CONF_HOUSE, CONF_SCAN_INTERVAL

class SvitloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            # МІНІМАЛЬНО: без мережевої валідації, просто створюємо запис
            await self.async_set_unique_id(
                f"{user_input[CONF_CITY]}|{user_input[CONF_STREET]}|{user_input[CONF_HOUSE]}"
            )
            self._abort_if_unique_id_configured()
            data = {
                CONF_CITY: user_input[CONF_CITY],
                CONF_STREET: user_input[CONF_STREET],
                CONF_HOUSE: user_input[CONF_HOUSE],
                CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, 180),
            }
            return self.async_create_entry(
                title=f"{data[CONF_CITY]}, {data[CONF_STREET]} {data[CONF_HOUSE]}",
                data=data,
            )

        schema = vol.Schema({
            vol.Required(CONF_CITY): str,
            vol.Required(CONF_STREET): str,
            vol.Required(CONF_HOUSE): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=180): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
