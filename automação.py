import git
import time
import sys

# Classe de progresso personalizada para acompanhar o progresso do clone
class CloneProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def clone_repository(repo_url, clone_path, cert_path=None, cert_key_path=None):
    try:
        if cert_path and cert_key_path:
            with open(cert_path, 'rb') as cert_file:
                cert_content = cert_file.read()
            with open(cert_key_path, 'rb') as cert_key_file:
                cert_key_content = cert_key_file.read()
            git.Repo.clone_from(repo_url, clone_path, progress=CloneProgress(), env={"GIT_SSL_CERT": cert_content, "GIT_SSL_CERT_KEY": cert_key_content})
        else:
            git.Repo.clone_from(repo_url, clone_path, progress=CloneProgress())
        print("Clonagem do repositório concluída com sucesso!")
    except git.exc.GitCommandError as e:
        print(f"Erro durante a clonagem do repositório: {e}")

def push_to_repository(clone_path, branch_name=None, git_username=None, git_password=None):
    try:
        repo = git.Repo(clone_path)
        if branch_name:
            origin = repo.remote()
            origin.push(refspec=f"refs/heads/{branch_name}", username=git_username, password=git_password)
            print(f"Push para a ramificação '{branch_name}' concluído com sucesso!")
        else:
            origin = repo.remote()
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

def main(repo_url, clone_path, branch_name=None, cert_path=None, cert_key_path=None, git_username=None, git_password=None):
    # Clonar o repositório
    clone_repository(repo_url, clone_path, cert_path, cert_key_path)
    
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
        push_to_repository(clone_path, branch_name, git_username, git_password)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 8:
        print("Uso: python script.py <url_do_repositorio> <caminho_para_clonar> [nome_da_ramificacao] [caminho_certificado] [caminho_chave_certificado] [git_username] [git_password]")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_path = sys.argv[2]
    branch_name = sys.argv[3] if len(sys.argv) >= 4 else None
    cert_path = sys.argv[4] if len(sys.argv) >= 5 else None
    cert_key_path = sys.argv[5] if len(sys.argv) >= 6 else None
    git_username = sys.argv[6] if len(sys.argv) >= 7 else None
    git_password = sys.argv[7] if len(sys.argv) >= 8 else None

    main(repo_url, clone_path, branch_name, cert_path, cert_key_path, git_username, git_password)
