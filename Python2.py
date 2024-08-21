import os
import pandas as pd
from twilio.rest import Client
from datetime import datetime, timedelta
import pytz

# Carregar credenciais do Twilio das variáveis de ambiente
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Verificar se as credenciais foram carregadas corretamente
if account_sid is None or auth_token is None:
    print("Twilio credentials not found. Please set the environment variables TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.")
    exit(1)

client = Client(account_sid, auth_token)

# Definir o fuso Horario do Brasil (São Paulo)
fuso_Horario_brasil = pytz.timezone('America/Sao_Paulo')

# Obter a data e Hora atual no fuso Horario do Brasil
data_atual_brasil = datetime.now(fuso_Horario_brasil).date()

# Definir a data final da semana (domingo)
data_final_semana = data_atual_brasil + timedelta(days=(6 - data_atual_brasil.weekday()))

# Carregar o CSV com as Tarefas
df = pd.read_csv('tarefas1.csv')

# Converter a coluna 'Dia' para datetime
df['Dia'] = pd.to_datetime(df['Dia']).dt.date

# Categorizar as Tarefas
Tarefas_overdue = df[df['Dia'] < data_atual_brasil]
Tarefas_hoje = df[df['Dia'] == data_atual_brasil]
Tarefas_futuras = df[(df['Dia'] > data_atual_brasil) & (df['Dia'] <= data_final_semana)]

# Montar a mensagem
mensagem = ""

# Adicionar Tarefas overdue
if not Tarefas_overdue.empty:
    mensagem += "Tarefas Overdue:\n"
    for index, row in Tarefas_overdue.iterrows():
        mensagem += f"- {row['Tarefas']} (Vencida em {row['Dia']}) às {row['Hora']}\n"
    mensagem += "\n"

# Adicionar Tarefas de hoje
if not Tarefas_hoje.empty:
    mensagem += "Tarefas para Hoje:\n"
    for index, row in Tarefas_hoje.iterrows():
        mensagem += f"- {row['Tarefas']} às {row['Hora']}\n"
    mensagem += "\n"

# Adicionar Tarefas futuras dentro da semana
if not Tarefas_futuras.empty:
    mensagem += "Tarefas Futuras desta Semana:\n"
    for index, row in Tarefas_futuras.iterrows():
        mensagem += f"- {row['Tarefas']} no dia {row['Dia']} às {row['Hora']}\n"
    mensagem += "\n"

# Verificar se há alguma tarefa a ser enviada
if mensagem:
    # Enviar a mensagem via WhatsApp
    message = client.messages.create(
        body=mensagem,
        from_='whatsapp:+14155238886',  # Número padrão do Twilio sandbox
        to='whatsapp:+5511998995650'  # Substitua pelo seu número de WhatsApp
    )
    
    print(f"Mensagem enviada com sucesso! ID: {message.sid}")
else:
    print("Nenhuma tarefa para enviar.")
