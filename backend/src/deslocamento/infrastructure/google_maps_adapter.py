import httpx

from src.config import settings


class GoogleMapsDistanceAdapter:
    """Adapter async para Google Maps Distance Matrix API."""

    BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

    async def get_distance_km(self, origem: str, destino: str) -> float:
        params = {
            "origins": origem,
            "destinations": destino,
            "key": settings.google_maps_api_key,
            "units": "metric",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        rows = data.get("rows", [])
        if not rows or not rows[0].get("elements"):
            raise ValueError("Google Maps nao retornou resultados")

        element = rows[0]["elements"][0]
        if element.get("status") != "OK":
            raise ValueError(f"Google Maps erro: {element.get('status')}")

        distance_meters = element["distance"]["value"]
        return distance_meters / 1000.0
