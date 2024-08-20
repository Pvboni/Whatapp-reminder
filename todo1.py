import csv
import os
from dotenv import load_dotenv
from todoist.api import TodoistAPI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
todoist_api_key = os.getenv('YOUR_TODOIST_API_KEY')

if todoist_api_key is None:
    print("Chave da API do Todoist não encontrada. Verifique o arquivo .env.")
    exit(1)

# Conectar à API do Todoist
api = TodoistAPI(todoist_api_key)
api.sync()

# Obter todas as tarefas pendentes
tasks = api.state['items']
pending_tasks = [task for task in tasks if task['checked'] == 0]

# Criar um arquivo CSV
with open('tarefas.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['tarefas', 'dia', 'hora'])

    for task in pending_tasks:
        task_name = task['content']
        due_date = task['due']['date'] if task['due'] else 'Sem data'
        due_time = task['due']['datetime'] if task['due'] and 'datetime' in task['due'] else 'Sem hora'
        writer.writerow([task_name, due_date, due_time])

print("Arquivo CSV gerado com sucesso.")
