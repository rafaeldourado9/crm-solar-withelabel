import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica
from io import BytesIO
import base64

class GraficoService:
    
    @staticmethod
    def gerar_grafico_geracao_anual(orcamento, premissa):
        """
        Gera gráfico de geração anual com perda de eficiência
        Retorna imagem em base64 para inserir no documento
        """
        anos = list(range(1, 26))  # 25 anos
        potencia_kwp = (orcamento.quantidade_paineis * orcamento.potencia_painel) / 1000
        
        # Calcular geração com perda de eficiência anual
        geracao_base = potencia_kwp * float(premissa.hsp_padrao) * 365 * (1 - float(premissa.perda_padrao))
        perda_anual = float(premissa.perda_eficiencia_anual) / 100
        
        geracoes = []
        for ano in anos:
            geracao_ano = geracao_base * ((1 - perda_anual) ** (ano - 1))
            geracoes.append(geracao_ano)
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(anos, geracoes, marker='o', linewidth=2, color='#FFA500')
        plt.fill_between(anos, geracoes, alpha=0.3, color='#FFA500')
        
        plt.title('Geração Estimada ao Longo de 25 Anos', fontsize=16, fontweight='bold')
        plt.xlabel('Ano', fontsize=12)
        plt.ylabel('Geração (kWh/ano)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Salvar em buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        # Converter para base64
        image_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{image_base64}"
    
    @staticmethod
    def gerar_grafico_economia_mensal(orcamento, premissa):
        """
        Gera gráfico comparando conta com e sem energia solar
        """
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        potencia_kwp = (orcamento.quantidade_paineis * orcamento.potencia_painel) / 1000
        geracao_mensal = potencia_kwp * float(premissa.hsp_padrao) * 30 * (1 - float(premissa.perda_padrao))
        
        # Simular variação sazonal (±15%)
        import random
        random.seed(42)
        geracoes = [geracao_mensal * (0.85 + random.random() * 0.3) for _ in meses]
        
        tarifa = float(premissa.tarifa_energia_atual)
        economia = [g * tarifa for g in geracoes]
        
        # Criar gráfico de barras
        plt.figure(figsize=(12, 6))
        plt.bar(meses, economia, color='#4CAF50', alpha=0.8)
        
        plt.title('Economia Mensal Estimada', fontsize=16, fontweight='bold')
        plt.xlabel('Mês', fontsize=12)
        plt.ylabel('Economia (R$)', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        # Adicionar valores nas barras
        for i, v in enumerate(economia):
            plt.text(i, v + 10, f'R$ {v:.0f}', ha='center', fontsize=9)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        image_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{image_base64}"
    
    @staticmethod
    def gerar_grafico_payback(orcamento, premissa):
        """
        Gera gráfico de payback (retorno do investimento)
        """
        anos = list(range(0, 26))
        investimento = float(orcamento.valor_final)
        
        potencia_kwp = (orcamento.quantidade_paineis * orcamento.potencia_painel) / 1000
        geracao_anual = potencia_kwp * float(premissa.hsp_padrao) * 365 * (1 - float(premissa.perda_padrao))
        tarifa = float(premissa.tarifa_energia_atual)
        inflacao = float(premissa.inflacao_energetica_anual) / 100
        
        economia_acumulada = [0]
        for ano in range(1, 26):
            tarifa_ano = tarifa * ((1 + inflacao) ** ano)
            economia_ano = geracao_anual * tarifa_ano
            economia_acumulada.append(economia_acumulada[-1] + economia_ano)
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(anos, [investimento] * len(anos), '--', color='red', label='Investimento', linewidth=2)
        plt.plot(anos, economia_acumulada, color='green', label='Economia Acumulada', linewidth=2)
        plt.fill_between(anos, economia_acumulada, alpha=0.3, color='green')
        
        # Encontrar ponto de payback
        for i, ec in enumerate(economia_acumulada):
            if ec >= investimento:
                plt.axvline(x=i, color='blue', linestyle=':', alpha=0.5)
                plt.text(i, investimento/2, f'Payback: {i} anos', rotation=90, va='center')
                break
        
        plt.title('Análise de Retorno do Investimento', fontsize=16, fontweight='bold')
        plt.xlabel('Ano', fontsize=12)
        plt.ylabel('Valor (R$)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        image_base64 = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{image_base64}"
