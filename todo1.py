name: Generate CSV from Todoist

on:
  workflow_dispatch:  # Manually trigger the workflow

jobs:
  run_python_script:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install python-dotenv todoist-api-python requests

    - name: Run Python script
      env:
        YOUR_TODOIST_API_KEY: ${{ secrets.YOUR_TODOIST_API_KEY }}
      run: python todo1.py

    - name: Display CSV file content
      run: cat tarefas1.csv

    - name: Commit and push changes
      run: |
        git config --global user.name 'GitHub Action'
        git config --global user.email 'action@github.com'
        git add -A
        git commit -m "Atualizando arquivo CSV de tarefas" || echo "No changes to commit"
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
