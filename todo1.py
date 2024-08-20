import csv
import os
import datetime
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Chave da API do Todoist
api_key = os.getenv('YOUR_TODOIST_API_KEY')
if not api_key:
    print("API key not found.")
    exit(1)

api = TodoistAPI(api_key)

try:
    # Data atual
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')

    # Obter todas as tarefas
    tasks = api.get_tasks()

    # Verificar se há tarefas
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        exit(0)

    # Definir o caminho do arquivo CSV
    file_name = 'tarefas1.csv'
    file_path = os.path.join(os.getcwd(), file_name)

    # Criar ou abrir o arquivo CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tarefa', 'Dia', 'Hora'])

        for task in tasks:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'

            if due_date == hoje:
                writer.writerow([task.content, due_date, due_time])

    print(f"Arquivo CSV gerado com sucesso em: {file_path}")

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
