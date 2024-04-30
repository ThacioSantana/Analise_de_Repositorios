import os
import subprocess
import re

class CloneError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def fetch_repositories(urls, destination):
    """
    Clona uma lista de repositórios Git a partir das URLs fornecidas para o diretório de destino.
    
    Parâmetros:
        urls (list): Uma lista de URLs dos repositórios a serem clonados.
        destination (str): O diretório onde os repositórios serão clonados.
    """
    for url in urls:
        try:
            fetch_repository(url, destination)
        except CloneError as e:
            print(f"Erro ao clonar o repositório: {e}")
        except Exception as e:
            print(f"Erro inesperado ao clonar o repositório: {e}")

def fetch_repository(url, destination):
    """
    Clona um repositório Git a partir de uma URL para o diretório de destino.
    
    Parâmetros:
        url (str): A URL do repositório a ser clonado.
        destination (str): O diretório onde o repositório será clonado.
    """
    try:
        repository_name = os.path.splitext(os.path.basename(url))[0]  # Extrai o nome do repositório da URL
        
        # Cria o diretório para o repositório clonado
        repository_dir = os.path.join(destination, repository_name)
        os.makedirs(repository_dir, exist_ok=True)
        
        # Clone o repositório usando o Git, desativando a verificação SSL
        subprocess.run(["git", "clone", "--config", "http.sslVerify=false", url, repository_dir], check=True)
        
        # Gera um relatório para o repositório clonado
        generate_report(repository_dir)
        
    except OSError as e:
        raise CloneError(f"Erro ao criar o diretório do repositório: {e}")
    except subprocess.CalledProcessError as e:
        raise CloneError(f"Erro ao clonar o repositório: {e}")
    except Exception as e:
        raise CloneError(f"Erro inesperado ao clonar o repositório: {e}")

def generate_report(directory):
    """
    Gera um relatório para um diretório de repositório clonado, procurando por arquivos com extensões específicas
    e palavras-chave dentro desses arquivos, e escrevendo os resultados em um arquivo de relatório.
    
    Parâmetros:
        directory (str): O diretório do repositório clonado.
    """
    report_path = os.path.join(directory, 'relatorio.txt')  # Caminho para o arquivo de relatório
    
    extensions = ['.json', '.xml', '.config']  # Extensões de arquivo a serem pesquisadas
    keywords = ['pwd', 'usr', 'username', 'password', 'usuario', 'senha', 'UserSecret', 'Catalog']  # Palavras-chave a serem pesquisadas
    
    occurrences_found = False  # Variável para acompanhar se foram encontradas ocorrências
    
    try:
        # Abre o arquivo de relatório para escrita
        with open(report_path, 'w', encoding='utf-8') as report_file:
            # Loop através das extensões e palavras-chave
            for ext in extensions:
                for keyword in keywords:
                    found_lines = []  # Lista para armazenar linhas encontradas com as palavras-chave
                    # Procura por arquivos com a extensão atual e extrai as linhas com as palavras-chave
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
        
        # Se não foram encontradas ocorrências, exclui o arquivo de relatório
        if not occurrences_found:
            print("Nenhuma ocorrência encontrada para as palavras-chave nos arquivos.")
            os.remove(report_path)
        else:
            print(f"Relatório gerado com sucesso em {report_path}")
    
    except OSError as e:
        raise CloneError(f"Erro ao gerar o relatório: {e}")

if __name__ == "__main__":
    # URLs dos repositórios como uma lista
    repository_urls = [
        "Lista de Repositorios"
    ]

    try:
        # Define o diretório base onde os repositórios serão clonados
        base_directory = input("Digite o diretório base para clonar os repositórios: ")

        # Clona os repositórios e gera os relatórios para cada um
        fetch_repositories(repository_urls, base_directory)
    except Exception as e:
        print(f"Erro inesperado: {e}")
