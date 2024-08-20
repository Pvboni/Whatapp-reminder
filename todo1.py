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

    # Criar ou abrir o arquivo CSV
    with open('tarefas1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tarefa', 'Dia', 'Hora'])

        # Escrever as tarefas no CSV
        for task in tasks:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'

            # Verifica se a tarefa é para o dia de hoje
            if due_date == hoje:
                writer.writerow([task.content, due_date, due_time])
                print(f"Tarefa adicionada: {task.content} - {due_date} {due_time}")

    print("Arquivo CSV gerado com sucesso em tarefas1.csv.")

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
