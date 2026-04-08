from typing import Protocol


class DistanceProvider(Protocol):
    async def get_distance_km(self, origem: str, destino: str) -> float: ...
