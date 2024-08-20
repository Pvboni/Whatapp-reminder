import os
import pandas as pd
from twilio.rest import Client
from datetime import datetime

# Carregar credenciais do Twilio das variáveis de ambiente
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Verificar se as credenciais foram carregadas corretamente
if account_sid is None or auth_token is None:
    print("Twilio credentials not found. Please set the environment variables TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.")
    exit(1)

client = Client(account_sid, auth_token)

# Carregar o CSV com as tarefas
df = pd.read_csv('tarefas.csv')

# Obter a data atual
data_atual = datetime.now().date()

# Filtrar as tarefas do dia
tarefas_do_dia = df[df['dia'] == data_atual.strftime('%Y-%m-%d')]

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
