import csv
import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI  # Corrigido o caminho de importação

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
todoist_api_key = os.getenv('YOUR_TODOIST_API_KEY')

if todoist_api_key is None:
    print("Chave da API do Todoist não encontrada. Verifique o arquivo .env.")
    exit(1)

# Conectar à API do Todoist
api = TodoistAPI(todoist_api_key)

try:
    tasks = api.get_tasks()
except Exception as e:
    print(f"Erro ao buscar tarefas: {e}")
    exit(1)

# Filtrar tarefas pendentes
pending_tasks = [task for task in tasks if task.due and not task.is_completed]

# Criar um arquivo CSV
csv_file_path = 'tarefas.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['tarefas', 'dia', 'hora'])

    for task in pending_tasks:
        task_name = task.content
        due_date = task.due.date if task.due else 'Sem data'
        due_time = task.due.datetime if task.due and 'datetime' in task.due else 'Sem hora'
        writer.writerow([task_name, due_date, due_time])

print(f"Arquivo CSV gerado com sucesso em {csv_file_path}.")
