import time
from datetime import datetime
from iqoptionapi.stable_api import IQ_Option

# 1. Conexão com a API (Insira seus dados ou use variáveis de ambiente)
API = IQ_Option("seu_email@email.com", "sua_senha")
API.connect()

if API.check_connect():
    print("Conectado com sucesso na IQ Option!")
else:
    print("Erro ao conectar.")
    exit()

# 2. Configuração do seu Sinal
HORA_SINAL = "14:00:00"  # Formato: HH:MM:SS
PARIDADE = "EURUSD"
DIRECAO = "call"         # 'call' para compra, 'put' para venda
TIMEFRAME = 5            # Tempo da vela do sinal (1, 5, 15 minutos)
VALOR_ENTRADA = 10

print(# Agendado para a hora definida
    f"Aguardando o sinal das {HORA_SINAL} na paridade {PARIDADE}..."
)

# 3. Loop de checagem do tempo exato
while True:
    # Pega o horário atual do sistema
    agora = datetime.now().strftime("%H:%M:%S")
    
    # Se quiser ser ainda mais preciso, você pode buscar o horário do servidor da IQ Option:
    # agora = datetime.fromtimestamp(API.get_server_time()).strftime("%H:%M:%S")

    if agora == HORA_SINAL:
        print(f"[{agora}] Horário atingido! Executando a ordem...")
        
        # Executa a operação na opção Digital (ou altere para Binary)
        status, id_operacao = API.buy_digital_spot(PARIDADE, VALOR_ENTRADA, DIRECAO, TIMEFRAME)
        
        if status:
            print(f"Ordem aceita! ID: {id_operacao}")
        else:
            print("Erro ao abrir a operação.")
            
        break # Sai do loop após enviar a ordem
        
    # Espera 0.5 segundos antes de checar de novo para não travar o processador
    time.sleep(0.5)
