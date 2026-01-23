from openai import OpenAI
from anthropic import Anthropic
from decouple import config
from decimal import Decimal
import json

class IAService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=config('OPENAI_API_KEY', default=''))
        self.anthropic_client = Anthropic(api_key=config('ANTHROPIC_API_KEY', default=''))
    
    def analisar_consumo(self, historico_consumo):
        """Analisa padrão de consumo e sugere melhor dimensionamento"""
        prompt = f"""Analise o histórico de consumo: {historico_consumo} kWh.
        Retorne JSON com: consumo_medio, pico_consumo, sazonalidade, recomendacao_kwp"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def otimizar_proposta(self, dados_orcamento):
        """Otimiza valores da proposta baseado em histórico"""
        prompt = f"""Dados: {dados_orcamento}. 
        Sugira otimizações de custo mantendo qualidade. Retorne JSON."""
        
        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.content[0].text)
    
    def gerar_descricao_tecnica(self, equipamentos):
        """Gera descrição técnica profissional"""
        prompt = f"Gere descrição técnica profissional para: {equipamentos}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def prever_economia(self, consumo, tarifa, anos=25):
        """Prevê economia ao longo dos anos com IA"""
        prompt = f"""Consumo: {consumo}kWh, Tarifa: R${tarifa}, Anos: {anos}.
        Considere inflação energética 8%/ano. Retorne JSON com previsao_anual."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def chatbot_atendimento(self, mensagem, contexto_cliente=None):
        """Chatbot para atendimento ao cliente"""
        system = """Você é assistente de vendas de energia solar. 
        Seja técnico, objetivo e persuasivo."""
        
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": mensagem}
        ]
        
        if contexto_cliente:
            messages.insert(1, {"role": "system", "content": f"Cliente: {contexto_cliente}"})
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    
    def analisar_viabilidade(self, dados_cliente):
        """Analisa viabilidade técnica e financeira"""
        prompt = f"""Analise viabilidade: {dados_cliente}.
        Retorne JSON: viavel (bool), score (0-100), motivos[], recomendacoes[]"""
        
        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.content[0].text)
    
    def gerar_email_followup(self, cliente_nome, status, dias_sem_resposta):
        """Gera email de follow-up personalizado"""
        prompt = f"""Gere email follow-up para {cliente_nome}.
        Status: {status}, Dias sem resposta: {dias_sem_resposta}.
        Tom: profissional e amigável."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def extrair_dados_conta_luz(self, imagem_base64):
        """Extrai dados da conta de luz via OCR + IA"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extraia: consumo_kwh, valor_total, concessionaria. Retorne JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem_base64}"}}
                ]
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
