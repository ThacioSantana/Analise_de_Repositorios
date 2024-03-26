import git
import time
import sys
import subprocess

# Carregar credenciais a partir de variáveis de ambiente
git_username = os.environ.get('GIT_USERNAME')
git_password = os.environ.get('GIT_PASSWORD')

def push_to_repository(branch_name):
    command = f'git push origin {branch_name} --username={git_username} --password={git_password}'
    subprocess.run(command, shell=True)

def clone_repository(repo_url, clone_path):
    git.Repo.clone_from(repo_url, clone_path)

def read_repository_data(repo_path):
    with open(repo_path, 'r') as file:
        data = file.read()
    return data

def store_data_to_txt(data, output_file):
    with open(output_file, 'w') as file:
        file.write(data)

def main(repo_url, clone_path, branch_name):
    clone_repository(repo_url, clone_path)
    data = read_repository_data(clone_path)
    timestamp = int(time.time()) # Obter o timestamp atual
    output_file = f"data_{timestamp}.txt" # Nome do arquivo com timestamp
    store_data_to_txt(data, output_file)
    # Chamar a função para fazer push para o repositório
    push_to_repository(branch_name, git_username, git_password)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python script.py <url_do_repositorio> <caminho_para_clonar> <nome_da_ramificacao> <git_username> <git_password>")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_path = sys.argv[2]
    branch_name = sys.argv[3]
    git_username = sys.argv[4]
    git_password = sys.argv[5]

    main(repo_url, clone_path, branch_name)
