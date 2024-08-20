import csv
import os
import datetime
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

# Token do GitHub
github_token = os.getenv('YOUR_GITHUB_TOKEN')
if not github_token:
    print("GitHub token not found.")
    exit(1)

# Repositório e caminho do arquivo no GitHub
repo = "Pvboni/Whatapp-reminder"
path = "tarefas1.csv"

api = TodoistAPI(api_key)

try:
    # Data atual
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"Data de hoje: {hoje}")

    # Obter todas as tarefas
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

        # Contador para tarefas adicionadas
        tarefa_adicionada = False

        # Escrever as tarefas no CSV
        for task in tasks:
            due_date = task.due.date if task.due else 'Sem data'
            due_time = task.due.datetime if task.due and task.due.datetime else 'Sem hora'

            # Imprimir todas as tarefas para depuração
            print(f"Tarefa: {task.content}, Data: {due_date}, Hora: {due_time}")

            # Verifica se a tarefa é para o dia de hoje
            if due_date == hoje:
                writer.writerow([task.content, due_date, due_time])
                print(f"Tarefa adicionada: {task.content} - {due_date} {due_time}")
                tarefa_adicionada = True

        if not tarefa_adicionada:
            print("Nenhuma tarefa foi adicionada ao arquivo CSV.")
        else:
            print("Arquivo CSV gerado com sucesso.")

    # Obter o caminho absoluto do arquivo
    absolute_path = os.path.abspath(file_path)
    print(f"Arquivo CSV salvo em: {absolute_path}")

    # Leitura do conteúdo do CSV gerado
    with open(file_path, mode='r') as file:
        content = file.read()
        print("Conteúdo do arquivo CSV:\n", content)

    # Converter o conteúdo do arquivo para base64
    content_bytes = content.encode('utf-8')
    content_base64 = base64.b64encode(content_bytes).decode('utf-8')

    # Enviar o arquivo para o GitHub
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {github_token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Adicionando arquivo de tarefas",
        "content": content_base64,
        "branch": "main"  # ou a branch que você deseja usar
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print("Arquivo enviado para o GitHub com sucesso.")
    else:
        print(f"Erro ao enviar arquivo para o GitHub: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
