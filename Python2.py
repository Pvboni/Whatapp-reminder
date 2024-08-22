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

# Definir o fuso horário do Brasil (São Paulo)
fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

# Obter a data e hora atual no fuso horário do Brasil
data_atual_brasil = datetime.now(fuso_horario_brasil).date()

# Definir a data final da semana (domingo)
data_final_semana = data_atual_brasil + timedelta(days=(6 - data_atual_brasil.weekday()))

# Carregar o CSV com as tarefas
df = pd.read_csv('tarefas1.csv')

# Ajustar o cabeçalho para ter a inicial maiúscula
df.columns = [col.capitalize() for col in df.columns]

# Converter a coluna 'Dia' para datetime
df['Dia'] = pd.to_datetime(df['Dia']).dt.date

# Colocar a inicial maiúscula nas colunas 'Tarefa' e 'Hora'
df['Tarefa'] = df['Tarefa'].str.title()
df['Hora'] = df['Hora'].str.title()

# Categorizar as tarefas
tarefas_overdue = df[df['Dia'] < data_atual_brasil]
tarefas_hoje = df[df['Dia'] == data_atual_brasil]
tarefas_futuras = df[(df['Dia'] > data_atual_brasil) & (df['Dia'] <= data_final_semana)]

# Montar a mensagem
mensagem = ""

# Adicionar tarefas overdue
if not tarefas_overdue.empty:
    mensagem += "Tarefas Overdue:\n"
    for index, row in tarefas_overdue.iterrows():
        mensagem += f"- {row['Tarefa']} (Vencida em {row['Dia']}) Às {row['Hora']}\n"
    mensagem += "\n"

# Adicionar tarefas de hoje
if not tarefas_hoje.empty:
    mensagem += "Tarefas para Hoje:\n"
    for index, row in tarefas_hoje.iterrows():
        mensagem += f"- {row['Tarefa']} Às {row['Hora']}\n"
    mensagem += "\n"

# Adicionar tarefas futuras dentro da semana
if not tarefas_futuras.empty:
    mensagem += "Tarefas Futuras Desta Semana:\n"
    for index, row in tarefas_futuras.iterrows():
        mensagem += f"- {row['Tarefa']} No Dia {row['Dia']} Às {row['Hora']}\n"
    mensagem += "\n"

# Verificar se há alguma tarefa a ser enviada
if mensagem:
    try:
        # Enviar a mensagem via WhatsApp
        message = client.messages.create(
            body=mensagem,
            from_='whatsapp:+14155238886',  # Número padrão do Twilio sandbox
            to='whatsapp:+5511998995650'  # Substitua pelo seu número de WhatsApp
        )
        
        print(f"Mensagem enviada com sucesso! ID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
else:
    print("Nenhuma tarefa para enviar.")
