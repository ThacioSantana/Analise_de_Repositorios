import os
import subprocess
import re

def fetch_repositories(urls, destination):
    # Clona cada repositório
    for url in urls:
        fetch_repository(url, destination)

def fetch_repository(url, destination):
    # Define o nome do repositório
    repository_name = os.path.splitext(os.path.basename(url))[0]
    
    # Cria o diretório para o repositório clonado
    repository_dir = os.path.join(destination, repository_name)
    os.makedirs(repository_dir, exist_ok=True)
    
    # Clone o repositório usando a autenticação do Git e desativando a verificação SSL
    subprocess.run(["git", "clone", "--config", "http.sslVerify=false", url, repository_dir])

    # Gera o relatório para o repositório clonado
    generate_report(repository_dir)

def generate_report(directory):
    # Nome do relatório
    report_path = os.path.join(directory, 'relatorio.txt')

    # Lista de extensões de arquivo para procurar
    extensions = ['.json', '.xml', '.config']

    # Lista de palavras-chave para procurar nas linhas dos arquivos
    keywords = ['pwd', 'usr', 'username', 'password', 'usuario', 'senha', 'UserSecret', 'Catalog']

    # Variável para acompanhar se foram encontradas ocorrências
    occurrences_found = False

    # Abre o arquivo do relatório para escrita
    with open(report_path, 'w', encoding='utf-8') as report_file:
        # Loop através das extensões e palavras-chave
        for ext in extensions:
            for keyword in keywords:
                # Procura por arquivos com a extensão atual e extrai as linhas com as palavras-chave
                found_lines = []
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(ext):
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                for line in f:
                                    if re.search(keyword, line):
                                        found_lines.append(f"{file_path}: {line.strip()}")
                                        occurrences_found = True

                # Escreve as linhas encontradas no relatório
                if found_lines:
                    report_file.write(f"\nArquivos com extensão {ext} e palavra-chave '{keyword}':\n")
                    report_file.write('\n'.join(found_lines))
                    report_file.write('\n')

    if not occurrences_found:
        print("Nenhuma ocorrência encontrada para as palavras-chave nos arquivos.")
        os.remove(report_path)
    else:
        print(f"Relatório gerado com sucesso em {report_path}")

if __name__ == "__main__":
    # URLs dos repositórios como uma lista
    repository_urls = [
        "https://github.com/ThacioSantana/encurtador-de-links"
    ]

    # Define o diretório base onde os repositórios serão clonados
    base_directory = input("Digite o diretório base para clonar os repositórios: ")

    # Clona os repositórios e gera os relatórios para cada um
    fetch_repositories(repository_urls, base_directory)
