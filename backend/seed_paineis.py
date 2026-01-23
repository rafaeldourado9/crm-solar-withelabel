import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.equipamentos.models import Painel

paineis = [
    # Canadian Solar - 15 modelos
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3W-400P', 'potencia_w': 400},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3W-405P', 'potencia_w': 405},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3W-410P', 'potencia_w': 410},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3W-415P', 'potencia_w': 415},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3W-420P', 'potencia_w': 420},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3U-350P', 'potencia_w': 350},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3U-355P', 'potencia_w': 355},
    {'fabricante': 'Canadian Solar', 'modelo': 'CS3U-360P', 'potencia_w': 360},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu6-450W', 'potencia_w': 450},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu6-455W', 'potencia_w': 455},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu6-460W', 'potencia_w': 460},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu7-530W', 'potencia_w': 530},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu7-535W', 'potencia_w': 535},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu7-540W', 'potencia_w': 540},
    {'fabricante': 'Canadian Solar', 'modelo': 'HiKu7-545W', 'potencia_w': 545},
    
    # DAH Solar - 15 modelos
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-54X10/FS-400W', 'potencia_w': 400},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-54X10/FS-405W', 'potencia_w': 405},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-54X10/FS-410W', 'potencia_w': 410},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-54X10/FS-415W', 'potencia_w': 415},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-60X10/FS-450W', 'potencia_w': 450},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-60X10/FS-455W', 'potencia_w': 455},
    {'fabricante': 'DAH Solar', 'modelo': 'DHM-60X10/FS-460W', 'potencia_w': 460},
    {'fabricante': 'DAH Solar', 'modelo': 'DHN-54X16/DG-450W', 'potencia_w': 450},
    {'fabricante': 'DAH Solar', 'modelo': 'DHN-54X16/DG-455W', 'potencia_w': 455},
    {'fabricante': 'DAH Solar', 'modelo': 'DHN-54X16/DG-460W', 'potencia_w': 460},
    {'fabricante': 'DAH Solar', 'modelo': 'DHT-60X10/FS-530W', 'potencia_w': 530},
    {'fabricante': 'DAH Solar', 'modelo': 'DHT-60X10/FS-535W', 'potencia_w': 535},
    {'fabricante': 'DAH Solar', 'modelo': 'DHT-60X10/FS-540W', 'potencia_w': 540},
    {'fabricante': 'DAH Solar', 'modelo': 'DHT-60X10/FS-545W', 'potencia_w': 545},
    {'fabricante': 'DAH Solar', 'modelo': 'DHT-60X10/FS-550W', 'potencia_w': 550},
    
    # JA Solar - 15 modelos
    {'fabricante': 'JA Solar', 'modelo': 'JAM54S30-400/MR', 'potencia_w': 400},
    {'fabricante': 'JA Solar', 'modelo': 'JAM54S30-405/MR', 'potencia_w': 405},
    {'fabricante': 'JA Solar', 'modelo': 'JAM54S30-410/MR', 'potencia_w': 410},
    {'fabricante': 'JA Solar', 'modelo': 'JAM54S30-415/MR', 'potencia_w': 415},
    {'fabricante': 'JA Solar', 'modelo': 'JAM60S20-450/MR', 'potencia_w': 450},
    {'fabricante': 'JA Solar', 'modelo': 'JAM60S20-455/MR', 'potencia_w': 455},
    {'fabricante': 'JA Solar', 'modelo': 'JAM60S20-460/MR', 'potencia_w': 460},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72S30-545/MR', 'potencia_w': 545},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72S30-550/MR', 'potencia_w': 550},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72S30-555/MR', 'potencia_w': 555},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72S30-560/MR', 'potencia_w': 560},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72D30-565/MB', 'potencia_w': 565},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72D30-570/MB', 'potencia_w': 570},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72D30-575/MB', 'potencia_w': 575},
    {'fabricante': 'JA Solar', 'modelo': 'JAM72D30-580/MB', 'potencia_w': 580},
    
    # Jinko Solar - 15 modelos
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM400M-54HL4-V', 'potencia_w': 400},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM405M-54HL4-V', 'potencia_w': 405},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM410M-54HL4-V', 'potencia_w': 410},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM415M-54HL4-V', 'potencia_w': 415},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM420M-54HL4-V', 'potencia_w': 420},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM450N-60HL4-V', 'potencia_w': 450},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM455N-60HL4-V', 'potencia_w': 455},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM460N-60HL4-V', 'potencia_w': 460},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM530N-72HL4-V', 'potencia_w': 530},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM535N-72HL4-V', 'potencia_w': 535},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM540N-72HL4-V', 'potencia_w': 540},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM545N-72HL4-V', 'potencia_w': 545},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM550N-72HL4-V', 'potencia_w': 550},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM555N-72HL4-V', 'potencia_w': 555},
    {'fabricante': 'Jinko Solar', 'modelo': 'JKM560N-72HL4-V', 'potencia_w': 560},
    
    # LONGi Solar - 15 modelos
    {'fabricante': 'LONGi Solar', 'modelo': 'LR4-54HPH-400M', 'potencia_w': 400},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR4-54HPH-405M', 'potencia_w': 405},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR4-54HPH-410M', 'potencia_w': 410},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR4-54HPH-415M', 'potencia_w': 415},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-54HPH-420M', 'potencia_w': 420},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-54HPH-425M', 'potencia_w': 425},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-60HPH-450M', 'potencia_w': 450},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-60HPH-455M', 'potencia_w': 455},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-60HPH-460M', 'potencia_w': 460},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-530M', 'potencia_w': 530},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-535M', 'potencia_w': 535},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-540M', 'potencia_w': 540},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-545M', 'potencia_w': 545},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-550M', 'potencia_w': 550},
    {'fabricante': 'LONGi Solar', 'modelo': 'LR5-72HPH-555M', 'potencia_w': 555},
    
    # OSDA Solar - 13 modelos
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA400-36-M', 'potencia_w': 400},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA405-36-M', 'potencia_w': 405},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA410-36-M', 'potencia_w': 410},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA415-36-M', 'potencia_w': 415},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA420-36-M', 'potencia_w': 420},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA450-36-M', 'potencia_w': 450},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA455-36-M', 'potencia_w': 455},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA460-36-M', 'potencia_w': 460},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA530-36-M', 'potencia_w': 530},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA535-36-M', 'potencia_w': 535},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA540-36-M', 'potencia_w': 540},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA545-36-M', 'potencia_w': 545},
    {'fabricante': 'OSDA Solar', 'modelo': 'ODA550-36-M', 'potencia_w': 550},
    
    # Risen Energy - 12 modelos
    {'fabricante': 'Risen Energy', 'modelo': 'RSM40-8-400BMDG', 'potencia_w': 400},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM40-8-405BMDG', 'potencia_w': 405},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM40-8-410BMDG', 'potencia_w': 410},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM40-8-415BMDG', 'potencia_w': 415},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM132-8-450BMDG', 'potencia_w': 450},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM132-8-455BMDG', 'potencia_w': 455},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM132-8-460BMDG', 'potencia_w': 460},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM144-8-530BMDG', 'potencia_w': 530},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM144-8-535BMDG', 'potencia_w': 535},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM144-8-540BMDG', 'potencia_w': 540},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM144-8-545BMDG', 'potencia_w': 545},
    {'fabricante': 'Risen Energy', 'modelo': 'RSM144-8-550BMDG', 'potencia_w': 550},
    
    # Sunova Solar - 15 modelos
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-400-54MDH', 'potencia_w': 400},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-405-54MDH', 'potencia_w': 405},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-410-54MDH', 'potencia_w': 410},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-415-54MDH', 'potencia_w': 415},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-420-54MDH', 'potencia_w': 420},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-425-54MDH', 'potencia_w': 425},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-450-60MDH', 'potencia_w': 450},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-455-60MDH', 'potencia_w': 455},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-460-60MDH', 'potencia_w': 460},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-530-72MDH', 'potencia_w': 530},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-535-72MDH', 'potencia_w': 535},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-540-72MDH', 'potencia_w': 540},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-545-72MDH', 'potencia_w': 545},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-550-72MDH', 'potencia_w': 550},
    {'fabricante': 'Sunova Solar', 'modelo': 'SS-555-72MDH', 'potencia_w': 555},
    
    # Trina Solar - 15 modelos
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-400DE09.08', 'potencia_w': 400},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-405DE09.08', 'potencia_w': 405},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-410DE09.08', 'potencia_w': 410},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-415DE09.08', 'potencia_w': 415},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-420DE09.08', 'potencia_w': 420},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-450DE15M.08', 'potencia_w': 450},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-455DE15M.08', 'potencia_w': 455},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-460DE15M.08', 'potencia_w': 460},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-530DE18M.08', 'potencia_w': 530},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-535DE18M.08', 'potencia_w': 535},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-540DE18M.08', 'potencia_w': 540},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-545DE18M.08', 'potencia_w': 545},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-550DE18M.08', 'potencia_w': 550},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-555DE18M.08', 'potencia_w': 555},
    {'fabricante': 'Trina Solar', 'modelo': 'TSM-560DE18M.08', 'potencia_w': 560},
]

for painel in paineis:
    Painel.objects.get_or_create(
        fabricante=painel['fabricante'],
        modelo=painel['modelo'],
        defaults={'potencia_w': painel['potencia_w']}
    )

print(f"✅ {len(paineis)} painéis solares cadastrados com sucesso!")
