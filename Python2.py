import os
from twilio.rest import Client
from datetime import datetime, timedelta
import pytz
import pandas as pd

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

# Enviar mensagens para cada tarefa pendente ou futura
for index, row in df.iterrows():
    task_name = row['Tarefa']
    due_date = row['Dia']
    due_time = row['Hora']
    
    try:
        # Enviar a mensagem via template no WhatsApp
        message = client.messages.create(
            messaging_service_sid='HX0241d8d4ce8d0cfbb20a045fb4291a84',  # ID do template
            from_='whatsapp:+14155238886',  # Número do Twilio
            to='whatsapp:+5511998995650',  # Substitua pelo seu número de WhatsApp
            body=f"Olá! Você tem uma tarefa pendente:\n\nTarefa: {task_name}\nData: {due_date}\nHora: {due_time}\n\nNão se esqueça de completá-la!\n\n- Seu Assistente de Tarefas"
        )
        
        print(f"Mensagem enviada com sucesso! ID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
