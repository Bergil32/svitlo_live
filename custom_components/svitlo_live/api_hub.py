from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import API_URL

_LOGGER = logging.getLogger(__name__)


class SvitloApiHub:
    """Єдиний хаб: 1 запит -> спільний JSON для всіх entry."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._session = async_get_clientsession(hass)
        self._lock = asyncio.Lock()
        self._data: Optional[dict[str, Any]] = None
        self._last_fetch_utc: Optional[datetime] = None

        # Антидубль / кеш
        self._debounce_sec = 15                      # мін інтервал між реальними фетчами
        self._cache_ttl = timedelta(seconds=900)     # 15 хв (як скан-інтервал)
        self._inflight: Optional[asyncio.Task] = None

        # Сигнал готовності кешу для координування паралельних entry
        self._ready_event = asyncio.Event()

    @property
    def json(self) -> Optional[dict[str, Any]]:
        return self._data

    def is_fresh(self) -> bool:
        return bool(self._last_fetch_utc and (dt_util.utcnow() - self._last_fetch_utc) < self._cache_ttl)

    async def warm_once(self) -> None:
        """Гарантовано прогріває кеш один раз; інші чекатимуть на готовність."""
        # Вже свіже — просто позначаємо готовність
        if self._data and self.is_fresh():
            self._ready_event.set()
            return

        async with self._lock:
            if self._data and self.is_fresh():
                self._ready_event.set()
                return

            # Якщо вже біжить фетч — чекаємо його завершення
            if self._inflight and not self._inflight.done():
                try:
                    await self._inflight
                finally:
                    self._ready_event.set()
                return

            # Запускаємо один спільний фетч
            self._inflight = self.hass.async_create_task(self._fetch())
            try:
                await self._inflight
            finally:
                self._inflight = None
                self._ready_event.set()

    async def wait_ready(self) -> None:
        """Чекає, доки warm_once зробить кеш готовим."""
        await self._ready_event.wait()

    async def ensure_data(self) -> dict[str, Any]:
        """
        Повертає JSON. Фетчить мережу лише якщо кеш прострочений і пройшов debounce.
        Всі одночасні виклики чекають одну in-flight задачу.
        """
        # Свіжий кеш — одразу
        if self._data and self.is_fresh():
            return self._data

        async with self._lock:
            now = dt_util.utcnow()

            if self._data and self.is_fresh():
                return self._data

            if (
                self._data
                and self._last_fetch_utc
                and (now - self._last_fetch_utc).total_seconds() < self._debounce_sec
            ):
                return self._data

            if self._inflight and not self._inflight.done():
                await self._inflight
                return self._data or {}

            self._inflight = self.hass.async_create_task(self._fetch())
            try:
                await self._inflight
            finally:
                self._inflight = None

            return self._data or {}

    async def _fetch(self) -> None:
        """Реальний мережевий фетч (один на всіх)."""
        _LOGGER.debug("API hub: fetching %s", API_URL)
        async with self._session.get(API_URL, timeout=20) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status} for {API_URL}")
            data = await resp.json()

        self._data = data
        self._last_fetch_utc = dt_util.utcnow()
