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

# Iterar sobre cada linha do CSV
for index, row in df.iterrows():
    tarefa = row['tarefas']
    dia = row['dia']
    hora = row['hora']
    
    # Verificar se a data e hora são iguais à data e hora atuais
    data_hora_tarefa = datetime.strptime(f"{dia} {hora}", '%Y-%m-%d %H:%M')
    data_hora_atual = datetime.now()
    
    if data_hora_tarefa.date() == data_hora_atual.date() and data_hora_tarefa.time().hour == data_hora_atual.time().hour:
        # Enviar a mensagem via WhatsApp
        message = client.messages.create(
            body=f"Lembrete: {tarefa} às {hora} no dia {dia}",
            from_='whatsapp:+14155238886',  # Número padrão do Twilio sandbox
            to='whatsapp:+5511998995650'  # Substitua pelo seu número de WhatsApp
        )
        
        print(f"Mensagem enviada para '{tarefa}' com sucesso! ID: {message.sid}")
    else:
        print(f"Ainda não é hora para a tarefa '{tarefa}'.")
