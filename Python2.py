import os
import pandas as pd
from twilio.rest import Client
from datetime import datetime
import pytz

# Carregar credenciais do Twilio das variáveis de ambiente
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Verificar se as credenciais foram carregadas corretamente
if account_sid is None or auth_token is None:
    print("Twilio credentials not found. Please set the environment variables TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.")
    exit(1)

client = Client(account_sid, auth_token)

# Definir o fuso horário do Brasil (São Paulo)
fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

# Obter a data e hora atual no fuso horário do Brasil
data_atual_brasil = datetime.now(fuso_horario_brasil).date()

# Carregar o CSV com as tarefas
df = pd.read_csv('tarefas.csv')

# Filtrar as tarefas do dia atual no Brasil
tarefas_do_dia = df[df['dia'] == data_atual_brasil.strftime('%Y-%m-%d')]

# Se houver tarefas no dia atual
if not tarefas_do_dia.empty:
    # Montar a mensagem com todas as tarefas do dia
    mensagem = "Tarefas para hoje:\n"
    for index, row in tarefas_do_dia.iterrows():
        mensagem += f"- {row['tarefas']} às {row['hora']}\n"
    
    # Enviar a mensagem via WhatsApp
    message = client.messages.create(
        body=mensagem,
        from_='whatsapp:+14155238886',  # Número padrão do Twilio sandbox
        to='whatsapp:+5511998995650'  # Substitua pelo seu número de WhatsApp
    )
    
    print(f"Mensagem enviada com sucesso! ID: {message.sid}")
else:
    print("Nenhuma tarefa para hoje.") 
