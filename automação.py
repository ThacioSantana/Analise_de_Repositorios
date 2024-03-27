import git
import time
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def convert_cert_to_pem(cert_path, output_path):
    try:
        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_der_x509_certificate(cert_data, default_backend())

            with open(output_path, 'wb') as pem_file:
                pem_file.write(cert.public_bytes(encoding=x509.Encoding.PEM))

        print(f"Certificado convertido para {output_path} com sucesso!")
    except Exception as e:
        print(f"Erro ao converter certificado: {e}")

convert_cert_to_pem(r'C:\Users\4063856\Documents\Programação\seu_certificado.crt', r'C:\Users\4063856\Documents\Programação\seu_certificado.pem')

# Definir globalmente a configuração para desativar a verificação SSL
# git.cmd.GitConfigParser().set("http", "sslVerify", "false")

# Classe de progresso personalizada para acompanhar o progresso do clone
class CloneProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def clone_repository(repo_url, clone_path):
    try:
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

def main(repo_url, clone_path, branch_name=None, git_username=None, git_password=None):
    # Clonar o repositório
    clone_repository(repo_url, clone_path)
    
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
    if len(sys.argv) < 3 or len(sys.argv) > 7:
        print("Uso: python script.py <url_do_repositorio> <caminho_para_clonar> [nome_da_ramificacao] [git_username] [git_password]")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_path = sys.argv[2]
    branch_name = sys.argv[3] if len(sys.argv) >= 4 else None
    git_username = sys.argv[4] if len(sys.argv) >= 5 else None
    git_password = sys.argv[5] if len(sys.argv) >= 6 else None

    main(repo_url, clone_path, branch_name, git_username, git_password)
