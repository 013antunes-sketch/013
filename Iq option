from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from iqoptionapi.stable_api import IQ_Option
import uvicorn
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    email: str
    senha: str
    ambiente: str

# Guardamos a API globalmente após o login da primeira tela
API_IQ = None

@app.post("/api/login")
def realizar_login(dados: LoginData):
    global API_IQ
    API_IQ = IQ_Option(dados.email, dados.senha)
    conectado, erro = API_IQ.connect()
    
    if not conectado:
        raise HTTPException(status_code=400, detail=f"Falha: {erro}")
    
    API_IQ.change_balance(dados.ambiente)
    return {
        "status": "sucesso",
        "mensagem": f"Conectado à conta!",
        "saldo_inicial": API_IQ.get_balance()
    }

# Roda a inteligência do robô conectado via WebSocket à tela do dashboard
@app.websocket("/ws/bot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global API_IQ
    
    lucro_total = 0.0
    wins = 0
    losses = 0

    try:
        # Recebe os sinais e parâmetros configurados na interface
        data = await websocket.receive_text()
        config = json.loads(data)
        
        await websocket.send_json({"type": "log", "message": "Sinais recebidos com sucesso na nuvem. Analisando horários...", "log_type": "info"})
        
        # Processa o texto dos sinais que o usuário colou
        linhas_sinais = config['sinais'].strip().split('\n')
        
        await websocket.send_json({"type": "log", "message": f"Total de {len(linhas_sinais)} sinais agendados.", "log_type": "system"})

        # Exemplo prático de loop simulado/real de monitoramento
        # (Em produção aqui rodaria a checagem exata de datetime vs horário do sinal)
        for sinal_str in linhas_sinais:
            if not sinal_str: continue
            
            # Divide a linha (M5;EURUSD;22:45;CALL)
            partes = sinal_str.split(';')
            if len(partes) < 4: continue
            
            timeframe, ativo, horario, direcao = partes
            direcao_api = "buy" if direcao.upper() in ["CALL", "COMPRA"] else "sell"
            
            await websocket.send_json({"type": "log", "message": f"Aguardando gatilho para {ativo} às {horario}...", "log_type": "system"})
            
            # Aqui simulamos o processamento da ordem para fins visuais imediatos
            await asyncio.sleep(4) 
            
            await websocket.send_json({"type": "log", "message": f"Entrada efetuada em {ativo} ({direcao.upper()})", "log_type": "info"})
            
            # Simulação de resultado (Troque pelo código de execução da IQ Option em conta real/demo)
            await asyncio.sleep(2)
            
            # Simulação alternada de Win/Loss para testar os cards
            if wins <= losses:
                wins += 1
                lucro_total += (config['entrada'] * 0.85) # Ganho padrão de payout de 85%
                await websocket.send_json({"type": "log", "message": f"WIN no ativo {ativo}! Payout 85%", "log_type": "success"})
            else:
                losses += 1
                lucro_total -= config['entrada']
                await websocket.send_json({"type": "log", "message": f"LOSS no ativo {ativo}!", "log_type": "error"})
                
            # Atualiza o placar e saldo total na tela do Dashboard na hora
            await websocket.send_json({
                "type": "update",
                "lucro": lucro_total,
                "wins": wins,
                "losses": losses
            })

    except WebSocketDisconnect:
        print("Interface desconectada.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
