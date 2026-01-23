from django.urls import path
from apps.ia_views import (
    AnalisarConsumoView,
    OtimizarPropostaView,
    ChatbotView,
    AnalisarViabilidadeView,
    GerarEmailFollowupView,
    ExtrairContaLuzView,
    PreverEconomiaView
)

urlpatterns = [
    path('analisar-consumo/', AnalisarConsumoView.as_view()),
    path('otimizar-proposta/<int:orcamento_id>/', OtimizarPropostaView.as_view()),
    path('chatbot/', ChatbotView.as_view()),
    path('analisar-viabilidade/', AnalisarViabilidadeView.as_view()),
    path('email-followup/<int:cliente_id>/', GerarEmailFollowupView.as_view()),
    path('extrair-conta-luz/', ExtrairContaLuzView.as_view()),
    path('prever-economia/', PreverEconomiaView.as_view()),
]
