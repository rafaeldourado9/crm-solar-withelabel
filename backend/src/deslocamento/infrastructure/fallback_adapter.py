TABELA_DISTANCIAS: dict[str, float] = {
    "dourados": 0,
    "itapora": 0,
    "ponta pora": 120,
    "naviraí": 110,
    "maracaju": 65,
    "rio brilhante": 65,
    "caarapo": 75,
    "fatima do sul": 25,
    "vicentina": 15,
    "deodapolis": 35,
    "gloria de dourados": 25,
    "jatei": 60,
    "nova alvorada do sul": 100,
    "campo grande": 220,
}


class FallbackDistanceAdapter:
    """Tabela de distancias estática como fallback quando Google Maps nao esta disponível."""

    async def get_distance_km(self, origem: str, destino: str) -> float:
        cidade = destino.split(",")[0].strip().lower()
        distancia = TABELA_DISTANCIAS.get(cidade)
        if distancia is not None:
            return distancia
        raise ValueError(f"Cidade '{destino}' nao encontrada na tabela de fallback")
