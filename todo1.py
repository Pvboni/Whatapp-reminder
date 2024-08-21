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
    # Obter todas as tarefas abertas (não completadas)
    tasks = api.get_tasks()

    # Verificar se há tarefas
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        exit(0)

    # Definir o caminho do arquivo CSV
    directory = os.getcwd()  # Diretório atual de trabalho
    file_name = 'tarefas1.csv'
    file_path = os.path.join(directory, file_name)

    # Criar ou abrir o arquivo CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tarefa', 'Dia', 'Hora'])

        # Filtrar apenas tarefas pendentes e ordenar pela data de conclusão
        tasks_sorted = sorted(
            (task for task in tasks if not task.is_completed), 
            key=lambda x: x.due.date if x.due else ''
        )

        # Escrever as tarefas pendentes no CSV
        for task in tasks_sorted:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'
            writer.writerow([task.content, due_date, due_time])
            print(f"Tarefa adicionada: {task.content} - {due_date} {due_time}")

    print("Arquivo CSV gerado com sucesso.")

    # Obter o caminho absoluto do arquivo
    absolute_path = os.path.abspath(file_path)
    print(f"Arquivo CSV salvo em: {absolute_path}")

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
