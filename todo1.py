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
    print(f"Data de hoje: {hoje}")

    # Obter todas as tarefas
    tasks = api.get_tasks()

    # Verificar se há tarefas
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        exit(0)

    # Definir o caminho do arquivo CSV
    directory = '/home/runner/work/Whatapp-reminder/Whatapp-reminder'
    file_name = 'tarefas1.csv'
    file_path = os.path.join(directory, file_name)

    # Criar o diretório, se não existir
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Diretório criado: {directory}")

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

except Exception as e:
    print(f"Erro ao gerar o arquivo CSV: {e}")
