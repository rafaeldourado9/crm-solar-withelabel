"""Engine de templates DOCX e utilitários de formatação."""
import re
from decimal import Decimal

UNIDADES = [
    '', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove',
    'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis',
    'dezessete', 'dezoito', 'dezenove',
]
DEZENAS = [
    '', '', 'vinte', 'trinta', 'quarenta', 'cinquenta',
    'sessenta', 'setenta', 'oitenta', 'noventa',
]
CENTENAS = [
    '', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos',
    'seiscentos', 'setecentos', 'oitocentos', 'novecentos',
]


def _centenas_extenso(n: int) -> str:
    if n == 0:
        return ''
    if n == 100:
        return 'cem'
    c, resto = divmod(n, 100)
    partes: list[str] = []
    if c:
        partes.append(CENTENAS[c])
    if resto < 20:
        if resto:
            partes.append(UNIDADES[resto])
    else:
        d, u = divmod(resto, 10)
        partes.append(DEZENAS[d])
        if u:
            partes.append(UNIDADES[u])
    return ' e '.join(partes)


def numero_por_extenso(valor: Decimal) -> str:
    """Converte valor monetário (Decimal) para extenso em português."""
    reais = int(valor)
    centavos = round((valor - Decimal(reais)) * 100)

    if reais == 0 and centavos == 0:
        return 'zero reais'

    partes_reais: list[str] = []
    n = reais
    if n >= 1_000_000:
        m = n // 1_000_000
        partes_reais.append(f'{_centenas_extenso(m)} {"milhão" if m == 1 else "milhões"}')
        n %= 1_000_000
    if n >= 1_000:
        mil = n // 1_000
        partes_reais.append(f'{_centenas_extenso(mil)} mil')
        n %= 1_000
    if n > 0:
        partes_reais.append(_centenas_extenso(n))

    partes_final: list[str] = []
    if reais > 0:
        extenso = ' e '.join(partes_reais)
        partes_final.append(f'{extenso} {"real" if reais == 1 else "reais"}')
    if centavos > 0:
        extenso_c = _centenas_extenso(int(centavos))
        partes_final.append(f'{extenso_c} {"centavo" if centavos == 1 else "centavos"}')

    return ' e '.join(partes_final)


VAR_PATTERN = re.compile(r'\{\{(\w+)\}\}')


class TemplateEngine:
    """Substituição robusta de variáveis {{CHAVE}} em strings."""

    @staticmethod
    def extrair_variaveis(texto: str) -> set[str]:
        return set(VAR_PATTERN.findall(texto))

    @staticmethod
    def substituir_texto(texto: str, variaveis: dict[str, str]) -> str:
        def replacer(match: re.Match) -> str:  # type: ignore[type-arg]
            return variaveis.get(match.group(1), match.group(0))
        return VAR_PATTERN.sub(replacer, texto)

    @staticmethod
    def variaveis_faltando(texto: str, variaveis: dict[str, str]) -> list[str]:
        encontradas = TemplateEngine.extrair_variaveis(texto)
        return [v for v in encontradas if v not in variaveis]
