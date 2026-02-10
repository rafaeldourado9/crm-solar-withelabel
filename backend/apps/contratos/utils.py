from decimal import Decimal

def numero_por_extenso(valor):
    """Converte número decimal para extenso em português"""
    
    unidades = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
    especiais = ['dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
    dezenas = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
    centenas = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
    
    def converter_grupo(n):
        if n == 0:
            return ''
        elif n < 10:
            return unidades[n]
        elif n < 20:
            return especiais[n - 10]
        elif n < 100:
            d, u = divmod(n, 10)
            return dezenas[d] + (' e ' + unidades[u] if u else '')
        else:
            c, resto = divmod(n, 100)
            if c == 1 and resto == 0:
                return 'cem'
            return centenas[c] + (' e ' + converter_grupo(resto) if resto else '')
    
    valor = Decimal(str(valor))
    reais = int(valor)
    centavos = int((valor - reais) * 100)
    
    if reais == 0:
        texto_reais = 'zero reais'
    else:
        # Milhões
        milhoes = reais // 1000000
        resto = reais % 1000000
        
        # Milhares
        milhares = resto // 1000
        resto = resto % 1000
        
        partes = []
        
        if milhoes:
            if milhoes == 1:
                partes.append('um milhão')
            else:
                partes.append(converter_grupo(milhoes) + ' milhões')
        
        if milhares:
            if milhares == 1:
                partes.append('mil')
            else:
                partes.append(converter_grupo(milhares) + ' mil')
        
        if resto:
            partes.append(converter_grupo(resto))
        
        texto_reais = ' e '.join(partes) + (' real' if reais == 1 else ' reais')
    
    if centavos:
        texto_centavos = converter_grupo(centavos) + (' centavo' if centavos == 1 else ' centavos')
        return f"{texto_reais} e {texto_centavos}"
    
    return texto_reais
