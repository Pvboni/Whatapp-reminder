import csv
import os
import base64
import requests
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Chave da API do Todoist
api_key = os.getenv('YOUR_TODOIST_API_KEY')
if not api_key:
    print("API key not found.")
    exit(1)

# Repositório e caminho do arquivo no GitHub
repo = "Pvboni/Whatapp-reminder"
path = "tarefas1.csv"

api = TodoistAPI(api_key)

try:
    # Obter todas as tarefas abertas
    tasks = api.get_tasks(filter="(today | overdue)")

    # Verificar se há tarefas
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        exit(0)

    # Ordenar as tarefas pela data de conclusão
    tasks.sort(key=lambda x: x.due.date if x.due else '')

    # Definir o caminho do arquivo CSV
    directory = os.getcwd()
    file_name = 'tarefas1.csv'
    file_path = os.path.join(directory, file_name)

    # Criar ou abrir o arquivo CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tarefa', 'Dia', 'Hora'])

        # Escrever as tarefas no CSV
        for task in tasks:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'
            writer.writerow([task.content, due_date, due_time])
            print(f"Tarefa adicionada: {task.content} - {due_date} {due_time}")

    print("Arquivo CSV gerado com sucesso.")
    print(f"Arquivo CSV salvo em: {os.path.abspath(file_path)}")

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
