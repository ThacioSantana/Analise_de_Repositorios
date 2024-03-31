import git
import time
import sys
#import conversor_certificado

# Classe de progresso personalizada para acompanhar o progresso do clone
class CloneProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def clone_repository(repo_url, clone_path, use_ssh=False):
    try:
        if use_ssh:
            repo = git.Repo.clone_from(repo_url, clone_path, progress=CloneProgress(), env={"GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no"})
        else:
            repo = git.Repo.clone_from(repo_url, clone_path, progress=CloneProgress())
        
        print("Clonagem do repositório concluída com sucesso!")
        return repo
    except git.exc.GitCommandError as e:
        print(f"Erro durante a clonagem do repositório: {e}")
        return None

def push_to_repository(repo, branch_name=None, git_username=None, git_password=None):
    try:
        origin = repo.remote()
        if branch_name:
            origin.push(refspec=f"refs/heads/{branch_name}", username=git_username, password=git_password)
            print(f"Push para a ramificação '{branch_name}' concluído com sucesso!")
        else:
            origin.push(username=git_username, password=git_password)
            print("Push para a ramificação padrão concluído com sucesso!")
    except git.exc.GitCommandError as e:
        print(f"Erro durante o push para o repositório: {e}")

def read_repository_data(repo_path):
    try:
        with open(repo_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None

def store_data_to_txt(data, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(data)
        print(f"Dados armazenados em '{output_file}' com sucesso!")
    except Exception as e:
        print(f"Erro ao armazenar os dados no arquivo: {e}")

def main(repo_url, clone_path, branch_name=None, git_username=None, git_password=None, use_ssh=False):
    # Clonar o repositório
    repo = clone_repository(repo_url, clone_path, use_ssh)
    
    if repo:
        # Ler os dados do repositório clonado
        data = read_repository_data(clone_path)
        
        if data:
            # Obter o timestamp atual
            timestamp = int(time.time())
            # Nome do arquivo com timestamp
            output_file = f"data_{timestamp}.txt"
            # Armazenar os dados em um arquivo
            store_data_to_txt(data, output_file)
            
            # Fazer push para o repositório
            push_to_repository(repo, branch_name, git_username, git_password)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 8:
        print("Uso: python script.py <url_do_repositorio> <caminho_para_clonar> [nome_da_ramificacao] [git_username] [git_password] [--ssh]")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_path = sys.argv[2]
    branch_name = sys.argv[3] if len(sys.argv) >= 4 else None
    git_username = sys.argv[4] if len(sys.argv) >= 5 else None
    git_password = sys.argv[5] if len(sys.argv) >= 6 else None
    use_ssh = "--ssh" in sys.argv

    main(repo_url, clone_path, branch_name, git_username, git_password, use_ssh)
