from decimal import Decimal


def format_brl(value: Decimal) -> str:
    """Formata valor para moeda brasileira: R$ 1.234,56"""
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def numero_por_extenso(valor: Decimal) -> str:
    """Converte numero para texto em portugues."""
    unidades = [
        "", "um", "dois", "tres", "quatro", "cinco",
        "seis", "sete", "oito", "nove", "dez",
        "onze", "doze", "treze", "quatorze", "quinze",
        "dezesseis", "dezessete", "dezoito", "dezenove",
    ]
    dezenas = [
        "", "", "vinte", "trinta", "quarenta", "cinquenta",
        "sessenta", "setenta", "oitenta", "noventa",
    ]
    centenas = [
        "", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
        "seiscentos", "setecentos", "oitocentos", "novecentos",
    ]

    inteiro = int(valor)
    centavos = int(round((valor - inteiro) * 100))

    if inteiro == 0 and centavos == 0:
        return "zero reais"

    partes: list[str] = []

    if inteiro == 100:
        partes.append("cem")
    elif inteiro > 0:
        partes.extend(_decompor_inteiro(inteiro, unidades, dezenas, centenas))

    resultado = " e ".join(partes)

    if inteiro == 1:
        resultado += " real"
    elif inteiro > 1:
        resultado += " reais"

    if centavos > 0:
        centavos_texto = _numero_menor_1000(centavos, unidades, dezenas, centenas)
        if inteiro > 0:
            resultado += " e "
        resultado += centavos_texto
        resultado += " centavo" if centavos == 1 else " centavos"

    return resultado


def _decompor_inteiro(
    n: int,
    unidades: list[str],
    dezenas: list[str],
    centenas: list[str],
) -> list[str]:
    partes: list[str] = []
    if n >= 1000:
        milhares = n // 1000
        n = n % 1000
        if milhares == 1:
            partes.append("mil")
        else:
            partes.append(f"{_numero_menor_1000(milhares, unidades, dezenas, centenas)} mil")

    if n > 0:
        partes.append(_numero_menor_1000(n, unidades, dezenas, centenas))

    return partes


def _numero_menor_1000(
    n: int,
    unidades: list[str],
    dezenas: list[str],
    centenas: list[str],
) -> str:
    if n == 0:
        return ""
    if n == 100:
        return "cem"

    partes: list[str] = []
    if n >= 100:
        partes.append(centenas[n // 100])
        n = n % 100

    if n >= 20:
        partes.append(dezenas[n // 10])
        n = n % 10

    if 0 < n < 20:
        partes.append(unidades[n])

    return " e ".join(partes)
