import csv
import os
import datetime
import requests
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from twilio.rest import Client

# Carregar variáveis de ambiente
load_dotenv()

# Chave da API do Todoist
api_key = os.getenv('YOUR_TODOIST_API_KEY')
if not api_key:
    print("API key not found.")
    exit(1)

api = TodoistAPI(api_key)

# Autenticação Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+5511998995650'

client = Client(account_sid, auth_token)

try:
    # Obter todas as tarefas abertas
    tasks = api.get_tasks()

    # Filtrar apenas as tarefas pendentes
    pending_tasks = [task for task in tasks if task.completed is False]

    # Verificar se há tarefas pendentes
    if not pending_tasks:
        print("Nenhuma tarefa pendente encontrada.")
        exit(0)

    # Definir o caminho do arquivo CSV
    directory = os.getcwd()  # Diretório atual de trabalho
    file_name = 'tarefas1.csv'
    file_path = os.path.join(directory, file_name)

    # Criar ou abrir o arquivo CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tarefa', 'Dia', 'Hora'])

        # Ordenar as tarefas pela data de conclusão
        tasks_sorted = sorted(
            pending_tasks, 
            key=lambda x: x.due.date if x.due else ''
        )

        # Escrever as tarefas no CSV e enviar a mensagem
        for task in tasks_sorted:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'
            writer.writerow([task.content, due_date, due_time])
            print(f"Tarefa adicionada: {task.content} - {due_date} {due_time}")

            # Enviar mensagem WhatsApp com o template
            message = client.messages.create(
                from_=from_whatsapp_number,
                to=to_whatsapp_number,
                template_sid='HX0241d8d4ce8d0cfbb20a045fb4291a84',
                template_data={'task_name': task.content, 'due_date': due_date}
            )
            print(f"Mensagem enviada para {to_whatsapp_number} com a tarefa {task.content}")

    print("Arquivo CSV gerado e mensagens enviadas com sucesso.")

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV ou enviar mensagens: {e}")
